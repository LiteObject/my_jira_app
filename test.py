"""
test.py

Fetches and prints all Jira issues assigned to a given email address.
Usage: py test.py <email_address>
"""

import sys
from dotenv import load_dotenv
from jira_issue_service import JiraIssueService
from jira_connection import JiraConnection

# Load environment variables from .env file
load_dotenv()

# Establish a connection to Jira
jira_conn = JiraConnection()
jira = jira_conn.connect()

# Check for required command-line argument (email address)
if len(sys.argv) < 2:
    print("Usage: py test.py <email_address>")
    sys.exit(1)

# Get the email address from command-line arguments
email = sys.argv[1]

# Build JQL query to find all issues assigned to the given email address
jql_query = f'assignee = "{email}"'
issues = jira.jql(jql_query)

# Print the key and summary of each issue found, or a message if none are found
if issues and 'issues' in issues:
    for issue in issues['issues']:
        # Try to get epic info from the parent field
        epic_key = None
        epic_name = None
        parent = issue['fields'].get('parent')
        if parent:
            epic_key = parent.get('key', 'No Epic')
            epic_name = parent.get('fields', {}).get('summary', 'No Epic Name')
        else:
            epic_key = 'No Epic'
            epic_name = 'No Epic Name'
        print(
            f"{issue['key']}: {issue['fields']['summary']} | Epic: {epic_key} | Epic Name: {epic_name}"
        )
else:
    print(f"No issues found for {email}")


total_story_points = JiraIssueService.get_total_story_points_for_epic(
    "SCRUM-1")
print(f"Total story points for epic {epic_key}: {total_story_points}")
