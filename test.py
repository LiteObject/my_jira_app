"""
test.py

Fetches and prints all Jira issues assigned to a given email address.
Usage: py test.py <email_address>
"""

import sys
from dotenv import load_dotenv
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
        print(f"{issue['key']}: {issue['fields']['summary']}")
else:
    print(f"No issues found for {email}")
