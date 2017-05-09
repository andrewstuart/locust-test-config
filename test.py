import uuid
from locust import HttpLocust, TaskSet, task
import time
import random
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

misCodes = ["ZZ1", "ZZ2"]

for i in range(200, 399):
    misCodes.append('{num:03d}'.format(num=i))

def randomMIS():
    return misCodes[random.randint(0, len(misCodes)-1)]

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

        res = self.client.post('https://login.ci.portal.ccctcportal.org/f/token?client_id=client&client_secret=secret2&scope=superuser&grant_type=client_credentials&response_type=token')
        self.token = res.json()['access_token']

    @task(1)
    def portlet_list(self):
        self.auth_get('/uPortal/api/portletListForSearch')

    @task(10)
    def rest_stories(self):
        self.auth_get('/uPortal/f/u27l1s1000/p/cvc.u27l1n22101/exclusive/render.uP')

#     @task(10)
#     def rest_user_info(self):
#         self.auth_get('api/v4-3/people/me/')

    @task(10)
    def rest_rest_urls(self):
        self.auth_get('/uPortal/api/cccRestUrls/')

    @task(10)
    def home_page(self):
        self.auth_get('/uPortal/')

    @task(10)
    def guest_page(self):
        self.client.get('/uPortal/f/u27l1s1000/normal/render.uP')

    @task(10)
    def advisor_cards(self):
        mis = randomMIS()
        self.auth_get('/advisorcard/api/v1/advisorcards?misCode=' + mis, name='/advisorcard/api/v1/advisorcards?misCode=[mis]')

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    min_wait=50
    max_wait=500
