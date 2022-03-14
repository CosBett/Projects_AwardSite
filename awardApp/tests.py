from django.test import TestCase
from .models import *

class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='Prime', password='123qwerty')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()

class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='Prime')
        self.post = Post.objects.create(id=1, title='Post testing', photo='image.png', description='This is test description',
        user=self.user, url='http://urltest.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_post(self):
        self.post.save_post()
        post = Post.objects.all()
        self.assertTrue(len(post) > 0)

    def test_get_posts(self):
        self.post.save()
        posts = Post.all_posts()
        self.assertTrue(len(posts) > 0)

    def test_search_post(self):
        self.post.save()
        post = Post.search_project('test')
        self.assertTrue(len(post) > 0)

    def test_delete_post(self):
        self.post.delete_post()
        post = Post.search_project('test')
        self.assertTrue(len(post) < 1)
