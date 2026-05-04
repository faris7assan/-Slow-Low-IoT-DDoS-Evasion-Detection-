from locust import HttpUser, task, between
class DynamicLoadTester(HttpUser):
    wait_time = between(1.0, 5.0)
    @task
    def test_target(self):
        self.client.get("/", name="root")
