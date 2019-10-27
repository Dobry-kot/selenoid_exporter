from flask                  import Flask, request, json
from werkzeug.wsgi          import DispatcherMiddleware
from prometheus_client      import Counter, Gauge, make_wsgi_app

import threading, requests, json, time, os

basic_url   = os.environ['url']
basic_type  = os.environ['type']

selenoid_browser_running    = Gauge('selenoid_{type}_browser_running'.format(type = basic_type), 
                                    'Running tasks.',         
                                    ["browser_name", "version"])

selenoid_concurrents        = Gauge('selenoid_{type}_concurrents'.format(type = basic_type), 
                                    'selenoid_concurrents.',   
                                    [])

selenoid_used               = Gauge('selenoid_{type}_used'.format(type = basic_type), 
                                    'selenoid_used.',         
                                    [])      

selenoid_queued             = Gauge('selenoid_{type}_queued'.format(type = basic_type), 
                                    'selenoid_queued.',       
                                    [])

selenoid_pending            = Gauge('selenoid_{type}_pending'.format(type = basic_type), 
                                    'selenoid_pending.',      
                                    [])

_app            = Flask(__name__)

app_dispatch    = DispatcherMiddleware(_app, {
                                              '/metrics': make_wsgi_app()
                                              })

class myThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        selenoidStatus()

def selenoidStatus():

    while True:

        request_data    = requests.get(url = basic_url).json()

        state           = request_data.get('state')
        concurrents     = state.get('total')
        used            = state.get('used')
        queued          = state.get('queued')
        pending         = state.get('pending')

        selenoid_concurrents.set(concurrents)
        selenoid_used.set(used)
        selenoid_queued.set(queued)
        selenoid_pending.set(pending)

        browsers        = state.get('browsers')

        for browser in browsers:
            browser_data = browsers.get(browser)

            for version in browser_data:
                version_data = browser_data.get(version)
                
                if not version_data:
                    selenoid_browser_running.labels(browser_name  = browser, 
                                                    version       = version).set(0)
                else:
                    for acconut in version_data:
                        acconut_data = version_data.get(acconut)
                        run_browsers = int(acconut_data.get('count'))
                        
                        selenoid_browser_running.labels(browser_name  = browser, 
                                                        version       = version).set(run_browsers)
        time.sleep(5)

selenoid_status_thread = myThread()
selenoid_status_thread.start()
