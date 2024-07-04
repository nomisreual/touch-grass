from django.test import TestCase

from main.models import Post


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
