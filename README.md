# projet7_flask
### API pour projet7_dashboard

## app.py
Le fichier app.py contient toutes les routes pour fonctionner avec flask.
- route principale http://127.0.0.1:5001
- route http://127.0.0.1:5001/api/v1/data/id_clients/all pour obtenir la liste de tous les id clients
- route http://127.0.0.1:5001/api/v1/data/id_clients pour obtenir les infos d'un client
- route http://127.0.0.1:5001/api/v1/model/id_clients pour obtenir le résultat de la modélisation pour un client
- route http://127.0.0.1:5001/api/v1/model/id_clients/importance_locale/ pour obtenir le graphe d'importance locale lime pour un client et un nombre de features
- route http://127.0.0.1:5001/api/v1/model/id_clients/importance_globale/ pour obtenir le graphe d'importance globale pour un nombre de features
- route http://127.0.0.1:5001/api/v1/model/id_clients/comparaison/ pour obtenir des graphes de comparaison entre l'individu choisi et le reste des individus et un nombre de features

Il faut renseigner l'ID de l'individu avec ?SK_ID_CURR= suivi de l'ID du client.
Il faut renseigner le nombre de features avec ?feature= ou &feature= suivi du nombre de features.

## dossier test
Le dossier test contient les tests unitaires réalisés avec pytest.

## dossier data
Le dossier data contient le modèle utilisé en .pickle, ainsi que 3 dataframes contenant les bases de données utilisées.

## Procfile
Le fichier Procfile sert à l'hébergement sous Heroku de l'API.
