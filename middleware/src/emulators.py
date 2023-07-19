import os
import atexit
import time
from copy import deepcopy
from dataclasses import dataclass

from pint import UnitRegistry
from tinydb import TinyDB, Query
from loguru import logger

import qtmessages37 as qt

HERE = os.path.dirname(os.path.abspath(__file__))

DB = TinyDB(os.path.join(HERE, 'db.json'))
atexit.register(DB.close)
TS_COL = 'ts'

unit = UnitRegistry(auto_reduce_dimensions=True)
amps = unit.ampere
volts = unit.volts
kWh = unit.kilowatthour
kW = unit.kilowatt
watts = unit.watts

SCALE_FACTORS = {-1: qt.SiScaleCode.D,
                 0: qt.SiScaleCode.NONE,
                 3: qt.SiScaleCode.K}

def ensure_unit(value, units):
    try:
        return value.to(units)
    except AttributeError:
        return value * units


class Inverter:
    def __init__(self, output=0*kW, setpoint=0*kW, vac=240*volts):
        self.output = ensure_unit(output, kW)
        self.setpoint = ensure_unit(setpoint, kW)
        self.vac = ensure_unit(vac, volts)
    
    def set_setpoint(self, setpoint):
        self.setpoint = ensure_unit(setpoint, kW)

    def advance_time(self, duration):
        return self.copy()
    def copy(self):
        return self.__class__(output=self.output, setpoint=self.setpoint, vac=self.vac)
    
    def as_dict(self):
        return {'output': self.output.magnitude,
                'setpoint': self.setpoint.magnitude,
                'vac': self.vac.magnitude}

class Battery:
    def __init__(self, capacity=18.5*kWh,  remaining=10*kWh, voltage=54*volts, current=0*amps,
                 max_charge_rate= -180*amps,  max_discharge_rate = 180*amps):
        self.capacity = ensure_unit(capacity, kWh)
        self.remaining = ensure_unit(remaining, kWh)
        self.voltage = ensure_unit(voltage, volts)
        self.current = ensure_unit(current, amps)

        self.max_charge_rate = ensure_unit(max_charge_rate, amps)
        assert self.max_charge_rate <= 0*amps        
        self.max_discharge_rate = ensure_unit(max_discharge_rate, amps)
        assert self.max_discharge_rate >= 0*amps

    def copy(self):
        return self.__class__(capacity=self.capacity, remaining=self.remaining,
                              voltage=self.voltage, current=self.current,
                              max_charge_rate=self.max_charge_rate, max_discharge_rate=self.max_discharge_rate)

    def as_dict(self):
        return {
            'capacity': self.capacity.magnitude,
            'remaining': self.remaining.magnitude,
            'voltage': self.voltage.magnitude,
            'max_charge_rate': self.max_charge_rate.magnitude,
            'max_discharge_rate': self.max_discharge_rate.magnitude,
        }


    def allowable_current(self, amps_demand):
        demand = ensure_unit(amps_demand, unit.ampere)
        demand = min(self.max_discharge_rate, demand)
        demand = max(self.max_charge_rate, demand)
        return demand
    
    def advance_time(self, duration, amps_demand):
        '''
        duration is seconds by default. 
        amps_demand is amps by default
        '''
        demand = self.allowable_current(amps_demand=amps_demand)
        duration = ensure_unit(duration, unit.seconds)
        next_battery = self.copy()
        next_battery.current = demand


        power_output = next_battery.current*self.voltage
        energy_output = power_output * duration

        remaining = self.remaining - energy_output
        next_battery.remaining = remaining
        return next_battery


class System:
    _tags = []
    def __init__(self, inverter, battery):
        self.inverter = deepcopy(inverter)
        self.battery = deepcopy(battery)
        self.tags = [tag(battery=self.battery, inverter=self.inverter) for tag in self._tags]

    def telemetry(self):
        return {tag.name:tag.value() for tag in self.tags}
        
    def advance_time(self, duration):
        duration = ensure_unit(duration, unit.seconds)
        amps_demand = (self.inverter.setpoint/self.battery.voltage).to(amps)

        battery = self.battery.advance_time(duration=duration, amps_demand=amps_demand)
        inverter = self.inverter.advance_time(duration=duration)
        inverter.output = (battery.current*battery.voltage).to(kW)
        return self.__class__(inverter=inverter, battery=battery)
    
    @classmethod
    def load(cls, system):
        battery = Battery(**system['battery'])
        inverter = Inverter(**system['inverter'])
        return cls(inverter=inverter, battery=battery)
    
    def intervals(self, *args, **kwargs):
        return [tag.interval( *args, **kwargs) for tag in self._tags]

