import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from loguru import logger

import qtmessages37 as qt
from emulators import Emulator

PORT_NUMBER = 8001
RESOURCE_ID = "eSpire1"

def create_report_from_intervals(usage_intervals, usage_report_id='Fortress_telemetry_usage_v0.0.1'):
    return qt.TelemetryReport(duration=qt.DurationDescription(60, qt.Modifier.M), 
                              interval_descriptions=usage_intervals,
                              report_name="TELEMETRY_USAGE", 
                              report_specifier_id=usage_report_id)

def create_response_from_reports(reports, usage_report_id='FORTRESS_TELEMETRY_USAGE'):
    response_message = qt.OnRegisterReportsResponseMessage(reports)
    response = qt.OnRegisterReportsResponse(response_message)
    return response


def register_report_response_pipeline(emulator:Emulator, sampling_period, resource_id=RESOURCE_ID, now=True, ts=None):
    battery_storage_system = emulator.system_at(now=now, ts=ts)

    usage_intervals = battery_storage_system.intervals(resource_id=resource_id, 
                                                        sampling_period=sampling_period, 
                                                        report_type=qt.ReportType.USAGE, 
                                                        market_context=None)

    report = create_report_from_intervals(usage_intervals=usage_intervals)
    response = create_response_from_reports([report])
    return response

def query_intervals(emulator:Emulator, r_ids:list, start:int, end:int, step:int=60):
    reports = list()
    report_intervals = list()

    start=int(start)
    end=int(end)
    step=int(step)
    
    logger.debug(f"Getting reports from {start} to {end}")
    for i in range(start, end, step):
        #for now, I'll just take the reading at "start" time
        #convert time to time since start
        this_timestep = i-emulator.created_at
        telemetry = emulator.telemetry_at(ts=this_timestep)
        logger.debug(f"Loading telemetry for step {i}, which is {this_timestep} since the start")
        for rid in r_ids:
            try:
                value = telemetry[rid]
                interval = qt.ReportInterval(data_quality=qt.DataQuality.QUALITY_GOOD_NON_SPECIFIC, 
                                            dt_start_timet=i,
                                            r_id=rid, 
                                            value=0.0)
                report_intervals.append(interval)
            except KeyError:
                logger.warning(f"No telemetry for {rid} in {telemetry}")
        
    report = qt.Report(report_intervals)

    reports.append(report)

    response_message = qt.OnQueryIntervalsResponseMessage(reports)
    response = qt.OnQueryIntervalsResponse(response_message)

    return response


class MyHandler(BaseHTTPRequestHandler):
    emulator = Emulator(system_type='eSpire')

    def register_reports(self, post_data):
        sampling_period = qt.SamplingPeriod(1, 1, False, qt.Modifier.M)
        response = register_report_response_pipeline(emulator=self.emulator, 
                                                     sampling_period=sampling_period,
                                                     resource_id=RESOURCE_ID,
                                                     now=True)

        return json.dumps(response.to_dict())

    def query_intervals(self, post_data):
        request = qt.on_query_intervals_from_dict(json.loads(post_data.decode('utf-8')))
        start = request.on_query_intervals_message.start_timet
        end = request.on_query_intervals_message.end_timet
        step = request.on_query_intervals_message.granularity_in_seconds if request.on_query_intervals_message.granularity_in_seconds != 0 else 60
        granularity = request.on_query_intervals_message.granularity_in_seconds if request.on_query_intervals_message.granularity_in_seconds != 0 else 60
        r_ids = request.on_query_intervals_message.r_ids
        response = query_intervals(emulator=self.emulator, 
                                   r_ids=r_ids,
                                   start=start,
                                   end=end + granularity,
                                   step=step)
        return json.dumps(response.to_dict())

    def distribute_event(self, post_data):
        request = qt.on_distribute_event_start_from_dict(json.loads(post_data.decode('utf-8')))

        message = qt.OnDistributeEventStartResponseMessage(qt.OptType.OPT_IN)
        response = qt.OnDistributeEventStartResponse(message)

        # message = qt.OnStatusResponseMessage('no special message', qt.StatusEnum.RETRY)
        # response = qt.OnStatusResponse(message)

        return json.dumps(response.to_dict())

    def process_event(self, post_data):
        request = qt.on_event_from_dict(json.loads(post_data.decode('utf-8')))

        opt_messages = list()

        opt_messages.append(qt.OptMessage("opt1", qt.OptReason.ECONOMIC, qt.OptType.OPT_IN, 'resource1'))
        opt_messages.append(qt.OptMessage("opt1", qt.OptReason.ECONOMIC, qt.OptType.OPT_IN, 'resource3'))
        opt_messages.append(qt.OptMessage("opt2", qt.OptReason.ECONOMIC, qt.OptType.OPT_OUT, 'resource2'))

        opt_event = qt.OptEvent(qt.OptType.OPT_IN, True, opt_messages)
        message = qt.OnEventResponseMessage(opt_event)

        response = qt.OnEventResponse(message)

        return json.dumps(response.to_dict())

    def process_cancel_event(self, post_data):
        request = qt.on_event_cancel_from_dict(json.loads(post_data.decode('utf-8')))

        opt_messages = list()

        opt_messages.append(qt.OptMessage("opt1", qt.OptReason.ECONOMIC, qt.OptType.OPT_IN, 'resource1'))
        opt_messages.append(qt.OptMessage("opt1", qt.OptReason.ECONOMIC, qt.OptType.OPT_IN, 'resource3'))
        opt_messages.append(qt.OptMessage("opt2", qt.OptReason.ECONOMIC, qt.OptType.OPT_OUT, 'resource2'))

        opt_event = qt.OptEvent(qt.OptType.OPT_IN, True, opt_messages)
        message = qt.OnEventCancelResponseMessage(opt_event)

        response = qt.OnEventCancelResponse(message)

        return json.dumps(response.to_dict())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        self.log_message("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), post_data.decode('utf-8'))

        response = ''

        if self.path.endswith("/registerReports"):
            response = self.register_reports(post_data)

        elif self.path.endswith("/queryIntervals"):
            response = self.query_intervals(post_data)

        elif self.path.endswith("/startDistributeEvent"):
            response = self.distribute_event(post_data)

        elif self.path.endswith("/event"):
            response = self.process_event(post_data)

        elif self.path.endswith("/cancelEvent"):
            response = self.process_cancel_event(post_data)

        self.log_message("Sending response: \n%s\n", response)

        self.wfile.write(bytes(response, 'utf-8'))

        return


if __name__ == '__main__':
    logger.level("DEBUG")
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), MyHandler)
        logger.info(f'Started httpserver on port {PORT_NUMBER}')

        #Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        logger.warning('^C received, shutting down the web server')
        server.socket.close()
