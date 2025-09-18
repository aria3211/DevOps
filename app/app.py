from flask import Flask, Response, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import redis, time, threading, requests, os


# Prometheus counters
CRAWLER_FETCH_TOTAL = Counter('crawler_fetch_total', 'Total fetch attempts')
CRAWLER_SUCCESS_TOTAL = Counter('crawler_success_total', 'Total successful fetches')
CRAWLER_ERROR_TOTAL = Counter('crawler_error_total', 'Total fetch errors')


app = Flask(__name__)


REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
QUEUE_KEY = os.getenv('QUEUE_KEY', 'urls')


r = redis.from_url(REDIS_URL)


@app.route('/healthz')
def healthz():
    try:
        r.ping()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'status': 'redis_unavailable', 'error': str(e)}), 500


@app.route('/metrics')
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


# mock fetcher
def fetch_url(url: str):
    CRAWLER_FETCH_TOTAL.inc()
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            CRAWLER_SUCCESS_TOTAL.inc()
        else:
            CRAWLER_ERROR_TOTAL.inc()
    except Exception:
        CRAWLER_ERROR_TOTAL.inc()


def worker_loop(poll_interval=2):
    while True:
        item = r.lpop(QUEUE_KEY)
        if item:
            url = item.decode('utf-8')
            fetch_url(url)
        else:
            time.sleep(poll_interval)


if __name__ == '__main__':
# background worker thread
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8000)