---
title: Self-service generation of TiDB Documentation PDF tutorial
summary: Learn how to locally customize the output of TiDB Documentation PDF that meets the needs of specific scenarios.
---

# Self-service generation of TiDB Documentation PDF tutorial

This tutorial provides a method to self-generate TiDB documents in PDF format. Through this method, you can freely sort and delete the contents of TiDB Documentation locally, and customize the output to PDF that meets the needs of specific scenarios.

## Environment preparation

The following preparations only need to be performed when generating a PDF file for the first time and can be skipped directly when generating again in the future.

### Preparation 1: Install and configure the Docker environment

> Estimated time: 30 minutes.

The following uses macOS or Windows as an example to install Docker Desktop.

1. Install [Docker Desktop](https://docs.docker.com/get-docker/)。

2. Run the `docker --version` command in macOS Terminal or Windows PowerShell.

    If you see the Docker version information, the installation is successful.

3. Configure Docker resources.

    1. Open the Docker application and click the gear icon in the upper-right corner.
    2. Click **Resources** and set **Memory** to `8.00 GB`.

4. Run the following command in macOS Terminal or Windows PowerShell to pull the Docker image used for TiDB PDF document construction:

    ```bash
    docker pull andelf/doc-build:0.1.9
    ```

### Preparation 2: Clone the TiDB Documentation repository to local

> Estimated time: 10 minutes.

TiDB Documentation in Chinese repository: <https://github.com/pingcap/docs-cn>, TiDB Documentation in English repository: <https://github.com/pingcap/docs>.

Follow the steps to clone the TiDB Documentation in English as an example:

1. Open TiDB Documentation repository: <https://github.com/pingcap/docs>。

2. Click [**Fork**](https://github.com/pingcap/docs/fork) in the upper-right corner, and wait for the Fork to complete.

3. Use any of the following methods to clone the TiDB Documentation repository locally.

    - Method 1: Use GitHub Desktop client.

        1. Install and launch [GitHub Desktop](https://desktop.github.com/).
        2. In the GitHub Desktop, click **File** > **Clone Repository**.
        3. Click the **GitHub.com** tab and select **Your Repositories**, then select the repository you forked, click **Clone** in the lower-right corner.

    - Method 2: Use the following `Git` command.

        ```shell
        cd $working_dir # Replace `$working_dir` with the directory where you want the repository to be placed. For example, `cd ~/Documents/GitHub`
        git clone git@github.com:$user/docs.git # Replace `$user` with your GitHub ID

        cd $working_dir/docs
        git remote add upstream git@github.com:pingcap/docs.git # Add upstream repository
        git remote -v
        ```

## Steps

> Estimated time: The operation only takes 2 minutes, and the PDF generation needs to wait 0.5 to 1 hour.

1. Make sure that the files in your local TiDB Documentation repository are the latest versions in the upstream GitHub repository.

2. Freely sort or delete the contents of TiDB Documentation according to your needs.

    1. Open the `TOC.md` file located in the root directory of your local repository.
    2. Edit the `TOC.md` file. For example, you can remove all unnecessary document chapters titles, and links.

3. Consolidate chapters from all documents into one Markdown file according to the `TOC.md` file.

    1. Start the Docker application.
    2. Run the following command in macOS Terminal or Windows PowerShell, to enter the Docker image for PDF document building:

        ```bash
        docker run -it -v ${doc-path}:/opt/data andelf/doc-build:0.1.9
        ```

        Among them, `${doc-path}` is the path of your local folder of the document to be generated. For example, if the path is `/Users/${username}/Documents/GitHub/docs`, the command is:

        ```bash
        docker run -it -v /Users/${username}/Documents/GitHub/docs:/opt/data andelf/doc-build:0.1.9
        ```

        After execution, if there is a warning `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested`, you can ignore it.

    3. Enter the `opt/data` directory.

        ```bash
        cd /opt/data
        ```

    4. Consolidate all Markdown document files into one `doc.md` file according to `TOC.md`.

        ```bash
        python3 scripts/merge_by_toc.py
        ```

       **Expected output:**

       In the same folder as `TOC.md`, you will see a newly generated `doc.md` file.

4. Generate document PDF:

    ```bash
    bash scripts/generate_pdf.sh
    ```

    **Expected output:**

    The time required to generate the PDF is related to the size of the document. For the complete TiDB documentation, it takes about 1 hour. After the generation is completed, you will see the newly generated PDF file `output.pdf` in the folder where the document is located.
