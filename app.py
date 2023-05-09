from flask import Flask, request, jsonify, make_response
import pandas as pd
import pickle
import lime
import lime.lime_tabular



app = Flask(__name__)
app.config["DEBUG"] = True


SK_ID_CURR = pd.read_csv("./data/SK_ID_CURR.csv").to_dict(orient='records')
DATA_SELECTION = pd.read_csv("./data/DATA_SELECTION.csv")
X_train = pd.read_csv("./data/X_train.csv")

# page de base
# test avec http://127.0.0.1:5001
@app.route('/', methods=['GET'])
def home():
    return "<h1>Projet 7 - Implémentez un modèle de scoring</h1><p>Ce site donne accès à l'API pour le dashboard du " \
           "projet 7 OC</p>"


# une route pour renvoyer la liste des id clients
# test avec http://127.0.0.1:5001/api/v1/data/id_clients/all
@app.route('/api/v1/data/id_clients/all', methods=['GET'])
def api_id_client_all():
    return jsonify(SK_ID_CURR)


# une route pour renvoyer la liste features sélectionnées pour un id client
# test avec http://127.0.0.1:5001/api/v1/data/id_clients?SK_ID_CURR=222222
@app.route('/api/v1/data/id_clients', methods=['GET'])
def api_id_client():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'SK_ID_CURR' in request.args:
        SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results

    for individu in DATA_SELECTION.to_dict(orient='records'):
        if individu['SK_ID_CURR'] == SK_ID_CURR_UNIQUE:
            results.append(individu)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


# une route pour renvoyer le résultat du modèle pour un id client
# test avec http://127.0.0.1:5001/api/v1/model/id_clients?SK_ID_CURR=222222
@app.route('/api/v1/model/id_clients', methods=['GET'])
def api_model_id_client():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'SK_ID_CURR' in request.args:
        SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    with open('./data/best_model_seuil.pickle', 'rb') as f:
        model, seuil = pickle.load(f)

    echantillon = DATA_SELECTION.loc[DATA_SELECTION["SK_ID_CURR"]==SK_ID_CURR_UNIQUE].drop('SK_ID_CURR', axis=1)

    probabilites = model.predict_proba(echantillon)[:, 1]
    predictions = (probabilites > seuil).astype(int)

    return jsonify(predictions.tolist())


# une route pour renvoyer un graphe d'importance locale lime du modèle pour un id client
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_locale?SK_ID_CURR=222222
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_locale?SK_ID_CURR=222222&feature=15
@app.route('/api/v1/model/id_clients/importance_locale/', methods=['GET'])
def explain_prediction():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'SK_ID_CURR' in request.args:
        SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    nb_feature = 10

    if 'feature' in request.args:
        nb_feature = int(request.args['feature'])

    echantillon = DATA_SELECTION.loc[DATA_SELECTION["SK_ID_CURR"] == SK_ID_CURR_UNIQUE].drop('SK_ID_CURR', axis=1).values[0]


    with open('./data/best_model_seuil.pickle', 'rb') as f:
        model, seuil = pickle.load(f)

    # initialisation de la méthode LIME pour expliquer les prédictions
    explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns,
                                                       class_names=['0', '1'])

    # explication de la première observation de test
    exp = explainer.explain_instance(echantillon, model.predict_proba,num_features=nb_feature)

    # génération d'une représentation HTML de l'explication
    exp_html = exp.as_html()

    # création d'une réponse Flask avec les données HTML
    response = make_response(exp_html)
    response.headers['Content-Type'] = 'text/html'

    return response



app.run(port=5001)