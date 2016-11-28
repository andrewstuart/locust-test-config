import uuid
from locust import HttpLocust, TaskSet, task
import random
import time

def login(l):
    res = l.client.get('https://idp.cw.astuart.co/idp/profile/SAML2/Unsolicited/SSO?providerId=ssp.dev&shire=https://mitre.cw.astuart.co/f/saml/SSO&target=http://portal.cw.astuart.co/uPortal/openid_connect_login?cccMisCode=ZZ1')

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

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        self.client.verify = False

    def get_some_stories(self):
        count = random.randint(20,60)
        date = randomDate('9/24/2016 12:00 AM', '11/24/2016 12:00 AM', random.random())
        self.client.get('/api/v1/stories?count={}&date={}'.format(count, date))

    @task
    def main(self):
        self.client.get('/api/version/')

    @task(1)
    def portlet_list(self):
        self.client.get('/api/portletListForSearch')

    # @task
    # def rest_stories(self):
    #     self.client.get('/f/u27l1s1000/p/cvc.u27l1n22101/exclusive/render.uP')

    @task(10)
    def home_page(self):
        self.client.get('/')

    @task(20)
    def guest_page(self):
        self.client.get('/f/u27l1s1000/normal/render.uP')

    # @task(5)
    # def get_login_page(self):
    #     self.client.get('/openid_connect_login')

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    min_wait=10
    max_wait=50
