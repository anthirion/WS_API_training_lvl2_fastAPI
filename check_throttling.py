"""
Ce script essaie de surcharger l'api gateway en faisant des appels en continu
à l'API. Attention, sans throttling, la gateway et le serveur API vont tomber !
"""

import requests
import time

gateway_ip = "34.78.130.129"
url = f"http://{gateway_ip}/products"
duration = 1    # 1s
seconds_count = 0

while True:
    api_calls_count = 0
    start_time = time.time()
    while (time.time() - start_time < duration):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                api_calls_count += 1
        except requests.exceptions.RequestException as e:
            print(f"La gateway est tombée au bout de {api_calls_count} appels")
            print("Erreur: ", e)
            raise SystemExit()

    seconds_count += duration
    print("Nombre d'appels par seconde:", api_calls_count)

# PROBLEME: ce script n'effectue que 40 appels par seconde au maximum, ce qui est insuffisant
# pour faire tomber la gateway
# Pistes :
#   - Utiliser la Concurrence avec ThreadPoolExecutor
#   - Utiliser les async et await avec aiohttp
