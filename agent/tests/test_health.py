def test_healthcheck(client):
    """Test that health check endpoint returns healthy status."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}