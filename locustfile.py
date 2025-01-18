from locust import HttpUser, task


class SyncBaselineUser(HttpUser):

    @task
    def sync_baseline(self):
        self.client.get("/sync_baseline")


class AsyncIndependentUser(HttpUser):
    @task
    def async_independent(self):
        self.client.get("/async_independent")


class AsyncDependentUser(HttpUser):
    @task
    def async_dependent(self):
        self.client.get("/async_dependent")


class AsyncConcurrentUser(HttpUser):
    @task
    def async_concurrent(self):
        self.client.get("/async_concurrent")
