def test_api_model_id_client(client):
    response = client.get('/api/v1/model/id_clients', query_string={'SK_ID_CURR': '222222'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data, str)
    assert data in ['Refus', 'Acceptation']
    # Ajoutez ici d'autres assertions pour vérifier les résultats attendus
