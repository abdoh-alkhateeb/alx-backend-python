#!/usr/bin/env python3
"""
Defines unit tests for `client.py`.
"""

import unittest
from unittest.mock import Mock, PropertyMock, patch

from parameterized import parameterized, parameterized_class

import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Defines unit tests for `client.GithubOrgClient`.
    """

    @parameterized.expand((("google"), ("abc")))
    @patch("client.get_json")
    def test_org(self, org_name, mock_method):
        """
        Tests `client.GithubOrgClient.org`.
        """
        test_instance = client.GithubOrgClient(org_name)
        test_instance.org
        mock_method.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Tests `client.GithubOrgClient._public_repos_url`.
        """
        test_instance = client.GithubOrgClient("abc")

        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock:
            mock.return_value = {"repos_url": "test_url"}
            self.assertEqual(test_instance._public_repos_url, "test_url")

    @patch("client.get_json", return_value=[{"name": "abc"}, {"name": "efg"}])
    def test_public_repos(self, mock_method):
        """
        Tests `client.GithubOrgClient.public_repos`.
        """
        test_instance = client.GithubOrgClient("abc")

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="test_url",
        ) as mock_property:
            self.assertEqual(test_instance.public_repos(), ["abc", "efg"])
            mock_method.assert_called_once_with("test_url")
            mock_property.assert_called_once()

    @parameterized.expand(
        (
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        )
    )
    def test_has_license(self, repo, license_key, returned_value):
        """
        Tests `client.GithubOrgClient.has_license`.
        """
        self.assertEqual(
            client.GithubOrgClient.has_license(repo, license_key),
            returned_value,
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Defines integration tests for `client.GithubOrgClient`.
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up class.
        """

        def mocked_requests_get(url):
            """
            Returns appropriate fixture data based on the URL.
            """
            mock_response = Mock()

            if url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            elif url == client.GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload

            return mock_response

        cls.get_patcher = patch("requests.get", side_effect=mocked_requests_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tears down class.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests `client.GithubOrgClient.public_repos`.
        """
        test_instace = client.GithubOrgClient("google")
        self.assertEqual(test_instace.public_repos(), self.expected_repos)
        self.assertEqual(
            test_instace.public_repos(license="apache-2.0"), self.apache2_repos
        )
