---
title: Addax
---

[Addax](https://github.com/wgzhao/Addax), originally derived from Alibaba's [DataX](https://github.com/alibaba/DataX), is a versatile open-source ETL (Extract, Transform, Load) tool. It excels at seamlessly transferring data between diverse RDBMS (Relational Database Management Systems) and NoSQL databases, making it an optimal solution for efficient data migration.

For information about the system requirements, download, and deployment steps for Addax, refer to Addax's [Getting Started Guide](https://github.com/wgzhao/Addax#getting-started). The guide provides detailed instructions and guidelines for setting up and using Addax.

### DatabendReader & DatabendWriter

DatabendReader and DatabendWriter are integrated plugins of Addax, allowing seamless integration with Databend. The DatabendReader plugin enables reading data from Databend. Databend provides compatibility with the MySQL client protocol, so you can also use the [MySQLReader](https://wgzhao.github.io/Addax/develop/reader/mysqlreader/) plugin to retrieve data from Databend. For more information about DatabendReader, see https://wgzhao.github.io/Addax/develop/reader/databendreader/

### Tutorials

- [Migrating from MySQL with Addax](/tutorials/migrate/migrating-from-mysql-with-addax)