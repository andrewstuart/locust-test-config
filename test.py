import uuid
from locust import HttpLocust, TaskSet, task
import time

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
        try:
            if kwargs['headers'] is None:
                kwargs['headers'] = {}
        except KeyError:
            kwargs['headers'] = {}

        kwargs['headers']['Authorization'] = 'Bearer {}'.format(self.token)
        print(kwargs['Authorization'])

        self.client.get(*args, **kwargs)

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
        self.client.verify = False

        self.token = "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJhcG9ydGFsYWRtaW5AZGVtb2NvbGxlZ2UuZWR1IiwiYXpwIjoiY2xpZW50IiwiZXBwbiI6ImFwb3J0YWxhZG1pbkBkZW1vY29sbGVnZS5lZHUiLCJzY29wZSI6WyJlcHBuIiwib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIl0sInJvbGVzIjpbIlJPTEVfREVWRUxPUEVSIiwiUk9MRV9VU0VSIiwic3RhZmYiLCJST0xFX0FETUlOIiwiUk9MRV9VU0VSIl0sImlzcyI6Imh0dHBzOlwvXC9taXRyZS5jdy5hc3R1YXJ0LmNvXC9mXC8iLCJleHAiOjE0ODAzNzg2NzAsIm1pc0NvZGUiOiIwMDAiLCJpYXQiOjE0ODAzNzUwNzAsImp0aSI6IjI2NDlmNWRlLTU4NmItNDRlZC05MDhjLTgyZTE2OTE3MmY1MyJ9.PDnIsGz87ndmc4l6_AWTLH6TLB8_ixo5DMl_axhdI_LWZASNrNlarJ7VvbRJ8vLCnNeGfu-GIGtJlFfsYZ1qKPCyRd3hjCqysc_Ta1zKIJgVoVUyWO4GzmKVQZinYvaLw7iovyObzoDn78SA1BKQkeKCByUsZUebhQUrTAYoj00Klcbfbdr6PdcbQ4ecNeWla8AtejZS5_4OA1d1FmgWopgQguCw6Pp--HCNHw-sY_2kQUWuQqegDBwKJb3NWR2DfhXCmqpfyMbOskUF9hTaBNohYUVElteOa32vRO6brXfQj5qvRMRCqVfneSTp7TmNHBfhuH9TQQ4UZlGXKDux6g"

    @task
    def main(self):
        self.auth_get('/api/version/')

    @task(10)
    def portlet_list(self):
        self.auth_get('/api/portletListForSearch')

    # @task
    # def rest_stories(self):
    #     self.client.get('/f/u27l1s1000/p/cvc.u27l1n22101/exclusive/render.uP')

    @task(10)
    def home_page(self):
        self.auth_get('/')

    @task(20)
    def guest_page(self):
        self.auth_get('/f/u27l1s1000/normal/render.uP')

    # @task(5)
    # def get_login_page(self):
    #     self.client.get('/openid_connect_login')

class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    min_wait=10
    max_wait=50
