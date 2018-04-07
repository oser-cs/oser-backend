# Site internet d'OSER - Backend

<p align="center"><img width=40% src="media/logo.png"></p>

<!-- Badges issus de Shields.io.

Les badges sont générés à partir de l'URL, qui ressemble à ceci :
https://img.shields.io/badge/<label>-<status>-couleur>.svg

Plus d'informations sur leur site : http://shields.io
-->

[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg)](https://www.djangoproject.com)
[![Documentation Status](https://readthedocs.org/projects/oser-tech-docs/badge/?version=latest)](http://oser-tech-docs.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/oser-cs/oser-backend.svg?branch=master)](https://travis-ci.org/oser-cs/oser-backend)
[![Heroku Status](https://heroku-badge.herokuapp.com/?app=oser-backend&style=flat)](https://dashboard.heroku.com/apps)

Bienvenue ! Ce dépôt est le lieu de développement du backend du site internet de l'association OSER, site qui a pour objectif de soutenir l'association dans son action quotidienne.

Si vous venez d'arriver, vous trouverez ci-dessous les ressources pour bien démarrer. :+1:

*Happy coding* !

## Table des matières

- [Documentation](#documentation)
- [Dépendances](#dépendances)
- [Contribuer](#contribuer)
- [À propos d'OSER](#À-propos-doser)

## Installation

Cette section vous explique comment installer le site sur votre ordinateur pour le faire tourner en mode développement.

### Logiciels

#### Python

Le backend d'OSER est développé avec Django, un framework web Python. Le site nécessite Python 3.5+.

[Télécharger Python 3.5+](https://www.python.org/downloads/)

#### PostgreSQL

Le site utilise une base de données SQL. Plusieurs technologies existent mais on utilise ici PostgreSQL qu'il vous faut donc installer (choisissez l'installateur selon votre OS).

[Télécharger PostgreSQL](https://www.postgresql.org/download/)

Après avoir installé PostgreSQL, démarrez le serveur en ouvrant pgAdmin, l'interface graphique qui sera installée en même temps que Postgres.

#### Optionnel : Redis, supervisord

Le backend Django est relié à [Celery](http://www.celeryproject.org), une librairie Python permet d'effectuer des traitements ou opérations en tâche de fond.

> NOTE : Pour l'instant, Celery n'est utilisé que pour effectuer un nettoyage périodique des fichiers de médias inutilisés, opération qui peut de toute façon être déclenchée par `$ python manage.py clean_media`. Il n'est donc **pas obligatoire d'installer ce qui suit en développement.**

Celery a besoin d'un système de *messaging* pour fonctionner, on utilise donc ici [Redis](https://redis.io).

Enfin, [supervisord](http://supervisord.org) est un gestionnaire de processus qui nous permet de lancer Redis et Celery en une seule commande.

Le plus simple est de se référer aux sites de chaque logiciel/librairie pour leur installation. :wink:

### Installation du projet

- (Recommandé) Créez un environnement virtuel (ici appelé `env`) puis activez-le :

```bash
$ python -m venv env
$ source env/bin/activate
```

- Installez les dépendances :

```bash
$ pip install -r requirements.txt
```

- Configurez la base de données en exécutant les migrations (rappelez-vous : *le serveur PostgreSQL doit être actif*) :

```bash
$ cd oser_backend
$ python manage.py migrate
```

Il ne vous reste plus qu'à lancer le serveur de développement :
```bash
$ python manage.py runserver
```

Celui-ci sera accessible à l'adresse http://localhost:8000.

## Documentation

La documentation complète du backend est disponible dans la documentation technique hébergée sur [ReadTheDocs](http://oser-tech-docs.readthedocs.io/fr/latest/).

### Accéder à l'administration

L'interface d'administration du site permet d'effectuer des opérations d'administration (modification de données, réinitialisation de mot de passe, création ou désactivation d'utilisateur…).

> En production, utilisez l'administration prudamment et n'y donnez accès qu'à des personnes de confiance et avec les autorisations adéquates !

Lorsque vous accéder au site (par exemple à http://localhost:8000), vous êtes redirigés vers la page d'authentification de l'administration. Authentifiez-vous avec un compte autorisé (compte administrateur ou autre compte auquel le statut `staff` a été attribué).

En développement, si vous venez d'installer le site, il n'y a pas encore d'utilisateurs dans la BDD. Il vous faut donc créer un compte administrateur. Pour cela, exécutez la commande `initadmin` :

```bash
$ python manage.py initadmin
```

Les identifiants par défaut sont indiqués dans le fichier `settings/common.py`. En production, pensez à mettre à jour le mot de passe de ce compte !

> Pour des raisons de sécurité, cette commande produira une erreur si des utilisateurs existent déjà dans la base de données. Vous ne pouvez donc l'exécuter que sur une BDD vide.

### Documentation de l'API

En développement, vous pouvez  accéder à la documentation de l'API à l'adresse http://localhost:8000/api/docs.

Vous pouvez aussi librement parcourir l'API à l'adresse http://localhost:8000/api.

Vous pouvez également accéder à la documentation de [l'API en production](http://oser-backend.herokuapp.com/api/docs).

![API Docs](media/api-docs.png)

### Authentification

Pour communiquer avec l'API, un client (une application Javascript par exemple) doit être authentifié. La méthode standard de la [token authentication](https://auth0.com/learn/token-based-authentication-made-easy/) est employée ici.

Le principe est le suivant :

- Le client s'authentifie en utilisant un nom d'utilisateur et un mot de passe.
- Le backend génère un *token* et le renvoie au client.
- Le client peut alors utiliser le *token* pour réaliser d'autres requêtes qui nécessitent d'être authentifié.

> Quel intérêt par rapport à une authentification username/password basique ?

L'avantage est de pouvoir stocker ce token dans un cookie ou dans le stockage local du navigateur, et ainsi éviter de redemander le nom d'utilisateur/mot de passe à chaque réouverture du navigateur.

#### Dans la pratique

Du point de vue d'un client, la procédure d'authentification est la suivante :

1. Récupération du token en envoyant une requête POST à l'endpoint `/api/auth/get-token` avec le `username` et le `password` fournis par l'utilisateur.

2. Stockage de ce token dans un cookie, le Local Storage ou autre système de stockage côté client.

3. Usage du token lors de futures requêtes en envoyant le paramètre `Authorization: Token <token>` dans l'entête.

#### Exemple

Nous allons nous identifier avec un utilisateur fictif en utilisant l'outil `curl` (disponible Linux/macOS).

On envoie la requête d'authentification qui nous répond avec le token :

```
$ curl -X POST -d "username=user&password=pass" localhost:8000/api/auth/get-token/
{"token":"b6302cebe7817532987e7a8767611b2600414915"}
```

Nous voilà authentifiés ! On peut ensuite utiliser ce token pour effectuer d'autres requêtes :

```
$ curl -X GET "localhost:8000/api/articles/" -H "Authorization: Token b6302cebe7817532987e7a8767611b2600414915"
[{"id": 39, "content": ...}, ...]
```

## Dépendances

### Django

[Django](https://www.djangoproject.com) est un framework de développement web pour Python. Le site d'OSER utilise Django en version 2.0.

> Note aux devs : il y a quelques changements non-rétrocompatibles de Django 2.0 par rapport à la version précédente 1.11. Faites attention à vérifier la version de Django supportée par des bibliothèques tierces que vous voudriez utiliser.

### Django REST Framework

Le [Django REST Framework](http://www.django-rest-framework.org) (DRF) permet d'écrire facilement des API REST avec Django.

Le site d'OSER utilise le DRF en version 3.7.3+. Cette version est entièrement compatible avec Django 2.0+.

## Contribuer

Le backlog est recensé sur le [Trello OSER_Geek](https://trello.com/b/bYlju4gE/site-internet-backlog).

Consultez la [documentation technique](http://oser-tech-docs.readthedocs.io/fr/latest/) pour plus d'informations sur le développement du site et l'installation d'un serveur de développement.

## À propos d'OSER

OSER, ou Ouverture Sociale pour la Réussite, est une association étudiante de CentraleSupélec œuvrant dans le cadre des Cordées de la Réussite. Elle accompagne des jeunes issus de tous milieux sociaux et leur propose à cet effet un programme de tutorat, des sorties culturels, des séjours thématiques ou encore des stages de découverte.
