"""
issue_fetcher.py

Provides the IssueFetcher class for fetching Jira issues and their status history.
"""

from datetime import datetime

from history_item import HistoryItem


class JiraIssueService:
    """
    Fetches issues and their status history from Jira.
    """

    def __init__(self, jira):
        """
        Initializes JiraIssueService with a Jira connection object.
        Args:
            jira: An instance of the Jira connection.
        """
        self.jira = jira

    def fetch_issues(self, username, pi):
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

    def get_time_in_status(self, issue_key, _):
        """
        Retrieves the history of status changes for a given issue and status name.
        Args:
            issue_key (str): The Jira issue key.
            status_name (str): The status name to filter history (unused).
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
