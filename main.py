"""
main.py

Entry point for the Jira API App. Handles setup, connection, issue processing, and plotting.
"""

import os
import logging
from datetime import datetime

import matplotlib.pyplot as plt
import colorlog
from dotenv import load_dotenv

from jira_issue_service import JiraIssueService
from jira_connection import JiraConnection


def setup_logging():
    """
    Configures colorized logging for the application.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(message)s',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))
    logging.basicConfig(level=logging.INFO, handlers=[handler])


def get_jira_connection():
    """
    Establishes and returns a Jira connection using environment variables.
    Returns:
        Jira: Jira connection object if successful, None otherwise.
    """
    jira_conn = JiraConnection()
    jira = jira_conn.connect()
    if not jira:
        logging.error("Failed to connect to JIRA.")
        return None
    return jira


def fetch_usernames():
    """
    Fetches the list of Jira usernames from the USERNAMES environment variable.
    Returns:
        list[str] or None: List of usernames if set, None otherwise.
    """
    jira_users = os.getenv('USERNAMES')
    if not jira_users:
        logging.error("Please set the USERNAMES environment variable.")
        return None
    return jira_users.split(',')


def process_issues(issue_service, usernames, pi):
    """
    Processes issues for each user and calculates total story points.
    Args:
        issue_service (JiraIssueService): Service for fetching Jira issues.
        usernames (list[str]): List of Jira usernames.
        pi (str): Program Increment identifier.
    Returns:
        dict: Mapping of username to total story points.
    """
    user_story_points = {}
    for username in usernames:
        issues = issue_service.fetch_issues(username, pi)
        print(f"## Jira tickets for {username}")
        if issues:
            total_custom_field_value = 0

            for issue in issues['issues']:
                custom_field_value = issue['fields'].get(
                    'customfield_10049', 0)
                issue_type = issue['fields']['issuetype']['name']
                if isinstance(custom_field_value, (int, float)):
                    total_custom_field_value += custom_field_value
                    user_story_points[username] = user_story_points.get(
                        username, 0) + custom_field_value
                else:
                    # Use lazy % formatting for logging
                    logging.warning(
                        ">>> %s %s has missing Story Point (customfield_10049) value.",
                        issue_type, issue['key']
                    )

                print(
                    f"#### [{issue['key']}] | {issue_type} | {issue['fields']['summary']} | Points: {custom_field_value}")

                status_name = 'In Development'
                history_items = issue_service.get_time_in_status(
                    issue['key'], status_name)
                # Print all HistoryItem objects in the list
                print(f"- Logs related to {status_name} for {issue['key']}")
                for item in history_items:
                    if item.from_status == status_name or item.to_status == status_name:
                        print(
                            f"  - **{item.from_status}** -> **{item.to_status}** by _{item.author}_ on {item.created}")

            print("\n")
            print(f"### Total {pi} Story Points: {total_custom_field_value}\n")
            # logging.info("=" * 75)
        else:
            logging.warning("No issues found.")
    return user_story_points


def plot_story_points(user_story_points, pi):
    """
    Plots a bar chart of total story points completed by each user.
    Args:
        user_story_points (dict): Mapping of username to total story points.
        pi (str): Program Increment identifier.
    """
    sorted_user_story_points = dict(
        sorted(user_story_points.items(), key=lambda item: item[1], reverse=True))
    plt.figure(figsize=(10, 6))
    try:
        plt.bar(sorted_user_story_points.keys(),
                sorted_user_story_points.values(), color='skyblue')
        plt.xlabel('Usernames')
        plt.ylabel('Total Story Points')
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plt.title(
            f'Total Story Points Completed by Each User in {pi} ({current_datetime})')
        plt.xticks(rotation=45)
        plt.tight_layout()
    except (ValueError, TypeError) as exc:
        # Catch only specific exceptions for plotting
        logging.error("Error plotting: %s", exc)
    plt.show()


def main():
    """
    Main entry point for the Jira API App.
    Sets up logging, loads environment variables, connects to Jira, 
    processes issues, and plots results.
    """
    setup_logging()
    load_dotenv()

    jira = get_jira_connection()
    if not jira:
        logging.error("Failed to connect to JIRA.")
        return

    usernames = fetch_usernames()
    if not usernames:
        logging.error("Please set the USERNAMES environment variable.")
        return

    issue_service = JiraIssueService(jira)
    pi = 'PI-10'
    user_story_points = process_issues(issue_service, usernames, pi)
    plot_story_points(user_story_points, pi)


if __name__ == "__main__":
    main()
