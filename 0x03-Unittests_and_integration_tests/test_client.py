#!/usr/bin/env python3
"""
Test file for client.py
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

# Extract the test data from TEST_PAYLOAD
org_payload, repos_payload, expected_repos, apache2_repos = TEST_PAYLOAD[0]


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test the GithubOrgClient.
    """
    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked_url.com"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url,
                             "http://mocked_url.com")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repositories.
        """
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/test/repos")
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that has_license returns the correct result for given repo and
        license key.
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected_result)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class-level fixtures for the integration test.
        """
        def get_side_effect(url):
            if "orgs" in url:
                return cls.org_payload
            if "repos" in url:
                return cls.repos_payload
            return {}

        cls.get_patcher = patch('utils.get_json', side_effect=get_side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class-level fixtures.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method with a known payload.
        """
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with license filter.
        """
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
