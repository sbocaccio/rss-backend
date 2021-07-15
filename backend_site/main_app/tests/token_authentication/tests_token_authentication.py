
from rest_framework.test import APITestCase, APIClient
from http import HTTPStatus
from requests.structures import CaseInsensitiveDict

class TokenAuthentication(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def create_user(self,user,password,email):
        data = {"username": user, "password": password ,"email": email}
        response= self.client.post('/main_app/register/', data)
        return response

    def get_token(self,user,password):
        data = {"username": user, "password": password }
        resp= self.client.post("/token/", data)
        token = resp.json().get('access')
        return token

    def test_new_user_can_register(self):
        resp = self.create_user('usuario','uno23456789','usuario@gmail.com')
        self.assertEquals(resp.status_code,HTTPStatus.OK)    
        self.assertEquals(resp.data['message'],'User Created Successfully')

    def test_valid_user_can_get_token(self):

        data = {"username": 'usuario', "password": 'uno23456789' }
        self.create_user('usuario','uno23456789','usuario@gmail.com')
        resp= self.client.post("/token/", data, format='json')
        self.assertEquals(resp.status_code,HTTPStatus.OK) 


    def test_unregistered_user_gets_cannot_get_token(self):
 
        data = {"username": 'invalid_user', "password":'uno2345667' }
        resp= self.client.post("/token/", data)
        self.assertEquals(resp.status_code,HTTPStatus.UNAUTHORIZED)        

    def test_same_user_can_not_be_registered_twice(self):
        self.create_user('usuario','uno23456789','usuario@gmail.com')
        resp = self.create_user('usuario','uno23456789','usuario@gmail.com')
        message = resp.json()

        self.assertEquals(resp.status_code,HTTPStatus.BAD_REQUEST)
        self.assertEquals(message['username'][0],'A user with that username already exists.')   

    def test_user_can_login_using_API(self):
        self.create_user('usuario','uno23456789','usuario@gmail.com')
        data = {"username": 'usuario', "password": 'uno23456789' }
        resp= self.client.post("/main_app/login/", data)
        self.assertEqual(resp.status_code,HTTPStatus.OK)
        self.assertEquals(resp.data['message'],'You Succesfully loged in')   

    def test_user_can_login_using_using_lower_and_upper(self):    
        self.create_user('usuario','uno23456789','usuario@gmail.com')
        data = {"username": 'usUaRiO', "password": 'uno23456789' }
        resp= self.client.post("/main_app/login/", data)
        self.assertEqual(resp.status_code,HTTPStatus.OK)
        self.assertEquals(resp.data['message'],'You Succesfully loged in')   

    def test_cannot_create_user_changing_only_case_sensitive(self):
        self.create_user('usuario','uno23456789','usuario@gmail.com')
        resp = self.create_user('usUarIo','uno23456789','usuario@gmail.com')
        self.assertEquals(resp.status_code,HTTPStatus.BAD_REQUEST)
        self.assertEquals(str(resp.data[0]),'User name already registered')   

    def test_register_user_returns_a_token(self):
        resp= self.create_user('newuser','uno23456789','usuario@gmail.com')
        token_access = resp.json().get('access')
        token_refresh = resp.json().get('refresh')
        self.assertNotEqual(token_access , None)
        self.assertNotEqual(token_refresh , None)
        self.assertEqual(resp.status_code,HTTPStatus.OK)
    


    def test_login_user_returns_a_token(self):
        resp= self.create_user('newuser','uno23456789','usuario@gmail.com')
        data = {"username": 'newuser', "password": 'uno23456789' }
        resp= self.client.post("/main_app/login/", data)
        token_access = resp.json().get('access')
        token_refresh = resp.json().get('refresh')
        self.assertNotEqual(token_access , None)
        self.assertNotEqual(token_refresh , None)
        self.assertEqual(resp.status_code,HTTPStatus.OK)    
     

    def test_cannot_create_user_when_password_is_invalid(self):
        resp= self.create_user('newuser','contra','usuario@gmail.com')
        self.assertEqual(resp.status_code,HTTPStatus.BAD_REQUEST)
        self.assertEquals(str(resp.data['message']),'Password must have at least 8 digits')   

