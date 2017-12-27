=================================
Outils de développement en Python
=================================

Vous voulez programmer en Python ? Merveilleux ! Vous vous êtes peut-être déjà munis d'un [éditeur de texte](Installer-un-éditeur-de-texte-(Atom)) multi-fonctions, et vous pensez prêts à relever tous les défis. Laissez-moi vous présenter quelques autres composantes de la boîte à outils du développeur Python moderne.

.. note::
  Cette page a été rédigée par un habitué d'Unix (Linux, macOS). Si vous utilisez ces outils sous Windows et que vous remarquez des différences dans les instructions à suivre par rapport à Unix, n'hésitez pas à apporter votre contribution !

.. tip::
  Si vous voulez en lire plus sur le sujet, je vous recommande vivement `The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/>`_. C'est une sorte de guide qui traite d'énormément de sujets, liés à la fois directement et indirectement à Python : la structure d'un projet, le *code style*, la documentation, les tests, les frameworks et packages utiles classés par scénario d'utilisation, etc...

Gérer ses packages avec Pip
===========================

Pip, qu'est-ce que c'est ?
--------------------------

.. _PyPI : https://pypi.python.org/pypi
.. _Pip : https://pip.pypa.io/en/stable/)
.. _PipDoc : https://pip.pypa.io/en/stable/installing/

Vous le savez, Python bénéficie d'une communauté très dynamique. PyPI_, le *Python Package Index*, est l'endroit où les développeurs du monde entier peuvent publier des packages pour qu'ils soient utilisés par d'autres personnes. Il y a aujourd'hui près de 120 000 packages publiés sur PyPI ! 😮

Pip_ est un gestionnaire de dépendances (pour ne pas dire LE gestionnaire de dépendances) pour Python. Avec Pip :

