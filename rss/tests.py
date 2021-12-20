from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Category
from .models import RSSFeed


class FeedsAPITest(TestCase):
    def setUp(self):
        self.health_category = Category.objects.create(name='Health')
        self.finance_category = Category.objects.create(name='Finance')

        self.rss1 = RSSFeed.objects.create(name='Test1', url='http://localhost/sample-url', is_visible=True)
        self.rss2 = RSSFeed.objects.create(name='Test2', url='http://localhost/sample-url-2', is_visible=True)

        self.rss1.categories.add(self.health_category)
        self.rss2.categories.add(self.finance_category)

        # https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.admin = User.objects.create(username='admin')
        self.admin.set_password('admin')
        self.admin.save()

        self.client = Client()

    def test_get_feeds_given_no_category_supplied_expect_return_all_feeds(self):
        response = self.client.get('/feeds/')
        feeds = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(feeds), 2)
        self.assertEqual(feeds[0]['name'], 'Test1')
        self.assertEqual(feeds[1]['name'], 'Test2')

    def test_get_feeds_given_a_category_expect_return_all_feeds_from_that_category(self):
        response = self.client.get('/feeds/', { 'category': 'Health' })
        feeds = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0]['name'], 'Test1')

    def test_create_feed_given_valid_params_expect_feed_created(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/feeds/', {
            'name': 'Test3',
            'url': 'http://localhost/sample-url-3',
            'category': 'Finance'
        })

        self.assertTrue(RSSFeed.objects.filter(name='Test3').exists())

    def test_create_feed_given_non_exists_category_expect_return_error(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/feeds/', {
            'name': 'Test4',
            'url': 'http://localhost/sample-url-3',
            'category': 'Car'
        })

        self.assertEqual(response.status_code, 400)
        self.assertFalse(RSSFeed.objects.filter(name='Test4').exists())

    def test_delete_feed_given_valid_id_expect_feed_deleted(self):
        self.client.login(username='admin', password='admin')
        response = self.client.delete('/feeds/3/')

        self.assertFalse(RSSFeed.objects.filter(name='Test3').exists())

    def test_delete_feed_given_invalid_id_expect_return_not_found(self):
        self.client.login(username='admin', password='admin')
        response = self.client.delete('/feeds/100/')

        self.assertEqual(response.status_code, 404)

    def test_update_feed_given_invalid_feed_id_expect_return_error_message(self):
        self.client.login(username='admin', password='admin')
        response = self.client.put(
            '/feeds/',
            { 'name': 'edited name', 'id': 100 },
            content_type='application/json'
        )
        self.assertEqual(response.data['message'], 'RSS Feed with id 100 does not exist')

    def test_update_feed_given_valid_params_expect_feed_updated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.put(
            '/feeds/',
            { 'name': 'edited Test1', 'id': 1 },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(RSSFeed.objects.filter(name='Test1').exists())
        self.assertTrue(RSSFeed.objects.filter(name='edited Test1').exists())
