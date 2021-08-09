from rest_framework.test import APITestCase, APIClient
import subprocess
from django.contrib.auth.models import User

class ImportOPMLFileSubscription(APITestCase):

    def test_command_needs_file_argument_to_run (self):
        out,error= subprocess.Popen('python3 manage.py import_subscriptions',shell=True,
                                          stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        error = error.splitlines()
        error_msg_expected = 'error: the following arguments are required: file'
        error_found = False
        for line in error:
            if (error_msg_expected in str(line)):
                error_found = True
        self.assertEqual(error_found, True)

    def test_command_create_subscription_for_existing_user(self):
        user = User.objects.create_user(username= 'username' ,password='password',email='email@email.com')
        user.save()
        out = subprocess.check_output('python3 manage.py import_subscriptions main_app/tests/import_subscriptions_tests/feeds.opml username', shell=True,
                                     )
        out = out.splitlines()
        print(out)





