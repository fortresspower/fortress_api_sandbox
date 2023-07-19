import unittest 
from emulators import Emulator
import qtmessages37 as qt
from middleware import register_report_response_pipeline


class TestIntervals(unittest.TestCase):
    def test_hardcoded_interval(self):
        resource_id = 'espire'
        sampling_period = qt.SamplingPeriod(1, 1, False, qt.Modifier.M)

        power_properties = qt.PowerProperties(False, 60.0, 240.0)
        power_units = qt.Units("", qt.SiScaleCode.NONE, "W", qt.UnitType.POWER_REAL, power_properties)
        power_interval_props = qt.UsageIntervalProperties(qt.ReadingType.DIRECT_READ, qt.ReportType.USAGE, power_units)

        power_interval = qt.IntervalDescription("", resource_id, "POWER", sampling_period, power_interval_props)
        #make sure this doesn't raise anything
        power_interval.to_dict()

    def test_interval(self):
        emulator = Emulator(system_type='eSpire')
        now = True
        ts = None
        resource_id = 'espire'


        sampling_period = qt.SamplingPeriod(1, 1, False, qt.Modifier.M)

        battery_storage_system = emulator.system_at(now=now, ts=ts)

        usage_intervals = battery_storage_system.intervals(resource_id=resource_id, 
                                                            sampling_period=sampling_period, 
                                                            report_type=qt.ReportType.USAGE, 
                                                            market_context=None)
        for interval in usage_intervals:
            interval.to_dict()

    def test_response_pipeline(self):
        emulator = Emulator(system_type='eSpire')
        sampling_period = qt.SamplingPeriod(1, 1, False, qt.Modifier.M)

        response = register_report_response_pipeline(emulator=emulator, 
                                                        sampling_period=sampling_period,
                                                        resource_id='eSpire1',
                                                        now=True)
    
        response.to_dict()
    
if __name__ == '__main__':
    unittest.main()