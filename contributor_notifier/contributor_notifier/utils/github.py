########################################################################
#                    Prurpose of the Package                           #
########################################################################

# Check if there is a change in the GitHub repo. 
# Detect the contributors.
# Check of the contributor wants to be notified. 
# Extract the subject and the datamodel that has been change.  
# Send them customized emails depending on the change. 

########################################################################
#                                 Imports                              #
########################################################################

import requests
import os
import time

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# GitHub personal access token environment variables
access_token = os.getenv("PERSONAL_ACCESS_TOKEN")


########################################################################
#                         github rate for api calls                    #
######################################################################## 

def _github_rate(user, token, security_margin=2):
    """
    Check the remaining GitHub API calls for the authenticated user and wait if necessary.
    """
    try:
        # Get the current rate limit status
        response = requests.get('https://api.github.com/rate_limit', auth=(user, token))
        resonse_text = response.text
        response.raise_for_status()  # Raise an exception if the request fails
        rate_limit_data = response.json()

        # Extract rate limit information
        resources = rate_limit_data["resources"]["core"]
        remaining = resources["remaining"]  # Remaining API calls for the current window
        reset_time = resources["reset"]  # Timestamp when the rate limit resets
        used_calls = resources["used"]  # Number of API calls made in the current window

        # Calculate the time until the rate limit resets
        time_until_reset = reset_time - time.time()

        # Check if we're close to the rate limit
        if remaining < security_margin:
            # Calculate the pause time to wait until the rate limit resets
            pause_time = max(0, time_until_reset + 1)  # Add 1 second as a buffer
            print(f"Waiting for {pause_time:.2f} seconds until rate limit resets...")
            time.sleep(pause_time)

        # Print rate limit information
        print(f"Remaining API calls: {remaining}")
        print(f"Time until rate limit reset: {time_until_reset:.2f} seconds")
        print(f"Total API calls made in this window: {used_calls}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


########################################################################
#                       Latest commit info                             #
########################################################################
        
def get_latest_commit_info(repo_owner, repo_name, access_token):
    """
    Get information about the latest commit in a GitHub repository.

    Parameters:
    - repo_owner (str): The owner or organization of the GitHub repository.
    - repo_name (str): The name of the GitHub repository.
    - access_token (str): GitHub personal access token with the 'repo' scope for authentication.

    Returns:
    - dict or None: A dictionary containing information about the latest commit,
                   or None if no commits are found.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    headers = {'Authorization': f'token {access_token}'}

    # Check the remaining API calls and wait if necessary.
    # the github_rate function is called to check the remaining API calls before making the repo.get_commit call. 
    # If the remaining API calls are close to the limit, the function will wait until the rate limit resets.
    # TODO chech where it fits in the code. 
    _github_rate(access_token)

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    if response.json():
        latest_commit = response.json()[0]
        commit_info = {
            'sha': latest_commit['sha'],
            'timestamp': latest_commit['commit']['committer']['date']
        }
        return commit_info
    else:
        return None


########################################################################
#                       GitHub repo changes                            #
########################################################################
    
def check_repo_changes(repo_links, access_token):
    """
    Check for changes in a list of GitHub repositories by comparing the latest commit information.

    Parameters:
    - repo_links (list): List of GitHub repository links (URLs).
    - access_token (str): GitHub personal access token with the 'repo' scope for authentication.

    Returns:
    - list: List of dictionaries, each containing the repository URL and the timestamp of the latest change.
    """
    changed_repos = []

    for repo_link in repo_links:
        # Extract owner and repo name from the GitHub link
        _, _, _, owner, repo = repo_link.rstrip('/').split('/')

        # Get information about the latest commit for the repository
        latest_commit_info = get_latest_commit_info(owner, repo, access_token)

        # Check if the repository had a change
        if latest_commit_info is not None and latest_commit_info['sha'] != repo_states.get(repo_link):
            changed_repo_info = {
                'repo_url': repo_link,
                'timestamp': latest_commit_info['timestamp']
            }
            changed_repos.append(changed_repo_info)
            repo_states[repo_link] = latest_commit_info['sha']

    return changed_repos

########################################################################
#                             Try the code                             #
########################################################################

# Example usage
repo_links = [
    'https://github.com/smart-data-models/dataModel.ManufacturingMachine'
]

# Use a dictionary to store the latest commit SHA for each repository
repo_states = {repo_link: None for repo_link in repo_links}

# Check for changes in repositories
changed_repos = check_repo_changes(repo_links, access_token)

if changed_repos:
    print('Changes detected in the following repositories:')
    for repo_info in changed_repos:
        print(f"Repo URL: {repo_info['repo_url']}, Latest Change Timestamp: {repo_info['timestamp']}")
else:
    print('No changes detected in the repositories.')
