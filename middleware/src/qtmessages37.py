# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = on_distribute_event_complete_from_dict(json.loads(json_string))
#     result = on_distribute_event_start_from_dict(json.loads(json_string))
#     result = on_distribute_event_start_response_from_dict(json.loads(json_string))
#     result = on_error_from_dict(json.loads(json_string))
#     result = on_event_archive_from_dict(json.loads(json_string))
#     result = on_event_cancel_from_dict(json.loads(json_string))
#     result = on_event_cancel_response_from_dict(json.loads(json_string))
#     result = on_event_complete_from_dict(json.loads(json_string))
#     result = on_event_interval_start_from_dict(json.loads(json_string))
#     result = on_event_from_dict(json.loads(json_string))
#     result = on_event_ramp_up_from_dict(json.loads(json_string))
#     result = on_event_response_from_dict(json.loads(json_string))
#     result = on_event_start_from_dict(json.loads(json_string))
#     result = on_heartbeat_from_dict(json.loads(json_string))
#     result = on_periodic_report_cancel_from_dict(json.loads(json_string))
#     result = on_periodic_report_complete_from_dict(json.loads(json_string))
#     result = on_periodic_report_start_from_dict(json.loads(json_string))
#     result = on_query_intervals_from_dict(json.loads(json_string))
#     result = on_query_intervals_response_from_dict(json.loads(json_string))
#     result = on_register_from_dict(json.loads(json_string))
#     result = on_register_reports_from_dict(json.loads(json_string))
#     result = on_register_reports_response_from_dict(json.loads(json_string))
#     result = on_status_response_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    # print(f'c is {type(c)}')
    # print(f'c origin is {dir(c)}')
    # print(f'x is {type(x)}')
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class MessageType(Enum):
    ON_DISTRIBUTE_EVENT_COMPLETE = "OnDistributeEventComplete"
    ON_DISTRIBUTE_EVENT_START = "OnDistributeEventStart"
    ON_ERROR = "OnError"
    ON_EVENT = "OnEvent"
    ON_EVENT_ARCHIVE = "OnEventArchive"
    ON_EVENT_CANCEL = "OnEventCancel"
    ON_EVENT_COMPLETE = "OnEventComplete"
    ON_EVENT_INTERVAL_START = "OnEventIntervalStart"
    ON_EVENT_RAMP_UP = "OnEventRampUp"
    ON_EVENT_START = "OnEventStart"
    ON_HEARTBEAT = "OnHeartbeat"
    ON_PERIODIC_REPORT_CANCEL = "OnPeriodicReportCancel"
    ON_PERIODIC_REPORT_COMPLETE = "OnPeriodicReportComplete"
    ON_PERIODIC_REPORT_START = "OnPeriodicReportStart"
    ON_QUERY_INTERVALS = "OnQueryIntervals"
    ON_REGISTER = "OnRegister"
    ON_REGISTER_REPORTS = "OnRegisterReports"


