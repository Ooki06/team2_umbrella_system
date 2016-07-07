from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.
class QuestionMethodTests(TestCase):

    def test_index_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_room_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:room')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_login_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_logout_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    def test_yoyaku_touroku_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:yoyaku_touroku')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    def test_yoyaku_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:yoyaku', args=('201601011','101','1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    def test_login_go_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:login')
        response = self.client.post(url, {u'user_name': [u'ooki'], u'password': [u'password'], })
        self.assertEqual(response.status_code, 200)
    def test_date_success(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:date', args=('20160111',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_index_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:index')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 302)
    def test_room_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:room')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 302)
    def test_login_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:login')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 302)
    def test_logout_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:logout')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
    def test_yoyaku_touroku_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:yoyaku_touroku')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    def test_yoyaku_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:yoyaku', args=('000000001','101','1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
#    def test_login_go_failure(self):
#        """
#        was_published_recently() should return False for questions whose
#        pub_date is in the future.
#        """
#        url = reverse('umbrella_system:login')
#        response = self.client.post(url, {u'user_name': [u'moudamepo'], u'password': [u'password'], })
#        self.assertNotEqual(response.status_code, 200)
    def test_date_failure(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        url = reverse('umbrella_system:date', args=('20160222',))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
