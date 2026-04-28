from locust import HttpUser, task, between

class DynamicLoadTester(HttpUser):
    # Think time: Simulate 'slow & low' behavior
    wait_time = between(1.0, 5.0)

    @task
    def task_0(self):
        self.client.get('/', name='/')

