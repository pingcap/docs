---
title: Migrate Data from MariaDB Galera Cluster to TiDB
summary: Learn to migrate data from MariaDB Galera Cluster to TiDB.
category: how-to
---

# Migrate Data from MariaDB Galera Cluster to TiDB

This document introduces how to migrate data from MariaDB Galera Cluster to TiDB. 

## Hardware and system requirements

### Hardware requirements

- NIC bonding or teaming
- PCIe SSDs (not SATA SSDs)
- CPU power saving management disabled in BIOS
- NUMA disabled in BIOS (`flush_caches` is optimized in Percona Server 5.7.10. For details, see [Improved NUMA support](https://www.percona.com/doc/percona-server/5.7/performance/innodb_numa_support.html))

### Operating system requirements

- Use CentOS 6.9 64-bit or CentOS 7.3-1611 64-bit as the operating system.

- If you use a virtual machine, do not deploy a cluster on a single physical machine.

- Use XFS as the file system.

- Disable SWAP space by setting `vm.swappiness` to 0.

- If the memory size exceeds 64 GB, enable huge pages.

- If the memory exceeds 32 GB, disable NUMA in the operating system.

- Disable IPv6.

    ```
    # vim /etc/sysctl.d/99-sysctl.conf
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    ```

- Enable port forwarding.

    ```
    # vim /etc/sysctl.d/99-sysctl.conf
    net.ipv4.ip_forward = 1
    ```

- Modify `limits`.

    ```
    # vim /etc/security/limits.conf
    mysql soft nofile 65535
    mysql hard nofile 65535
    ```

- Modify `/etc/pam.d/login`.

    ```
    # vim /etc/pam.d/login 
    session required /lib64/security/pam_limits.so
    ```

- Configure the MariaDB yum repository.

    ```
    Create mariadb.repo.
    # vi /etc/yum.repo.d/mariadb.repo
    Add the following (the official repository)
    [mariadb-main]
    name = MariaDB Server
    baseurl = https://downloads.mariadb.com/MariaDB/mariadb-10.3/yum/rhel/$releasever/$basearch
    gpgkey = file:///etc/pki/rpm-gpg/MariaDB-Server-GPG-KEY
    gpgcheck = 1
    enabled = 1

    [mariadb-maxscale]
    # To use the latest stable release of MaxScale, use "latest" as the version.
    # To use the latest beta (or stable if no current beta) release of MaxScale, use "beta" as the version.
    name = MariaDB MaxScale
    baseurl = https://downloads.mariadb.com/MaxScale/2.3/centos/$releasever/$basearch
    gpgkey = file:///etc/pki/rpm-gpg/MariaDB-MaxScale-GPG-KEY
    gpgcheck = 1
    enabled = 1

    [mariadb-tools]
    name = MariaDB Tools
    baseurl = https://downloads.mariadb.com/Tools/rhel/$releasever/$basearch
    gpgkey = file:///etc/pki/rpm-gpg/MariaDB-Enterprise-GPG-KEY
    gpgcheck = 1
    enabled = 1
    ```

- Install the following software.

    ```
    # yum install iotop sysstat -y
    ```

## Install MariaDB

You need to install the following on all the nodes in the database.

1. Install MariaDB.

    ```
    # yum install MariaDB-server MariaDB-client galera mariabackup socat –y
    ```

2. Install `percona-toolkit`. It is a collection of advanced command-line tools, used for performance tuning, and it is an essential tool for DBAs.

    ```
    # yum install percona-toolkit –y
    ```

3. Configure parameters according to your actual demand.
   
    1. Edit `/etc/my.cnf`.

        ```
        #
        # This group is read both by the client and the server.
        # Use it for options that affect everything.
        #
        [client-server]
        
        #
        # Include all files from the config directory.
        #
        

        [client]
        port = 3306
        socket = /mydata/mysql/log/mysql.sock

        [mysql]
        #default_character_set = 'utf8mb4'
        default_character_set = 'utf8'
        auto_rehash = FALSE
        local_infile = 0
        max_allowed_packet = 1G
    
        [mysqld]
        plugin_maturity=stable
        port = 3306
        socket = /mydata/mysql/log/mysql.sock
        pid_file = /mydata/mysql/data/mysql.pid
        #bind-address=0.0.0.0
        log-error=/mydata/mysql/log/error.log

        ### DATA STORAGE #
        basedir  = /usr
        datadir  = /mydata/mysql/data
        tmpdir=/mydata/mysql/tmp


        ### General

        default_storage_engine = InnoDB
        character-set-server = utf8
        collation-server = utf8_general_ci
        external_locking = FALSE
        skip_external_locking
        feedback = 0
        back_log = 103
        skip_name_resolve

        lower_case_table_names = 1
        table_open_cache = 2048
        open_files_limit = 65535
        max_connect_errors = 200
        max_connections = 1500
        max_user_connections = 1000
        max_prepared_stmt_count= 1048576

        extra_max_connections = 5
        extra_port = 3309
        thread_handling = pool-of-threads


        ###Replication / Binary logs
        binlog_stmt_cache_size = 32M
        slave_transaction_retries = 10

        log_bin = /mydata/mysql/binlogs/mysql-bin
        binlog_format = row
        expire_logs_days = 7
        sync_binlog = 1
        binlog_cache_size = 4M
        max_binlog_cache_size = 512M 
        max_binlog_size = 1024M

        ### REPLICATION #

        server_id=1299178
        binlog_ignore_db = information_schema
        binlog_ignore_db = performance_schema
        binlog_ignore_db = mysql
        log_slave_updates = 1
        replicate_wild_ignore_table = 'mysql.%'
        slave_net_timeout = 300

        ###GTID
        relay_log = /mydata/mysql/relaylog/relay-bin
        log_slave_updates = true 
        relay_log_recovery = 1
        sync_master_info = 1
        slave_parallel_threads = 5
        binlog_checksum = CRC32
        master_verify_checksum = 1
        slave_sql_verify_checksum = 1
        report_port = 3306


        ## FOR MaRIADB  percona
        userstat = ON
        ## performance-schema
        performance_schema = ON
        performance-schema-instrument='wait/synch/mutex/innodb/%=ON'
        performance-schema-instrument='memory/%=COUNTED'


        #!includedir /etc/my.cnf.d/
        ``` 

    2. Go to `/etc/my.cnf.d/`, create a `wsrep.cnf` file, and add the following content in `wsrep.cnf`. You can modify this file according to your actual demand.

        ```
        [mysqld]
        wsrep_on=1 # Indicates enabling galera. 
        wsrep_cluster_name='galera_cluster-quppdb178'  # The cluster name. All the cluster nodes use the same name.
        wsrep_cluster_address="gcomm://192.168.200.31:4567,192.168.200.32:4567,192.168.200.33:4567"
        wsrep_node_address='192.168.200.31'  # The IP address of the local node.
        wsrep_provider=/usr/lib64/galera/libgalera_smm.so
        wsrep_slave_threads=4
        wsrep_notify_cmd=/opt/scripts/wsrep_notify.sh
        wsrep_sst_method=rsync
        wsrep_sst_auth=galera:123  # The account name used by galera: password. Modify it according to your actual demand.
        innodb_autoinc_lock_mode=2
        innodb_doublewrite=1
        wsrep_log_conflicts=ON
        wsrep_provider_options="evs.auto_evict=5;evs.version=1;gcs.fc_limit=100"
        wsrep_max_ws_size=134217728
        ```

4. Create contents.

    ``` 
    # Create contents according to the configuration information in the parameter file. You can modify it according to your actual demand.
    mkdir -p /mydata/mysql/binlogs
    mkdir -p /mydata/mysql/data
    mkdir -p /mydata/mysql/log
    mkdir -p /mydata/mysql/relaylog
    mkdir -p /mydata/mysql/tmp
    chown -R mysql:mysql /mydata/mysql/binlogs
    chown -R mysql:mysql /mydata/mysql/data
    chown -R mysql:mysql /mydata/mysql/log
    chown -R mysql:mysql /mydata/mysql/relaylog
    chown -R mysql:mysql /mydata/mysql/tmp
    ```

5. Initialize MariaDB. 
 
    1. Initialize MariaDB.

        ```
        # Initialize MariaDB according to the configuration information in the parameter file. You can modify it according to your actual demand.
        /usr/bin/mysql_install_db --user=mysql --basedir=/usr --defaults-file=/etc/my.cnf
        ```

    2. Start MariaDB.

        ```
        systemctl start mariadb
        ```

## Start MariaDB Galera Cluster

1. Start MariaDB Galera Cluster.

    1. Stop the MariaDB service.

        ```
        systemctl stop mariadb
        ```

    2. Remove the last line of comments in `/etc/my.cnf`.

        ```
        !includedir /etc/my.cnf.d/
        ```

    3. Start the first node of Galera.

        ```
        galera_new_cluster
        ```

    4. Add a user in the master node. 

        ```
        grant all privileges on *.* to sst@'localhost' identified by 'sst123';
        # Privileges can be dropped.
        grant select,REPLICATION CLIENT,replication slave,reload on *.* to sst@'localhost' identified by 'sst123';
        ```

    5. Restart the MariaDB service on other nodes.

        ```
        systemctl restart mariadb
        ```

2. Check the cluster status. 

    ``` 
    MariaDB [(none)]> show global status like '%wsrep%';
    +------------------------------+---------------------------------------------------+
    | Variable_name                | Value                                             |
    +------------------------------+---------------------------------------------------+
    | wsrep_apply_oooe             | 0.000000                                          |
    | wsrep_apply_oool             | 0.000000                                          |
    | wsrep_apply_window           | 1.000000                                          |
    | wsrep_causal_reads           | 0                                                 |
    | wsrep_cert_deps_distance     | 1.853659                                          |
    | wsrep_cert_index_size        | 54                                                |
    | wsrep_cert_interval          | 0.000000                                          |
    | wsrep_cluster_conf_id        | 3                                                 |
    | wsrep_cluster_size           | 3                                                 |
    | wsrep_cluster_state_uuid     | eb0f4303-2ea7-11e9-87ba-679c851caca2              |
    | wsrep_cluster_status         | Primary                                           |
    | wsrep_cluster_weight         | 3                                                 |
    | wsrep_commit_oooe            | 0.000000                                          |
    | wsrep_commit_oool            | 0.000000                                          |
    | wsrep_commit_window          | 1.000000                                          |
    | wsrep_connected              | ON                                                |
    | wsrep_desync_count           | 0                                                 |
    | wsrep_evs_delayed            |                                                   |
    | wsrep_evs_evict_list         |                                                   |
    | wsrep_evs_repl_latency       | 0/0/0/0/0                                         |
    | wsrep_evs_state              | OPERATIONAL                                       |
    | wsrep_flow_control_paused    | 0.000000                                          |
    | wsrep_flow_control_paused_ns | 0                                                 |
    | wsrep_flow_control_recv      | 0                                                 |
    | wsrep_flow_control_sent      | 0                                                 |
    | wsrep_gcomm_uuid             | eb0e893c-2ea7-11e9-be54-da25e2f153fb              |
    | wsrep_incoming_addresses     | 10.9.120.111:3306,10.9.34.68:3306,10.9.10.65:3306 |
    | wsrep_last_committed         | 41                                                |
    | wsrep_local_bf_aborts        | 2                                                 |
    | wsrep_local_cached_downto    | 1                                                 |
    | wsrep_local_cert_failures    | 0                                                 |
    | wsrep_local_commits          | 9                                                 |
    | wsrep_local_index            | 2                                                 |
    | wsrep_local_recv_queue       | 0                                                 |
    | wsrep_local_recv_queue_avg   | 0.000000                                          |
    | wsrep_local_recv_queue_max   | 1                                                 |
    | wsrep_local_recv_queue_min   | 0                                                 |
    | wsrep_local_replays          | 0                                                 |
    | wsrep_local_send_queue       | 0                                                 |
    | wsrep_local_send_queue_avg   | 0.000000                                          |
    | wsrep_local_send_queue_max   | 1                                                 |
    | wsrep_local_send_queue_min   | 0                                                 |
    | wsrep_local_state            | 4                                                 |
    | wsrep_local_state_comment    | Synced                                            |
    | wsrep_local_state_uuid       | eb0f4303-2ea7-11e9-87ba-679c851caca2              |
    | wsrep_open_connections       | 0                                                 |
    | wsrep_open_transactions      | 0                                                 |
    | wsrep_protocol_version       | 9                                                 |
    | wsrep_provider_name          | Galera                                            |
    | wsrep_provider_vendor        | Codership Oy <info@codership.com>                 |
    | wsrep_provider_version       | 25.3.25(r3836)                                    |
    | wsrep_ready                  | ON                                                |
    | wsrep_received               | 30                                                |
    | wsrep_received_bytes         | 9726                                              |
    | wsrep_repl_data_bytes        | 6205                                              |
    | wsrep_repl_keys              | 60                                                |
    | wsrep_repl_keys_bytes        | 960                                               |
    | wsrep_repl_other_bytes       | 0                                                 |
    | wsrep_replicated             | 20                                                |
    | wsrep_replicated_bytes       | 8496                                              |
    | wsrep_thread_count           | 5                                                 |
    +------------------------------+---------------------------------------------------+
    61 rows in set (0.00 sec)
    ```

3. Run the `show global status like '%wsrep%';` command to make sure the following conditions are satisfied:

    - `wsrep_local_state_commment` is `synced`.
    - `wsrep_local_state` is 4.
    - `swrep_cluster_status` is `primary`.
    - Values of `wsrep_local_index`s are different.

4. Log in to different nodes respectively, create testing tables, insert data, and observe the data replication status.

## Migrate data to TiDB using Data Migration

1. Deploy Data Migration.

    For how to deploy the Data Migration cluster using DM-Ansible, see [Deploy Data Migration Using DM-Ansible](https://pingcap.com/docs/dev/how-to/deploy/data-migration-with-ansible/).

    1. Use dmctl to encrypt the upstream MySQL password.

        ```
        $ cd /home/tidb/dm-ansible/resources/bin
        $ ./dmctl -encrypt 123456
        VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
        ```

    2. Edit `inventory.ini`.

        ```
        ## DM modules
        [dm_master_servers]
        dm_master ansible_host=192.168.200.12

        [dm_worker_servers]
        dm-worker1 ansible_host=192.168.200.13 flavor="mariadb" source_id="mysql-replica-01" server_id=1299178 relay_binlog_name="mysql-bin.000001" mysql_host=192.168.200.31 mysql_user=galera  mysql_password='EC6QbyWa5eLfjW5D4GrgBEACIGA=' mysql_port=3306

        ## Monitoring modules
        [prometheus_servers]
        prometheus ansible_host=192.168.200.11

        [grafana_servers]
        grafana ansible_host=192.168.200.11

        [alertmanager_servers]
        alertmanager ansible_host=192.168.200.11

        ## Global variables
        [all:vars]
        cluster_name = test-cluster

        ansible_user = tidb

        dm_version = latest

        deploy_dir = /data/dmwork

        grafana_admin_user = "admin"
        grafana_admin_password = "admin"
        ```

    3. Deploy and start the DM cluster.

        ```
        $ cd /home/tidb/dm-ansible/
        $ ansible-playbook deploy.yml
        $ ansible-playbook start.yml
        ```

2. Configure the data replication task.

    1. Configure the `task.yaml` configuration file.

        Copy and edit `{ansible deploy}/conf/task.yaml.example`, and generate the following task configuration file `task.yaml`:

        ```
        ---
        name: "test"                    # The task name. The names of different tasks that are running simultaneously cannot be the same.
        task-mode: "incremental"        # Full + incremental (all) replication modes.
        is-sharding: true               # Whether it is a sharding task.
        meta-schema: "dm_meta"          # The downstream database that stores the meta data.
        remove-meta: true               # Removes the meta data table every time the task runs.
        target-database:                # The configuration information of TiDB.
          host: "192.168.200.12"
          port: 4000
          user: "root"
          password: "EC6QbyWa5eLfjW5D4GrgBEACIGA="
 
        mysql-instances:                         # All the MySQL instances required for the current data replication task.
        -
          source-id: "mysql-replica-01"          # The ID of the upstream instance or replication group ID. It can be configured by referring to the `source_id` in the `inventory.ini` file or the `source-id` in the `dm-master.toml` file.
          mydumper-config-name: "global_1"       # The configuration item name of Mydumper, used to refer to the global Mydumper configuration. A single instance corresponds to a single task list.
          syncer-config-name: "global"
          loader-config-name: "global"
          meta:
            binlog-name: mysql-bin.000007
            binlog-pos: 1532
          route-rules: ["user-route-rules-schema", "user-route-rules"]
 

 
        routes:                                                           # Schema/Table route mapping.
          user-route-rules-schema:
            schema-pattern: "wk"
            target-schema: "wk_mariadb"
          user-route-rules:
            schema-pattern: "wk"
            table-pattern: "test"
            target-schema: "wk_mariadb"
            target-table: "test"
 
        mydumpers:                   # Specific configurations for the mydumper processing unit. A MySQL instance can refer to one configuration in it.
          global_1:
            mydumper-path: "/home/tidb/mydumper"
            threads: 4
            chunk-filesize: 64
            skip-tz-utc: true
            extra-args: "-B wk -o /data/dmdump/wk"
 
        loaders:                     # Specific configurations for the loader processing unit. A MySQL instance can refer to one configuration in it.
          global:
            pool-size: 16
            dir: "/data/dmdump/wk"
 
        syncers:                     # Specific configurations for the syncer processing unit. A MySQL instance can refer to one configuration in it.
          global:
            worker-count: 16
            batch: 100
            max-retry: 100
        ```

        For more description of the configuration file, see [Synchronize Data Using Data Migration](https://www.pingcap.com/docs/tools/dm/practice/#).
 
3. Start the task.

    1. Go to the dmctl directory `/home/tidb/dm-ansible/resources/bin/`.

    2. Run the following command to enter the interface.

        ```
        ./dmctl --master-addr 192.168.200.13:8261
        ```

    3. Run the following command to start the data replication task.

        ```
        # `task.yaml` is the previously edited configuration file.
        start-task <YOU TASK FILE PATH>/task.yaml
        ```

    4. After you run the above command, if the returned result is as follows, the task has been started successfully.

        ```
        {
            "result": true,
            "msg": "",
            "workers": [
                {
                    "result": true,
                    "worker": "192.168.200.13:8262",
                    "msg": ""
                }
            ]
        }

    5. Insert data in the upstream `wk.test` to check whether the data can be replicated to the downstream TiDB.

4. Query and stop the task.

    - Query the task.

        You can run the `query-status` command in dmctl to check whether a replication task is running in the Data Migration cluster and the task status information. 

    - Stop the task.

        If you do not need to replicate data, you can run the following command in dmctl to stop the data replication task.

        ```
        # `test` is the task name of the `name` configuration item in the `task.yaml` configuration file.
        stop-task test
        ```
 
For more information about dmctl basic usage, see [Manage the Data Synchronization Task](https://pingcap.com/docs/dev/reference/tools/data-migration/manage-tasks/).
 
## Note

- Add `flavor="mariadb"` when writing `invintory.ini`, because the binlog formats between MariaDB and MySQL are different.
- Currently, Data Migration supports only MariaDB 10.1.2 and later.
