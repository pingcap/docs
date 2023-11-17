# Vitess to TiDB migration

As the Vitess backend is based on MySQL you can use the regular MySQL migration tools like Dumpling, Lightning and DM which then need to be setup for each shard.

In addition to this there is a [Debezium connector for Vitess](https://debezium.io/documentation/reference/connectors/vitess.html) which allows you to use Kafka Connect or Apache Flink to stream changes from Vitess to TiDB.

As both Vitess and TiDB support the MySQL protocol and SQL dialect the amount of application level changes is expected to be small, except for things that directly manage sharding or other implementation specific things. To bridge the gap even more TiDB has support for the [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md) function.

## Examples

### Dumpling and Lightning

![Vitess to TiDB Migration with TiDB backend](/media/vitess_to_tidb.png)

This is with Dumpling and Lightning where Lightning uses the `tidb` backend.

---

![Vitess to TiDB Migration with local backend](/media/vitess_to_tidb_dumpling_local.png)

This is with Dumpling and Lightning where Lightning uses the `local` backend to directly ingest data into TiKV.

### DM

![Vitess to TiDB with DM](/media/vitess_to_tidb_dm.png)
