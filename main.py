from flask import Flask, Response
from classes.middleware import setup_metrics
import prometheus_client
from classes.selenoid_status import selenoidStatus

content_type = str('text/plain; version=0.0.4; charset=utf-8')
app = Flask(__name__)
setup_metrics(app)

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype = content_type)

if __name__ == '__main__':
    init = selenoidStatus().run()
    app.run()