@dataclass
class Tag:
    battery: Battery
    inverter: Inverter
    """
    To implement you also must have
    name: str='tag name'
    help: str='human readable tag description'
    unit: str=kW  #pint unit

    si_units: str=str(watts)  #string of unit name
    scale_factor: str='k' #must be one of qt.SiScaleCode
    unit_type: str=qt.UnitType.POWER_REAL
    #for power units only
    ac: bool=True
    #for ac power only
    hertz: int=60
    voltage: int=480
    """

    def value(self):
        return None
    def scale(self, value):
        return value * (10**self.scale_factor)
    
    @classmethod
    def power_properties(self):
        is_power = self.unit_type in (qt.UnitType.POWER_REAL, qt.UnitType.POWER_APPARENT, qt.UnitType.POWER_REACTIVE)
        if is_power and self.ac:
            return qt.PowerProperties(ac=self.ac, hertz=self.hertz, voltage=self.voltage)
        return None
    
    @classmethod            
    def interval(self, resource_id, sampling_period, report_type=qt.ReportType.USAGE, market_context=None):
        power_properties = self.power_properties()

        si_scale_code = SCALE_FACTORS[self.scale_factor]
        qtunit = qt.Units(description='', 
                               si_scale_code=si_scale_code, 
                               units=self.si_units, 
                               unit_type=self.unit_type, 
                               power_properties=power_properties)

        interval_props = qt.UsageIntervalProperties(qt.ReadingType.DIRECT_READ, report_type, qtunit)

        market_context=market_context or ""
        interval = qt.IntervalDescription(market_context=market_context, resource_id=resource_id,
                                                rid=self.name, sampling_period=sampling_period, 
                                                usage_interval_properties=interval_props)
        logger.debug(f'Interval made: {interval}')
        return interval

class BatteryCharging(Tag):
    name: str='BatteryCharging'
    help: str='Power sent to energy storage'
    unit: str=kW

    si_units: str="W"
    scale_factor: int=3 
    unit_type: str=qt.UnitType.POWER_REAL
    ac: bool=False


    def value(self):
        inverter_output = int(self.scale(self.inverter.output.to(self.unit).magnitude))
        if inverter_output < 0:
            return abs(inverter_output)
        else:
            return 0

class BatteryDischarging(Tag):
    name: str='BatteryDisharging'
    help: str='Power sent from energy storage'
    unit: str=kW
    si_units: str="W"
    scale_factor: int=3
    unit_type: str=qt.UnitType.POWER_REAL
    ac: bool=False
    def value(self):
        inverter_output = int(self.scale(self.inverter.output.to(self.unit).magnitude))
        if inverter_output > 0:
            return abs(inverter_output)
        else:
            return 0


class SoC(Tag):
    name: str='MBMU_system_SOC'
    help: str='Battery state of charge, in 0.1percent.  1000=100%'
    unit: str=''
    si_units: str=''
    scale_factor: int=-1
    unit_type: str=qt.UnitType.NONE
    def value(self):
        soc = self.battery.remaining/self.battery.capacity*1000
        return int(soc)

    
class eSpire(System):
    _tags = [BatteryCharging, BatteryDischarging, SoC]
    @classmethod
    def make_default(cls):
        battery = Battery(capacity=233*kWh,  remaining=150*kWh, voltage=832*volts, current=0*amps,
                 max_charge_rate= -150*amps,  max_discharge_rate = 150*amps)
        inverter = Inverter(output=0*kW, setpoint=0*kW, vac=480*volts)
        return cls(battery=battery, inverter=inverter)
    
    def as_dict(self):
        return {'battery': self.battery.as_dict(),
                'inverter': self.inverter.as_dict()}
SYSTEMS = {'eSpire': eSpire}



def make_record(ts, **kwargs):
    rec = kwargs
    rec.update({TS_COL: ts})
    return rec

def store(ts, table, **kwargs):
    rec = make_record(ts=ts, **kwargs)
    DB.table(table).insert(rec)

def charge_experiment():
    ts = 0
    es = eSpire.make()
    es.battery.remaining = es.battery.capacity*.35
    es.inverter.set_setpoint(-100*kW)

    stepsize = 60*unit.seconds
    for _ in range(60):
        store(ts=ts, table='eSpire', **es.as_dict())
        es = es.advance_time(duration=stepsize)
        ts += stepsize.to(unit.seconds).magnitude

class Emulator:
    def __init__(self, system_type, db=None, created_at=None):
        self.db = db or DB
        self.system_type  = system_type
        self.table = self.db.table(system_type)
        self.system_class = SYSTEMS[self.system_type]
        self.created_at = time.time() if created_at is None else created_at

    def play(self, max_records=10):
        for record in self.table.all()[:max_records]:
            system = self.system_class.load(record)
            print(record['ts'], system.telemetry())

    def ts_since_start(self):
        return time.time()-self.created_at

    def as_of(self, ts):
        # Define a query to retrieve the last record where ts is smaller than the target value
        Record = Query()
        query = (Record.ts <= ts)
        # Retrieve the last record that matches the query
        result = self.table.search(query)[-1] if self.table.search(query) else None
        return result
    
    def system_at(self, ts=None, now=False):
        assert now or ts is not None
        if now:
            ts = self.ts_since_start()
        record = self.as_of(ts)
        logger.debug(f'System at {ts} is {record}')
        return self.system_class.load(record)

    def telemetry_at(self, ts=None, now=False):
        assert (now) or (ts is not None)
        system = self.system_at(now=now, ts=ts)
        return system.telemetry()



if __name__ == '__main__':
    pass


