import requests
import threading

server_ip = "34.79.191.125"
url = f"http://{server_ip}/products"

request_timeout = 5   # in seconds
num_threads = 10
threads = []


def send_request():
  while True:
    try:
      response = requests.get(url, timeout=request_timeout)
    except requests.exceptions.RequestException as e:
      print("La gateway est tombée")
      print("Erreur: ", e)
      raise SystemExit()


# Make API calls with several threads
# It will not take long until the timeout is reached

for _ in range(num_threads):
  try:
    thread = threading.Thread(target=send_request)
    thread.start()
    threads.append(thread)
  except requests.exceptions.RequestException:
    # when connection timed out, stop the threads
    for thread in threads:
      thread.join()
