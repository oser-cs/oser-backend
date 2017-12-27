===========================
Petit topo sur les API Rest
===========================

Qu'est-ce qu'une API ?
======================

Commençons par la base : une API, késako ? Wikipedia nous dit :

  En informatique, une interface de programmation applicative (souvent désignée par le terme API pour Application Programming Interface) est un ensemble normalisé de classes, de méthodes ou de fonctions qui sert de façade par laquelle un logiciel offre des services à d'autres logiciels. Elle est offerte par une bibliothèque logicielle ou un service web, le plus souvent accompagnée d'une description qui spécifie comment des programmes consommateurs peuvent se servir des fonctionnalités du programme fournisseur.

Autrement dit, une API fournit un ensemble de services et nous dit comment on les utilise.

En équation : **API = ⚙️ + 📖**.

Dans le domaine du web, le terme API désigne plus spécifiquement les services qu'un client (votre navigateur, par exemple) peut utiliser pour interagir avec une autre application.

Il existe toutes sortes d'API. Par exemple :

.. _Facebook Login : https://developers.facebook.com/docs/facebook-login/
.. _Twitter for Websites : https://dev.twitter.com/web/overview

- L'API `Facebook Login`_, qui permet d'intégrer un bouton "Se connecter avec Facebook" sur son site ;
- L'API `Twitter for Websites`_ qui permet d'ajouter des murs de tweets à un site ;
- L'API d'authentification de ViaRézo qui permet d'authentifier des visiteurs par leur compte ViaRézo !
- Etc...

Les spécificités des API REST
=============================

.. _TutsPlusHTTP: https://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-1--net-31177

Une API REST est une API qui permet d'accéder aux ressources d'une application. Concrètement, elle vous permet de questionner la base de données via une simple requête HTTP et de récupérer les données dans un format conventionnel (le plus souvent JSON ou XML).

.. important::
  On a tous entendu parler d'HTTP, mais on ne sait pas forcément vraiment comment ce protocole fonctionne. N'hésitez pas à vous renseigner sur le sujet car c'est un aspect crucial pour la création d'APIs REST ! Par exemple, `cet article <TutsPlusHTTP_>`_ de TutsPlus.

En fait, une API REST permet non seulement de récupérer des données, mais également d'en envoyer afin de réaliser des opérations sur elles. En effet, chaque opération classique des bases de données relationnelles (CRUD : Create, Read, Update, Delete) peut être mise en correspondance avec une méthode HTTP :

- Create => POST : création d'enregistrements dans la BDD
- Read => GET : récupération d'enregistrements dans la BDD
- Update => PUT : mise à jour d'enregistrements existants dans la BDD
- Delete => DELETE : suppression d'enregistrements dans la BDD

Les API REST informent donc le service web de l'opération demandée grâce à la méthode HTTP employée.

Enfin, parce qu'elles utilisent des standards du web (le protocole HTTP, JSON, XML...), les API REST sont extrêmement flexibles et servent en fait de "colle" entre des services web qui veulent échanger des données.

Concrètement, à quoi ça ressemble une API REST ?
================================================

Concrètement, une API REST fournit des *endpoints*, ou points d'entrées, d'où on peut interagir avec le service web. Pour faire simple, on peut considérer **qu'un point d'entrée est entièrement déterminé par son URL et la méthode HTTP employée.**

Pour prendre un exemple, imaginons qu'on dispose d'une API OSER qui nous permet d'interroger une base de données des tutorés.

Cette API pourrait par exemple définir les points d'entrée suivants :
::
  GET http://oser-cs.fr/api/students/ : retrieve all students
  GET http://oser-cs.fr/api/students/{id}/ : retrieve a student by id
  POST http://oser-cs.fr/api/students/ : create a new student

Ainsi, pour récupérer les données du tutoré correspondant à ``id = 1``, on pourrait envoyer une requête GET à ``http://oser-cs.fr/api/students/1``. On obtiendrait des données pouvant avoir cette tête-là :
::
  {
      "id": 1,
      "first_name": "Jean",
      "last_name": "Dupont",
      "school": "Lycée Jean Jaurès",
      ...
  }

Si la requête est faite depuis un navigateur web via du code Javascript, on peut alors utiliser l'objet JSON obtenu pour, par exemple, effectuer le rendu de la page contenant les informations du lycéen.

Conclusion
==========

.. _restful : https://www.ibm.com/developerworks/library/ws-restful/index.html

On s'aperçoit donc qu'en résumé, le grand avantage des API REST est de totalement découpler les services *backend* (tout ce qui a trait à la gestion de la BDD) et les services *frontend* (tout ce qui attrait au rendu des données sur le navigateur).

Si vous vous demandiez encore pourquoi tout ceci nous intéresse : une API REST pour le site OSER va nous permettre de faire communiquer le backend (construit avec Django) et le frontend (construit avec JS/React) 🎉 !

Si vous voulez en savoir plus sur l'architecture REST, jetez un œil à `cet article <restful_>`_.
