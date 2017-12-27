=================
Pratiques de test
=================

  *Untested code is broken code.*

  — Quelqu'un de connu

On ne rappellera jamais assez l'importance de tester le logiciel.

Si vous avez suivi le tutoriel d'installation, vous avez dû remarqué que l'on lançait des tests Django avec ``python manage.py test`` pour s'assurer que tout "allait bien" avant de démarrer les serveurs. C'est bien la preuve que des tests automatiques servent **d'assurance qualité**.

Pour garantir son fonctionnement et sa maintenabilité, **le code du site d'OSER doit être testé** le plus possible.

Conseils généraux
=================

- Dès que vous corrigez un bug, pensez à écrire un test de non-régression (qui permettra de s’assurer que le bug n’arrive plus).
- Tout élément de *business logic* devrait être testé par un test fonctionnel.

Concernant le backend
=====================

Test de l'API
-------------

- Les tests de l’API sont définis dans le package ``tests/test_api``.
- Tous les endpoints d’une ressource doivent être testés par un test fonctionnel qui envoie la requête et s’assure que le ``status_code`` est celui attendu.
- Les permissions d’un endpoint doivent être testées par un test fonctionnel également.
- Un template de cas de test de ressource basée sur un modèle est proposé dans ``tests/test_api/model_api_boilerplate.py``.
