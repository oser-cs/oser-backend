================================
Gestion des comptes utilisateurs
================================

Cette page est destinée aux administrateurs du site. On vous explique ici comment gérer les comptes des utilisateurs.

Opérations usuelles
===================

.. _siteadmin : http://www.oser-cs.fr/admin/

Connectez-vous à `l'administration du site <siteadmin_>`_ avec les identifiants admin. Sur cette partie du site, vous pouvez effectuer un certain nombre d'opérations comme :

- Lister les utilisateurs
- Filtrer ou trier cette liste selon différents critères
- Déclencher une récupération de mot de passe
- Désactiver un compte
- Supprimer un compte

.. todo:: Screenshots de l'administration du site

Téléchargement de la base de données
====================================

Le site vous permet de télécharger la base de données des utilisateurs au format Excel. Cela s'avère utile pour effectuer de l'analyse de données ou tout simplement archiver des snapshots de la BDD utilisateurs.

Pour télécharger la base de données des utilisateurs, procédez comme suit :

1. Do this
2. ...

.. todo:: Documenter les étapes de téléchargement de la BDD des utilisateurs

Procédures de réinitialisation
==============================

Adresse email
-------------

Bien que l'adresse email constitue l'identifiant de l'utilisateur, elle peut être modifiée. La seule contrainte est que celle-ci soit unique parmi les utilisateurs.

.. important::
  Les utilisateurs peuvent modifier leur adresse email eux-mêmes. Il est préférable de les inviter à réaliser cette opération de leur côté. Cette section n'est présente que pour les cas particuliers.

Pour modifier l'adresse email d'un utilisateur, voici comment procéder :

1. Do this.
2. ...

.. todo:: Documenter les étapes de modiication d'adresse email d'un utilisateur

Mot de passe
------------

.. important::
  Les utilisateurs peuvent récupérer leur mot de passe eux-mêmes. Cette procédure leur est accessible depuis l'écran de connexion. Cette section n'est présente que pour gérer les cas particuliers.

En tant qu'administrateur, vous pouvez demander la réinitialisation du mot de passe d'un utilisateur de la manière suivante :

1. Do this
2. ...

.. todo:: Documenter les étapes de réinitialisation d'un mot de passe

L'utilisateur recevra un email avec un mot de passe provisoire qu'il sera invité à changer lors de sa première connexion.

Maintenance des comptes lycéens
===============================

Dans le cadre du processus d'inscription administrative des lycéens, leur compte dispose d'un **état provisoire** dans lequel les fonctionnalités accessibles sont limitées. Lors de sa création, un compte lycéen est dans l'état provisoire et passe à l'état définitif après validation d'un responsable de séance.

Il se peut qu'un compte lycéen soit abandonné et reste à l'état provisoire (par exemple si un lycéen se désiste et ne participe plus au tutorat). Le site prévoit pour cela **un système de nettoyage automatique** qui désactive les comptes provisoires après N mois d'inactivité. M mois après leur désactivation, ces comptes sont définitivement supprimés.

Vous pouvez cependant déclencher manuellement le nettoyage des comptes provisoires. Celui-ci sera réalisé dans un délai de 3 jours et pourra être annulé si besoin. Voici comment déclencher le nettoyage manuel :

1. Do this
2. ...

.. todo:: Screenshots, valeur de N, valeur de M, étapes

Désactivation d'un utilisateur
==============================

.. todo:: Documenter la procédure de désactivation d'un utilisateur

Suppression d'un utilisateur
============================

.. attention::
  Il est en général préférable de désactiver un compte utilisateur plutôt que de le supprimer. De cette manière, le compte reste en base de données mais l'utilisateur ne peut plus accéder au site. Supprimez un utilisateur si vous êtes certains que son compte ne sera plus d'aucune utilité.

.. todo:: Documenter la procédure de suppression d'un utilisateur
