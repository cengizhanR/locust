from locust import HttpUser, task, between

class MyUser(HttpUser):

    wait_time = between(1,2)
    host = "http://newtours.demoaut.com/"
    @task
    def launch_URL(self):
        self.client.get("/mercurysignon.php",name="launchmercury")

    def login(self):
        self.client.post("/login.php",name="login",data={"action":"process","username":"qamile1@gmail.com",
                                                         "passpord":"qamile","login.x":"41","login.y":"12"})