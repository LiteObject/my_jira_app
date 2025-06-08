"""
jira_connection.py

Provides the JiraConnection class for connecting to a Jira instance using environment variables.
"""

import os
import requests
from atlassian import Jira


class JiraConnection:
    """
    Handles connection to a Jira instance using credentials from environment variables.
    """

    def __init__(self):
        """
        Initializes JiraConnection with credentials from environment variables:
        JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN.
        """
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_username = os.getenv('JIRA_USERNAME')
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')

    def connect(self):
        """
        Establishes a connection to Jira using the atlassian-python-api Jira class.
        Returns:
            Jira: Jira connection object if successful, None otherwise.
        """
        try:
            jira = Jira(
                url=self.jira_url,
                username=self.jira_username,
                password=self.jira_api_token,
                cloud=True
            )
            return jira
        except requests.exceptions.RequestException as e:
            print(f"Network error connecting to Jira: {e}")
            return None
        except ValueError as e:
            print(f"Invalid Jira connection parameters: {e}")
            return None
