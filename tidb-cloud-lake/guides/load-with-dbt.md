---
title: Load Data with dbt
summary: dbt is a transformation workflow that helps you get more work done while producing higher quality results. You can use dbt to modularize and centralize your analytics code, while also providing your data team with guardrails typically found in software engineering workflows. Collaborate on data models, version them, and test and document your queries before safely deploying them to production, with monitoring and visibility.
---

# Load Data with dbt

[dbt](https://www.getdbt.com/) is a transformation workflow that helps you get more work done while producing higher quality results. You can use dbt to modularize and centralize your analytics code, while also providing your data team with guardrails typically found in software engineering workflows. Collaborate on data models, version them, and test and document your queries before safely deploying them to production, with monitoring and visibility.

[tidbcloudlake-dbt](https://github.com/tidbcloud/lake-dbt) is a plugin developed by {{{ .lake }}} with the primary goal of enabling smooth integration between dbt and {{{ .lake }}}. By utilizing this plugin, you can seamlessly perform data modeling, transformation, and cleansing tasks using dbt and conveniently load the output into {{{ .lake }}}. The table below illustrates the level of support that the tidbcloudlake-dbt plugin offers for commonly used features in dbt:

| Feature                      | Supported ? |
|----------------------------- |----------- |
| Table Materialization        | Yes        |
| View Materialization         | Yes        |
| Incremental Materialization  | Yes        |
| Ephemeral Materialization    | No         |
| Seeds                        | Yes        |
| Sources                      | Yes        |
| Custom Data Tests            | Yes        |
| Docs Generate                | Yes        |
| Snapshots                    | Yes        |
| Connection Retry             | Yes        |

## Install tidbcloudlake-dbt

Installing the tidbcloudlake-dbt plugin has been streamlined for your convenience, as it now includes dbt as a required dependency. To effortlessly set up both dbt and the tidbcloudlake-dbt plugin, run the following command:

```shell
pip3 install tidbcloudlake-dbt
```

However, if you prefer to install dbt separately, you can refer to the official dbt installation guide for detailed instructions.

## Tutorial: Run dbt Project jaffle_shop

If you're new to dbt, {{{ .lake }}} recommends completing the official dbt tutorial available at <https://github.com/dbt-labs/jaffle_shop>. Before you start, follow [Install tidbcloudlake-dbt](#install-tidbcloudlake-dbt) to install dbt and tidbcloudlake-dbt.

This tutorial provides a sample dbt project called "jaffle_shop," offering hands-on experience with the dbt tool. By configuring the default global profile (~/.dbt/profiles.yml) with the necessary information to connect to your {{{ .lake }}} instance, the project will generate tables and views defined in the dbt models directly in your {{{ .lake }}} database. Here's an example of the file profiles.yml that connects to a {{{ .lake }}} instance:

```yml title="~/.dbt/profiles.yml"
jaffle_shop_lake:
  target: dev
  outputs:
    dev:
      type: tidbcloudlake
      host: tnxxxx.gw.aws-us-east-2.default.tidbcloud.com
      port: 443
      schema: sjh_dbt
      user: <username>
      pass: ********
      warehouse: default
      secure: true
```

For more information about configuring and using the adapter, see the [lake-dbt repository](https://github.com/tidbcloud/lake-dbt).
