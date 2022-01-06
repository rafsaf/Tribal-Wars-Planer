from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def login(self):
        self.client.post("/pl/login/", json={"username": "admin", "password": "admin"})

    @task
    def hello_world(self):
        self.client.get("/pl/")
        self.client.get("/pl/documentation")
        self.client.get("/pl/planer/")
