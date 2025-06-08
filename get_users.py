from dotenv import load_dotenv

from jira_connection import JiraConnection

load_dotenv()

jira_conn = JiraConnection()
jira = jira_conn.connect()

# Fetch all available groups and print them to find the correct group name
print("Available Jira groups:")
groups = jira.get_groups()
for group in groups.get('groups', []):
    group_name = group.get('name', group)
    print(f"\nUsers in group: {group_name}")
    users = jira.get_all_users_from_group(group_name)
    # Handle paginated or dict response
    if isinstance(users, dict) and 'values' in users:
        user_list = users['values']
    else:
        user_list = users

    for user in user_list:
        if isinstance(user, dict):
            username = user.get('displayName', user.get(
                'accountId', 'Unknown User'))
            email = user.get('emailAddress', 'No Email')
            print(f"Display Name: {username}, Email: {email}")
        else:
            print(user)
