.. _Atom : https://atom.io

====================================
Installer un éditeur de texte (Atom)
====================================

Vous voulez programmer ? Excellente nouvelle ! Pour ça, il va vous falloir un environnement de développement. En la matière, deux grandes options s'offrent à vous :

- Les IDE ( *Integrated Development Environment* ) : tels le célèbre Eclipse ou le pythonique PyCharm, ces logiciels regroupent en un même endroit un éditeur de code source, un debugger et d'autres outils ;
- Les éditeurs de texte.

Contrairement à ce que l'on pourrait penser, les éditeurs de texte peuvent tout-à-fait rivaliser avec les IDE en tant qu'environnements de développement. Si vous choisissez cette option, oubliez Notepad ou TextEdit et laissez-moi vous présenter un éditeur qui fait fureur : Atom_ !

.. note::
  Il existe pléthore d'éditeurs de texte tels que Notepad++ (Windows), TextWrangler (macOS), Sublime Text (multi-plateforme)... On évoque ici Atom parce que c'est un éditeur open source, extrêmement flexible et avec une très bonne communauté. Vous êtes bien sûr libres de choisir et de développer votre *workflow* comme bon vous semble !

Qu'est-ce qu'Atom ?
===================

Atom un éditeur de texte open source développé par les équipes de GitHub. Il est "pensé pour les besoins du développeur du 21ème siècle". Atom est flexible, hautement personnalisable et disponible pour Windows, macOS et Linux. C'est un éditeur assez récent mais il y a déjà pléthore de packages et de plugins disponibles, souvent de très bonne qualité, afin de vous permettre de programmer toujours plus efficacement ! Et puis, l'interface a de la gueule, vous ne trouvez pas ?

.. image:: /media/atom-preview.png

Installer Atom
==============

1. Allez sur le site d'Atom : https://atom.io ;
2. Téléchargez Atom (environ 200Mo) ;
3. Installez Atom en suivant les instructions propres à votre système d'exploitation ;
4. Enjoy !

Installer des packages
======================

Tout l'intérêt d'Atom réside dans sa modularité ! Il existe des milliers de packages que vous pouvez installer pour personnaliser l'éditeur et le rendre encore plus agréable à utiliser. Voici comment procéder pour installer un package :

1. Ouvrez le panneau de préférences ( ``Cmd + ,`` sur macOS) ;
2. Allez dans l'onglet "Install" ;
3. Recherchez un package grâce à la barre de recherche ;
4. Installez le package qui vous intéresse.

Les thèmes s'installent aussi via cet onglet "Install".

Atom vous renseigne le nombre de fois qu'un package ou un thème a été installé. Bien que ce soit discutable, c'est souvent un indicateur de la qualité du package.

Vous retrouvez les packages et les thèmes installés dans les onglets correspondants du panneau de préférences.

Intégration de Git
==================

.. _git diff : https://atom.io/packages/git-diff
.. _github : https://atom.io/packages/github

Bonne nouvelle : Atom prend déjà tout en charge ! 😄 Atom inclut par défaut des packages vous permettant d'intégrer Git à l'éditeur. Par exemple, le package `git diff`_ vous indique en temps réel l'état de votre repo local, en affichant les lignes ajoutées, modifiées ou supprimées dans la gouttière de l'éditeur. Le package `github`_ ajoute une interface vers GitHub pour gérer vos Pull Requests directement dans Atom. Tous ces packages sont activés par défaut et vous n'avez normalement pas trop à vous soucier de leur configuration. Voici un aperçu de ce que ça donne concrètement :

.. image:: /media/git-diff-preview.png

Sur cet exemple, le fichier ``collections.lua`` a été modifié, il apparaît donc en orange dans la ``tree-view`` ainsi que ses répertoires parents (ici les dossiers ``rope`` et ``src``). Les lignes 64 à 77 ont été ajoutées, la gouttière est donc verte à cet endroit. De même, les lignes 79 et 80 ont été modifiées, la gouttière est donc orange à cet endroit. Lorsqu'une ligne a été modifiée, un petit trait rouge apparaît dans la gouttière.

Quelques packages utiles
========================

