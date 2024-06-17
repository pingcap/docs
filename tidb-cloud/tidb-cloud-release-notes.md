---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2023

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2023.

## December 5, 2023

**General changes**

- [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) enables you to resume a failed changefeed, which saves your effort to recreate a new one.

    For more information, see [Changefeed states](/tidb-cloud/changefeed-overview.md#changefeed-states).

**Console changes**

- Enhance the connection experience for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless).

    Refine the **Connect** dialog interface to offer TiDB Serverless users a smoother and more efficient connection experience. In addition, TiDB Serverless introduces more client types and allows you to select the desired branch for connection.

    For more information, see [Connect to TiDB Serverless](/tidb-cloud/connect-via-standard-connection-serverless.md).

## November 28, 2023

**General changes**

- [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) supports restoring SQL bindings from backups.

    TiDB Dedicated now restores user accounts and SQL bindings by default when restoring from a backup. This enhancement is available for clusters of v6.2.0 or later versions, streamlining the data restoration process. The restoration of SQL bindings ensures the smooth reintegration of query-related configurations and optimizations, providing you with a more comprehensive and efficient recovery experience.

    For more information, see [Back up and restore TiDB Dedicated data](/tidb-cloud/backup-and-restore.md).

**Console changes**

- [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) supports monitoring SQL statement RU costs.

    TiDB Serverless now provides detailed insights into each SQL statement's [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit). You can view both the **Total RU** and **Mean RU** costs per SQL statement. This feature helps you identify and analyze RU costs, offering opportunities for potential cost savings in your operations.

    To check your SQL statement RU details, navigate to the **Diagnosis** page of [your TiDB Serverless cluster](https://tidbcloud.com/console/clusters) and then click the **SQL Statement** tab.

## November 21, 2023

**General changes**

- [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) supports high-speed physical mode for TiDB clusters deployed on Google Cloud.

    Now you can use physical mode for TiDB clusters deployed on AWS and Google Cloud. The migration speed of physical mode can reach up to 110 MiB/s, which is 2.4 times faster than logical mode. The improved performance is suitable for quickly migrating large datasets to TiDB Cloud.

    For more information, see [Migrate existing data and incremental data](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data).

## November 14, 2023

**General changes**

- When you restore data from TiDB Dedicated clusters, the default behavior is now modified from restoring without user accounts to restoring with all user accounts.

    For more information, see [Back Up and Restore TiDB Dedicated Data](/tidb-cloud/backup-and-restore.md).

- Introduce event filters for changefeeds.

    This enhancement empowers you to easily manage event filters for changefeeds directly through the [TiDB Cloud console](https://tidbcloud.com/), streamlining the process of excluding specific events from changefeeds and providing better control over data replication downstream.

    For more information, see [Changefeed](/tidb-cloud/changefeed-overview.md#edit-a-changefeed).

## November 7, 2023

**General changes**

- Add the following resource usage alerts. The new alerts are disabled by default. You can enable them as needed.

    - Max memory utilization across TiDB nodes exceeded 70% for 10 minutes
    - Max memory utilization across TiKV nodes exceeded 70% for 10 minutes
    - Max CPU utilization across TiDB nodes exceeded 80% for 10 minutes
    - Max CPU utilization across TiKV nodes exceeded 80% for 10 minutes

  For more information, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md#resource-usage-alerts).

## October 31, 2023

**General changes**

- Support directly upgrading to the Enterprise support plan in the TiDB Cloud console without contacting sales.

    For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## October 25, 2023

**General changes**

- [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) supports dual region backup (beta) on Google Cloud.

    TiDB Dedicated clusters hosted on Google Cloud work seamlessly with Google Cloud Storage. Similar to the [Dual-regions](https://cloud.google.com/storage/docs/locations#location-dr) feature of Google Cloud Storage, the pair of regions that you use for the dual-region in TiDB Dedicated must be within the same multi-region. For example, Tokyo and Osaka are in the same multi-region `ASIA` so they can be used together for dual-region storage.

    For more information, see [Back Up and Restore TiDB Dedicated Data](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup-beta).

- The feature of [streaming data change logs to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) is now in General Availability (GA).

    After a successful 10-month beta trial, the feature of streaming data change logs from TiDB Cloud to Apache Kafka becomes generally available. Streaming data from TiDB to a message queue is a common need in data integration scenarios. You can use Kafka sink to integrate with other data processing systems (such as Snowflake) or support business consumption.

    For more information, see [Changefeed overview](/tidb-cloud/changefeed-overview.md).

## October 11, 2023

**General changes**

- Support [dual region backup (beta)](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup-beta) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters deployed on AWS.

    You can now replicate backups across geographic regions within your cloud provider. This feature provides an additional layer of data protection and disaster recovery capabilities.

    For more information, see [Back up and restore TiDB Dedicated data](/tidb-cloud/backup-and-restore.md).

- Data Migration now supports both physical mode and logical mode for migrating existing data.

    In physical mode, the migration speed can reach up to 110 MiB/s. Compared with 45 MiB/s in logical mode, the migration performance has improved significantly.

    For more information, see [Migrate existing data and incremental data](/tidb-cloud/migrate-from-mysql-using-data-migration.md#migrate-existing-data-and-incremental-data).

## October 10, 2023

**General changes**

- Support using TiDB Serverless branches in [Vercel Preview Deployments](https://vercel.com/docs/deployments/preview-deployments), with TiDB Cloud Vercel integration.

    For more information, see [Connect with TiDB Serverless branching](/tidb-cloud/integrate-tidbcloud-with-vercel.md#connect-with-tidb-serverless-branching).

## September 28, 2023

**API changes**

- Introduce a TiDB Cloud Billing API endpoint to retrieve the bill for the given month of a specific organization. 

    This Billing API endpoint is released in TiDB Cloud API v1beta1, which is the latest API version of TiDB Cloud. For more information, refer to the [API documentation (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1#tag/Billing).

## September 19, 2023

**General changes**

- Remove 2 vCPU TiDB and TiKV nodes from [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    The 2 vCPU option is no longer available on the **Create Cluster** page or the **Modify Cluster** page.

- Release [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md) for JavaScript.

    TiDB Cloud serverless driver for JavaScript allows you to connect to your [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster over HTTPS. It is particularly useful in edge environments where TCP connections are limited, such as [Vercel Edge Function](https://vercel.com/docs/functions/edge-functions) and [Cloudflare Workers](https://workers.cloudflare.com/).

    For more information, see [TiDB Cloud serverless driver (beta)](/tidb-cloud/serverless-driver.md).

**Console changes**

- For [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, you can get an estimation of cost in the **Usage This Month** panel or while setting up the spending limit.

## September 5, 2023

**General changes**

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports customizing the rate limit for each API key to meet specific rate-limiting requirements in different situations.

    You can adjust the rate limit of an API key when you [create](/tidb-cloud/data-service-api-key.md#create-an-api-key) or [edit](/tidb-cloud/data-service-api-key.md#edit-an-api-key) the key.

    For more information, see [Rate limiting](/tidb-cloud/data-service-api-key.md#rate-limiting).

- Support a new AWS region for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters: São Paulo (sa-east-1).

- Support adding up to 100 IP addresses to the IP access list for each [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) cluster.

    For more information, see [Configure an IP access list](/tidb-cloud/configure-ip-access-list.md).

**Console changes**

- Introduce the **Events** page for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, which provides the records of main changes to your cluster.

    On this page, you can view the event history for the last 7 days and track important details such as the trigger time and the user who initiated an action.

    For more information, see [TiDB Cloud cluster events](/tidb-cloud/tidb-cloud-events.md).

**API changes**

- Release several TiDB Cloud API endpoints for managing the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) or [Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters:

    - Create a private endpoint service for a cluster
    - Retrieve the private endpoint service information of a cluster
    - Create a private endpoint for a cluster
    - List all private endpoints of a cluster
    - List all private endpoints in a project
    - Delete a private endpoint of a cluster

  For more information, refer to the [API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster).

## August 23, 2023

**General changes**

- Support Google Cloud [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    You can now create a private endpoint and establish a secure connection to a TiDB Dedicated cluster hosted on Google Cloud.

    Key benefits:

    - Intuitive operations: helps you create a private endpoint with only several steps.
    - Enhanced security: establishes a secure connection to protect your data.
    - Improved performance: provides low-latency and high-bandwidth connectivity.

  For more information, see [Connect via Private Endpoint with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

- Support using a changefeed to stream data from a [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) cluster to [Google Cloud Storage (GCS)](https://cloud.google.com/storage).

    You can now stream data from TiDB Cloud to GCS by using your own account's bucket and providing precisely tailored permissions. After replicating data to GCS, you can analyze the changes in your data as you wish.

    For more information, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

## August 15, 2023

**General changes**

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports pagination for `GET` requests to improve the development experience.

    For `GET` requests, you can paginate results by enabling **Pagination** in **Advance Properties** and specifying `page` and `page_size` as query parameters when calling the endpoint. For example, to get the second page with 10 items per page, you can use the following command:

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>?page=2&page_size=10'
    ```

    Note that this feature is available only for `GET` requests where the last query is a `SELECT` statement.

    For more information, see [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint).

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports caching endpoint response of `GET` requests for a specified time-to-live (TTL) period.

    This feature decreases database load and optimizes endpoint latency.

    For an endpoint using the `GET` request method, you can enable **Cache Response** and configure the TTL period for the cache in **Advance Properties**.

    For more information, see [Advanced properties](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties).

- Disable the load balancing improvement for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters that are hosted on AWS and created after August 15, 2023, including:

    - Disable automatically migrating existing connections to new TiDB nodes when you scale out TiDB nodes hosted on AWS.
    - Disable automatically migrating existing connections to available TiDB nodes when you scale in TiDB nodes hosted on AWS.

  This change avoids resource contention of hybrid deployments and does not affect existing clusters with this improvement enabled. If you want to enable the load balancing improvement for your new clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## August 8, 2023

**General changes**

- [Data Service (beta)](https://tidbcloud.com/console/data-service) now supports Basic Authentication.

    You can provide your public key as the username and private key as the password in requests using the ['Basic' HTTP Authentication](https://datatracker.ietf.org/doc/html/rfc7617). Compared with Digest Authentication, the Basic Authentication is simpler, enabling more straightforward usage when calling Data Service endpoints.

    For more information, see [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint).

## August 1, 2023

**General changes**

- Support the OpenAPI Specification for Data Apps in TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service).

    TiDB Cloud Data Service provides autogenerated OpenAPI documentation for each Data App. In the documentation, you can view the endpoints, parameters, and responses, and try out the endpoints.

    You can also download an OpenAPI Specification (OAS) for a Data App and its deployed endpoints in YAML or JSON format. The OAS provides standardized API documentation, simplified integration, and easy code generation, which enables faster development and improved collaboration.

    For more information, see [Use the OpenAPI Specification](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification) and [Use the OpenAPI Specification with Next.js](/tidb-cloud/data-service-oas-with-nextjs.md).

- Support running Data App in [Postman](https://www.postman.com/).

    The Postman integration empowers you to import a Data App's endpoints as a collection into your preferred workspace. Then you can benefit from enhanced collaboration and seamless API testing with support for both Postman web and desktop apps.

    For more information, see [Run Data App in Postman](/tidb-cloud/data-service-postman-integration.md).

- Introduce a new **Pausing** status for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, allowing cost-effective pauses with no charges during this period.

    When you click **Pause** for a TiDB Dedicated cluster, the cluster will enter the **Pausing** status first. Once the pause operation is completed, the cluster status will transition to **Paused**.

    A cluster can only be resumed after its status transitions to **Paused**, which resolves the abnormal resumption issue caused by rapid clicks of **Pause** and **Resume**.

    For more information, see [Pause or resume a TiDB Dedicated cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md).

## July 26, 2023

**General changes**

- Introduce a powerful feature in TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service): Automatic endpoint generation.

    Developers can now effortlessly create HTTP endpoints with minimal clicks and configurations. Eliminate repetitive boilerplate code, simplify and accelerate endpoint creation, and reduce potential errors.

    For more information on how to use this feature, see [Generate an endpoint automatically](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically).

- Support `PUT` and `DELETE` request methods for endpoints in TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service).

    - Use the `PUT` method to update or modify data, similar to an `UPDATE` statement.
    - Use the `DELETE` method to delete data, similar to a `DELETE` statement.

  For more information, see [Configure properties](/tidb-cloud/data-service-manage-endpoint.md#configure-properties).

- Support **Batch Operation** for `POST`, `PUT`, and `DELETE` request methods in TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service).

    When **Batch Operation** is enabled for an endpoint, you gain the ability to perform operations on multiple rows in a single request. For instance, you can insert multiple rows of data using a single `POST` request.

    For more information, see [Advanced properties](/tidb-cloud/data-service-manage-endpoint.md#advanced-properties).

## July 25, 2023

**General changes**

- Upgrade the default TiDB version of new [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3) to [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1).

**Console changes**

- Simplify access to PingCAP Support for TiDB Cloud users by optimizing support entries. Improvements include:

    - Add an entrance for **Support** in the <MDSvgIcon name="icon-top-organization" /> in the lower-left corner.
    - Revamp the menus of the **?** icon in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com/) to make them more intuitive.

  For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## July 18, 2023

**General changes**

- Refine role-based access control at both the organization level and project level, which lets you grant roles with minimum permissions to users for better security, compliance, and productivity.

    - The organization roles include `Organization Owner`, `Organization Billing Admin`, `Organization Console Audit Admin`, and `Organization Member`.
    - The project roles include `Project Owner`, `Project Data Access Read-Write`, and `Project Data Access Read-Only`.
    - To manage clusters in a project (such as cluster creation, modification, and deletion), you need to be in the `Organization Owner` or `Project Owner` role.

  For more information about permissions of different roles, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

- Support the Customer-Managed Encryption Key (CMEK) feature (beta) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted on AWS.

    You can create CMEK based on AWS KMS to encrypt data stored in EBS and S3 directly from the TiDB Cloud console. This ensures that customer data is encrypted with a key managed by the customer, which enhances security.

    Note that this feature still has restrictions and is only available upon request. To apply for this feature, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

- Optimize the Import feature in TiDB Cloud, aimed at enhancing the data import experience. The following improvements have been made:

    - Unified Import entry for TiDB Serverless: consolidate the entries for importing data, allowing you to seamlessly switch between importing local files and importing files from Amazon S3.
    - Streamlined configuration: importing data from Amazon S3 now only requires a single step, saving time and effort.
    - Enhanced CSV configuration: the CSV configuration settings are now located under the file type option, making it easier for you to quickly configure the necessary parameters.
    - Enhanced target table selection: support choosing the desired target tables for data import by clicking checkboxes. This improvement eliminates the need for complex expressions and simplifies the target table selection.
    - Refined display information: resolve issues related to inaccurate information displayed during the import process. In addition, the Preview feature has been removed to prevent incomplete data display and avoid misleading information.
    - Improved source files mapping: support defining mapping relationships between source files and target tables. It addresses the challenge of modifying source file names to meet specific naming requirements.

## July 11, 2023

**General changes**

- [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) now is Generally Available.

- Introduce TiDB Bot (beta), an OpenAI-powered chatbot that offers multi-language support, 24/7 real-time response, and integrated documentation access.

    TiDB Bot provides you with the following benefits:

    - Continuous support: always available to assist and answer your questions for an enhanced support experience.
    - Improved efficiency: automated responses reduce latency, improving overall operations.
    - Seamless documentation access: direct access to TiDB Cloud documentation for easy information retrieval and quick issue resolution.

  To use TiDB Bot, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and select **Ask TiDB Bot** to start a chat.

- Support [the branching feature (beta)](/tidb-cloud/branch-overview.md) for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    TiDB Cloud lets you create branches for TiDB Serverless clusters. A branch for a cluster is a separate instance that contains a diverged copy of data from the original cluster. It provides an isolated environment, allowing you to connect to it and experiment freely without worrying about affecting the original cluster.

    You can create branches for TiDB Serverless clusters created after July 5, 2023 by using either [TiDB Cloud console](/tidb-cloud/branch-manage.md) or [TiDB Cloud CLI](/tidb-cloud/ticloud-branch-create.md).

    If you use GitHub for application development, you can integrate TiDB Serverless branching into your GitHub CI/CD pipeline, which lets you automatically test your pull requests with branches without affecting the production database. For more information, see [Integrate TiDB Serverless Branching (Beta) with GitHub](/tidb-cloud/branch-github-integration.md).

- Support weekly backup for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters. For more information, see [Back up and restore TiDB Dedicated data](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup).

## July 4, 2023

**General changes**

- Support point-in-time recovery (PITR) (beta) for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    You can now restore your TiDB Serverless cluster to any point in time within the last 90 days. This feature enhances the data recovery capability of TiDB Serverless clusters. For example, you can use PITR when data write errors occur and you want to restore the data to an earlier state.

    For more information, see [Back up and restore TiDB Serverless data](/tidb-cloud/backup-and-restore-serverless.md#restore).

**Console changes**

- Enhance the **Usage This Month** panel on the cluster overview page for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters to provide a clearer view of your current resource usage.

- Enhance the overall navigation experience by making the following changes:

    - Consolidate <MDSvgIcon name="icon-top-organization" /> **Organization** and <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner into the left navigation bar.
    - Consolidate <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin** in the left navigation bar into <MDSvgIcon name="icon-left-projects" /> **Project** in the left navigation bar, and remove the ☰ hover menu in the upper-left corner. Now you can click <MDSvgIcon name="icon-left-projects" /> to switch between projects and modify project settings.
    - Consolidate all the help and support information for TiDB Cloud into the menu of the **?** icon in the lower-right corner, such as documentation, interactive tutorials, self-paced training, and support entries.

- TiDB Cloud console now supports Dark Mode, which provides a more comfortable, eye-friendly experience. You can switch between light mode and dark mode from the bottom of the left navigation bar.

## June 27, 2023

**General changes**

- Remove the pre-built sample dataset for newly created [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## June 20, 2023

**General changes**

- Upgrade the default TiDB version of new [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2) to [v6.5.3](https://docs.pingcap.com/tidb/v6.5/release-6.5.3).

## June 13, 2023

**General changes**

- Support using changefeeds to stream data to Amazon S3.

    This enables seamless integration between TiDB Cloud and Amazon S3. It allows real-time data capture and replication from [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters to Amazon S3, ensuring that downstream applications and analytics have access to up-to-date data.

    For more information, see [Sink to cloud storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

- Increase the maximum node storage of 16 vCPU TiKV for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from 4 TiB to 6 TiB.

    This enhancement increases the data storage capacity of your TiDB Dedicated cluster, improves workload scaling efficiency, and accommodates growing data requirements.

    For more information, see [Size your cluster](/tidb-cloud/size-your-cluster.md).

- Extend the [monitoring metrics retention period](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters from 3 days to 7 days.

    By extending the metrics retention period, now you have access to more historical data. This helps you identify trends and patterns of the cluster for better decision-making and faster troubleshooting.

**Console changes**

- Release a new native web infrastructure for the [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) page of [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    With the new infrastructure, you can easily navigate through the **Key Visualizer** page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the SQL diagnosis process more user-friendly.

## June 6, 2023

**General changes**

- Introduce [Index Insight (beta)](/tidb-cloud/index-insight.md) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, which optimizes query performance by providing index recommendations for slow queries.

    With Index Insight, you can improve the overall application performance and efficiency of your database operations in the following ways:

    - Enhanced query performance: Index Insight identifies slow queries and suggests appropriate indexes for them, thereby speeding up query execution, reducing response time, and improving user experience.
    - Cost efficiency: By using Index Insight to optimize query performance, the need for extra computing resources is reduced, enabling you to use existing infrastructure more effectively. This can potentially lead to operational cost savings.
    - Simplified optimization process: Index Insight simplifies the identification and implementation of index improvements, eliminating the need for manual analysis and guesswork. As a result, you can save time and effort with accurate index recommendations.
    - Improved application efficiency: By using Index Insight to optimize database performance, applications running on TiDB Cloud can handle larger workloads and serve more users concurrently, which makes scaling operations of applications more efficient.

  To use Index Insight, navigate to the **Diagnosis** page of your TiDB Dedicated cluster and click the **Index Insight BETA** tab.

    For more information, see [Use Index Insight (beta)](/tidb-cloud/index-insight.md).

- Introduce [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes), an interactive platform for experiencing the full capabilities of TiDB, without registration or installation.

    TiDB Playground is an interactive platform designed to provide a one-stop-shop experience for exploring the capabilities of TiDB, such as scalability, MySQL compatibility, and real-time analytics.

    With TiDB Playground, you can try out TiDB features in a controlled environment free from complex configurations in real-time, making it ideal to understand the features in TiDB.

    To get started with TiDB Playground, go to the [**TiDB Playground**](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_release_notes) page, select a feature you want to explore, and begin your exploration.

## June 5, 2023

**General changes**

- Support connecting your [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) to GitHub.

    By [connecting your Data App to GitHub](/tidb-cloud/data-service-manage-github-connection.md), you can manage all configurations of the Data App as [code files](/tidb-cloud/data-service-app-config-files.md) on Github, which integrates TiDB Cloud Data Service seamlessly with your system architecture and DevOps process.

    With this feature, you can easily accomplish the following tasks, which improves the CI/CD experience of developing Data Apps:

    - Automatically deploy Data App changes with GitHub.
    - Configure CI/CD pipelines of your Data App changes on GitHub with version control.
    - Disconnect from a connected GitHub repository.
    - Review endpoint changes before the deployment.
    - View deployment history and take necessary actions in the event of a failure.
    - Re-deploy a commit to roll back to an earlier deployment.

  For more information, see [Deploy Data App automatically with GitHub](/tidb-cloud/data-service-manage-github-connection.md).

## June 2, 2023

**General changes**

- In our pursuit to simplify and clarify, we have updated the names of our products:

    - "TiDB Cloud Serverless Tier" is now called "TiDB Serverless".
    - "TiDB Cloud Dedicated Tier" is now called "TiDB Dedicated".
    - "TiDB On-Premises" is now called "TiDB Self-Hosted".

    Enjoy the same great performance under these refreshed names. Your experience is our priority.

## May 30, 2023

**General changes**

- Enhance support for incremental data migration for the Data Migration feature in TiDB Cloud.

    You can now specify a binlog position or a global transaction identifier (GTID) to replicate only incremental data generated after the specified position to TiDB Cloud. This enhancement empowers you with greater flexibility to select and replicate the data you need, aligning with your specific requirements.

    For details, refer to [Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

- Add a new event type (`ImportData`) to the [**Events**](/tidb-cloud/tidb-cloud-events.md) page.

- Remove **Playground** from the TiDB Cloud console.

    Stay tuned for the new standalone Playground with an optimized experience.

## May 23, 2023

**General changes**

- When uploading a CSV file to TiDB, you can use not only English letters and numbers, but also characters such as Chinese and Japanese to define column names. However, for special characters, only underscore (`_`) is supported.

    For details, refer to [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md).

## May 16, 2023

**Console changes**

- Introduce the left navigation entries organized by functional categories for both Dedicated and Serverless tiers.

    The new navigation makes it easier and more intuitive for you to discover the feature entries. To view the new navigation, access the overview page of your cluster.

- Release a new native web infrastructure for the following two tabs on the **Diagnosis** page of Dedicated Tier clusters.

    - [Slow Query](/tidb-cloud/tune-performance.md#slow-query)
    - [SQL Statement](/tidb-cloud/tune-performance.md#statement-analysis)

    With the new infrastructure, you can easily navigate through the two tabs and access the necessary information in a more intuitive and efficient manner. The new infrastructure also improves user experience, making the SQL diagnosis process more user-friendly.

## May 9, 2023

**General changes**

- Support changing node sizes for GCP-hosted clusters created after April 26, 2023.

    With this feature, you can upgrade to higher-performance nodes for increased demand or downgrade to lower-performance nodes for cost savings. With this added flexibility, you can adjust your cluster's capacity to align with your workloads and optimize costs.

    For detailed steps, see [Change node size](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram).

- Support importing compressed files. You can import CSV and SQL files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst`, and `.snappy`. This feature provides a more efficient and cost-effective way to import data and reduces your data transfer costs.

    For more information, see [Import CSV Files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-csv-files.md) and [Import Sample Data](/tidb-cloud/import-sample-data.md).

- Support AWS PrivateLink-powered endpoint connection as a new network access management option for TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    The private endpoint connection does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

    For more information, see [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md).

**Console changes**

- Add new event types to the [**Event**](/tidb-cloud/tidb-cloud-events.md) page to record backup, restore, and changefeed actions for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    To get a full list of the events that can be recorded, see [Logged events](/tidb-cloud/tidb-cloud-events.md#logged-events).

- Introduce the **SQL Statement** tab on the [**SQL Diagnosis**](/tidb-cloud/tune-performance.md) page for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    The **SQL Statement** tab provides the following:

    - A comprehensive overview of all SQL statements executed by your TiDB database, allowing you to easily identify and diagnose slow queries.
    - Detailed information on each SQL statement, such as the query time, execution plan, and the database server response, helping you optimize your database performance.
    - A user-friendly interface that makes it easy to sort, filter, and search through large amounts of data, enabling you to focus on the most critical queries.

  For more information, see [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis).

## May 6, 2023

**General changes**

- Support directly accessing the [Data Service endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint) in the region where a TiDB [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster is located.

    For newly created Serverless Tier clusters, the endpoint URL now includes the cluster region information. By requesting the regional domain `<region>.data.tidbcloud.com`, you can directly access the endpoint in the region where the TiDB cluster is located.

    Alternatively, you can also request the global domain `data.tidbcloud.com` without specifying a region. In this way, TiDB Cloud will internally redirect the request to the target region, but this might result in additional latency. If you choose this way, make sure to add the `--location-trusted` option to your curl command when calling an endpoint.

    For more information, see [Call an endpoint](/tidb-cloud/data-service-manage-endpoint.md#call-an-endpoint).

## April 25, 2023

**General changes**

- For the first five [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

    - Row storage: 5 GiB
    - [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

  Until May 31, 2023, Serverless Tier clusters are still free, with a 100% discount off. After that, usage beyond the free quota will be charged.

    You can easily [monitor your cluster usage or increase your usage quota](/tidb-cloud/manage-serverless-spend-limit.md#manage-spending-limit-for-tidb-serverless-clusters) in the **Usage This Month** area of your cluster **Overview** page. Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you increase the quota or the usage is reset upon the start of a new month.

    For more information about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Cloud Serverless Tier Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

- Support backup and restore for TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

     For more information, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore-serverless.md).

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1) to [v6.5.2](https://docs.pingcap.com/tidb/v6.5/release-6.5.2).

- Provide a maintenance window feature to enable you to easily schedule and manage planned maintenance activities for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    A maintenance window is a designated timeframe during which planned maintenance activities, such as operating system updates, security patches, and infrastructure upgrades, are performed automatically to ensure the reliability, security, and performance of the TiDB Cloud service.

    During a maintenance window, temporary connection disruptions or QPS fluctuations might occur, but the clusters remain available, and SQL operations, the existing data import, backup, restore, migration, and replication tasks can still run normally. See [a list of allowed and disallowed operations](/tidb-cloud/configure-maintenance-window.md#allowed-and-disallowed-operations-during-a-maintenance-window) during maintenance.

    We will strive to minimize the frequency of maintenance. If a maintenance window is planned, the default start time is 03:00 Wednesday (based on the time zone of your TiDB Cloud organization) of the target week. To avoid potential disruptions, it is important to be aware of the maintenance schedules and plan your operations accordingly.

    - To keep you informed, TiDB Cloud will send you three email notifications for every maintenance window: one before, one starting, and one after the maintenance tasks.
    - To minimize the maintenance impact, you can modify the maintenance start time to your preferred time or defer maintenance activities on the **Maintenance** page.

  For more information, see [Configure maintenance window](/tidb-cloud/configure-maintenance-window.md).

- Improve load balancing of TiDB and reduce connection drops when you scale TiDB nodes of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters that are hosted on AWS and created after April 25, 2023.

    - Support automatically migrating existing connections to new TiDB nodes when you scale out TiDB nodes.
    - Support automatically migrating existing connections to available TiDB nodes when you scale in TiDB nodes.

  Currently, this feature is provided for all Dedicated Tier clusters hosted on AWS.

**Console changes**

- Release a new native web infrastructure for the [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    With the new infrastructure, you can easily navigate through the [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the monitoring process more user-friendly.

## April 18, 2023

**General changes**

- Support scaling up or down [Data Migration job specifications](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration) for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    With this feature, you can improve migration performance by scaling up specifications or reduce costs by scaling down specifications.

    For more information, see [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md#scale-a-migration-job-specification).

**Console changes**

- Revamp the UI to make [cluster creation](https://tidbcloud.com/console/clusters/create-cluster) experience more user-friendly, enabling you to create and configure clusters with just a few clicks.

    The new design focuses on simplicity, reducing visual clutter, and providing clear instructions. After clicking **Create** on the cluster creation page, you will be directed to the cluster overview page without having to wait for the cluster creation to be completed.

    For more information, see [Create a cluster](/tidb-cloud/create-tidb-cluster.md).

- Introduce the **Discounts** tab on the **Billing** page to show the discount information for organization owners and billing administrators.

    For more information, see [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts).

## April 11, 2023

**General changes**

- Improve the load balance of TiDB and reduce connection drops when you scale TiDB nodes of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted on AWS.

    - Support automatically migrating existing connections to new TiDB nodes when you scale out TiDB nodes.
    - Support automatically migrating existing connections to available TiDB nodes when you scale in TiDB nodes.

  Currently, this feature is only provided for Dedicated Tier clusters that are hosted on the AWS `Oregon (us-west-2)` region.

- Support the [New Relic](https://newrelic.com/) integration for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

    With the New Relic integration, you can configure TiDB Cloud to send metric data of your TiDB clusters to [New Relic](https://newrelic.com/). Then, you can monitor and analyze both your application performance and your TiDB database performance on [New Relic](https://newrelic.com/). This feature can help you quickly identify and troubleshoot potential issues and reduce the resolution time.

    For integration steps and available metrics, see [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md).

- Add the following [changefeed](/tidb-cloud/changefeed-overview.md) metrics to the Prometheus integration for Dedicated Tier clusters.

    - `tidbcloud_changefeed_latency`
    - `tidbcloud_changefeed_replica_rows`

    If you have [integrated TiDB Cloud with Prometheus](/tidb-cloud/monitor-prometheus-and-grafana-integration.md), you can monitor the performance and health of changefeeds in real time using these metrics. Additionally, you can easily create alerts to monitor the metrics using Prometheus.

**Console changes**

- Update the [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters to use [node-level resource metrics](/tidb-cloud/built-in-monitoring.md#server).

    With node-level resource metrics, you can see a more accurate representation of resource consumption to better understand the actual usage of purchased services.

    To access these metrics, navigate to the [Monitoring](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page of your cluster, and then check the **Server** category under the **Metrics** tab.

- Optimize the [Billing](/tidb-cloud/tidb-cloud-billing.md#billing-details) page by reorganizing the billing items in **Summary by Project** and **Summary by Service**, which makes the billing information clearer.

## April 4, 2023

**General changes**

- Remove the following two alerts from [TiDB Cloud built-in alerts](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) to prevent false positives. This is because temporary offline or out-of-memory (OOM) issues on one of the nodes do not significantly affect the overall health of a cluster.

    - At least one TiDB node in the cluster has run out of memory.
    - One or more cluster nodes are offline.

**Console changes**

- Introduce the [Alerts](/tidb-cloud/monitor-built-in-alerting.md) page for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, which lists both active and closed alerts for each Dedicated Tier cluster.

    The **Alerts** page provides the following:

    - An intuitive and user-friendly user interface. You can view alerts for your clusters on this page even if you have not subscribed to the alert notification emails.
    - Advanced filtering options to help you quickly find and sort alerts based on their severity, status, and other attributes. It also allows you to view the historical data for the last 7 days, which eases the alert history tracking.
    - The **Edit Rule** feature. You can customize alert rule settings to meet your cluster's specific needs.

  For more information, see [TiDB Cloud built-in alerts](/tidb-cloud/monitor-built-in-alerting.md).

- Consolidate the help-related information and actions of TiDB Cloud into a single place.

    Now, you can get all the [TiDB Cloud help information](/tidb-cloud/tidb-cloud-support.md) and contact support by clicking **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com/).

- Introduce the [Getting Started](https://tidbcloud.com/console/getting-started) page to help you learn about TiDB Cloud.

    The **Getting Started** page provides you with interactive tutorials, essential guides, and useful links. By following interactive tutorials, you can easily explore TiDB Cloud features and HTAP capabilities with pre-built industry-specific datasets (Steam Game Dataset and S&P 500 Dataset).

    To access the **Getting Started** page, click <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Getting Started** in the left navigation bar of the [TiDB Cloud console](https://tidbcloud.com/). On this page, you can click **Query Sample Dataset** to open the interactive tutorials or click other links to explore TiDB Cloud. Alternatively, you can click **?** in the lower-right corner and click **Interactive Tutorials**.

## March 29, 2023

**General changes**

- [Data Service (beta)](/tidb-cloud/data-service-overview.md) supports more fine-grained access control for Data Apps.

    On the Data App details page, now you can link clusters to your Data App and specify the role for each API key. The role controls whether the API key can read or write data to the linked clusters and can be set to `ReadOnly` or `ReadAndWrite`. This feature provides cluster-level and permission-level access control for Data Apps, giving you more flexibility to control the access scope according to your business needs.

    For more information, see [Manage linked clusters](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) and [Manage API keys](/tidb-cloud/data-service-api-key.md).

## March 28, 2023

**General changes**

- Add 2 RCUs, 4 RCUs, and 8 RCUs specifications for [changefeeds](/tidb-cloud/changefeed-overview.md), and support choosing your desired specification when you [create a changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed).

    Using these new specifications, the data replication costs can be reduced by up to 87.5% compared to scenarios where 16 RCUs were previously required.

- Support scaling up or down specifications for [changefeeds](/tidb-cloud/changefeed-overview.md) created after March 28, 2023.

    You can improve replication performance by choosing a higher specification or reduce replication costs by choosing a lower specification.

    For more information, see [Scale a changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed).

- Support replicating incremental data in real-time from a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) cluster in AWS to a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster in the same project and same region.

    For more information, see [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md).

- Support two new GCP regions for the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) feature of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters: `Singapore (asia-southeast1)` and `Oregon (us-west1)`.

    With these new regions, you have more options for migrating your data to TiDB Cloud. If your upstream data is stored in or near these regions, you can now take advantage of faster and more reliable data migration from GCP to TiDB Cloud.

    For more information, see [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

**Console changes**

- Release a new native web infrastructure for the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) page of [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    With this new infrastructure, you can easily navigate through the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the SQL diagnosis process more user-friendly.

## March 21, 2023

**General changes**

- Introduce [Data Service (beta)](https://tidbcloud.com/console/data-service) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, which enables you to access data via an HTTPS request using a custom API endpoint.

    With Data Service, you can seamlessly integrate TiDB Cloud with any application or service that is compatible with HTTPS. The following are some common scenarios:

    - Access the database of your TiDB cluster directly from a mobile or web application.
    - Use serverless edge functions to call endpoints and avoid scalability issues caused by database connection pooling.
    - Integrate TiDB Cloud with data visualization projects by using Data Service as a data source.
    - Connect to your database from an environment that MySQL interface does not support.

    In addition, TiDB Cloud provides the [Chat2Query API](/tidb-cloud/use-chat2query-api.md), a RESTful interface that allows you to generate and execute SQL statements using AI.

    To access Data Service, navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page in the left navigation pane. For more information, see the following documentation:

    - [Data Service Overview](/tidb-cloud/data-service-overview.md)
    - [Get Started with Data Service](/tidb-cloud/data-service-get-started.md)
    - [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)

- Support decreasing the size of TiDB, TiKV, and TiFlash nodes to scale in a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) cluster that is hosted on AWS and created after December 31, 2022.

    You can decrease the node size [via the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) or [via the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

- Support a new GCP region for the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) feature of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters: `Tokyo (asia-northeast1)`.

    The feature can help you migrate data from MySQL-compatible databases in Google Cloud Platform (GCP) to your TiDB cluster easily and efficiently.

    For more information, see [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

**Console changes**

- Introduce the **Events** page for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, which provides the records of main changes to your cluster.

    On this page, you can view the event history for the last 7 days and track important details such as the trigger time and the user who initiated an action. For example, you can view events such as when a cluster was paused or who modified the cluster size.

    For more information, see [TiDB Cloud cluster events](/tidb-cloud/tidb-cloud-events.md).

- Add the **Database Status** tab to the **Monitoring** page for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters, which displays the following database-level metrics:

    - QPS Per DB
    - Average Query Duration Per DB
    - Failed Queries Per DB

  With these metrics, you can monitor the performance of individual databases, make data-driven decisions, and take actions to improve the performance of your applications.

  For more information, see [Monitoring metrics for Serverless Tier clusters](/tidb-cloud/built-in-monitoring.md).

## March 14, 2023

**General changes**

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0) to [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1).

- Support modifying column names of the target table to be created by TiDB Cloud when uploading a local CSV file with a header row.

    When importing a local CSV file with a header row to a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster, if you need TiDB Cloud to create the target table and the column names in the header row do not follow the TiDB Cloud column naming conventions, you will see a warning icon next to the corresponding column name. To resolve the warning, you can move the cursor over the icon and follow the message to edit the existing column names or enter new column names.

    For information about column naming conventions, see [Import local files](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files).

## March 7, 2023

**General changes**

- Upgrade the default TiDB version of all [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters from [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0) to [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0).

## February 28, 2023

**General changes**

- Add the [SQL Diagnosis](/tidb-cloud/tune-performance.md) feature for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    With SQL Diagnosis, you can gain deep insights into SQL-related runtime status, which makes the SQL performance tuning more efficient. Currently, the SQL Diagnosis feature for Serverless Tier only provides slow query data.

    To use SQL Diagnosis, click **SQL Diagnosis** on the left navigation bar of your Serverless Tier cluster page.

**Console changes**

- Optimize the left navigation.

    You can navigate pages more efficiently, for example:

    - You can hover the mouse in the upper-left corner to quickly switch between clusters or projects.
    - You can switch between the **Clusters** page and the **Admin** page.

**API changes**

- Release several TiDB Cloud API endpoints for data import：

    - List all import tasks
    - Get an import task
    - Create an import task
    - Update an import task
    - Upload a local file for an import task
    - Preview data before starting an import task
    - Get the role information for import tasks

  For more information, refer to the [API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import).

## February 22, 2023

**General changes**

- Support using the [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) feature to track various activities performed by members within your organization in the [TiDB Cloud console](https://tidbcloud.com/).

    The console audit logging feature is only visible to users with the `Owner` or `Audit Admin` role and is disabled by default. To enable it, click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging** in the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/).

    By analyzing console audit logs, you can identify suspicious operations performed within your organization, thereby improving the security of your organization's resources and data.

    For more information, see [Console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md).

**CLI changes**

- Add a new command [`ticloud cluster connect-info`](/tidb-cloud/ticloud-cluster-connect-info.md) for [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

    `ticloud cluster connect-info` is a command that allows you to get the connection string of a cluster. To use this command, [update `ticloud`](/tidb-cloud/ticloud-update.md) to v0.3.2 or a later version.

## February 21, 2023

**General changes**

- Support using the AWS access keys of an IAM user to access your Amazon S3 bucket when importing data to TiDB Cloud.

    This method is simpler than using Role ARN. For more information, refer to [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

- Extend the [monitoring metrics retention period](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) from 2 days to a longer period:

    - For Dedicated Tier clusters, you can view metrics data for the past 7 days.
    - For Serverless Tier clusters, you can view metrics data for the past 3 days.

  By extending the metrics retention period, now you have access to more historical data. This helps you identify trends and patterns of the cluster for better decision-making and faster troubleshooting.

**Console changes**

- Release a new native web infrastructure on the Monitoring page of [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    With the new infrastructure, you can easily navigate through the Monitoring page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the monitoring process a lot more user-friendly.

## February 17, 2023

**CLI changes**

- Add a new command [`ticloud connect`](/tidb-cloud/ticloud-connect.md) for [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

    `ticloud connect` is a command that allows you to connect to your TiDB Cloud cluster from your local machine without installing any SQL clients. After connecting to your TiDB Cloud cluster, you can execute SQL statements in the TiDB Cloud CLI.

## February 14, 2023

**General changes**

- Support decreasing the number of TiKV and TiFlash nodes to scale in a TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) cluster.

    You can decrease the node number [via the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-node-number) or [via the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

**Console changes**

- Introduce the **Monitoring** page for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    The **Monitoring** page provides a range of metrics and data, such as the number of SQL statements executed per second, the average duration of queries, and the number of failed queries, which helps you better understand the overall performance of SQL statements in your Serverless Tier cluster.

    For more information, see [TiDB Cloud built-in monitoring](/tidb-cloud/built-in-monitoring.md).

## February 2, 2023

**CLI changes**

- Introduce the TiDB Cloud CLI client [`ticloud`](/tidb-cloud/cli-reference.md).

    Using `ticloud`, you can easily manage your TiDB Cloud resources from a terminal or other automatic workflows with a few lines of commands. Especially for GitHub Actions, we have provided [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli) for you to easily set up `ticloud`.

    For more information, see [TiDB Cloud CLI Quick Start](/tidb-cloud/get-started-with-cli.md) and [TiDB Cloud CLI Reference](/tidb-cloud/cli-reference.md).

## January 18, 2023

**General changes**

* Support [signing up](https://tidbcloud.com/free-trial) TiDB Cloud with a Microsoft account.

## January 17, 2023

**General changes**

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) to [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0).

- For new sign-up users, TiDB Cloud will automatically create a free [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster so that you can quickly start a data exploration journey with TiDB Cloud.

- Support a new AWS region for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters: `Seoul (ap-northeast-2)`.

    The following features are enabled for this region:

    - [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [Stream data from TiDB Cloud to other data services using changefeed](/tidb-cloud/changefeed-overview.md)
    - [Back up and restore TiDB cluster data](/tidb-cloud/backup-and-restore.md)

## January 10, 2023

**General changes**

- Optimize the feature of importing data from local CSV files to TiDB to improve the user experience for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

    - To upload a CSV file, now you can simply drag and drop it to the upload area on the **Import** page.
    - When creating an import task, if your target database or table does not exist, you can enter a name to let TiDB Cloud create it for you automatically. For the target table to be created, you can specify a primary key or select multiple fields to form a composite primary key.
    - After the import is completed, you can explore your data with [AI-powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) by clicking **Explore your data by Chat2Query** or clicking the target table name in the task list.

  For more information, see [Import local files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md).

**Console changes**

- Add the **Get Support** option for each cluster to simplify the process of requesting support for a specific cluster.

    You can request support for a cluster in either of the following ways:

    - On the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click **...** in the row of your cluster and select **Get Support**.
    - On your cluster overview page, click **...** in the upper-right corner and select **Get Support**.

## January 5, 2023

**Console changes**

- Rename SQL Editor (beta) to Chat2Query (beta) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters and support generating SQL queries using AI.

  In Chat2Query, you can either let AI generate SQL queries automatically or write SQL queries manually, and run SQL queries against databases without a terminal.

  To access Chat2Query, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click your cluster name, and then click **Chat2Query** in the left navigation pane.

## January 4, 2023

**General changes**

- Support scaling up TiDB, TiKV, and TiFlash nodes by increasing the **Node Size(vCPU + RAM)** for TiDB Dedicated clusters hosted on AWS and created after December 31, 2022.

    You can increase the node size [using the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) or [using the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

- Extend the metrics retention period on the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page to two days.

    Now you have access to metrics data of the last two days, giving you more flexibility and visibility into your cluster performance and trends.

    This improvement comes at no additional cost and can be accessed on the **Diagnosis** tab of the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page for your cluster. This will help you identify and troubleshoot performance issues and monitor the overall health of your cluster more effectively.

- Support customizing Grafana dashboard JSON for Prometheus integration.

    If you have [integrated TiDB Cloud with Prometheus](/tidb-cloud/monitor-prometheus-and-grafana-integration.md), you can now import a pre-built Grafana dashboard to monitor TiDB Cloud clusters and customize the dashboard to your needs. This feature enables easy and fast monitoring of your TiDB Cloud clusters and helps you identify any performance issues quickly.

    For more information, see [Use Grafana GUI dashboards to visualize the metrics](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics).

- Upgrade the default TiDB version of all [Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters from [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0) to [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0). The cold start issue after upgrading the default TiDB version of Serverless Tier clusters to v6.4.0 has been resolved.

**Console changes**

- Simplify the display of the [**Clusters**](https://tidbcloud.com/console/clusters) page and the cluster overview page.

    - You can click the cluster name on the [**Clusters**](https://tidbcloud.com/console/clusters) page to enter the cluster overview page and start operating the cluster.
    - Remove the **Connection** and **Import** panes from the cluster overview page. You can click **Connect** in the upper-right corner to get the connection information and click **Import** in the left navigation pane to import data.
