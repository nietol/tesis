"""API Bootstrap"""

import falcon
from falcon.http_status import HTTPStatus

from classification_engine.services import tweets
from classification_engine.services import realtimetweets
from classification_engine.services import classifications

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

app = falcon.API(middleware=[HandleCORS()])

tweets = tweets.TweetsResource()
rt_tweets = realtimetweets.RealtimeTweetsResource()
classify = classifications.ClassificationsResource()

app.add_route('/tweets/{fechaDesde:dt("%Y-%m-%dT%H:%M-UTC%z")}/{fechaHasta:dt("%Y-%m-%dT%H:%M-UTC%z")}', tweets)
app.add_route('/realtimetweets/{timestamp:int}', rt_tweets)
app.add_route('/classifications', classify)