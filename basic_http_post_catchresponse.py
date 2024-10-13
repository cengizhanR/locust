from locust import HttpUser,SequentialTaskSet,task,between

class UserBehaviour(SequentialTaskSet):

    @task
    def launch_URL(self):
        with self.client.get("/mercurysignon.php", name="launchmercury",catch_response=True) as resp1:
            # print("resp1"+resp1.txt)
            if("Mechury Tours") in resp1.txt:
                resp1.success()
            else:
                resp1.failure("Failed to launch url")

    @task
    def login(self):
        with self.client.post("/login.php", name="login", data={"action": "process","userName": "qamile1@gmail.com",
                                                           "password": "qamile","login.x": "41","login.y": "12"},catch_response=True) as resp2:
            # print("resp1"+resp2.txt)
            if("Find a Flight") in resp2.txt:
                resp2.success()
            else:
                resp2.failure("Failed to login")



class MyUser(HttpUser):
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]
