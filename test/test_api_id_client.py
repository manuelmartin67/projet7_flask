def test_api_id_client(client):
    response = client.get('/api/v1/data/id_clients', query_string={'SK_ID_CURR': '222222'})
    assert response.status_code == 200 # Vérifier la réponse HTTP
    data = response.get_json()
    assert len(data) == 1 # Vérifier s'il ne renvoie qu'un seul individu
    assert data[0]['SK_ID_CURR'] == 222222 # Vérifier qu'il s'agit bien de l'individu demandé