- Vous installez des packages disponibles sur PyPI avec la ligne de commande ;
- La gestion des dépendances (packages nécessaires au fonctionnement d'autres packages) est grandement simplifiée.

Prenez un exemple : imaginons que vous vouliez utiliser NumPy pour faire quelques calculs matriciels. Vous lancez un interpréteur Python et importez NumPy :
::
  >>> import numpy
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ModuleNotFoundError: No module named 'numpy'

Mince ! NumPy n'est pas encore installé ! Avec Pip, vous pouvez l'installez très facilement :
::
  $ pip install numpy

Et voilà, le tour est joué !
::
  >>> import numpy
  >>> numpy.__version__
  '1.11.3'

Installer Pip
-------------

Si vous utilisez la version 3.4+ de Python, bonne nouvelle : Pip est déjà installé ! 🎉

Pour les versions ≤ 3.3, il vous faut l'installer vous-mêmes. Le processus d'installation n'a rien de compliqué et vous le trouverez dans `la documentation officielle de Pip <PipDoc_>`_ que vous pouvez d'ailleurs consulter pour avoir plus d'informations sur Pip et ses usages. 😉

.. attention::
  Sur certains OS, le nom d'exécutable ``pip`` est réservé à la version de Pip pour Python 2.x. C'est le cas de macOS notamment. Il se peut que vous deviez utiliser ``pip3`` et non ``pip``.

Usage de Pip
------------

Installer un package
********************

Cela se fait avec la commande ``$ pip install <package-name>``. Vous pouvez donner plusieurs noms de packages pour en installer plusieurs en même temps.
::
  $ pip install django
  $ pip install numpy matplotlib scipy


Lister les packages installés
*****************************

Vous pouvez obtenir la liste des packages installés sur votre machine à l'aide de la commande ``freeze`` :
::
  $ pip freeze
  autopep8==1.2.4
  beautifulsoup4==4.6.0
  bokeh==0.12.5
  click==6.7
  cycler==0.10.0
  Django==1.11.5
  entrypoints==0.2.2
  flake8==3.4.1
  ...

Les environnements virtuels avec VirtualEnv
===========================================

.. _VirtualEnv: https://virtualenv.pypa.io/en/stable/)
.. _VirtualEnvDocs: https://virtualenv.pypa.io/en/stable/

VirtualEnv_ est un outil qui permet de créer des environnements Python isolés. VirtualEnv vous permet de créer un dossier unique où sont regroupés à la fois une distribution de Python (par exemple Python 3.6) et des packages installés dans cet environnement.

.. note::
  Cela peut paraître farfelu, mais l'idée est en fait toute simple. Lorsque vous travaillez sur différents projets, il arrive très souvent que ceux-ci nécessitent certains packages et dans certaines versions, qui peuvent être différentes. Si un projet ``A`` nécessite un package ``P`` en version ``X`` et le projet ``B`` nécessite ``P`` en version ``Y``, vous voyez bien qu'il y a un problème à installer ``P`` "globalement" sur votre ordinateur, car vous ne pouvez installer qu'une seule version à la fois ! Vous avez besoin donc **d'isoler** l'environnement des projets ``A`` et ``B``, et c'est là que des outils comme VirtualEnv interviennent.

Pour plus d'informations sur VirtualEnv, n'hésitez pas à aller voir `la documentation officielle <VirtualEnvDocs_>`_.

Installer VirtualEnv
--------------------

Maintenant que vous avez installé Pip, cela se fait en un tour de mains :
::
  $ pip install virtualenv

Tada ! Vous devriez maintenant avoir à disposition en ligne de commande un exécutable ``virtualenv``. Vérifiez-le de cette façon :
::
  $ virtualenv --version
  15.1.0

Usage de VirtualEnv
--------------------

Création d'un environnement virtuel
************************************

L'usage basique de VirtualEnv est le suivant : placez-vous dans un répertoire où vous souhaitez installer l'environnement virtuel (ici nous nous situons dans un dossier ``mon-projet``), et saisissez :
::
  mon-projet $ virtualenv env

Cela créera un environnement virtuel appelé ``env`` (vous pouvez l'appeler comme vous voulez). Vous devriez voir quelques lignes de log vous indiquant que VirtualEnv installe une distribution de Python et quelques packages de base (normalement ``setuptools``, ``wheels`` et... ``pip`` !).

.. note::
  Par défaut, VirtualEnv installe la version de Python la plus récente qu'il trouve sur votre ordinateur. Vous pouvez spécifier la version de Python à utiliser pour l'environnement virtuel avec le paramètre ``-p``. Par exemple :
  ::
    mon-projet $ virtualenv env -p python3.4


Entrer dans un environnement virtuel
************************************

Pour entrer dans l'environnement virtuel, il faut **l'activer**. Sur les systèmes Unix (macOS, Linux), cela se fait comme ci-dessous. Une fois l'environnement activé, le nom de l'environnement apparaît entre parenthèses au début de la ligne de commande :
::
  mon-projet $ source env/bin/activate
  (env) mon-projet $  # l'environnement est activé !

Pour sortir de l'environnement virtuel, utilisez la commande `deactivate` :
::
  (env) mon-projet $ deactivate
  mon-projet $  # nous voilà sortis de l'environnement virtuel !

Lorsque l'environnement est actif, vous avez accès aux Python et Pip de l'environnement par les exécutables `python` et `pip`. Vous pouvez installer des packages avec Pip comme vous le feriez au niveau global, sauf que ceux-ci seront uniquement installés dans l'environnement virtuel ! La preuve, en supposant que NumPy n'est pas installé au niveau global :
::
  (env) mon-projet $ pip install numpy
  # -c permet d'exécuter un script écrit directement en ligne de commande
  (env) mon-projet $ python -c 'import numpy; print(numpy.__version__)'
  1.11.3
  (env) mon-projet $ deactivate
  mon-projet $ python -c 'import numpy'
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
  ModuleNotFoundError: No module named 'numpy'

En mode interactif avec IPython
===============================

.. _IPython: https://ipython.org
.. _Jupyter: https://jupyter.readthedocs.io/en/latest/

IPython_ signifie "Interactive Python". Vous connaissez l'interpréteur Python classique ? IPython le rend 100x mieux. Je ne peux pas vous expliquer toutes les fonctionnalités qu'IPython ajoute à l'interpréteur classique, je vous renvoie pour cela à la documentation officielle, mais en voici quelques unes :

- Ajout de couleurs à l'interpréteur — extrêmement pratique !

.. image:: /media/ipython-colors.png

- Autocomplétions à tout va (variables, imports...) avec Tab et les flèches haut/bas — extrêmement pratique !

.. image:: /media/ipython-autocomplete.png

- Appel à la documentation en ajoutant `?` derrière un objet — extrêmement pratique !

.. image:: /media/ipython-help.png

- Utilisation des outils de ligne de commande comme `ls` ou `cd` directement dans IPython — extrêmement pratique !

.. image:: /media/ipython-shellbin.png

- Et bien d'autres choses !

Bref : IPython c'est *extrêmement pratique*. 😁

Si vous voulez en découvrir encore plus sur le Python interactif, jetez un œil à Jupyter_ et ses notebooks.
