import json


def test_api_id_client_all(client):
    response = client.get('/api/v1/data/id_clients/all')
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0