from django.test import TestCase

from django.contrib.auth.models import User
from client.models import Client
from unittest.mock import patch


class TestClient(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser",
            email="test@mail.com",
            password="password",
        )
        self.client = Client.objects.create(
            user=self.user,
            name="Test Client",
        )

    def test_client_str(self):
        self.assertEqual(str(self.client), "TestUser - Test Client")

    @patch("os.environ.get")
    def test_client_key(self, mock_get):
        """Setting a key should encrypt it and getting it should decrypt it."""
        # Mock encryption key:
        mock_get.return_value = "X_Op4l6wzXW50RZJ48uAeJbOIxaiKTx2fvOfOtY_PTU="
        # Test Key:
        api_key = "test_api_key"

        # Assign the key:
        self.client.key = api_key
        # If encryption works as expected, the original key should be returned.
        self.assertEqual(self.client.key, api_key)

    def test_client_key_no_encrypted_key(self):
        """If no key is set, an empty string is to be returned."""
        self.assertEqual(self.client.key, "")

    @patch("os.environ.get")
    def test_client_no_encryption_key_raises_set(self, mock_get):
        """Trying to set a key without encryption key should
        raise a ValueError."""
        # Mock encryption key:
        mock_get.return_value = None
        with self.assertRaises(ValueError):
            # Test Key:
            api_key = "test_api_key"

            # Assign the key:
            self.client.key = api_key

    @patch("os.environ.get")
    def test_client_no_encryption_key_raises_get(self, mock_get):
        """Trying to get a key without encryption key should
        raise a ValueError."""
        # Mock encryption key:
        mock_get.return_value = "X_Op4l6wzXW50RZJ48uAeJbOIxaiKTx2fvOfOtY_PTU="

        # Test Key:
        api_key = "test_api_key"

        # Assign the key:
        self.client.key = api_key

        # Remove the encryption key:
        mock_get.return_value = None

        with self.assertRaises(ValueError):
            self.client.key

    def test_encrypted_key(self):
        """The key should be encrypted when set."""
        # Test Key:
        api_key = "test_api_key"
        # Assign the key:
        self.client.key = api_key
        # The encrypted key should not match the original key:
        self.assertNotEqual(self.client.encrypted_api_key, api_key.encode())
