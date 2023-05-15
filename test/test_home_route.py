def test_home_route(client):
    response = client.get('/')

    assert response.status_code == 200
    assert "Projet 7 - Implémentez un modèle de scoring".encode("utf-8") in response.data
    assert "Ce site donne accès à l'API pour le dashboard du projet 7 OC".encode("utf-8") in response.data

