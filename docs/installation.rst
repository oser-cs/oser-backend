============
Installation
============

Cette page vous indique étape par étape comme installer l'environnement de développement du site. À la fin de ce processus, vous aurez un site local fonctionnel !

Prérequis
=========

Vous aurez besoin de `Git <https://git-scm.com>`_ pour cloner le dépôt.

Côté back, le site repose sur Django. Munissez-vous de `Python 3.5+ <https://www.python.org/downloads/>`_ et de `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ si ce n'est pas encore fait.

Côté front, c'est React qui est utilisé. Vous allez donc avoir besoin de `npm <https://www.npmjs.com>`_ .

Installation des dépendances
============================

Tout d'abord, clonez le dépôt sur votre ordinateur :
::
  $ git clone https://github.com/oser-cs/oser-website.git
  $ cd oser-website

Créez ensuite un environnement virtuel (ici appelé ``env``) puis activez-le :
::
  oser-website $ virtualenv env -p python 3
  oser-website $ source env/bin/activate

Installez les dépendances Python en utilisant ``pip`` :
::
  (env) oser-website $ pip install -r requirements.txt

Rendez-vous ensuite dans ``oser_cs/frontend`` puis installez le package npm (cela prendra quelques minutes selon la vitesse de votre connexion internet) :
::
  (env) oser-website $ cd oser_cs/frontend
  (env) frontend $ npm install

Configuration de la base de données
===================================

Tout d'abord, créez puis exécutez les migrations Django :
::
  (env) frontend $ cd ..
  (env) oser_cs $ python manage.py makemigrations
  (env) oser_cs $ python manage.py migrate

Lancez les tests pour vous assurer que tout fonctionne comme prévu :
::
  (env) oser_cs $ python manage.py test

Si vous le souhaitez, vous pouvez peupler la BDD de développement avec des données d'imitation en utilisant la commande ``populatedb`` :
::
  (env) oser_cs $ python manage.py populatedb

Démarrage du site en mode développement
=======================================

Vous en fait avez besoin de démarrer deux serveurs : le serveur backend avec Django et le serveur frontend avec npm (le second communicant avec le premier via l'API).

Démarrez le serveur local Django avec la commande `runserver` :
::
  (env) oser_cs $ python manage.py runserver

Si vous vous rendez à l'adresse `http://localhost:8000/api/ <http://localhost:8000/api/>`_, vous devriez arriver à la racine de l'API comme ci-dessous. Si c'est le cas, le serveur Django est fonctionnel !

.. image:: media/api_home.png

Pour le serveur front, rendez-vous dans `oser_cs/frontend` et démarrez le serveur npm :
::
  oser_cs $ cd frontend/
  frontend $ npm start

Une page de navigateur devrait s'ouvrir à l'adresse `http://localhost:3000/ <http://localhost:3000/>`_ avec 3 boutons vous invitant à envoyer des requêtes GET de test :

.. image:: media/front_home.png

Et voilà, le site tourne en mode développement !

Détail des dépendances
======================

Backend
-------

.. _Django : https://www.djangoproject.com
.. _release news: https://www.djangoproject.com/weblog/2017/dec/02/django-20-released/)
.. _Django REST Framework : http://www.django-rest-framework.org
.. _DRY Rest Permissions : https://github.com/dbkaplan/dry-rest-permissions
.. _FactoryBoy : http://factoryboy.readthedocs.io/en/latest/index.html

Django
******

Django_ est un framework de développement web pour Python.

Le site d'OSER utilise Django en version 2.0.

> À l'heure actuelle, peu de tutoriels Django se basent sur la version 2.0, mais il y a en fait très peu de changements non-rétro-compatibles par rapport à la version 1.11, et aucun changement n'est réellement critique. Les améliorations apportées par la version 2.0 sont intéressantes, on peut notamment citer le système d'écriture des URLs qui est grandement simplifié. Pour plus d'infos, lire la `release news`_ associée.

Django REST Framework
*********************

Le `Django REST Framework`_ (DRF) permet d'écrire facilement des API REST avec Django.

Le site d'OSER utilise le DRF en version 3.7.3. Cette version est entièrement compatible avec Django 2.0.

DRY Rest Permissions
********************

`DRY Rest Permissions`_ est utilisé pour définir les permissions directement sur les modèles Django.

FactoryBoy
**********

`FactoryBoy`_ est utilisé pour faciliter la création d'objets de test en définissant des usines (*factories*) directement à partir des modèles Django. Les usines sont définies dans ``oser_cs/tests/factory.py``.

Frontend
--------

.. todo:: Lister les dépendances du frontend
