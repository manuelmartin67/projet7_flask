from flask import Flask, request, jsonify, make_response
import pandas as pd
import pickle
import lime.lime_tabular
from matplotlib.figure import Figure
import base64
from io import BytesIO
import numpy as np



app = Flask(__name__)
app.config["DEBUG"] = True


SK_ID_CURR = pd.read_csv("./data/SK_ID_CURR.csv").to_dict(orient='records')
DATA_SELECTION = pd.read_csv("./data/DATA_SELECTION.csv")
X_train = pd.read_csv("./data/X_train.csv")

with open('./data/best_model_seuil.pickle', 'rb') as f:
    model, seuil = pickle.load(f)

# initialisation de la méthode LIME pour expliquer les prédictions
explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns,
                                                   class_names=['Accept. > 0.55', 'Refus > 0.45'])

# Obtenez le modèle LGBMClassifier du pipeline
clf_model = model.named_steps['clf']
# Obtenez les feature importance
importance = clf_model.feature_importances_
# Obtenez les noms de colonnes correspondant aux feature importance
feature_names = model.named_steps['scale'].get_feature_names_out()
# Créez un DataFrame pour stocker les feature importance
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importance}).sort_values('importance',
                                                                                                       ascending=False)


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
    SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.

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
    SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    echantillon = DATA_SELECTION.loc[DATA_SELECTION["SK_ID_CURR"]==SK_ID_CURR_UNIQUE].drop('SK_ID_CURR', axis=1)

    probabilites = model.predict_proba(echantillon)[:, 1]
    predictions = (probabilites > seuil).astype(int)

    if predictions== 1 :
        predictions = "Refus"
    if predictions== 0 :
        predictions = "Acceptation"

    return jsonify(predictions)



# une route pour renvoyer un graphe d'importance locale lime du modèle pour un id client
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_locale?SK_ID_CURR=222222
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_locale?SK_ID_CURR=222222&feature=15
@app.route('/api/v1/model/id_clients/importance_locale/', methods=['GET'])
def importance_locale():
    SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    nb_feature = 10

    if 'feature' in request.args:
        nb_feature = int(request.args['feature'])

    echantillon = DATA_SELECTION.loc[DATA_SELECTION["SK_ID_CURR"] == SK_ID_CURR_UNIQUE].drop('SK_ID_CURR', axis=1).values[0]

    # explication de la première observation de test
    exp = explainer.explain_instance(echantillon, model.predict_proba,num_features=nb_feature)

    # génération d'une représentation HTML de l'explication
    exp_html = exp.as_html()

    # création d'une réponse Flask avec les données HTML
    response = make_response(exp_html)

    return response



# une route pour renvoyer un graphe d'importance globale
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_globale?feature=15
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/importance_globale
@app.route('/api/v1/model/id_clients/importance_globale/', methods=['GET'])
def importance_globale():
    nb_feature = 10

    if 'feature' in request.args:
        nb_feature = int(request.args['feature'])

    # Triez les features par ordre d'importance décroissant
    feature_importance_df_selection = feature_importance_df.head(nb_feature)

    # Tracez la feature importance globale
    fig= Figure(figsize=(8, 5))
    axe = fig.add_subplot(111)
    axe.barh(y=feature_importance_df_selection['feature'], width=feature_importance_df_selection['importance'])

    axe.set_xlabel('Importance')
    axe.set_ylabel('Feature')
    axe.set_title('Feature Importance')
    axe.legend()
    axe.invert_yaxis()
    fig.subplots_adjust(left=0.4)


    # https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"



# une route pour renvoyer un graphe de comparaison entre l'échantillon de l'id client et la population
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/comparaison?SK_ID_CURR=222222
# test avec http://127.0.0.1:5001/api/v1/model/id_clients/comparaison?SK_ID_CURR=222222&feature=15
@app.route('/api/v1/model/id_clients/comparaison/', methods=['GET'])
def comparaison():
    SK_ID_CURR_UNIQUE = int(request.args['SK_ID_CURR'])

    nb_feature = 10

    if 'feature' in request.args:
        nb_feature = int(request.args['feature'])

    colonnes = feature_importance_df['feature'].head(nb_feature)
    echantillon = DATA_SELECTION.loc[DATA_SELECTION["SK_ID_CURR"] == SK_ID_CURR_UNIQUE]

    # calcul des dimensions des sous-plots
    n = colonnes.nunique()

    fig = Figure(figsize=(6, n * 3))
    axs = fig.subplots(nrows=n, ncols=1, squeeze=False)

    # génération des graphes pour chaque feature
    for i, feature in enumerate(colonnes):
        row = i

        # Calcul de la moyenne et de l'écart type de l'échantillon
        all_mean = np.mean(DATA_SELECTION[feature])
        sample_mean = np.mean(echantillon[feature])

        # histogramme des valeurs pour tous les individus dans le dataset
        axs[row,0].hist(DATA_SELECTION[feature].values, bins=20, alpha=0.5, label='Population')

        # Affichage de la droite verticale de la moyenne de l'échantillon
        axs[row,0].axvline(x=sample_mean, color='red', linestyle='--', label='Sample')

        # Affichage de la droite verticale de la moyenne de la population
        axs[row,0].axvline(x=all_mean, color='black', linestyle='-', label='Population Mean')

        # Configuration du graphique
        axs[row,0].set_xlabel('Values')
        axs[row,0].set_ylabel('Frequency')
        axs[row,0].set_title('Distribution of Data')
        axs[row,0].legend()

        # ajout d'un titre pour le graphe
        axs[row,0].set_title(feature)

        # ajout d'une légende pour les histogrammes
        axs[row,0].legend()

    # ajustement de l'espacement entre les sous-plots
    fig.tight_layout()

    # https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(port=5001)