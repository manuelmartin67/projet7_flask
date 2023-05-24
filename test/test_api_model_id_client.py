def test_api_model_id_client(client):
    response = client.get('/api/v1/model/id_clients', query_string={'SK_ID_CURR': '222222'})
    assert response.status_code == 200 # Vérifier la réponse HTTP
    data = response.get_json()
    assert isinstance(data, str) # Vérifier qu'il s'agit bien d'un string
    assert data in ['Acceptation'] # Vérifier qu'il renvoie bien Refus pour l'individu 222222
