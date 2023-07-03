---
title: Branching GitHub Integration
summary: Learn how to use the Branching GitHub integration.
---

# Branching GitHub Integration (Beta)

> **Note:**
>
> Branching GitHub integration is based on the TiDB Serverless Branch. Make sure you are familiar with [TiDB Serverless Branch](/tidb-cloud/branch-overview.md) before you read this tutorial.

You can integrate branches into your GitHub CI/CD pipeline using the Branching GitHub Integration. It allows you to connect a GitHub repository to your TiDB serverless cluster. Then a GitHub App that manages TiDB Serverless branches will work in this repository.

The following tutorial will show you:

1. How to use the branching GitHub integration.
2. How GitHub App works.
3. How to build a branching-based CI workflow to test every pull request in a branch rather than the production cluster.

## Use the branching GitHub integration

The branching GitHub integration is used for connecting a serverless cluster to a GitHub repository. Here are the steps:

1. Navigate to the [cluster](https://tidbcloud.com/console/clusters) page and click **Branch** in the left navigation pane to go to the branch list page.

2. Click **Connect to GitHub** button.
    - If you have not logged in the GitHub, you will be asked to log in the GitHub account in a pop-up.
    - If it is the first time you use the integration, you will be asked to authorize the GitHub app in a pop-up.
    
3. Install accounts (Skip if you have installed the account)

   Click the `GitHub account` drop-down and choose the `install other account`. You will be redirected to the installation page to install accounts.

4. Select an account under the `GitHub Account` drop-down.

5. Select a repository under `GitHub Repository` drop-down. You can search the repository by name.

6. Click the `Connect` button to connect between the TiDB Serverless cluster and the GitHub repository.

## GitHub App

After you connect a TiDB serverless cluster to a GitHub repository. A [GitHub App](https://github.com/apps/tidb-cloud-branching) will work in this repository, trying to manage the TiDB Serverless branch in every pull request.

### Open a PR

GitHub App will create a TiDB Serverless branch every time you open a PR under the repository. The branch name is ${github_branch_name}_${pr_id}_${commit_sha}

### New commit in a PR

GitHub App will delete the previous branch and create a new TiDB Serverless branch for the lasted commit.

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

If set to true, TiDB Cloud App will not delete the TiDB Serverless branch which created in the previous commit.

```
github:
    branch:
       autoReserved: false
```

### branch.autoDestroy

**type:** boolean. **Default:** `true`.

If set to false, TiDB Cloud App will not delete the TiDB Serverless branch when the pull request is closed or merged.

```
github:
    branch:
       autoDestroy: true
```

## Branching CI workflow

One of the best practices of branches is building a branching CI workflow. So that you can test your code with the TiDB Serverless branch rather than the production cluster before merge the pull request. See our live demo [here](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example).

Here are the main steps:

1. Connect a TiDB serverless cluster to a GitHub repository using the branching GitHub integration.

2. Get branch connection information.

   Use [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch) action to wait for the ready of the TiDB Serverless branch and get the connection information in the GitHub action. Here is an example:
   
   ```
   steps:
     - name: Wait for TiDB Serverless branch ready
       uses: tidbcloud/wait-for-tidbcloud-branch@v0
       id: wait-for-branch
       with:
         token: ${{ secrets.GITHUB_TOKEN }}
         public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
         private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}
   
     - name: Test with TiDB Serverless branch
        run: |
           echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
           echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
           echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
   ```

3. Adjust your test code.

   Adjust your test code to accept the connection information from GitHub action. For example, accept the connection information by the environment as our live demo does.

## What's next

You can also build your branching CI/CD workflow without our branching GitHub integration. For example, using GitHub action to custom CI/CD workflows by our [tidbcloud-cli](https://github.com/tidbcloud/setup-tidbcloud-cli).
