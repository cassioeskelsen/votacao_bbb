from locust import HttpUser, task, between


class HelloWorldUser(HttpUser):
    # wait_time = between(0.5, 2.5)

    @task
    def vote_post(self):
        vote_id = 1
        self.client.post(f'/vote')