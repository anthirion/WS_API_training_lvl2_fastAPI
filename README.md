# WS API training Niveau 2

## Instructions pour les exercices aux participants de la formation

1. Basculer sur la branche exercices
2. Récupérer les secrets nécessaires pour se connecter à la bdd (host, username, password, etc) et les écrire dans un fichier .env au niveau du fichier main.py
3. Compléter les fonctions/classes avec un TODO pour chaque type d'API (sans DB et sans doc, sans DB et avec doc, avec DB)

## Instructions aux formateurs

### Provisionnement de l'infra

Prérequis:

- avoir un compte GCP pour la formation
- avoir une clé SSH pour se connecter aux VMs et l'avoir renseignée dans GCP
- avoir initier terraform dans le dossier gcp_infra/ (commande terraform init)

0. Si nécessaire, configurer les différentes variables nécessaires à terraform (nom du compte, zone, etc) dans un fichier variables.tf (voir la doc officielle de terraform pour la syntaxe).

1. Changer de branche : aller sur la branche gcp_deployment

2. Ajouter les utilisateurs dans le fichier de configuration à l'emplacement infra\roles\geerlingguy.mysql\defaults\main.yml. Le paramètre à modifier se trouve ligne 123 et se nomme "mysql_users". Ajouter un utilisateur par participant (ou par groupe de participants, à vous de voir) en suivant le modèle donné et en gardant les mêmes droits pour tout le monde. Normalement, chaque participant aura un username de la forme attendeeXX où XX sera un nombre de la forme 01, 02, etc.
   **ATTENTION**: assurez-vous que personne n'accède à la bdd dont le nom d'utilisateur est user (c'est la bdd qui est utilisée par l'api server).

Sans modification de votre part, les credentials sont les suivants:

- user: attendeeXX
- password: ApiTraining (même password pour tout le monde)

3. Provisionner les VMs nécessaires en exécutant la commande suivante depuis le dossier gcp_infra/:

```tf
    terraform apply
```

4. Récupérer les addresses IP depuis la console GCP et les copier dans le fichier inventory.ini

5. Lancer la configuration des VMs avec le playbook init-api-playbook.yml avec la commande suivante (commande à lancer depuis le dossier gcp_infra/):

```bash
   ansible-playbook init-api-playbook.yml -i inventory.ini
```

[ATTENTION] Changer la séquence de fin de ligne du script gcp_install.sh à LF pour être pris en compte par Linux (voir dans les paramètres de VSCode)

6. [VERIFIATION] Si vous taper dans le navigateur l'url _GatewayIP/products_ (où l'adresse ip de la gateway est à récupérer sur la console gcp), vous devriez voir s'afficher la liste des produits enregistrée dans la bdd

7. Compléter le .env avec les informations adéquates (aidez-vous du template)

8. A la fin de la formation, ne pas oublier de détruire les ressources construites via la commande suivante:
```tf
    terraform destroy
```

### Démo de charge (partie throttling)

Cette démo a pour but de montrer un test de charge avec l'outil **Locust**.

0. Si nécessaire, installer locust avec pip (pip3 install locust)

1. Commenter les configurations de throttling (rate limiting et circuit breaker) puis relancer la configuration de la gateway avec le tag gateway_config

2. Depuis le dossier load_testing, lancer la commande suivante:

```bash
    locust -f load_test.py -H http://{gateway_ip}
```

où l'ip de la gateway doit être récupérée depuis la console gcp

3. Entrer les valeurs suivantes dans l'interface graphique de Locust:

- number of users: 1000
- ramp up: 10 users per second

4. Afficher les graphiques pour que ce soit plus visuel (onglet Charts en haut à gauche)

Renouveler l'expérience en décommentant les paramètres de throttling dans la configuration de la gateway

**Conclusion de la démo**:
