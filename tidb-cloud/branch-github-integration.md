---
title: Branch GitHub Integration
summary: Learn how use the Branch GitHub integration.
---

# Branch GitHub Integration

TiDB Cloud Branch provides a GitHub integration to connect a GitHub repository to your TiDB Cloud serverless cluster. After that, a GitHub App that manage TiDB Cloud branches will be installed in this repository.

The following tutorial will show how to use the GitHub integration.

## Before you start

Before you start, make sure you:

- Familiar with [TiDB Cloud branches](./branch-overview.md)
- Have a TiDB Cloud account and a serverless cluster
- Have a GitHub account and a repository

## Connect serverless cluster to GitHub repository

You can connect a serverless cluster to a GitHub repository by the GitHub integration.

1. Go to the branch page on the TiDB Cloud console, and click **Connect** button.
    - If you have not logged in the GitHub, you will be asked to log in the GitHub account in a pop-up.
    - If it is the first time you use the integration, you will be asked to authorize the GitHub app in a pop-up.

picture

2. Install an account

   Skip if you have installed the account. Click the `GitHub account` and choose the `install other account`, you will be redirected to an installation page to install the account.

picture

3. Select an account

    After you have installed your account, it will be shown under the GitHub account drop-down. Select the account you need.

picture

4. Select a repository under the account

   Choose a repository under the account you selected.

picture

5. Connect

   Click the `Connect` button to connect between the TiDB Cloud cluster and The GitHub repository.

picture

## GitHub App

After you connect a TiDB Cloud serverless cluster to a GitHub repository. A [GitHub App](https://github.com/apps/tidb-cloud-branching) will work in this repository, trying to manage TiDB Cloud branch in every PR.

### Open a PR

GitHub App will create a TiDB Cloud branch every time you open a PR under the repository. The branch name is ${github_branch_name}_${pr_id}_${commit_sha}

### New commit in a PR

GitHub App will delete the previous branch and create a new TiDB Cloud Branch for the lasted commit.

### Close or merge a PR

GitHub App will delete all the branches in this PR.

### Reopen a PR

GitHub App will create a branch for the lasted commit.

## Configuring GitHub App

The following configuration options can be used through a tidbcloud.yml file in the root of your repository.

### branch.blackList

**type:** Array of string. **Default:** `[]`.

Specify the branches that forbid the GitHub App, even if it is in the whiteList.

```
github:
    branch:
       blackList:
           - ".*_doc"
           - ".*_blackList"
```

### branch.whiteList

**type:** Array of string. **Default:** `[.*]`.

Specify the branches that allow the GitHub App.

```
github:
    branch:
       whiteList: 
           - ".*_db"
```

### branch.autoReserved

**type:** boolean. **Default:** `false`.

If set to true, TiDB Cloud App will not delete the TiDB Cloud branch which created in the previous commit.

```
github:
    branch:
       autoReserved: false
```

### branch.autoDestroy

**type:** boolean. **Default:** `true`.

If set to false, TiDB Cloud App will not delete the TiDB Cloud branch when the pull request is closed or merged.

```
github:
    branch:
       autoDestroy: true
```

## Branching workflow

You can do a lot with GitHub integration. One of the best practices is building a branching workflow on GitHub, it will test your code with TiDB Cloud branch rather than the production cluster in every PR. See our live demo [here](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)

1. Connected a TiDB Cloud serverless cluster to a GitHub repository by the GitHub integration.

2. Wait for the TiDB Cloud branch

   Use [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch) action to wait for the ready of the TiDB Cloud branch and get the connection information in the GitHub action. Here is an example:
   
   ```
   steps:
     - name: Wait for TiDB Cloud branch ready
       uses: tidbcloud/wait-for-tidbcloud-branch@v0
       id: wait-for-branch
       with:
         token: ${{ secrets.GITHUB_TOKEN }}
         public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
         private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}
   
     - name: Test with TiDB Cloud branch
        run: |
           echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
           echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
           echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
   ```

3. Accept the connection information

   Adjust your code to accept the connection information from GitHub action. For example, accept the connection information by environment just like our live demo.

   
