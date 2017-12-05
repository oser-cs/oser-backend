# Site internet d'OSER

<p align="center"><img width=40% src="media/logo.png"></p>

<!-- Badges issus de Shields.io.

Les badges sont générés à partir de l'URL, qui ressemble à ceci :
https://img.shields.io/badge/<label>-<status>-couleur>.svg

Plus d'informations sur leur site : http://shields.io
-->
[![Python](https://img.shields.io/badge/python-3.6-blue.svg)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.0-blue.svg)](https://www.djangoproject.com)
![Dependencies](https://img.shields.io/badge/dependencies-wip-yellow.svg)

Bienvenue ! Ce dépôt est le lieu de développement du site internet de l'association OSER. Ce site a pour objectif de soutenir l'association dans son action quotidienne.

Si vous venez d'arriver, vous trouverez ci-dessous les ressources pour bien démarrer.

De nombreuses informations sont également disponibles sur le [Wiki](https://github.com/oser-cs/oser-website/wiki). Il est écrit avec amour, allez y faire un tour à l'occasion. :wink:

*Happy coding* !

## Table des matières

- [Dépendances](#dépendances)
- [Installation](#installation)
- [Documentation](#documentation)
- [Contribuer](#contribuer)
- [À propos d'OSER](#À-propos-doser)

## Dépendances

:construction_worker_man: Section en construction.

> Lister ici les frameworks, packages et autres technos sur lesquelles le projet s'appuie. Pour chaque dépendance, indiquer :
> - la version utilisée ;
> - pour quoi la dépendance est utilisée ;
> -  comment l'installer (instructions ou lien vers une ressource externe).

### Backend

#### [Django](https://www.djangoproject.com)

Django est un framework de développement web pour Python.

Le site d'OSER utilise Django en version 2.0.

À l'heure actuelle (05/12/2017), peu de tutoriels Django sont passés à la version 2.0, mais il y a en fait très peu de modifications non-rétro-compatibles par rapport à la version 1.11, et aucune modification n'est réellement critique. Les améliorations apportées par la version 2.0 sont intéressantes, on peut notamment citer le système d'écriture des URLs qui est grandement simplifié.

Pour plus d'infos, lire la [release news](https://www.djangoproject.com/weblog/2017/dec/02/django-20-released/) de Django 2.0.

Django est installé lors de l'installation des `requirements.txt`.

#### [Django REST Framework](http://www.django-rest-framework.org)

Le Django REST Framework (DRF) permet d'écrire facilement des API REST avec Django.

Le site d'OSER utilise le DRF en version 3.7.3. Cette version est entièrement compatible avec Django 2.0.

Le DRF est installé lors de l'installation des `requirements.txt`.

## Installation

:construction_worker_man: Section en construction.

> Expliquer ici comment installer l'environnement de développement du site, du clonage du dépôt au démarrage du site en local.

1. Clonez ce dépôt sur votre ordinateur :

```bash
$ git clone https://github.com/oser-cs/oser-website.git
$ cd oser-website
```

2. Créez un [environnement virtuel](https://github.com/oser-cs/oser-website/wiki/Outils-de-développement-pour-Python#les-environnements-virtuels-avec-virtualenv) puis activez-le :

```bash
oser-website $ virtualenv env -p python3
oser-website $ source env/bin/activate
```

3. Installez les dépendances Python :

```bash
(env) oser-website $ pip install -r requirements.txt
```

## Documentation

:construction_worker_man: Section en construction.

## Contribuer

:construction_worker_man: Section en construction.

## À propos d'OSER

OSER, ou Ouverture Sociale pour la Réussite, est une association étudiante de CentraleSupélec œuvrant dans le cadre des Cordées de la Réussite. Elle accompagne des jeunes issus de tous milieux sociaux et leur propose à cet effet un programme de tutorat, des sorties culturels, des séjours thématiques ou encore des stages de découverte.
