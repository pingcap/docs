# This script can create an empty PR in your target repo based on your specified source language PR.
# Before running this script:
# 1. Get a GitHub personal access token (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and save it in a text file.
# 2. Ensure that you have forked your target repo because the changes in the new PR will be committed to your forked repository first.

import requests
import base64
import re

source_pr_url = "https://github.com/pingcap/docs-cn/pull/13895" # update this URL to your PR link
my_github_id = "qiancai" # update this ID to your GitHub ID
my_github_token_file_path = r"/Users/grcai/Documents/PingCAP/Python_scripts/GitHub/gh_token5.txt"

# Read the GitHub personal access token from your local file.
with open(my_github_token_file_path, "r") as f:
    access_token = f.read().strip()

# For getting the information about the source language PR
def get_pr_info(pr_url):
    url_parts = pr_url.split("/")
    source_repo_owner = url_parts[3]
    source_repo_name = url_parts[4]
    pr_number = url_parts[6]

    url = f"https://api.github.com/repos/{source_repo_owner}/{source_repo_name}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        pr_data = response.json()

        source_title = pr_data["title"]
        source_description = pr_data["body"]
        source_labels = [label["name"] for label in pr_data.get("labels", []) if "size" not in label["name"] and "translation" not in label["name"] and "status" not in label["name"]]
        base_repo = pr_data["base"]["repo"]["full_name"]
        base_branch = pr_data["base"]["ref"]
        head_repo = pr_data["head"]["repo"]["full_name"]
        head_branch = pr_data["head"]["ref"]

        print(f"Getting source language PR information was successful. The head branch name is: {head_branch}")

        return source_title, source_description, source_labels, base_repo, base_branch, head_repo, head_branch, pr_number
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get source language PR information: {response.text}")
        raise e

# For syncing the corresponding branch of my forked repository to the latest upstream
def sync_my_repo_branch(target_repo_owner, target_repo_name,my_repo_owner, my_repo_name, base_branch):
    #  Get the branch reference SHA of the upstream repository.
    api_url = f"https://api.github.com/repos/{target_repo_owner}/{target_repo_name}/git/refs/heads/{base_branch}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        upstream_sha = response.json().get("object", {}).get("sha")
    else:
        print("Failed to get the upstream repository branch reference.")
        exit()

    # Update the branch reference of your fork repository
    api_url = f"https://api.github.com/repos/{my_repo_owner}/{my_repo_name}/git/refs/heads/{base_branch}"
    data = {
        "sha": upstream_sha,
        "force": True
    }

    print("Syncing the latest content from the upstream branch...")

    response = requests.patch(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print("The content sync is successful!")
    else:
        print("Failed to sync the latest content from the upstream branch.")


# For creating a new branch in my forked repository
def create_branch(repo_owner, repo_name, branch_name, base_branch, access_token):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get a reference to the base branch
    base_branch_url = f"heads/{base_branch}"
    response = requests.get(f"{api_url}/{base_branch_url}", headers=headers)

    if response.status_code == 200:
        base_branch_ref = response.json().get("object", {}).get("sha")

        if base_branch_ref:
            # Create a reference to a new branch
            branch_ref = f"refs/heads/{branch_name}"
            data = {
                "ref": branch_ref,
                "sha": base_branch_ref
            }

            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 201:
                branch_url = f"https://github.com/{repo_owner}/{repo_name}/tree/{branch_name}"
                print(f"A new branch is created successfully. The branch address is: {branch_url}")
                return branch_url
            else:
                print(f"Failed to create the branch: {response.text}")
                raise requests.exceptions.HTTPError(response.text)
        else:
            print("Base branch reference not found.")
            raise ValueError("Base branch reference not found.")
    else:
        print(f"Failed to get base branch reference: {response.text}")
        raise requests.exceptions.HTTPError(response.text)

# For adding a temporary temp.md file to the new branch
def create_file_in_branch(repo_owner, repo_name, branch_name, access_token, file_path, file_content, commit_message):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": commit_message,
        "branch": branch_name,
        "content": base64.b64encode(file_content.encode()).decode()
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    print("A temp file is created successfully!")

# For creating a PR in the target repository and adding labels to the target PR
def create_pull_request(target_repo_owner, target_repo_name, base_branch, my_repo_owner, my_repo_name, new_branch_name, access_token, title, body, labels):
    url = f"https://api.github.com/repos/{target_repo_owner}/{target_repo_name}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "title": title,
        "body": body,
        "head": f"{my_repo_owner}:{new_branch_name}",
        "base": base_branch
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        pr_data = response.json()
        pr_url = pr_data["html_url"]
        print(f"Your target PR is created successfully. The PR address is: {pr_url}")
        url_parts = pr_url.split("/")
        pr_number = url_parts[6]
        # Add labels to the created PR
        label_url = f"https://api.github.com/repos/{target_repo_owner}/{target_repo_name}/issues/{pr_number}/labels"
        payload = labels  #  which is an array containing the labels to be added
        response_labels = requests.post(label_url, headers=headers, json=payload)
        if response_labels.status_code == 200:
            print("Labels are added successfully.")
        else:
            print("Failed to add labels.")
        return pr_url

    except requests.exceptions.HTTPError as e:
        print(f"Fails to create the target PR: {response.text}")
        raise e

# For changing the description of the translation PR
def update_pr_description(source_description):

    source_pr_CLA = "https://cla-assistant.io/pingcap/" + base_repo
    new_pr_CLA = "https://cla-assistant.io/pingcap/" + target_repo_name
    new_pr_description = source_description.replace(source_pr_CLA, new_pr_CLA)

    new_pr_description = new_pr_description.replace("This PR is translated from:", "This PR is translated from: " + source_pr_url)

    if "tips for choosing the affected versions" in source_description:
        new_pr_description = re.sub(r'.*?\[tips for choosing the affected version.*?\n\n?',"",new_pr_description)

    return new_pr_description

# For deleting temp.md
def delete_file_in_branch(repo_owner, repo_name, branch_name, access_token, file_path, commit_message):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "ref": branch_name
    }

    # Get information about the file
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        file_info = response.json()

        # Prepare the request data to delete the file
        data = {
            "message": commit_message,
            "sha": file_info["sha"],
            "branch": branch_name
        }

        # Send a request to delete a file
        try:
            response = requests.delete(url, headers=headers, params=params, json=data)
            response.raise_for_status()
            print("The temp.md is deleted successfully!")
        except requests.exceptions.HTTPError as e:
            print(f"Failed to delete temp.md. Error message: {response.text}")
            raise e
    elif response.status_code == 404:
        print(f"The temp.md file does not exist in branch {branch_name}.")
    else:
        print(f"Failed to get file information. Error message: {response.text}")