Quand vous installez Atom, un certain nombre de packages sont disponibles. Voici une liste d'autres packages qui peuvent vous être (très) utiles. N'hésitez pas à en suggérer ou à en ajouter d'autres ! 👍

Général
-------

.. _File icons : https://atom.io/packages/file-icons
.. _Highlight Selected : https://atom.io/packages/highlight-selected
.. _Merge Conflicts: https://atom.io/packages/merge-conflicts
.. _Linter: https://atom.io/packages/linter

- `File icons`_ : package tout simple qui associe une image et une couleur à chaque fichier afin de mieux les identifier dans Atom.
- `Highlight Selected`_ : il vous permet de sélectionner toutes les occurrences d'un nom dans un fichier, simplement en double-cliquant dessus !
- `Merge Conflicts`_ : lorsque vous gérez des conflits suite à un merge sur Git, il n'est pas toujours facile de s'y retrouver. Ce package vous facilite la vie en rendant le processus beaucoup plus visuel.
- Linter_ : ce package fait gagner un temps fou ! Il permet de détecter automatiquement des erreurs telles que les erreurs de syntaxe, les variables non-déclarées, etc... sans avoir besoin d'exécuter le code ! Cependant, Linter est le package de base, tout seul il ne fait pas grand chose : il faudra l'agrémenter d'un package par langage (voir l'exemple pour Python).

Pour le développement Python
----------------------------

.. _autocomplete-python: https://atom.io/packages/autocomplete-python
.. _linter-flake8: https://github.com/AtomLinter/linter-flake8
.. _python-autopep8 : https://github.com/markbaas/atom-python-autopep8
.. _PEP8 : https://www.python.org/dev/peps/pep-0008/

- autocomplete-python_ : des autocomplétions pour Python
- linter-flake8_ : la version pour Python du linter de base. Avec ce package, les erreurs de syntaxe Python s'affiche directement dans l'éditeur, sans avoir besoin d'exécuter le code ! Comme indiqué dans la documentation du package, ``linter-flake8`` suppose que vous ayez installé le package Python ``flake8`` (avec ``pip`` : ``pip install flake8``). Évidemment, vous devez avoir installé Linter pour que ``linter-flake8`` fonctionne.
- python-autopep8_ : ce package formate automatiquement votre code afin qu'il respecte les conventions PEP8_. En activant l'option "Format On Save" du package, vous pouvez rendre votre code plus "PEP8-compliant" en un clin d'œil ! Il suppose que vous ayez installé le package Python ``autopep8`` (avec ``pip`` : ``pip install autopep8``).

Pour le développement web (HTML/CSS/JS)
---------------------------------------

.. _atom-bootstrap4 : https://github.com/mdegoo/atom-bootstrap4
.. _pigments : https://atom.io/packages/pigments
.. _Color picker: https://atom.io/packages/color-picker
.. _atom-django-templates: https://github.com/benjohnson/atom-django-templates

- atom-bootstrap4_ : un snippet qui peut générer un template Bootstrap4 avec `htmlb4 + Tab` et bien d'autres choses !
- pigments_ : ce package vous montre les couleurs qu'il trouve dans vos fichiers directement dans l'éditeur ! Très pratique lorsqu'on veut avoir un aperçu d'une palette de couleurs, dans un fichier CSS par exemple.
- `Color picker`_ : dans le même genre, ce package vous permet de sélectionner une couleur et inclut un nuancier intégré ! Cliquez droit sur un texte comme `rgb(126, 145, 233` et choisissez "Color Picker" pour afficher le nuancier.
- atom-django-templates_ : ajoute le support du langage de templates de Django, avec des autocomplétions bien pratiques !

Personnaliser Atom
==================

Vous pouvez personnaliser l'apparence d'Atom en installant des thèmes (qui gèrent l'apparence globale de l'interface) et des colorations syntaxiques (qui colorent le code pour le rendre plus lisible).

Vous pouvez installer ces thèmes et colorations dans l'onglet "Install/Themes" du panneau de Préférences. N'hésitez pas à `faire quelques recherches <https://atom.io/themes>`_ pour découvrir les thèmes les plus sympas !
