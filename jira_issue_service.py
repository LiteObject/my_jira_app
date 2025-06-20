"""
issue_fetcher.py

Provides the IssueFetcher class for fetching Jira issues and their status history.
"""

from datetime import datetime
from typing import Optional

from history_item import HistoryItem


class JiraIssueService:
    """
    Fetches issues and their status history from Jira.
    """

    def __init__(self, jira) -> None:
        """
        Initializes JiraIssueService with a Jira connection object.
        Args:
            jira: An instance of the Jira connection.
        """
        self.jira = jira

    def fetch_issues_by_username(self, username: str, pi: str) -> Optional[dict]:
        """
        Fetches issues assigned to a user for a specific Program Increment (PI).
        Args:
            username (str): The Jira username to fetch issues for.
            pi (str): The Program Increment identifier.
        Returns:
            dict or None: Issues data if successful, None otherwise.
        """
        try:
            jql_query = f'assignee = "{username}" AND "Program Increment (PI)[Dropdown]" = {pi}'
            issues = self.jira.jql(jql_query)
            return issues
        except (AttributeError, TypeError, ValueError) as e:
            print(f"Error fetching issues: {e}")
            return None

    def fetch_issues_by_email(self, email: str) -> Optional[dict]:
        """
        Fetches issues assigned to a user by their email address.
        Args:
            email (str): The email address of the Jira user.
        Returns:
            dict or None: Issues data if successful, None otherwise.
        """
        try:
            jql_query = f'assignee = "{email}"'
            issues = self.jira.jql(jql_query)
            return issues
        except (AttributeError, TypeError, ValueError) as e:
            print(f"Error fetching issues by email: {e}")
            return None

    def get_issue_history(self, issue_key: str) -> Optional[list[HistoryItem]]:
        """
        Retrieves the history of status changes for a given issue.
        Args:
            issue_key (str): The Jira issue key.
        Returns:
            list[HistoryItem] or None: List of HistoryItem objects or None if no changelog found.
        """
        issue = self.jira.issue(issue_key, expand='changelog')
        history_items = []
        if 'changelog' in issue:
            changelog = issue['changelog']
            for history in changelog['histories']:
                for item in history['items']:
                    from_status = item['fromString']
                    to_status = item['toString']
                    # Create a HistoryItem object and add it to the list
                    created_datetime = history.get('created', '')
                    created_date = datetime.strptime(
                        created_datetime, '%Y-%m-%dT%H:%M:%S.%f%z').date() if created_datetime else ''
                    history_item = HistoryItem(
                        from_status=from_status,
                        to_status=to_status,
                        author=history.get('author', {}).get(
                            'displayName', ''),
                        created=created_date
                    )

                    history_items.append(history_item)
        else:
            print(f"No changelog found for issue {issue_key}")
            return None

        return history_items

    def get_total_story_points_for_epic(self, epic_key: str) -> int:
        """
        Calculates the total story points for all issues under a given epic.
        Args:
            epic_key (str): The Jira key of the epic.
        Returns:
            int: Total story points for all issues under the epic.
        """
        try:
            # JQL to find all issues linked to the epic
            jql_query = f'"Epic Link" = "{epic_key}"'
            issues = self.jira.jql(jql_query)
            total_points = 0
            if issues and 'issues' in issues:
                for issue in issues['issues']:
                    # Adjust the custom field key if your Jira instance uses a different one
                    story_points = issue['fields'].get('customfield_10049', 0)
                    if isinstance(story_points, (int, float)):
                        total_points += story_points
            return total_points
        except (AttributeError, TypeError, ValueError) as e:
            print(f"Error calculating story points for epic {epic_key}: {e}")
            return 0
