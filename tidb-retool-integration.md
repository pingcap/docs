# TiDB and Retool Integration
1. Get TiDB Details & Whitelist Retool IP Address

    You can get your database connection details from whoever set up the database. You'll also need to get them to [whitelist][1] the Retool IP address.

2. Add TiDB as a resource in Retool

    Create a new resource in Retool, and select "MySQL" as the type.
    Enter your database connection details.
    * Name: &lt;Your resource name&gt;
    * Host: &lt;your_tidb_cloud_ip_address&gt;
    * Port: 4000
    * Database name: &lt;database_name&gt;
    * Username: &lt;tidb_cloud_user_name&gt;
    * Password: &lt;password_of_your_tidb_cloud_cluster&gt;

3. Create queries

    You can now select your newly-created TiDB resource from the Resource dropdown when creating queries in your Retool apps. You can toggle between SQL mode for raw SQL statements or the GUI mode for [structured writes][2].

[1]: https://docs.retool.com/docs/connect-database-resource#connecting-your-database
[2]: https://docs.retool.com/docs/sql-writes
