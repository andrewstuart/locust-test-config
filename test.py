import uuid
from locust import HttpLocust, TaskSet, task
import time
# import jwt

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)


class MetricsTaskSet(TaskSet):
    _deviceid = None

    token = None

    def auth_get(self, *args, **kwargs):
        if self.token is not None:
            try:
                if kwargs['headers'] is None:
                    kwargs['headers'] = {}
            except KeyError:
                kwargs['headers'] = {}

            bearer = 'Bearer {}'.format(self.token)
            kwargs['headers']['Authorization'] = bearer

        self.client.get(*args, **kwargs)

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        self.client.verify = False

        res = self.client.post('http://mitreid-server/f/token?client_id=client&client_secret=secret&scope=superuser&grant_type=client_credentials&response_type=token').json()
        self.token = res['access_token']

    @task(5)
    def main(self):
        self.auth_get('/api/version/')

    # @task
    # def portlet_list(self):
    #     self.auth_get('/api/portletListForSearch')

    # @task
    # def rest_stories(self):
    #     self.client.get('/f/u27l1s1000/p/cvc.u27l1n22101/exclusive/render.uP')

    @task
    def home_page(self):
        self.auth_get('/')

    @task(2)
    def guest_page(self):
        self.auth_get('/f/u27l1s1000/normal/render.uP')

    # @task(5)
    # def get_login_page(self):
    #     self.client.get('/openid_connect_login')

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    min_wait=50
    max_wait=500
