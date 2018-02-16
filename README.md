# Site internet d'OSER - Backend

<p align="center"><img width=40% src="media/logo.png"></p>

<!-- Badges issus de Shields.io.

Les badges sont générés à partir de l'URL, qui ressemble à ceci :
https://img.shields.io/badge/<label>-<status>-couleur>.svg

Plus d'informations sur leur site : http://shields.io
-->
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg)](https://www.djangoproject.com)
[![Docs status](https://readthedocs.org/projects/oser-website/badge/?version=latest)](http://oser-website.readthedocs.io/fr/latest/?badge=latest)

Bienvenue ! Ce dépôt est le lieu de développement du backend du site internet de l'association OSER, site site a pour objectif de soutenir l'association dans son action quotidienne.

Si vous venez d'arriver, vous trouverez ci-dessous les ressources pour bien démarrer. :+1:

*Happy coding* !

## Table des matières

- [Documentation](#documentation)
- [Dépendances](#dépendances)
- [Contribuer](#contribuer)
- [À propos d'OSER](#À-propos-doser)

## Documentation

La documentation complète du backend est hébergée sur [ReadTheDocs](http://oser-website.readthedocs.io/fr/latest/).

En supplément, la documentation de l'API générée par Django est accessible à l'endpoint `/api/docs/`. Sur le serveur local, vous pouvez donc y accéder à l'URL [`http://localhost:8000/api/docs`](http://localhost:8000/api/docs). Vous pouvez aussi librement parcourir l'API à l'adresse [`http://localhost:8000/api/`](http://localhost:8000/api/).

![API Docs](media/api-docs.png)

#### Authentification

> Remarque : actuellement, certaines ressources (les articles par exemple) sont accessibles sans authentification. Cela ne sera plus le cas dans de futures versions.

Pour communiquer avec l'API, un client doit être authentifié. La méthode standard de la [*token authentication*](https://auth0.com/learn/token-based-authentication-made-easy/) est employée ici.

Le principe est le suivant :

- Le client s'authentifie en utilisant un nom d'utilisateur et un mot de passe.
- Le backend génère un *token* et le renvoie au client.
- Le client peut alors utiliser le *token* pour réaliser d'autres requêtes qui nécessitent d'être authentifié.

> Quel intérêt par rapport à une authentification username/password basique ?

L'avantage est de pouvoir stocker ce token dans un cookie ou dans le stockage local du navigateur, et ainsi éviter de redemander le nom d'utilisateur/mot de passe à chaque réouverture du navigateur.

> Concrètement, comment faire pour authentifier un utilisateur ?

Du point de vue d'un client, la procédure d'authentification se fait en 2 étapes :

A. Récupération du token en envoyant une requête POST à l'endpoint `/api/auth/get-token` avec `username` et le `password` fournis par l'utilisateur.

```
$ curl -X POST -d "username=user&password=pass" localhost:8000/api/auth/get-token/
{"token":"b6302cebe7817532987e7a8767611b2600414915"}
```

B. Usage du token lors de futures requêtes en envoyant le paramètre `Authorization: Token <token>` dans l'entête.

```
$ curl -X GET "localhost:8000/api/articles/" -H "Authorization: Token b6302cebe7817532987e7a8767611b2600414915"
[{"id": 39, "content": ...}, ...]
```

## Dépendances

### Django

[Django](https://www.djangoproject.com) est un framework de développement web pour Python.

Le site d'OSER utilise Django en version 2.0.

> À l'heure actuelle, peu de tutoriels Django se basent sur la version 2.0, mais il y a en fait très peu de changements non-rétro-compatibles par rapport à la version 1.11, et aucun changement n'est réellement critique. Les améliorations apportées par la version 2.0 sont intéressantes, on peut notamment citer le système d'écriture des URLs qui est grandement simplifié. Pour plus d'infos, lire la [release news](https://www.djangoproject.com/weblog/2017/dec/02/django-20-released/) associée.

### Django REST Framework

Le [Django REST Framework](http://www.django-rest-framework.org) (DRF) permet d'écrire facilement des API REST avec Django.

Le site d'OSER utilise le DRF en version 3.7.3. Cette version est entièrement compatible avec Django 2.0.

## Contribuer

Le backlog est recensé sur le [Trello OSER_Geek](https://trello.com/b/bYlju4gE/site-internet-backlog).

Consultez le guide du développeur de la [documentation backend](http://oser-website.readthedocs.io/fr/latest/) pour plus d'informations sur le développement du site.

## À propos d'OSER

OSER, ou Ouverture Sociale pour la Réussite, est une association étudiante de CentraleSupélec œuvrant dans le cadre des Cordées de la Réussite. Elle accompagne des jeunes issus de tous milieux sociaux et leur propose à cet effet un programme de tutorat, des sorties culturels, des séjours thématiques ou encore des stages de découverte.
