from playwright.sync_api import sync_playwright
from guess_number.db import sessions, users


def test_register_with_valid_input():
    with sync_playwright() as pw:
        context = pw.request.new_context()

        url = "http://127.0.0.1:8000/register"
        payload = {
                "username": "kacha",
                "password": "asc"
                }

        response = context.post(url, data=payload)
        assert response.status == 201
        assert response.status_text == "Created"
        assert response.json()["detail"] == "User creation successfull!"
        assert response.json()["message"] == "New user kacha created!"
        context.dispose()
        users.clear()
        
