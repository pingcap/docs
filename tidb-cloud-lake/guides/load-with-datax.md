---
title: DataX
---

[DataX](https://github.com/alibaba/DataX) is an open-source data integration tool developed by Alibaba. It is designed to efficiently and reliably transfer data between various data storage systems and platforms, such as relational databases, big data platforms, and cloud storage services. DataX supports a wide range of data sources and data sinks, including but not limited to MySQL, Oracle, SQL Server, PostgreSQL, HDFS, Hive, HBase, MongoDB, and more.

:::tip
[Apache DolphinScheduler](https://dolphinscheduler.apache.org/) now has added support for Databend as a data source. This enhancement enables you to leverage DolphinScheduler for managing DataX tasks and effortlessly load data from MySQL to Databend.
:::

For information about the system requirements, download, and deployment steps for DataX, refer to DataX's [Quick Start Guide](https://github.com/alibaba/DataX/blob/master/userGuid.md). The guide provides detailed instructions and guidelines for setting up and using DataX.

### DatabendWriter

DatabendWriter is an integrated plugin of DataX, which means it comes pre-installed and does not require any manual installation. It acts as a seamless connector that enables the effortless transfer of data from other databases to Databend. With DatabendWriter, you can leverage the capabilities of DataX to efficiently load data from various databases into Databend. 

DatabendWriter supports two operational modes: INSERT (default) and REPLACE. In INSERT Mode, new data is added while conflicts with existing records are prevented to maintain data integrity. On the other hand, the REPLACE Mode prioritizes data consistency by replacing existing records with newer data in case of conflicts.

If you need more information about DatabendWriter and its functionalities, you can refer to the documentation available at https://github.com/alibaba/DataX/blob/master/databendwriter/doc/databendwriter.md

### Tutorials

- [Migrating from MySQL with DataX](/tutorials/migrate/migrating-from-mysql-with-datax)