# Automatically generated locustfile for Load Testing Dashboard
from locust import HttpUser, task, between

class DynamicLoadTester(HttpUser):
    # Think time: Simulate 'slow & low' behavior with randomized wait times
    wait_time = between(1.0, 5.0)

    @task
    def task_0(self):
        self.client.get('/', name='/')
    @task
    def task_1(self):
        self.client.get('/api/data', name='/api/data')
    @task
    def task_2(self):
        self.client.get('/health', name='/health')