# Get the information of the source language PR
source_title, source_description, source_labels, base_repo, base_branch, head_repo, head_branch, source_pr_number = get_pr_info(source_pr_url)

# Get the repo info of my foked repository and the target repository, and the translation label
my_repo_owner = my_github_id
target_repo_owner = "pingcap"
if "pingcap/docs-cn/pull" in source_pr_url:
    my_repo_name = "docs"
    target_repo_name = "docs"
    translation_label = "translation/from-docs-cn"
elif "pingcap/docs/pull" in source_pr_url:
    target_repo_name = "docs-cn"
    my_repo_name = "docs-cn"
    translation_label = "translation/from-docs"
else:
    print ("Error: The provided URL is not a pull request of pingcap/docs-cn or pingcap/docs.")
    print("Exiting the program...")
    exit(1)

source_labels.append(translation_label)
#print ("The following labels will be reused for the translation PR.")
#print (source_labels)

# Sync from upstream
sync_my_repo_branch(target_repo_owner, target_repo_name,my_repo_owner, my_repo_name, base_branch)

# Create a new branch in the repository that I forked
new_branch_name = head_branch + "-" + source_pr_number
## print (my_repo_owner, my_repo_name, new_branch_name, base_branch )

create_branch(my_repo_owner, my_repo_name, new_branch_name, base_branch, access_token)

#  Create a temporary temp.md file in the new branch
file_path = "temp.md"
file_content = "This is a test file."
commit_message = "Add temp.md"
create_file_in_branch(my_repo_owner, my_repo_name, new_branch_name, access_token, file_path, file_content, commit_message)

# Create the target PR
title = source_title
body = update_pr_description(source_description)
labels = source_labels
create_pull_request(target_repo_owner, target_repo_name, base_branch, my_repo_owner, my_repo_name, new_branch_name, access_token, title, body, labels)

# Delete the temporary temp.md file
commit_message2 = "Delete temp.md"
delete_file_in_branch(my_repo_owner, my_repo_name, new_branch_name, access_token, file_path, commit_message2)