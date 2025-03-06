from dotenv import load_dotenv
import os
from atlassian import Jira
from history_item import HistoryItem

from issue_fetcher import IssueFetcher
from jira_connection import JiraConnection

load_dotenv()

jira_conn = JiraConnection()
jira = jira_conn.connect()

issue = jira.issue('ILX-51628', expand='changelog')
history_items = []
if 'changelog' in issue:
    changelog = issue['changelog']    
    for history in changelog['histories']:
        # print(f"History: {history}")        
        for item in history['items']:
            from_status = item['fromString']
            to_status = item['toString']

            # Create a HistoryItem object and add it to the list
            history_item = HistoryItem(
                from_status=from_status,
                to_status=to_status,
                author=history.get('author', {}).get('displayName', ''),
                created=history.get('created', '')
            )
            history_items.append(history_item)
            # if from_status == 'In Development' or to_status == 'In Development':
            #     status_change = f"Status changed from '{from_status}' to '{to_status}'"
            #     print(f"{status_change}")
            #     print(f"By: {history.get('author', {}).get('displayName', '')} on {history.get('created', '')}\n")
else:
    print(f"No changelog found for issue")

# Print all HistoryItem objects in the list
for item in history_items:
    if item.from_status == 'In Development' or item.to_status == 'In Development':
        print(f"Status From: {item.from_status}, To: {item.to_status}\nAuthor: {item.author}, Created: {item.created}\n")