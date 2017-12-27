.. |REPO| replace:: https://github.com/oser-cs/oser-website.git

============
Installation
============

Cette page vous indique étape par étape comme installer l'environnement de développement du site. À la fin de ce processus, vous aurez un serveur local fonctionnel !

Prérequis
=========

Tout d'abord, munissez-vous de `Python 3.5+ <https://www.python.org/downloads/>`_ et de `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ si ce n'est pas encore fait. Vous aurez aussi besoin de `Git <https://git-scm.com>`_ pour cloner le dépôt.

Installer le serveur local
==========================

Tout d'abord, clonez le dépôt sur votre ordinateur :

.. parsed-literal::
  $ git clone |REPO|
  $ cd oser-website

Créez ensuite un environnement virtuel (ici appelé ```env``) puis activez-le :
::
  oser-website $ virtualenv env -p python 3
  oser-website $ source env/bin/activate

Installez les dépendances Python en utilisant ``pip`` :
::
  (env) oser-website $ pip install -r requirements.txt

Configurez la BDD de développement :
::
  (env) oser-website $ cd oser_cs
  (env) oser_cs $ python manage.py makemigrations
  (env) oser_cs $ python manage.py migrate

Lancez les tests pour vous assurer que tout fonctionne comme prévu :
::
  (env) oser_cs $ python manage.py test

Si vous le souhaitez, vous pouvez peupler la BDD de développement avec des données d'imitation en utilisant la commande ``populatedb`` :
::
  (env) oser_cs $ python manage.py populatedb

Démarrez enfin le serveur local :
::
  (env) oser_cs $ python manage.py runserver

Le serveur local devrait se mettre en route et être accessible à l'URL ``http://localhost:8000/``.

Si vous vous rendez à l'adresse `http://localhost:8000/api/ <http://localhost:8000/api/>`_, vous arriverez à la racine de l'API :

.. image:: media/api_home.png

Et voilà, le serveur de développement est fonctionnel ! :)
