from playwright.sync_api import APIRequestContext


class Ggaclient:
    register_url = "/register"
    login_url = "/login"

    def __init__(self, api_context: APIRequestContext):

       self.context = api_context 
       self.token = None

    def register_user(self, username, password):

        response = self.context.post(self.register_url, data={"username": username, "password": password})

        return response

    def login_user(self, username, password):

        response = self.context.post(self.login_url, form={"username": username, "password": password})

        if response.status == 200:
            self.token = response.json().get("access_token")

        return response



