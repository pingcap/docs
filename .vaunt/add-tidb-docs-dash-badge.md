# How to Add TiDB Docs Dash Badges to your GitHub Profile

Your [GitHub profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile) is more than just a collection of repositories; it is your professional identity in the coding world.

This guide walks you through the steps of adding [TiDB Docs Dash 2024](https://www.pingcap.com/event/tidb-docs-dash/) badges to your GitHub profile.

## Step 1. Create a repository for your profile README

If you have already set up your GitHub profile README, skip the following and go to [Step 2. Edit your profile README](#step-2-edit-your-profile-readme).

1. In the upper-right corner of any GitHub page, click **+**, and then click **New repository**.

    <img src="https://docs.github.com/assets/cb-34248/mw-1440/images/help/repository/repo-create-global-nav-update.webp" width="350" />

2. Type a repository name that matches your GitHub username. For example, if your username is `ilovetidb`, the repository name must be `ilovetidb`.
3. Choose **Public** for the repository visibility.
4. Select **Initialize this repository with a README file**.
5. Click **Create repository**.

### Editing a Profile README

#### Edit Your README

- After creating the repository, click on "Edit README" above the right sidebar
- Your README file is now open for editing

#### Integrate the Achievement Card

<img src="1st_place.png" alt="1st place achievement" width="200"/>

- Add this code to your README file and replace `{{github_username}}` with your username

```HTML
<p>
  <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/achievements?format=svg&limit=3" width="350" />
</p>
```

#### Integrate the Vaunt Developer Card (Optional)

<p>
    <a href="https://vaunt.dev">
        <img src="https://api.vaunt.dev/v1/github/entities/jeff1010322/contributions?format=svg" width="350" />
    </a>
</p>

Add this code to your README file and replace `{{github_username}}` with your username

```HTML
<p>
    <a href="https://vaunt.dev">
        <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/contributions?format=svg" width="350" />
    </a>
</p>
```

#### Integrate Community Boards (Optional)

[![VauntCommunity](https://api.vaunt.dev/v1/github/entities/pingcap/badges/community)](https://community.vaunt.dev/board/pingcap)

Take collaboration to the next level by integrating Vaunt's Community Board.

- Explore [Your Own Community Boards](https://community.vaunt.dev/)
- Add this code to your README file and replace `{{github_username}}` with your username

```Markdown
[![VauntCommunity](https://api.vaunt.dev/v1/github/entities/{{github_username}}/badges/community)](https://community.vaunt.dev/board/{{github_username}})
```

### Commit Changes

- Once you've added Vaunt elements to your README, scroll up and commit the changes directly from GitHub.

Your GitHub profile now proudly displays a dynamic Developer Card and Community Board, offering a snapshot of your contributions and achievements.

## Install Vaunt on GitHub Marketplace

By integrating Vaunt into your README, you're not just showcasing your code; you're telling the story of your coding journey.
Unlock the full potential of your GitHub profile with Vaunt and make your mark in the open-source community.

[Install Vaunt](https://github.com/marketplace/vaunt-dev) today and start showcasing more of your contributions!

**TIP**

We recommend installing Vaunt on all owned repositories.
This ensures that your contributions are counted accurately.
That said, by default all public contributions will be counted.