@dataclass
class Header:
    instance_id: str
    message_type: MessageType
    plugin_api_version: str
    plugin_version: str
    ven_id: str
    vtn_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Header':
        assert isinstance(obj, dict)
        instance_id = from_str(obj.get("instanceId"))
        message_type = MessageType(obj.get("messageType"))
        plugin_api_version = from_str(obj.get("pluginApiVersion"))
        plugin_version = from_str(obj.get("pluginVersion"))
        ven_id = from_str(obj.get("venId"))
        vtn_id = from_str(obj.get("vtnId"))
        return Header(instance_id, message_type, plugin_api_version, plugin_version, ven_id, vtn_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["instanceId"] = from_str(self.instance_id)
        result["messageType"] = to_enum(MessageType, self.message_type)
        result["pluginApiVersion"] = from_str(self.plugin_api_version)
        result["pluginVersion"] = from_str(self.plugin_version)
        result["venId"] = from_str(self.ven_id)
        result["vtnId"] = from_str(self.vtn_id)
        return result


@dataclass
class OnDistributeEventCompleteMessage:
    now_timet: int

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventCompleteMessage':
        assert isinstance(obj, dict)
        now_timet = from_int(obj.get("nowTimet"))
        return OnDistributeEventCompleteMessage(now_timet)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nowTimet"] = from_int(self.now_timet)
        return result


@dataclass
class OnDistributeEventComplete:
    header: Header
    on_distribute_event_complete_message: OnDistributeEventCompleteMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventComplete':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_distribute_event_complete_message = OnDistributeEventCompleteMessage.from_dict(obj.get("onDistributeEventCompleteMessage"))
        return OnDistributeEventComplete(header, on_distribute_event_complete_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onDistributeEventCompleteMessage"] = to_class(OnDistributeEventCompleteMessage, self.on_distribute_event_complete_message)
        return result


@dataclass
class SignalInterval:
    duration_in_seconds: int
    payload: float
    uid: int

    @staticmethod
    def from_dict(obj: Any) -> 'SignalInterval':
        assert isinstance(obj, dict)
        duration_in_seconds = from_int(obj.get("durationInSeconds"))
        payload = from_float(obj.get("payload"))
        uid = from_int(obj.get("uid"))
        return SignalInterval(duration_in_seconds, payload, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["durationInSeconds"] = from_int(self.duration_in_seconds)
        result["payload"] = to_float(self.payload)
        result["uid"] = from_int(self.uid)
        return result


@dataclass
class PowerProperties:
    ac: bool
    hertz: float
    voltage: float

    @staticmethod
    def from_dict(obj: Any) -> 'PowerProperties':
        assert isinstance(obj, dict)
        ac = from_bool(obj.get("ac"))
        hertz = from_float(obj.get("hertz"))
        voltage = from_float(obj.get("voltage"))
        return PowerProperties(ac, hertz, voltage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ac"] = from_bool(self.ac)
        result["hertz"] = to_float(self.hertz)
        result["voltage"] = to_float(self.voltage)
        return result


class SiScaleCode(Enum):
    C = "c"
    D = "d"
    G = "G"
    K = "k"
    M = "m"
    MICRO = "micro"
    N = "n"
    NONE = "none"
    P = "p"
    SI_SCALE_CODE_M = "M"
    T = "T"


class UnitType(Enum):
    CURRENCY = "CURRENCY"
    CURRENCY_PER_KW = "CURRENCY_PER_KW"
    CURRENCY_PER_KWH = "CURRENCY_PER_KWH"
    CURRENCY_PER_THM = "CURRENCY_PER_THM"
    CURRENT = "CURRENT"
    CUSTOM_UNIT = "CUSTOM_UNIT"
    ENERGY_APPARENT = "ENERGY_APPARENT"
    ENERGY_REACTIVE = "ENERGY_REACTIVE"
    ENERGY_REAL = "ENERGY_REAL"
    FREQUENCY = "FREQUENCY"
    NONE = "NONE"
    POWER_APPARENT = "POWER_APPARENT"
    POWER_REACTIVE = "POWER_REACTIVE"
    POWER_REAL = "POWER_REAL"
    PULSE_COUNT = "PULSE_COUNT"
    TEMPERATURE = "TEMPERATURE"
    THERM = "THERM"
    VOLTAGE = "VOLTAGE"


@dataclass
class Units:
    description: str
    si_scale_code: SiScaleCode
    units: str
    unit_type: UnitType
    power_properties: Optional[PowerProperties] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Units':
        assert isinstance(obj, dict)
        description = from_str(obj.get("description"))
        si_scale_code = SiScaleCode(obj.get("siScaleCode"))
        units = from_str(obj.get("units"))
        unit_type = UnitType(obj.get("unitType"))
        power_properties = from_union([PowerProperties.from_dict, from_none], obj.get("powerProperties"))
        return Units(description, si_scale_code, units, unit_type, power_properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_str(self.description)
        result["siScaleCode"] = to_enum(SiScaleCode, self.si_scale_code)
        result["units"] = from_str(self.units)
        result["unitType"] = to_enum(UnitType, self.unit_type)
        result["powerProperties"] = from_union([lambda x: to_class(PowerProperties, x), from_none], self.power_properties)
        return result


@dataclass
class Baseline:
    baseline_id: str
    baseline_name: str
    dt_start_timet: int
    duration_in_seconds: int
    intervals: List[SignalInterval]
    resource_ids: List[str]
    units: Optional[Units] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Baseline':
        assert isinstance(obj, dict)
        baseline_id = from_str(obj.get("baselineId"))
        baseline_name = from_str(obj.get("baselineName"))
        dt_start_timet = from_int(obj.get("dtStartTimet"))
        duration_in_seconds = from_int(obj.get("durationInSeconds"))
        intervals = from_list(SignalInterval.from_dict, obj.get("intervals"))
        resource_ids = from_list(from_str, obj.get("resourceIds"))
        units = from_union([Units.from_dict, from_none], obj.get("units"))
        return Baseline(baseline_id, baseline_name, dt_start_timet, duration_in_seconds, intervals, resource_ids, units)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baselineId"] = from_str(self.baseline_id)
        result["baselineName"] = from_str(self.baseline_name)
        result["dtStartTimet"] = from_int(self.dt_start_timet)
        result["durationInSeconds"] = from_int(self.duration_in_seconds)
        result["intervals"] = from_list(lambda x: to_class(SignalInterval, x), self.intervals)
        result["resourceIds"] = from_list(from_str, self.resource_ids)
        result["units"] = from_union([lambda x: to_class(Units, x), from_none], self.units)
        return result


@dataclass
class Duration:
    interval_in_seconds: int
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'Duration':
        assert isinstance(obj, dict)
        interval_in_seconds = from_int(obj.get("intervalInSeconds"))
        value = from_str(obj.get("value"))
        return Duration(interval_in_seconds, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["intervalInSeconds"] = from_int(self.interval_in_seconds)
        result["value"] = from_str(self.value)
        return result


@dataclass
class Randomization:
    is_randomized: bool
    randomization_in_seconds: int
    randomization_period_in_seconds: int

    @staticmethod
    def from_dict(obj: Any) -> 'Randomization':
        assert isinstance(obj, dict)
        is_randomized = from_bool(obj.get("isRandomized"))
        randomization_in_seconds = from_int(obj.get("randomizationInSeconds"))
        randomization_period_in_seconds = from_int(obj.get("randomizationPeriodInSeconds"))
        return Randomization(is_randomized, randomization_in_seconds, randomization_period_in_seconds)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isRandomized"] = from_bool(self.is_randomized)
        result["randomizationInSeconds"] = from_int(self.randomization_in_seconds)
        result["randomizationPeriodInSeconds"] = from_int(self.randomization_period_in_seconds)
        return result


@dataclass
class Signal:
    intervals: List[SignalInterval]
    signal_id: str
    signal_name: str
    signal_type: str
    units: Optional[Units] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Signal':
        assert isinstance(obj, dict)
        intervals = from_list(SignalInterval.from_dict, obj.get("intervals"))
        signal_id = from_str(obj.get("signalId"))
        signal_name = from_str(obj.get("signalName"))
        signal_type = from_str(obj.get("signalType"))
        units = from_union([Units.from_dict, from_none], obj.get("units"))
        return Signal(intervals, signal_id, signal_name, signal_type, units)

    def to_dict(self) -> dict:
        result: dict = {}
        result["intervals"] = from_list(lambda x: to_class(SignalInterval, x), self.intervals)
        result["signalId"] = from_str(self.signal_id)
        result["signalName"] = from_str(self.signal_name)
        result["signalType"] = from_str(self.signal_type)
        result["units"] = from_union([lambda x: to_class(Units, x), from_none], self.units)
        return result


@dataclass
class Targets:
    group_ids: List[str]
    resource_ids: List[str]
    party_id: Optional[str] = None
    ven_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Targets':
        assert isinstance(obj, dict)
        group_ids = from_list(from_str, obj.get("groupIds"))
        resource_ids = from_list(from_str, obj.get("resourceIds"))
        party_id = from_union([from_str, from_none], obj.get("partyId"))
        ven_id = from_union([from_str, from_none], obj.get("venId"))
        return Targets(group_ids, resource_ids, party_id, ven_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupIds"] = from_list(from_str, self.group_ids)
        result["resourceIds"] = from_list(from_str, self.resource_ids)
        result["partyId"] = from_union([from_str, from_none], self.party_id)
        result["venId"] = from_union([from_str, from_none], self.ven_id)
        return result


@dataclass
class Event:
    dt_start_timet: int
    duration: Duration
    duration_in_seconds: int
    event_id: str
    modification_number: int
    randomization: Randomization
    randomized_dt_start_timet: int
    signals: List[Signal]
    status: str
    targets: Targets
    baseline: Optional[Baseline] = None
    notification: Optional[Duration] = None
    ramp_up: Optional[Duration] = None
    recovery: Optional[Duration] = None
    tolerance: Optional[Duration] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        dt_start_timet = from_int(obj.get("dtStartTimet"))
        duration = Duration.from_dict(obj.get("duration"))
        duration_in_seconds = from_int(obj.get("durationInSeconds"))
        event_id = from_str(obj.get("eventId"))
        modification_number = from_int(obj.get("modificationNumber"))
        randomization = Randomization.from_dict(obj.get("randomization"))
        randomized_dt_start_timet = from_int(obj.get("randomizedDtStartTimet"))
        signals = from_list(Signal.from_dict, obj.get("signals"))
        status = from_str(obj.get("status"))
        targets = Targets.from_dict(obj.get("targets"))
        baseline = from_union([Baseline.from_dict, from_none], obj.get("baseline"))
        notification = from_union([Duration.from_dict, from_none], obj.get("notification"))
        ramp_up = from_union([Duration.from_dict, from_none], obj.get("rampUp"))
        recovery = from_union([Duration.from_dict, from_none], obj.get("recovery"))
        tolerance = from_union([Duration.from_dict, from_none], obj.get("tolerance"))
        return Event(dt_start_timet, duration, duration_in_seconds, event_id, modification_number, randomization, randomized_dt_start_timet, signals, status, targets, baseline, notification, ramp_up, recovery, tolerance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dtStartTimet"] = from_int(self.dt_start_timet)
        result["duration"] = to_class(Duration, self.duration)
        result["durationInSeconds"] = from_int(self.duration_in_seconds)
        result["eventId"] = from_str(self.event_id)
        result["modificationNumber"] = from_int(self.modification_number)
        result["randomization"] = to_class(Randomization, self.randomization)
        result["randomizedDtStartTimet"] = from_int(self.randomized_dt_start_timet)
        result["signals"] = from_list(lambda x: to_class(Signal, x), self.signals)
        result["status"] = from_str(self.status)
        result["targets"] = to_class(Targets, self.targets)
        result["baseline"] = from_union([lambda x: to_class(Baseline, x), from_none], self.baseline)
        result["notification"] = from_union([lambda x: to_class(Duration, x), from_none], self.notification)
        result["rampUp"] = from_union([lambda x: to_class(Duration, x), from_none], self.ramp_up)
        result["recovery"] = from_union([lambda x: to_class(Duration, x), from_none], self.recovery)
        result["tolerance"] = from_union([lambda x: to_class(Duration, x), from_none], self.tolerance)
        return result


@dataclass
class OnDistributeEventStartMessage:
    events: List[Event]

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventStartMessage':
        assert isinstance(obj, dict)
        events = from_list(Event.from_dict, obj.get("events"))
        return OnDistributeEventStartMessage(events)

    def to_dict(self) -> dict:
        result: dict = {}
        result["events"] = from_list(lambda x: to_class(Event, x), self.events)
        return result


@dataclass
class OnDistributeEventStart:
    header: Header
    on_distribute_event_start_message: OnDistributeEventStartMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventStart':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_distribute_event_start_message = OnDistributeEventStartMessage.from_dict(obj.get("onDistributeEventStartMessage"))
        return OnDistributeEventStart(header, on_distribute_event_start_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onDistributeEventStartMessage"] = to_class(OnDistributeEventStartMessage, self.on_distribute_event_start_message)
        return result


class OptType(Enum):
    OPT_IN = "optIn"
    OPT_OUT = "optOut"


@dataclass
class OnDistributeEventStartResponseMessage:
    default_opt_type: OptType

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventStartResponseMessage':
        assert isinstance(obj, dict)
        default_opt_type = OptType(obj.get("defaultOptType"))
        return OnDistributeEventStartResponseMessage(default_opt_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["defaultOptType"] = to_enum(OptType, self.default_opt_type)
        return result


@dataclass
class OnDistributeEventStartResponse:
    on_distribute_event_start_response_message: OnDistributeEventStartResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnDistributeEventStartResponse':
        assert isinstance(obj, dict)
        on_distribute_event_start_response_message = OnDistributeEventStartResponseMessage.from_dict(obj.get("onDistributeEventStartResponseMessage"))
        return OnDistributeEventStartResponse(on_distribute_event_start_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onDistributeEventStartResponseMessage"] = to_class(OnDistributeEventStartResponseMessage, self.on_distribute_event_start_response_message)
        return result


@dataclass
class OnErrorMessage:
    message: str

    @staticmethod
    def from_dict(obj: Any) -> 'OnErrorMessage':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        return OnErrorMessage(message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        return result


@dataclass
class OnError:
    header: Header
    on_error_message: OnErrorMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnError':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_error_message = OnErrorMessage.from_dict(obj.get("onErrorMessage"))
        return OnError(header, on_error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onErrorMessage"] = to_class(OnErrorMessage, self.on_error_message)
        return result


@dataclass
class OnEventArchiveMessage:
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventArchiveMessage':
        assert isinstance(obj, dict)
        event = Event.from_dict(obj.get("event"))
        return OnEventArchiveMessage(event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventArchive:
    header: Header
    on_event_archive_message: OnEventArchiveMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventArchive':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_archive_message = OnEventArchiveMessage.from_dict(obj.get("onEventArchiveMessage"))
        return OnEventArchive(header, on_event_archive_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventArchiveMessage"] = to_class(OnEventArchiveMessage, self.on_event_archive_message)
        return result


@dataclass
class OnEventCancelMessage:
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventCancelMessage':
        assert isinstance(obj, dict)
        event = Event.from_dict(obj.get("event"))
        return OnEventCancelMessage(event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventCancel:
    header: Header
    on_event_cancel_message: OnEventCancelMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventCancel':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_cancel_message = OnEventCancelMessage.from_dict(obj.get("onEventCancelMessage"))
        return OnEventCancel(header, on_event_cancel_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventCancelMessage"] = to_class(OnEventCancelMessage, self.on_event_cancel_message)
        return result


class OptReason(Enum):
    ECONOMIC = "economic"
    EMERGENCY = "emergency"
    MUST_RUN = "mustRun"
    NOT_PARTICIPATING = "notParticipating"
    OUTAGE_RUN_STATUS = "outageRunStatus"
    OVERRIDE_STATUS = "overrideStatus"
    PARTICIPATING = "participating"
    X_SCHEDULE = "x-schedule"


@dataclass
class OptMessage:
    opt_id: str
    opt_reason: OptReason
    opt_type: OptType
    resource_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'OptMessage':
        assert isinstance(obj, dict)
        opt_id = from_str(obj.get("optId"))
        opt_reason = OptReason(obj.get("optReason"))
        opt_type = OptType(obj.get("optType"))
        resource_id = from_str(obj.get("resourceId"))
        return OptMessage(opt_id, opt_reason, opt_type, resource_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["optId"] = from_str(self.opt_id)
        result["optReason"] = to_enum(OptReason, self.opt_reason)
        result["optType"] = to_enum(OptType, self.opt_type)
        result["resourceId"] = from_str(self.resource_id)
        return result


@dataclass
class OptEvent:
    opt_type: OptType
    schedule_event: bool
    opt_messages: Optional[List[OptMessage]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'OptEvent':
        assert isinstance(obj, dict)
        opt_type = OptType(obj.get("optType"))
        schedule_event = from_bool(obj.get("scheduleEvent"))
        opt_messages = from_union([lambda x: from_list(OptMessage.from_dict, x), from_none], obj.get("optMessages"))
        return OptEvent(opt_type, schedule_event, opt_messages)

    def to_dict(self) -> dict:
        result: dict = {}
        result["optType"] = to_enum(OptType, self.opt_type)
        result["scheduleEvent"] = from_bool(self.schedule_event)
        result["optMessages"] = from_union([lambda x: from_list(lambda x: to_class(OptMessage, x), x), from_none], self.opt_messages)
        return result


@dataclass
class OnEventCancelResponseMessage:
    opt_event: OptEvent

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventCancelResponseMessage':
        assert isinstance(obj, dict)
        opt_event = OptEvent.from_dict(obj.get("optEvent"))
        return OnEventCancelResponseMessage(opt_event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["optEvent"] = to_class(OptEvent, self.opt_event)
        return result


@dataclass
class OnEventCancelResponse:
    on_event_cancel_response_message: OnEventCancelResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventCancelResponse':
        assert isinstance(obj, dict)
        on_event_cancel_response_message = OnEventCancelResponseMessage.from_dict(obj.get("onEventCancelResponseMessage"))
        return OnEventCancelResponse(on_event_cancel_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onEventCancelResponseMessage"] = to_class(OnEventCancelResponseMessage, self.on_event_cancel_response_message)
        return result


@dataclass
class OnEventCompleteMessage:
    dt_end_timet: int
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventCompleteMessage':
        assert isinstance(obj, dict)
        dt_end_timet = from_int(obj.get("dtEndTimet"))
        event = Event.from_dict(obj.get("event"))
        return OnEventCompleteMessage(dt_end_timet, event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dtEndTimet"] = from_int(self.dt_end_timet)
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventComplete:
    header: Header
    on_event_complete_message: OnEventCompleteMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventComplete':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_complete_message = OnEventCompleteMessage.from_dict(obj.get("onEventCompleteMessage"))
        return OnEventComplete(header, on_event_complete_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventCompleteMessage"] = to_class(OnEventCompleteMessage, self.on_event_complete_message)
        return result


@dataclass
class ActiveInterval:
    dt_start_timet: int
    interval_index: int
    payload: float
    signal_id: str
    signal_index: int

    @staticmethod
    def from_dict(obj: Any) -> 'ActiveInterval':
        assert isinstance(obj, dict)
        dt_start_timet = from_int(obj.get("dtStartTimet"))
        interval_index = from_int(obj.get("intervalIndex"))
        payload = from_float(obj.get("payload"))
        signal_id = from_str(obj.get("signalId"))
        signal_index = from_int(obj.get("signalIndex"))
        return ActiveInterval(dt_start_timet, interval_index, payload, signal_id, signal_index)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dtStartTimet"] = from_int(self.dt_start_timet)
        result["intervalIndex"] = from_int(self.interval_index)
        result["payload"] = to_float(self.payload)
        result["signalId"] = from_str(self.signal_id)
        result["signalIndex"] = from_int(self.signal_index)
        return result


@dataclass
class OnEventIntervalStartMessage:
    active_interval: ActiveInterval
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventIntervalStartMessage':
        assert isinstance(obj, dict)
        active_interval = ActiveInterval.from_dict(obj.get("activeInterval"))
        event = Event.from_dict(obj.get("event"))
        return OnEventIntervalStartMessage(active_interval, event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activeInterval"] = to_class(ActiveInterval, self.active_interval)
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventIntervalStart:
    header: Header
    on_event_interval_start_message: OnEventIntervalStartMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventIntervalStart':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_interval_start_message = OnEventIntervalStartMessage.from_dict(obj.get("onEventIntervalStartMessage"))
        return OnEventIntervalStart(header, on_event_interval_start_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventIntervalStartMessage"] = to_class(OnEventIntervalStartMessage, self.on_event_interval_start_message)
        return result


@dataclass
class OnEventMessage:
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventMessage':
        assert isinstance(obj, dict)
        event = Event.from_dict(obj.get("event"))
        return OnEventMessage(event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEvent:
    header: Header
    on_event_message: OnEventMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEvent':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_message = OnEventMessage.from_dict(obj.get("onEventMessage"))
        return OnEvent(header, on_event_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventMessage"] = to_class(OnEventMessage, self.on_event_message)
        return result


@dataclass
class OnEventRampUpMessage:
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventRampUpMessage':
        assert isinstance(obj, dict)
        event = Event.from_dict(obj.get("event"))
        return OnEventRampUpMessage(event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventRampUp:
    header: Header
    on_event_ramp_up_message: OnEventRampUpMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventRampUp':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_ramp_up_message = OnEventRampUpMessage.from_dict(obj.get("onEventRampUpMessage"))
        return OnEventRampUp(header, on_event_ramp_up_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventRampUpMessage"] = to_class(OnEventRampUpMessage, self.on_event_ramp_up_message)
        return result


@dataclass
class OnEventResponseMessage:
    opt_event: OptEvent

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventResponseMessage':
        assert isinstance(obj, dict)
        opt_event = OptEvent.from_dict(obj.get("optEvent"))
        return OnEventResponseMessage(opt_event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["optEvent"] = to_class(OptEvent, self.opt_event)
        return result


@dataclass
class OnEventResponse:
    on_event_response_message: OnEventResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventResponse':
        assert isinstance(obj, dict)
        on_event_response_message = OnEventResponseMessage.from_dict(obj.get("onEventResponseMessage"))
        return OnEventResponse(on_event_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onEventResponseMessage"] = to_class(OnEventResponseMessage, self.on_event_response_message)
        return result


@dataclass
class OnEventStartMessage:
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventStartMessage':
        assert isinstance(obj, dict)
        event = Event.from_dict(obj.get("event"))
        return OnEventStartMessage(event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = to_class(Event, self.event)
        return result


@dataclass
class OnEventStart:
    header: Header
    on_event_start_message: OnEventStartMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnEventStart':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_event_start_message = OnEventStartMessage.from_dict(obj.get("onEventStartMessage"))
        return OnEventStart(header, on_event_start_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onEventStartMessage"] = to_class(OnEventStartMessage, self.on_event_start_message)
        return result


@dataclass
class OnHeartbeatMessage:
    now_timet: int

    @staticmethod
    def from_dict(obj: Any) -> 'OnHeartbeatMessage':
        assert isinstance(obj, dict)
        now_timet = from_int(obj.get("nowTimet"))
        return OnHeartbeatMessage(now_timet)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nowTimet"] = from_int(self.now_timet)
        return result


@dataclass
class OnHeartbeat:
    header: Header
    on_heartbeat_message: OnHeartbeatMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnHeartbeat':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_heartbeat_message = OnHeartbeatMessage.from_dict(obj.get("onHeartbeatMessage"))
        return OnHeartbeat(header, on_heartbeat_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onHeartbeatMessage"] = to_class(OnHeartbeatMessage, self.on_heartbeat_message)
        return result


@dataclass
class OnPeriodicReportCancelMessage:
    report_request_id: str
    report_specifier_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportCancelMessage':
        assert isinstance(obj, dict)
        report_request_id = from_str(obj.get("reportRequestId"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        return OnPeriodicReportCancelMessage(report_request_id, report_specifier_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reportRequestId"] = from_str(self.report_request_id)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        return result


@dataclass
class OnPeriodicReportCancel:
    header: Header
    on_periodic_report_cancel_message: OnPeriodicReportCancelMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportCancel':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_periodic_report_cancel_message = OnPeriodicReportCancelMessage.from_dict(obj.get("onPeriodicReportCancelMessage"))
        return OnPeriodicReportCancel(header, on_periodic_report_cancel_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onPeriodicReportCancelMessage"] = to_class(OnPeriodicReportCancelMessage, self.on_periodic_report_cancel_message)
        return result


@dataclass
class OnPeriodicReportCompleteMessage:
    report_request_id: str
    report_specifier_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportCompleteMessage':
        assert isinstance(obj, dict)
        report_request_id = from_str(obj.get("reportRequestId"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        return OnPeriodicReportCompleteMessage(report_request_id, report_specifier_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reportRequestId"] = from_str(self.report_request_id)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        return result


@dataclass
class OnPeriodicReportComplete:
    header: Header
    on_periodic_report_complete_message: OnPeriodicReportCompleteMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportComplete':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_periodic_report_complete_message = OnPeriodicReportCompleteMessage.from_dict(obj.get("onPeriodicReportCompleteMessage"))
        return OnPeriodicReportComplete(header, on_periodic_report_complete_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onPeriodicReportCompleteMessage"] = to_class(OnPeriodicReportCompleteMessage, self.on_periodic_report_complete_message)
        return result


@dataclass
class ReportingInterval:
    dt_start_timet: int
    duration: str

    @staticmethod
    def from_dict(obj: Any) -> 'ReportingInterval':
        assert isinstance(obj, dict)
        dt_start_timet = from_int(obj.get("dtStartTimet"))
        duration = from_str(obj.get("duration"))
        return ReportingInterval(dt_start_timet, duration)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dtStartTimet"] = from_int(self.dt_start_timet)
        result["duration"] = from_str(self.duration)
        return result


@dataclass
class SpecifierPayload:
    reading_type: str
    r_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'SpecifierPayload':
        assert isinstance(obj, dict)
        reading_type = from_str(obj.get("readingType"))
        r_id = from_str(obj.get("rId"))
        return SpecifierPayload(reading_type, r_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["readingType"] = from_str(self.reading_type)
        result["rId"] = from_str(self.r_id)
        return result


@dataclass
class ReportRequest:
    granularity: str
    report_back_duration: str
    report_request_id: str
    report_specifier_id: str
    specifier_payloads: List[SpecifierPayload]
    reporting_interval: Optional[ReportingInterval] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ReportRequest':
        assert isinstance(obj, dict)
        granularity = from_str(obj.get("granularity"))
        report_back_duration = from_str(obj.get("reportBackDuration"))
        report_request_id = from_str(obj.get("reportRequestId"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        specifier_payloads = from_list(SpecifierPayload.from_dict, obj.get("specifierPayloads"))
        reporting_interval = from_union([ReportingInterval.from_dict, from_none], obj.get("reportingInterval"))
        return ReportRequest(granularity, report_back_duration, report_request_id, report_specifier_id, specifier_payloads, reporting_interval)

    def to_dict(self) -> dict:
        result: dict = {}
        result["granularity"] = from_str(self.granularity)
        result["reportBackDuration"] = from_str(self.report_back_duration)
        result["reportRequestId"] = from_str(self.report_request_id)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        result["specifierPayloads"] = from_list(lambda x: to_class(SpecifierPayload, x), self.specifier_payloads)
        result["reportingInterval"] = from_union([lambda x: to_class(ReportingInterval, x), from_none], self.reporting_interval)
        return result


@dataclass
class OnPeriodicReportStartMessage:
    report_request: ReportRequest

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportStartMessage':
        assert isinstance(obj, dict)
        report_request = ReportRequest.from_dict(obj.get("reportRequest"))
        return OnPeriodicReportStartMessage(report_request)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reportRequest"] = to_class(ReportRequest, self.report_request)
        return result


@dataclass
class OnPeriodicReportStart:
    header: Header
    on_periodic_report_start_message: OnPeriodicReportStartMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnPeriodicReportStart':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_periodic_report_start_message = OnPeriodicReportStartMessage.from_dict(obj.get("onPeriodicReportStartMessage"))
        return OnPeriodicReportStart(header, on_periodic_report_start_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onPeriodicReportStartMessage"] = to_class(OnPeriodicReportStartMessage, self.on_periodic_report_start_message)
        return result


@dataclass
class OnQueryIntervalsMessage:
    end_timet: int
    granularity_in_seconds: int
    report_request_id: str
    report_specifier_id: str
    r_ids: List[str]
    start_timet: int

    @staticmethod
    def from_dict(obj: Any) -> 'OnQueryIntervalsMessage':
        assert isinstance(obj, dict)
        end_timet = from_int(obj.get("endTimet"))
        granularity_in_seconds = from_int(obj.get("granularityInSeconds"))
        report_request_id = from_str(obj.get("reportRequestId"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        r_ids = from_list(from_str, obj.get("rIds"))
        start_timet = from_int(obj.get("startTimet"))
        return OnQueryIntervalsMessage(end_timet, granularity_in_seconds, report_request_id, report_specifier_id, r_ids, start_timet)

    def to_dict(self) -> dict:
        result: dict = {}
        result["endTimet"] = from_int(self.end_timet)
        result["granularityInSeconds"] = from_int(self.granularity_in_seconds)
        result["reportRequestId"] = from_str(self.report_request_id)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        result["rIds"] = from_list(from_str, self.r_ids)
        result["startTimet"] = from_int(self.start_timet)
        return result


@dataclass
class OnQueryIntervals:
    header: Header
    on_query_intervals_message: OnQueryIntervalsMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnQueryIntervals':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_query_intervals_message = OnQueryIntervalsMessage.from_dict(obj.get("onQueryIntervalsMessage"))
        return OnQueryIntervals(header, on_query_intervals_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onQueryIntervalsMessage"] = to_class(OnQueryIntervalsMessage, self.on_query_intervals_message)
        return result


@dataclass
class ReportIdentifier:
    name: str
    report_id: str
    report_request_id: str
    report_specifier_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'ReportIdentifier':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        report_id = from_str(obj.get("reportId"))
        report_request_id = from_str(obj.get("reportRequestId"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        return ReportIdentifier(name, report_id, report_request_id, report_specifier_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["reportId"] = from_str(self.report_id)
        result["reportRequestId"] = from_str(self.report_request_id)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        return result


class DataQuality(Enum):
    NO_NEW_VALUE_PREVIOUS_VALUE_USED = "No New Value - Previous Value Used"
    NO_QUALITY_NO_VALUE = "No Quality - No Value"
    QUALITY_BAD_COMM_FAILURE = "Quality Bad - Comm Failure"
    QUALITY_BAD_CONFIGURATION_ERROR = "Quality Bad - Configuration Error"
    QUALITY_BAD_DEVICE_FAILURE = "Quality Bad - Device Failure"
    QUALITY_BAD_LAST_KNOWN_VALUE = "Quality Bad - Last Known Value"
    QUALITY_BAD_NON_SPECIFIC = "Quality Bad - Non Specific"
    QUALITY_BAD_NOT_CONNECTED = "Quality Bad - Not Connected"
    QUALITY_BAD_OUT_OF_SERVICE = "Quality Bad - Out of Service"
    QUALITY_BAD_SENSOR_FAILURE = "Quality Bad - Sensor Failure"
    QUALITY_GOOD_LOCAL_OVERRIDE = "Quality Good - Local Override"
    QUALITY_GOOD_NON_SPECIFIC = "Quality Good - Non Specific"
    QUALITY_LIMIT_FIELD_CONSTANT = "Quality Limit - Field/Constant"
    QUALITY_LIMIT_FIELD_HIGH = "Quality Limit - Field/High"
    QUALITY_LIMIT_FIELD_LOW = "Quality Limit - Field/Low"
    QUALITY_LIMIT_FIELD_NOT = "Quality Limit - Field/Not"
    QUALITY_UNCERTAIN_EU_UNITS_EXCEEDED = "Quality Uncertain - EU Units Exceeded"
    QUALITY_UNCERTAIN_LAST_USABLE_VALUE = "Quality Uncertain - Last Usable Value"
    QUALITY_UNCERTAIN_NON_SPECIFIC = "Quality Uncertain - Non Specific"
    QUALITY_UNCERTAIN_SENSOR_NOT_ACCURATE = "Quality Uncertain - Sensor Not Accurate"
    QUALITY_UNCERTAIN_SUB_NORMAL = "Quality Uncertain - Sub Normal"


class Modifier(Enum):
    H = "H"
    M = "M"
    S = "S"


@dataclass
class DurationDescription:
    duration: int
    duration_modifier: Modifier

    @staticmethod
    def from_dict(obj: Any) -> 'DurationDescription':
        assert isinstance(obj, dict)
        duration = from_int(obj.get("duration"))
        duration_modifier = Modifier(obj.get("durationModifier"))
        return DurationDescription(duration, duration_modifier)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_int(self.duration)
        result["durationModifier"] = to_enum(Modifier, self.duration_modifier)
        return result


@dataclass
class StatusClass:
    online: bool
    override: bool

    @staticmethod
    def from_dict(obj: Any) -> 'StatusClass':
        assert isinstance(obj, dict)
        online = from_bool(obj.get("online"))
        override = from_bool(obj.get("override"))
        return StatusClass(online, override)

    def to_dict(self) -> dict:
        result: dict = {}
        result["online"] = from_bool(self.online)
        result["override"] = from_bool(self.override)
        return result


@dataclass
class ReportInterval:
    data_quality: DataQuality
    dt_start_timet: int
    r_id: str
    value: float
    duration: Optional[DurationDescription] = None
    status: Optional[StatusClass] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ReportInterval':
        assert isinstance(obj, dict)
        data_quality = DataQuality(obj.get("dataQuality"))
        dt_start_timet = from_int(obj.get("dtStartTimet"))
        r_id = from_str(obj.get("rId"))
        value = from_float(obj.get("value"))
        duration = from_union([DurationDescription.from_dict, from_none], obj.get("duration"))
        status = from_union([StatusClass.from_dict, from_none], obj.get("status"))
        return ReportInterval(data_quality, dt_start_timet, r_id, value, duration, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataQuality"] = to_enum(DataQuality, self.data_quality)
        result["dtStartTimet"] = from_int(self.dt_start_timet)
        result["rId"] = from_str(self.r_id)
        result["value"] = to_float(self.value)
        result["duration"] = from_union([lambda x: to_class(DurationDescription, x), from_none], self.duration)
        result["status"] = from_union([lambda x: to_class(StatusClass, x), from_none], self.status)
        return result


@dataclass
class Report:
    report_intervals: List[ReportInterval]
    report_identifier: Optional[ReportIdentifier] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Report':
        assert isinstance(obj, dict)
        report_intervals = from_list(ReportInterval.from_dict, obj.get("reportIntervals"))
        report_identifier = from_union([ReportIdentifier.from_dict, from_none], obj.get("reportIdentifier"))
        return Report(report_intervals, report_identifier)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reportIntervals"] = from_list(lambda x: to_class(ReportInterval, x), self.report_intervals)
        result["reportIdentifier"] = from_union([lambda x: to_class(ReportIdentifier, x), from_none], self.report_identifier)
        return result


@dataclass
class OnQueryIntervalsResponseMessage:
    reports: List[Report]

    @staticmethod
    def from_dict(obj: Any) -> 'OnQueryIntervalsResponseMessage':
        assert isinstance(obj, dict)
        reports = from_list(Report.from_dict, obj.get("reports"))
        return OnQueryIntervalsResponseMessage(reports)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reports"] = from_list(lambda x: to_class(Report, x), self.reports)
        return result


@dataclass
class OnQueryIntervalsResponse:
    on_query_intervals_response_message: OnQueryIntervalsResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnQueryIntervalsResponse':
        assert isinstance(obj, dict)
        on_query_intervals_response_message = OnQueryIntervalsResponseMessage.from_dict(obj.get("onQueryIntervalsResponseMessage"))
        return OnQueryIntervalsResponse(on_query_intervals_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onQueryIntervalsResponseMessage"] = to_class(OnQueryIntervalsResponseMessage, self.on_query_intervals_response_message)
        return result


@dataclass
class OnRegisterMessage:
    now_timet: int

    @staticmethod
    def from_dict(obj: Any) -> 'OnRegisterMessage':
        assert isinstance(obj, dict)
        now_timet = from_int(obj.get("nowTimet"))
        return OnRegisterMessage(now_timet)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nowTimet"] = from_int(self.now_timet)
        return result


@dataclass
class OnRegister:
    header: Header
    on_register_message: OnRegisterMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnRegister':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        on_register_message = OnRegisterMessage.from_dict(obj.get("onRegisterMessage"))
        return OnRegister(header, on_register_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        result["onRegisterMessage"] = to_class(OnRegisterMessage, self.on_register_message)
        return result


@dataclass
class OnRegisterReports:
    header: Header

    @staticmethod
    def from_dict(obj: Any) -> 'OnRegisterReports':
        assert isinstance(obj, dict)
        header = Header.from_dict(obj.get("header"))
        return OnRegisterReports(header)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = to_class(Header, self.header)
        return result


@dataclass
class SamplingPeriod:
    max_sampling_period: int
    min_sampling_period: int
    on_change: bool
    sampling_period_modifier: Modifier

    @staticmethod
    def from_dict(obj: Any) -> 'SamplingPeriod':
        assert isinstance(obj, dict)
        max_sampling_period = from_int(obj.get("maxSamplingPeriod"))
        min_sampling_period = from_int(obj.get("minSamplingPeriod"))
        on_change = from_bool(obj.get("onChange"))
        sampling_period_modifier = Modifier(obj.get("samplingPeriodModifier"))
        return SamplingPeriod(max_sampling_period, min_sampling_period, on_change, sampling_period_modifier)

    def to_dict(self) -> dict:
        result: dict = {}
        result["maxSamplingPeriod"] = from_int(self.max_sampling_period)
        result["minSamplingPeriod"] = from_int(self.min_sampling_period)
        result["onChange"] = from_bool(self.on_change)
        result["samplingPeriodModifier"] = to_enum(Modifier, self.sampling_period_modifier)
        return result


class ReadingType(Enum):
    ALLOCATED = "Allocated"
    CONTRACT = "Contract"
    DERIVED = "Derived"
    DIRECT_READ = "Direct Read"
    ESTIMATED = "Estimated"
    HYBRID = "Hybrid"
    MEAN = "Mean"
    NET = "Net"
    PEAK = "Peak"
    PROJECTED = "Projected"
    SUMMED = "Summed"
    X_RMS = "x-RMS"


class ReportType(Enum):
    AVAILABLE_ENERGY_STORAGE = "availableEnergyStorage"
    AVG_DEMAND = "avgDemand"
    AVG_USAGE = "avgUsage"
    BASELINE = "baseline"
    DELTA_DEMAND = "deltaDemand"
    DELTA_SETPOINT = "deltaSetpoint"
    DELTA_USAGE = "deltaUsage"
    DEMAND = "demand"
    DEVIATION = "deviation"
    DOWN_REGULATION_CAPACITY_AVAILABLE = "downRegulationCapacityAvailable"
    LEVEL = "level"
    OPERATING_STATE = "operatingState"
    PERCENT_DEMAND = "percentDemand"
    PERCENT_USAGE = "percentUsage"
    POWER_FACTOR = "powerFactor"
    PRICE = "price"
    READING = "reading"
    REGULATION_SETPOINT = "regulationSetpoint"
    SET_POINT = "setPoint"
    STORED_ENERGY = "storedEnergy"
    TARGET_ENERGY_STORAGE = "targetEnergyStorage"
    UP_REGULATION_CAPACITY_AVAILABLE = "upRegulationCapacityAvailable"
    USAGE = "usage"


@dataclass
class UsageIntervalProperties:
    reading_type: ReadingType
    report_type: ReportType
    units: Units

    @staticmethod
    def from_dict(obj: Any) -> 'UsageIntervalProperties':
        assert isinstance(obj, dict)
        reading_type = ReadingType(obj.get("readingType"))
        report_type = ReportType(obj.get("reportType"))
        units = Units.from_dict(obj.get("units"))
        return UsageIntervalProperties(reading_type, report_type, units)

    def to_dict(self) -> dict:
        result: dict = {}
        result["readingType"] = to_enum(ReadingType, self.reading_type)
        result["reportType"] = to_enum(ReportType, self.report_type)
        result["units"] = to_class(Units, self.units)
        return result


@dataclass
class IntervalDescription:
    market_context: str
    resource_id: str
    rid: str
    sampling_period: SamplingPeriod
    usage_interval_properties: Optional[UsageIntervalProperties] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IntervalDescription':
        assert isinstance(obj, dict)
        market_context = from_str(obj.get("marketContext"))
        resource_id = from_str(obj.get("resourceId"))
        rid = from_str(obj.get("rid"))
        sampling_period = SamplingPeriod.from_dict(obj.get("samplingPeriod"))
        usage_interval_properties = from_union([UsageIntervalProperties.from_dict, from_none], obj.get("usageIntervalProperties"))
        return IntervalDescription(market_context, resource_id, rid, sampling_period, usage_interval_properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["marketContext"] = from_str(self.market_context)
        result["resourceId"] = from_str(self.resource_id)
        result["rid"] = from_str(self.rid)
        result["samplingPeriod"] = to_class(SamplingPeriod, self.sampling_period)
        result["usageIntervalProperties"] = from_union([lambda x: to_class(UsageIntervalProperties, x), from_none], self.usage_interval_properties)
        return result


@dataclass
class TelemetryReport:
    duration: DurationDescription
    interval_descriptions: List[IntervalDescription]
    report_name: str
    report_specifier_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'TelemetryReport':
        assert isinstance(obj, dict)
        duration = DurationDescription.from_dict(obj.get("duration"))
        interval_descriptions = from_list(IntervalDescription.from_dict, obj.get("intervalDescriptions"))
        report_name = from_str(obj.get("reportName"))
        report_specifier_id = from_str(obj.get("reportSpecifierId"))
        return TelemetryReport(duration, interval_descriptions, report_name, report_specifier_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = to_class(DurationDescription, self.duration)
        result["intervalDescriptions"] = from_list(lambda x: to_class(IntervalDescription, x), self.interval_descriptions)
        result["reportName"] = from_str(self.report_name)
        result["reportSpecifierId"] = from_str(self.report_specifier_id)
        return result


@dataclass
class OnRegisterReportsResponseMessage:
    telemetry_reports: List[TelemetryReport]

    @staticmethod
    def from_dict(obj: Any) -> 'OnRegisterReportsResponseMessage':
        assert isinstance(obj, dict)
        telemetry_reports = from_list(TelemetryReport.from_dict, obj.get("telemetryReports"))
        return OnRegisterReportsResponseMessage(telemetry_reports)

    def to_dict(self) -> dict:
        result: dict = {}
        result["telemetryReports"] = from_list(lambda x: to_class(TelemetryReport, x), self.telemetry_reports)
        return result


@dataclass
class OnRegisterReportsResponse:
    on_register_reports_response_message: OnRegisterReportsResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnRegisterReportsResponse':
        assert isinstance(obj, dict)
        on_register_reports_response_message = OnRegisterReportsResponseMessage.from_dict(obj.get("onRegisterReportsResponseMessage"))
        return OnRegisterReportsResponse(on_register_reports_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onRegisterReportsResponseMessage"] = to_class(OnRegisterReportsResponseMessage, self.on_register_reports_response_message)
        return result


class StatusEnum(Enum):
    ERROR = "ERROR"
    OK = "OK"
    RETRY = "RETRY"


@dataclass
class OnStatusResponseMessage:
    message: str
    status: StatusEnum

    @staticmethod
    def from_dict(obj: Any) -> 'OnStatusResponseMessage':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        status = StatusEnum(obj.get("status"))
        return OnStatusResponseMessage(message, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        result["status"] = to_enum(StatusEnum, self.status)
        return result


@dataclass
class OnStatusResponse:
    on_status_response_message: OnStatusResponseMessage

    @staticmethod
    def from_dict(obj: Any) -> 'OnStatusResponse':
        assert isinstance(obj, dict)
        on_status_response_message = OnStatusResponseMessage.from_dict(obj.get("onStatusResponseMessage"))
        return OnStatusResponse(on_status_response_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["onStatusResponseMessage"] = to_class(OnStatusResponseMessage, self.on_status_response_message)
        return result


def on_distribute_event_complete_from_dict(s: Any) -> OnDistributeEventComplete:
    return OnDistributeEventComplete.from_dict(s)


def on_distribute_event_complete_to_dict(x: OnDistributeEventComplete) -> Any:
    return to_class(OnDistributeEventComplete, x)


def on_distribute_event_start_from_dict(s: Any) -> OnDistributeEventStart:
    return OnDistributeEventStart.from_dict(s)


def on_distribute_event_start_to_dict(x: OnDistributeEventStart) -> Any:
    return to_class(OnDistributeEventStart, x)


def on_distribute_event_start_response_from_dict(s: Any) -> OnDistributeEventStartResponse:
    return OnDistributeEventStartResponse.from_dict(s)


def on_distribute_event_start_response_to_dict(x: OnDistributeEventStartResponse) -> Any:
    return to_class(OnDistributeEventStartResponse, x)


def on_error_from_dict(s: Any) -> OnError:
    return OnError.from_dict(s)


def on_error_to_dict(x: OnError) -> Any:
    return to_class(OnError, x)


def on_event_archive_from_dict(s: Any) -> OnEventArchive:
    return OnEventArchive.from_dict(s)


def on_event_archive_to_dict(x: OnEventArchive) -> Any:
    return to_class(OnEventArchive, x)


def on_event_cancel_from_dict(s: Any) -> OnEventCancel:
    return OnEventCancel.from_dict(s)


def on_event_cancel_to_dict(x: OnEventCancel) -> Any:
    return to_class(OnEventCancel, x)


def on_event_cancel_response_from_dict(s: Any) -> OnEventCancelResponse:
    return OnEventCancelResponse.from_dict(s)


def on_event_cancel_response_to_dict(x: OnEventCancelResponse) -> Any:
    return to_class(OnEventCancelResponse, x)


def on_event_complete_from_dict(s: Any) -> OnEventComplete:
    return OnEventComplete.from_dict(s)


def on_event_complete_to_dict(x: OnEventComplete) -> Any:
    return to_class(OnEventComplete, x)


def on_event_interval_start_from_dict(s: Any) -> OnEventIntervalStart:
    return OnEventIntervalStart.from_dict(s)


def on_event_interval_start_to_dict(x: OnEventIntervalStart) -> Any:
    return to_class(OnEventIntervalStart, x)


def on_event_from_dict(s: Any) -> OnEvent:
    return OnEvent.from_dict(s)


def on_event_to_dict(x: OnEvent) -> Any:
    return to_class(OnEvent, x)


def on_event_ramp_up_from_dict(s: Any) -> OnEventRampUp:
    return OnEventRampUp.from_dict(s)


def on_event_ramp_up_to_dict(x: OnEventRampUp) -> Any:
    return to_class(OnEventRampUp, x)


def on_event_response_from_dict(s: Any) -> OnEventResponse:
    return OnEventResponse.from_dict(s)


def on_event_response_to_dict(x: OnEventResponse) -> Any:
    return to_class(OnEventResponse, x)


def on_event_start_from_dict(s: Any) -> OnEventStart:
    return OnEventStart.from_dict(s)


def on_event_start_to_dict(x: OnEventStart) -> Any:
    return to_class(OnEventStart, x)


def on_heartbeat_from_dict(s: Any) -> OnHeartbeat:
    return OnHeartbeat.from_dict(s)


def on_heartbeat_to_dict(x: OnHeartbeat) -> Any:
    return to_class(OnHeartbeat, x)


def on_periodic_report_cancel_from_dict(s: Any) -> OnPeriodicReportCancel:
    return OnPeriodicReportCancel.from_dict(s)


def on_periodic_report_cancel_to_dict(x: OnPeriodicReportCancel) -> Any:
    return to_class(OnPeriodicReportCancel, x)


def on_periodic_report_complete_from_dict(s: Any) -> OnPeriodicReportComplete:
    return OnPeriodicReportComplete.from_dict(s)


def on_periodic_report_complete_to_dict(x: OnPeriodicReportComplete) -> Any:
    return to_class(OnPeriodicReportComplete, x)


def on_periodic_report_start_from_dict(s: Any) -> OnPeriodicReportStart:
    return OnPeriodicReportStart.from_dict(s)


def on_periodic_report_start_to_dict(x: OnPeriodicReportStart) -> Any:
    return to_class(OnPeriodicReportStart, x)


def on_query_intervals_from_dict(s: Any) -> OnQueryIntervals:
    return OnQueryIntervals.from_dict(s)


def on_query_intervals_to_dict(x: OnQueryIntervals) -> Any:
    return to_class(OnQueryIntervals, x)


def on_query_intervals_response_from_dict(s: Any) -> OnQueryIntervalsResponse:
    return OnQueryIntervalsResponse.from_dict(s)


def on_query_intervals_response_to_dict(x: OnQueryIntervalsResponse) -> Any:
    return to_class(OnQueryIntervalsResponse, x)


def on_register_from_dict(s: Any) -> OnRegister:
    return OnRegister.from_dict(s)


def on_register_to_dict(x: OnRegister) -> Any:
    return to_class(OnRegister, x)


def on_register_reports_from_dict(s: Any) -> OnRegisterReports:
    return OnRegisterReports.from_dict(s)


def on_register_reports_to_dict(x: OnRegisterReports) -> Any:
    return to_class(OnRegisterReports, x)


def on_register_reports_response_from_dict(s: Any) -> OnRegisterReportsResponse:
    return OnRegisterReportsResponse.from_dict(s)


def on_register_reports_response_to_dict(x: OnRegisterReportsResponse) -> Any:
    return to_class(OnRegisterReportsResponse, x)


def on_status_response_from_dict(s: Any) -> OnStatusResponse:
    return OnStatusResponse.from_dict(s)


def on_status_response_to_dict(x: OnStatusResponse) -> Any:
    return to_class(OnStatusResponse, x)
