from atlassian import Jira
from jira_connection import JiraConnection
from history_item import HistoryItem
from datetime import datetime

class IssueFetcher:
    def __init__(self, jira):
        self.jira = jira

    def fetch_issues(self, username, pi):
        try:
            jql_query = f'assignee = "{username}" AND "Program Increment (PI)[Dropdown]" = {pi}'
            issues = self.jira.jql(jql_query)
            return issues
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return None
        
    def get_time_in_status(self, issue_key, status_name):        
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
                    created_date = datetime.strptime(created_datetime, '%Y-%m-%dT%H:%M:%S.%f%z').date() if created_datetime else ''
                    history_item = HistoryItem(
                        from_status=from_status,
                        to_status=to_status,
                        author=history.get('author', {}).get('displayName', ''),
                        created=created_date
                    )

                    history_items.append(history_item)
        else:
            print(f"No changelog found for issue {issue_key}")
            return None

        return history_items