import requests
import json

requests.post('http://0.0.0.0:8080/start', data=json.dumps({'processing': True, 'crawl': False}))
