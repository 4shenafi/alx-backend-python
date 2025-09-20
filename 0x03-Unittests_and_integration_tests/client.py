#!/usr/bin/env python3
"""
GitHub organization client for testing purposes.
This module provides a client for interacting with GitHub organization data.
"""
from utils import get_json
from typing import Dict, List, Union


class GithubOrgClient:
    """
    A client for accessing GitHub organization information.
    
    This class provides methods to retrieve organization data,
    public repositories, and repository license information.
    """
    
    def __init__(self, org_name: str) -> None:
        """
        Initialize the GitHub organization client.
        
        Args:
            org_name: The name of the GitHub organization
        """
        self._org_name = org_name
        self._org = None
    
    @property
    def org(self) -> Dict:
        """
        Get organization information from GitHub API.
        
        Returns:
            Dictionary containing organization data
        """
        if self._org is None:
            self._org = get_json(f"https://api.github.com/orgs/{self._org_name}")
        return self._org
    
    @property
    def _public_repos_url(self) -> str:
        """
        Get the URL for public repositories.
        
        Returns:
            The URL for the organization's public repositories
        """
        return self.org["repos_url"]
    
    def public_repos(self, license: Union[str, None] = None) -> List[str]:
        """
        Get list of public repository names.
        
        Args:
            license: Optional license key to filter repositories
            
        Returns:
            List of repository names
        """
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        
        if license is not None:
            filtered_repos = []
            for repo in repos:
                if self.has_license(repo, license):
                    filtered_repos.append(repo["name"])
            return filtered_repos
        
        return repo_names
    
    def has_license(self, repo: Dict, license_key: str) -> bool:
        """
        Check if a repository has a specific license.
        
        Args:
            repo: Repository dictionary
            license_key: The license key to check for
            
        Returns:
            True if the repository has the specified license, False otherwise
        """
        return repo.get("license", {}).get("key") == license_key
