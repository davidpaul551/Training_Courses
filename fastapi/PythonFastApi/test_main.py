from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_all_blogs():
    response = client.get('/blog/all')
    assert response.status_code==200



def test_auth_error():
    response = client.post('/token', data={"username": " ", "password": " "})

    # Debugging: Print the JSON response
    print("Response JSON:", response.json())

    json_response = response.json()

    # Get access token if it exists
    access_token = json_response.get("access_token")

    # Handle "detail" key properly
    detail = json_response.get("detail")
    if isinstance(detail, list) and len(detail) > 0:
        message = detail[0].get("msg", "No message found")
    elif isinstance(detail, dict):
        message = detail.get("msg", "No message found")
    elif isinstance(detail, str):  # If it's a simple string
        message = detail
    else:
        message = "Invalid response format"

    # Update assertion based on actual API response
    assert message == "Invalid Credentials"  # Adjust if needed
    assert access_token is None



def test_auth_success():
     response = client.post('/token', data={"username": "cat", "password": "cat"})

    # Debugging: Print the JSON response
     print("Response JSON:", response.json())

     json_response = response.json()

    # Get access token if it exists
     access_token = json_response.get("access_token")
     assert access_token

def test_post_article():
     auth = client.post('/token', data={"username": "cat", "password": "cat"})

     print("Response JSON:", auth.json())

     json_response = auth.json()

     access_token = json_response.get("access_token")
     assert access_token
     
     response=client.post(
         "/article/",
         json={
             'title':'test article',
             'content':'Test Content',
             'published': True,
             'creator_id':1
         },
         headers={
             "Authorization":"bearer "+access_token
         }
     )
     assert response.status_code==200
     assert response.json().get('title')=="test article"