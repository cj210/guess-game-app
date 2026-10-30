from fastapi.testclient import TestClient
from guess_number.app import forest


class GgaClient:
    register_url = "/register"
    login_url = "/login"
    session_url = "/sessions"
    
    def __init__(self):
        self.http_client = TestClient(forest)
        self.token = None
        self.sessionid = None
    
    def user_register(self, username, password):
        payload = {"username": username, "password": password}
        response = self.http_client.post(self.register_url, json=payload)
        return response
    
    def user_login(self, username, password):
        payload = {"username": username, "password": password}
        log_response = self.http_client.post(self.login_url, data=payload)
        if log_response.status_code == 200:
            self.token = log_response.json().get("access_token")
        return log_response
    
    def create_session(self):
        response = self.http_client.post(self.session_url, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code in [201, 200]:
            self.sessionid = [sid for sid in response.json().get("message").split() if "-" in sid][0]
        return response

            
        
        