def test_api_id_client(client):
    response = client.get('/api/v1/data/id_clients', query_string={'SK_ID_CURR': '222222'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['SK_ID_CURR'] == 222222
    # Ajoutez ici d'autres assertions pour vérifier les résultats attendus
