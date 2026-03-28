def test_create_user(client):
    """Test creating a new user."""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "address": "123 Test St",
            "phone_number": "1234567890"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_get_users(client):
    """Test retrieving the list of users."""
    # First create a user
    client.post(
        "/users/",
        json={
            "username": "listuser",
            "first_name": "List",
            "last_name": "User",
            "address": "456 List Ave",
            "phone_number": "0987654321"
        }
    )
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 1
    assert any(u["username"] == "listuser" for u in data["users"])

def test_get_user_by_id(client):
    """Test retrieving a single user by ID."""
    create_response = client.post(
        "/users/",
        json={
            "username": "getuser",
            "first_name": "Get",
            "last_name": "User",
            "address": "789 Get Ln",
            "phone_number": "1112223333"
        }
    )
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "getuser"

def test_suggest_username(client):
    """Test the username suggestion endpoint."""
    response = client.get("/users/suggest-username?first_name=John&last_name=Doe")
    assert response.status_code == 200
    assert response.json() == {"username": "john.doe"}
    
    # Test suggestion when username exists
    client.post(
        "/users/",
        json={
            "username": "john.doe",
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "phone_number": "1234567890"
        }
    )
    response = client.get("/users/suggest-username?first_name=John&last_name=Doe")
    assert response.status_code == 200
    # It should append a counter
    assert response.json()["username"] == "john.doe1"

def test_update_user(client):
    """Test updating an existing user."""
    create_response = client.post(
        "/users/",
        json={
            "username": "updateuser",
            "first_name": "Old",
            "last_name": "Name",
            "address": "Old Addr",
            "phone_number": "0000000000"
        }
    )
    user_id = create_response.json()["id"]
    
    response = client.put(
        f"/users/{user_id}",
        json={
            "first_name": "New",
            "last_name": "Name",
            "address": "New Addr"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "New"
    assert data["address"] == "New Addr"
    assert data["username"] == "updateuser"  # Unchanged

def test_delete_user(client):
    """Test deleting a user."""
    create_response = client.post(
        "/users/",
        json={
            "username": "deleteuser",
            "first_name": "Delete",
            "last_name": "Me",
            "address": "Nowhere",
            "phone_number": "5555555555"
        }
    )
    user_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
