"""
Ce script utilise Locust pour déterminer le nombre d'appels GET /products que peu encaisser le serveur API.
La gateway, elle, est configurée de telle sorte à ne pas recevoir trop d'appels API, qui seraient susceptibles
de la faire tomber.
"""

from locust import HttpUser, task


class MaliciousUser(HttpUser):
  @task
  def hello_world(self):
    self.client.get("/products")


################ DEMO INSTRUCTIONS ################
###################################################
# Run this script with the following command line:
# locust -f load_test.py -H http://{host_ip}

# For the demo, apply the following configuration params:
# number of users: 600
# ramp up: 10 users per second
# On se rend compte que le serveur ne tombe pas mais le temps de réponse devient très important (inacceptable)
