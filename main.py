from flask import Flask, Response
from prometheus_client      import Counter, Gauge
import threading, requests, json, time, os, prometheus_client

app             = Flask(__name__)
basic_url       = os.environ['url']
basic_type      = os.environ['type']
content_type    = str('text/plain; version=0.0.4; charset=utf-8')

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

def selenoidStatus():

    request_data    = requests.get(url = basic_url).json()

    concurrents     = request_data.get('total')
    used            = request_data.get('used')
    queued          = request_data.get('queued')
    pending         = request_data.get('pending')

    selenoid_concurrents.set(concurrents)
    selenoid_used.set(used)
    selenoid_queued.set(queued)
    selenoid_pending.set(pending)

    browsers        = request_data.get('browsers')

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


@app.route('/metrics')
def metrics():
    selenoidStatus()
    return Response(prometheus_client.generate_latest(), mimetype = content_type)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 64580)

