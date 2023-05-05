from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Projet 7 - Implémentez un modèle de scoring</h1><p>Ce site donne accès à l'API pour le dashboard du " \
           "projet 7 OC</p>"


#app.run(port=5001)


# une route pour renvoyer la liste des id clients
# test avec http://127.0.0.1:5001/api/v1/data/id_clients/all
@app.route('/api/v1/data/id_clients/all', methods=['GET'])
def api_id_client_all():
    SK_ID_CURR = pd.read_csv("./data/SK_ID_CURR.csv").to_dict(orient='records')
    return jsonify(SK_ID_CURR)


app.run(port=5001)