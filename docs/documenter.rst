=============================
Contribuer à la documentation
=============================

La présente documentation est une ressource fondamentale pour le développement du site. Elle peut nécessiter des mises à jour et c'est pourquoi cette page vous explique comment y apporter des modifications.

Les fichiers servant à générer la documentation `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ sont situés dans le dossier ``docs/`` du dépôt.

Environnement
=============

Pour écrire de la documentation confortablement, on conseille d'activer le serveur de documentation. Pour ce faire, placez-vous dans le dossier ``docs/`` et utilisez :
::
  (env) docs $ make livehtml

Vous devriez alors pouvoir accéder à la documentation à l'adresse http://localhost:8000.

Vous pouvez maintenant apporter des modifications aux différements documents. Chaque fois que vous sauvegardez un document, le serveur va automatiquement reconstruire la documentation et rafraîchir la page web le cas échant. Pratique !

À propos de reStructuredText
============================

La documentation étant générée avec Sphinx, les documents sont écrits avec `reStructuredText <https://fr.wikipedia.org/wiki/ReStructuredText>`_. Il s'agit d'un langage de balisage léger assez bien adapté à la documentation technique (il est plus complet que Markdown). Les documents reStructuredText (et donc ceux de cette doc) ont l'extension ``.rst``.

Pour une introduction au reStructuredText, voir le `reStructuredText Primer <http://www.sphinx-doc.org/en/stable/rest.html>`_ de la documentation de Sphinx, ou encore la `RST Cheat Sheet <http://docs.sphinxdocs.com/en/latest/cheatsheet.html>`_.


Todos
=====

Les éléments restant à documenter ou incompléments sont signalés par une note "À faire". Ces todos sont automatiquement recensés dans la liste ci-dessous. Vous pouvez insérer un nouveau todo avec la directive ``.. todo:: Voici une tâche à réaliser...``.

Si vous souhaitez contribuer à la documentation, le plus simple est de choisir l'un de ces *todo* et de le compléter ! :)

.. todolist::
