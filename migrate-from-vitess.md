# Vitess to TiDB migration

As the Vitess backend is based on MySQL you can use the regular MySQL migration tools like Dumpling, Lightning and DM which then need to be setup for each shard.

In addition to this there is a [Debezium connector for Vitess](https://debezium.io/documentation/reference/connectors/vitess.html) which allows you to use Kafka Connect or Apache Flink to stream changes from Vitess to TiDB.

As both Vitess and TiDB support the MySQL protocol and SQL dialect the amount of application level changes is expected to be small, except for things that directly manage sharding or other implementation specific things. To bridge the gap even more TiDB has support for the `VITESS_HASH()` function.