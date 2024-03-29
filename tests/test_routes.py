def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_post_route(client):
    response = client.post('/', data={'year': '2022', 'season': 'Spring'})
    assert response.status_code == 200
    assert 'No anime data found' not in response.data.decode('utf-8')
