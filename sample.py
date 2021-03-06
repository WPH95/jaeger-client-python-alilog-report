import opentracing
import logging
import time
from jaeger_client import Config
import subprocess
from ali_log_reporter import AliLogReporter


    
config = Config(
    config={ # usually read from some yaml config
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },  
    service_name='your-app-name',
)

tracer = config.initialize_tracer()
log_endpoint = 'http://cn-hangzhou.log.aliyuncs.com/'
access_id = '' 
access_key = '' 
log_project =  ''
log_logstore =  ''
reporter = AliLogReporter(log_endpoint, access_id, access_key, log_project, log_logstore)
tracer.reporter = reporter

if __name__ == '__main__' : 
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


    time.sleep(1)
    with tracer.start_span('TestSpan') as span:
        span.log_event('test message 111', payload={'life': 111})
        span.log_event('test message 222', payload={'life': 222})

        time.sleep(1)
        with tracer.start_span('ChildSpan', child_of=span) as child_span:
            time.sleep(1)
            child_span.log_event('down below 111')
            child_span.log_event('down below 222')
            child_span.error("make a error", ["error info"])

    with tracer.start_span('NextSpan') as xspan:
        xspan.error("error again")
        time.sleep(0.4)
    
    reporter.flush()  # flush any buffered spans
