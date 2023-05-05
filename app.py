from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True


SK_ID_CURR = pd.read_csv("./data/SK_ID_CURR.csv").to_dict(orient='records')
DATA_SELECTION = pd.read_csv("./data/DATA_SELECTION.csv").to_dict(orient='records')


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

    for individu in DATA_SELECTION:
        if individu['SK_ID_CURR'] == SK_ID_CURR_UNIQUE:
            results.append(individu)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)



app.run(port=5001)