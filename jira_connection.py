import os
from atlassian import Jira

class JiraConnection:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_username = os.getenv('JIRA_USERNAME')
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')

    def connect(self):
        try:
            jira = Jira(
                url=self.jira_url,
                username=self.jira_username,
                password=self.jira_api_token,
                cloud=True
            )
            return jira
        except Exception as e:
            print(f"Error connecting to Jira: {e}")
            return None