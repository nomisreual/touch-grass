from django.test import TestCase, Client as Agent
from django.contrib.auth.models import User

from main.models import Post
from client.models import Client
from main.api import router
from ninja.testing import TestClient


class TestPost(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_content(self):
        self.assertEqual(self.post.content, "Test Content")

    def test_post_title(self):
        self.assertEqual(self.post.title, "Test Post")


class TestPosts(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
        )
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@mail.com",
            password="password",
        )
        self.client = Client.objects.create(
            user=self.user,
            name="Test Client",
        )
        self.client.key = "testkey"
        self.client.save()

    def test_posts(self):
        agent = TestClient(router)
        response = agent.get(
            "/post",
            headers={"X-API-Key": "testkey", "USER-ID": self.user.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"title": "Test Post", "content": "Test Content"}],
        )

    def test_posts_no_header(self):
        agent = TestClient(router)
        response = agent.get(
            "/post",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Unauthorized"},
        )

    def test_posts_no_user_id(self):
        agent = TestClient(router)
        response = agent.get(
            "/post",
            headers={"X-API-Key": "testkey"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Unauthorized"},
        )

    def test_posts_invalid_key(self):
        agent = TestClient(router)
        response = agent.get(
            "/post",
            headers={"X-API-Key": "wrongkey", "USER-ID": self.user.id},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Unauthorized"},
        )

    def test_posts_no_matching_client(self):
        agent = TestClient(router)
        response = agent.get(
            "/post",
            headers={"X-API-Key": "wrongkey", "USER-ID": 100},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Unauthorized"},
        )


class TestMainViews(TestCase):
    def test_index(self):
        agent = Agent()
        response = agent.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("title"), "Welcome")
        self.assertTemplateUsed(response, "main/index.html")
        self.assertInHTML(
            "<h1>This page is under construction.</h1>",
            response.content.decode(),
        )
