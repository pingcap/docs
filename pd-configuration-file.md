---
title: PD 配置文件
summary: 了解 PD 配置文件。
---

# PD 配置文件

<!-- markdownlint-disable MD001 -->

PD 配置文件支持比命令行参数更多的选项。你可以在[这里](https://github.com/pingcap/pd/blob/release-8.1/conf/config.toml)找到默认的配置文件。

本文档仅描述未包含在命令行参数中的参数。有关命令行参数，请查看[这里](/command-line-flags-for-pd-configuration.md)。

> **Tip:**
>
> 如果你需要调整某个配置项的值，请参考[修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration)。

### `name`

- PD 节点的唯一名称
- 默认值：`"pd"`
- 若要启动多个 PD 节点，需为每个节点使用唯一的名称。

### `data-dir`

- PD 存储数据的目录
- 默认值：`"default.${name}"`

### `client-urls`

- PD 监听的客户端 URL 列表
- 默认值：`"http://127.0.0.1:2379"`
- 在部署集群时，必须将当前主机的 IP 地址指定为 `client-urls`（例如，`"http://192.168.100.113:2379"`）。如果集群在 Docker 上运行，则指定 Docker 的 IP 地址为 `"http://0.0.0.0:2379"`。

### `advertise-client-urls`

- 客户端访问 PD 的广告 URL 列表
- 默认值：`"${client-urls}"`
- 在某些情况下，例如在 Docker 或 NAT 网络环境中，如果客户端无法通过 PD 监听的默认 `client-urls` 访问 PD，则必须手动设置广告客户端 URL。
- 例如，Docker 的内网 IP 为 `172.17.0.1`，而主机的 IP 为 `192.168.100.113`，端口映射设置为 `-p 2380:2380`。此时，可以将 `advertise-client-urls` 设置为 `"http://192.168.100.113:2380"`。客户端可以通过 `"http://192.168.100.113:2380"` 找到此服务。

### `peer-urls`

- PD 节点监听的对等 URL 列表
- 默认值：`"http://127.0.0.1:2380"`
- 在部署集群时，必须将 `peer-urls` 指定为当前主机的 IP 地址，例如 `"http://192.168.100.113:2380"`。如果集群在 Docker 上运行，则指定 Docker 的 IP 地址为 `"http://0.0.0.0:2380"`。

### `advertise-peer-urls`

- 其他 PD 节点（对等节点）访问此 PD 节点的广告 URL 列表
- 默认值：`"${peer-urls}"`
- 在某些情况下，例如在 Docker 或 NAT 网络环境中，如果其他节点（对等节点）无法通过此 PD 节点监听的默认 `peer-urls` 访问此节点，则必须手动设置广告对等 URL。
- 例如，Docker 的内网 IP 为 `172.17.0.1`，主机 IP 为 `192.168.100.113`，端口映射为 `-p 2380:2380`。此时，可以将 `advertise-peer-urls` 设置为 `"http://192.168.100.113:2380"`。其他 PD 节点可以通过 `"http://192.168.100.113:2380"` 访问此服务。

### `initial-cluster`

- 引导启动的集群初始配置
- 默认值：`"{name}=http://{advertise-peer-url}"`
- 例如，如果 `name` 为 `"pd"`，`advertise-peer-urls` 为 `"http://192.168.100.113:2380"`，则 `initial-cluster` 为 `"pd=http://192.168.100.113:2380"`。
- 若要启动三个 PD 服务器，`initial-cluster` 可能为：

    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

### `initial-cluster-state`

+ 集群的初始状态
+ 默认值：`"new"`

### `initial-cluster-token`

+ 在引导阶段识别不同的集群
+ 默认值：`"pd-cluster"`
+ 如果连续部署多个配置相同的集群，必须指定不同的 token 以隔离不同的集群节点。

### `lease`

+ PD Leader Key 租约的超时时间。超时后，系统会重新选举 Leader。
+ 默认值：`3`
+ 单位：秒

### `quota-backend-bytes`

+ 元信息数据库的存储大小，默认值为 8GiB
+ 默认值：`8589934592`

### `auto-compaction-mod`

+ 元信息数据库的自动压缩模式
+ 可用选项：`periodic`（周期性）和 `revision`（按版本号）
+ 默认值：`periodic`

### `auto-compaction-retention`

+ 当 `auto-compaction-retention` 为 `periodic` 时，自动压缩的时间间隔。设置为 `revision` 时，此参数表示自动压缩的版本号。
+ 默认值：`1h`

### `tick-interval`

+ 等同于 etcd 的 `heartbeat-interval` 配置项。控制不同 PD 节点中嵌入式 etcd 实例之间的 Raft 心跳间隔。值越小，故障检测越快，但网络负载增加。
+ 默认值：`500ms`

### `election-interval`

+ 等同于 etcd 的 `election-timeout` 配置项。控制 PD 节点中嵌入式 etcd 实例的选举超时时间。如果在此时间内未收到其他 etcd 实例的有效心跳，则发起 Raft 选举。
+ 默认值：`3000ms`
+ 此值必须至少是 [`tick-interval`](#tick-interval) 的五倍。例如，如果 `tick-interval` 为 `500ms`，则 `election-interval` 必须大于等于 `2500ms`。

### `enable-prevote`

+ 等同于 etcd 的 `pre-vote` 配置项。控制 PD 节点中嵌入式 etcd 是否启用 Raft 预投票。当启用时，etcd 会进行额外的选举阶段，以确认是否有足够的投票赢得选举，从而最小化服务中断。
+ 默认值：`true`

### `force-new-cluster`

+ 决定是否强制 PD 以新集群方式启动，并将 Raft 成员数修改为 `1`
+ 默认值：`false`

### `tso-update-physical-interval`

+ PD 更新 TSO 物理时间的间隔
+ 在默认的 TSO 物理时间更新间隔中，PD 最多提供 262144 个 TSOs。若需获取更多 TSO，可以减小此配置项的值。最小值为 `1ms`。
+ 减小此值可能会增加 PD 的 CPU 使用率。根据测试，与 `50ms` 的间隔相比，`1ms` 时 PD 的[CPU 使用率](https://man7.org/linux/man-pages/man1/top.1.html)会增加约 10%。
+ 默认值：`50ms`
+ 最小值：`1ms`

## pd-server

与 pd-server 相关的配置项

### `server-memory-limit` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> 此配置为实验性功能，不建议在生产环境中使用。

+ PD 实例的内存限制比例。值为 `0` 表示无内存限制。
+ 默认值：`0`
+ 最小值：`0`
+ 最大值：`0.99`

### `server-memory-limit-gc-trigger` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> 此配置为实验性功能，不建议在生产环境中使用。

+ PD 尝试触发 GC 的阈值比例。当 PD 的内存使用达到 `server-memory-limit` * `server-memory-limit-gc-trigger` 时，触发 Golang GC。每分钟最多触发一次 GC。
+ 默认值：`0.7`
+ 最小值：`0.5`
+ 最大值：`0.99`

### `enable-gogc-tuner` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> 此配置为实验性功能，不建议在生产环境中使用。

+ 控制是否启用 GOGC 调优器。
+ 默认值：`false`

### `gc-tuner-threshold` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> 此配置为实验性功能，不建议在生产环境中使用。

+ 调优 GOGC 的最大内存阈值比例。当内存超过此阈值，即 `server-memory-limit` * `gc-tuner-threshold` 时，GOGC 调优器停止工作。
+ 默认值：`0.6`
+ 最小值：`0`
+ 最大值：`0.9`

### `flow-round-by-digit` <span class="version-mark">New in TiDB 5.1</span>

+ 默认值：3
+ PD 对流量数字的最低位进行四舍五入，减少因 Region 流量信息变化引起的统计更新。此配置项用于指定对 Region 流量信息进行最低位的舍入位数。例如，流量 `100512` 会被舍入为 `101000`，因为默认值为 `3`。此配置取代了 `trace-region-flow`。

> **Note:**
>
> 如果你将集群从 TiDB 4.0 升级到当前版本，`flow-round-by-digit` 升级后与升级前 `trace-region-flow` 的行为默认保持一致。这意味着，如果升级前 `trace-region-flow` 为 false，升级后 `flow-round-by-digit` 的值为 127；如果升级前 `trace-region-flow` 为 true，升级后 `flow-round-by-digit` 的值为 `3`。

### `min-resolved-ts-persistence-interval` <span class="version-mark">New in v6.0.0</span>

+ 决定最小已解决时间戳的持久化间隔。如果设置为 `0`，表示禁用持久化。
+ 默认值：在 v6.3.0 之前为 `"0s"`，从 v6.3.0 起为 `"1s"`，这是最小的正值。
+ 最小值：`0`
+ 单位：秒

> **Note:**
>
> 升级自 v6.0.0~v6.2.0 的集群，`min-resolved-ts-persistence-interval` 的默认值在升级后不变，仍为 `"0s"`。若要启用此功能，需要手动修改此配置项的值。

## security

与安全相关的配置项

### `cacert-path`

+ CA 文件的路径
+ 默认值：`""`

### `cert-path`

+ 包含 X509 证书的 PEM 文件路径
+ 默认值：`""`

### `key-path`

+ 包含 X509 密钥的 PEM 文件路径
+ 默认值：`""`

### `redact-info-log` <span class="version-mark">New in v5.0</span>

+ 控制是否在 PD 日志中启用信息日志的红色化
+ 设置为 `true` 时，用户数据在 PD 日志中会被隐藏。
+ 默认值：`false`

## `log`

与日志相关的配置项

### `level`

+ 指定输出日志的级别
+ 可选值：`"debug"`、`"info"`、`"warn"`、`"error"`、`"fatal"`
+ 默认值：`"info"`

### `format`

+ 日志格式
+ 可选值：`"text"`、`"json"`
+ 默认值：`"text"`

### `disable-timestamp`

+ 是否禁用日志中的自动生成时间戳
+ 默认值：`false`

## `log.file`

与日志文件相关的配置项

### `max-size`

+ 单个日志文件的最大尺寸。超过此值，系统会自动将日志拆分成多个文件。
+ 默认值：`300`
+ 单位：MiB
+ 最小值：`1`

### `max-days`

+ 日志保留的最大天数
+ 如果未设置此配置项或其值为默认的 `0`，则 PD 不会清理日志文件。
+ 默认值：`0`

### `max-backups`

+ 要保留的最大日志文件数
+ 如果未设置此配置项或其值为默认的 `0`，则 PD 会保留所有日志文件。
+ 默认值：`0`

## `metric`

与监控相关的配置项

### `interval`

+ 监控指标数据推送到 Prometheus 的时间间隔
+ 默认值：`15s`

## `schedule`

与调度相关的配置项

> **Note:**
>
> 若要修改这些与 `schedule` 相关的 PD 配置项，请根据你的集群状态选择以下方法之一：
>
> - 新部署的集群，可以直接修改 PD 配置文件。
> - 现有集群，建议使用命令行工具 [PD Control](/pd-control.md) 进行修改。直接在配置文件中修改这些与 `schedule` 相关的 PD 配置项，不会影响已存在的集群。

### `max-merge-region-size`

+ 控制 `Region Merge` 的大小限制。当 Region 大小超过指定值时，PD 不会将其与相邻的 Region 合并。
+ 默认值：`20`
+ 单位：MiB

### `max-merge-region-keys`

+ 指定 `Region Merge` 的最大 key 数。当 Region 的 key 数大于此值时，PD 不会将其与相邻 Region 合并。
+ 默认值：`200000`

### `patrol-region-interval`

+ 控制 `replicaChecker` 检查 Region 健康状态的运行频率。值越小，检查越快。通常无需调整此参数。
+ 默认值：`10ms`

### `split-merge-interval`

+ 控制同一 Region 上 `split` 和 `merge` 操作之间的时间间隔。即新拆分的 Region 在一段时间内不会被合并。
+ 默认值：`1h`

### `max-movable-hot-peer-size` <span class="version-mark">New in v6.1.0</span>

+ 控制可调度的热点 Region 的最大大小
+ 默认值：`512`
+ 单位：MiB

### `max-snapshot-count`

+ 控制单个存储节点同时接收或发送的快照最大数量。PD 调度器依赖此配置，防止正常流量的资源被抢占。
+ 默认值：`64`

### `max-pending-peer-count`

+ 控制单个存储节点中待处理的最大对等节点数。PD 调度器依赖此配置，防止某些节点生成过多带有过时日志的 Region。
+ 默认值：`64`

### `max-store-down-time`

+ 判断存储节点断开后无法恢复的宕机时间。PD 在未收到存储节点的心跳超出此时间后，会在其他节点添加副本。
+ 默认值：`30m`

### `max-store-preparing-time` <span class="version-mark">New in v6.1.0</span>

+ 控制存储节点上线的最大等待时间。在存储节点上线阶段，PD 可以查询存储节点的上线进度。超过此时间后，PD 认为存储节点已上线，不再查询上线进度，但不会阻止 Region 转移到新上线的存储节点。大多数场景下无需调整此参数。
+ 默认值：`48h`

### `leader-schedule-limit`

+ 同时进行的 Leader 调度任务数
+ 默认值：`4`

### `region-schedule-limit`

+ 同时进行的 Region 调度任务数
+ 默认值：`2048`

### `enable-diagnostic` <span class="version-mark">New in v6.3.0</span>

+ 控制是否启用诊断功能。启用后，PD 会记录调度过程中的状态，帮助诊断。如果启用，可能会略微影响调度速度，并在存储节点较多时消耗更多内存。
+ 默认值：从 v7.1.0 起，默认值由 `false` 改为 `true`。如果你的集群从 v7.1.0 之前的版本升级到 v7.1.0 或更高版本，默认值不变。

### `hot-region-schedule-limit`

+ 控制同时运行的热点 Region 调度任务数。与 Region 调度无关。
+ 默认值：`4`

### `hot-region-cache-hits-threshold`

+ 设置识别热点 Region 所需的分钟数阈值。Region 在热点状态持续超过此时间后，PD 才会参与热点调度。
+ 默认值：`3`

### `replica-schedule-limit`

+ 同时进行的副本调度任务数
+ 默认值：`64`

### `merge-schedule-limit`

+ 同时进行的 `Region Merge` 调度任务数。将此参数设为 `0` 可禁用 `Region Merge`。
+ 默认值：`8`

### `high-space-ratio`

+ 存储容量充足的阈值比例。当存储空间占用率小于此阈值时，PD 在调度时会忽略剩余空间，主要根据 Region 大小进行负载均衡。此配置仅在 `region-score-formula-version` 设置为 `v1` 时生效。
+ 默认值：`0.7`
+ 最小值：大于 `0`
+ 最大值：小于 `1`

### `low-space-ratio`

+ 存储容量不足的阈值比例。当存储空间占用率超过此阈值时，PD 会尽量避免迁移数据到此存储节点。同时，为防止存储空间耗尽，PD 主要根据剩余空间进行调度。
+ 默认值：`0.8`
+ 最小值：大于 `0`
+ 最大值：小于 `1`

### `tolerant-size-ratio`

+ 控制 `balance` 缓冲区大小
+ 默认值：`0`（自动调整缓冲区大小）
+ 最小值：`0`

### `enable-cross-table-merge`

+ 决定是否启用跨表 Region 的合并
+ 默认值：`true`

### `region-score-formula-version` <span class="version-mark">New in v5.0</span>

+ 控制 Region 评分公式的版本
+ 默认值：`v2`
+ 可选值：`v1` 和 `v2`。与 v1 相比，v2 的变化更平滑，空间回收引起的调度抖动得到改善。

> **Note:**
>
> 如果你将集群从 TiDB 4.0 版本升级到当前版本，`region-score-formula-version` 会默认被禁用，以确保升级前后 PD 行为一致。如果你想切换公式版本，需要通过 `pd-ctl` 手动切换。详情请参考[PD Control](/pd-control.md#config-show--set-option-value--placement-rules)。

### `store-limit-version` <span class="version-mark">New in v7.1.0</span>

> **Warning:**
>
> 将此配置项设置为 `"v2"` 是一个实验性功能，不建议在生产环境中使用。

+ 控制存储限制公式的版本
+ 默认值：`v1`
+ 取值选项：
    + `v1`：在 v1 模式下，可以手动修改 `store limit` 来限制单个 TiKV 的调度速度。
    + `v2`： (实验性功能) 在 v2 模式下，无需手动设置 `store limit`，PD 会根据 TiKV 快照的能力动态调整。详情请参考[store limit v2 原理](/configure-store-limit.md#principles-of-store-limit-v2)。

### `enable-joint-consensus` <span class="version-mark">New in v5.0</span>

+ 控制是否使用联合共识进行副本调度。若禁用，PD 会逐个调度副本。
+ 默认值：`true`

### `hot-regions-write-interval` <span class="version-mark">New in v5.4.0</span>

+ PD 存储热点 Region 信息的时间间隔
+ 默认值：`10m`

> **Note:**
>
> 热点 Region 信息每三分钟更新一次。如果设置的间隔少于三分钟，期间的更新可能没有意义。

### `hot-regions-reserved-days` <span class="version-mark">New in v5.4.0</span>

+ 指定热点 Region 信息的保留天数
+ 默认值：`7`

### `enable-heartbeat-breakdown-metrics` <span class="version-mark">New in v8.0.0</span>

+ 控制是否启用 Region 心跳的细分指标。这些指标衡量 Region 心跳处理的各个阶段耗时，便于监控分析。
+ 默认值：`true`

### `enable-heartbeat-concurrent-runner` <span class="version-mark">New in v8.0.0</span>

+ 控制是否启用 Region 心跳的异步并发处理。启用后，独立的执行器会异步并发处理 Region 心跳请求，有助于提升心跳处理吞吐量和降低延迟。
+ 默认值：`true`

## `replication`

与副本相关的配置项

### `max-replicas`

+ 副本数，即领导者和跟随者的总数。默认值 `3` 表示 1 个领导者和 2 个跟随者。动态修改此配置后，PD 会在后台调度 Region，使副本数与配置匹配。
+ 默认值：`3`

### `location-labels`

+ TiKV 集群的拓扑信息
+ 默认值：`[]`
+ [集群拓扑配置](/schedule-replicas-by-topology-labels.md)

### `isolation-level`

+ TiKV 集群的最小拓扑隔离级别
+ 默认值：`""`
+ [集群拓扑配置](/schedule-replicas-by-topology-labels.md)

### `strictly-match-label`

+ 启用严格检查 TiKV 标签是否匹配 PD 的 `location-labels`
+ 默认值：`false`

### `enable-placement-rules`

+ 启用 `placement-rules`
+ 默认值：`true`
+ 详见 [Placement Rules](/configure-placement-rules.md)。

## `label-property`（已废弃）

与标签相关的配置项，仅支持 `reject-leader` 类型。

> **Note:**
>
> 从 v5.2 起，标签相关的配置项已废弃。建议使用 [Placement Rules](/configure-placement-rules.md#scenario-2-place-five-replicas-in-three-data-centers-in-the-proportion-of-221-and-the-leader-should-not-be-in-the-third-data-center) 来配置副本策略。

### `key`（已废弃）

+ 拒绝 Leader 的存储标签键
+ 默认值：`""`

### `value`（已废弃）

+ 拒绝 Leader 的存储标签值
+ 默认值：`""`

## `dashboard`

与 PD 内置的 [TiDB Dashboard](/dashboard/dashboard-intro.md) 相关的配置项。

### `disable-custom-prom-addr`

+ 是否禁用在 [TiDB Dashboard](/dashboard/dashboard-intro.md) 中配置自定义 Prometheus 数据源地址
+ 默认值：`false`
+ 设置为 `true` 时，如果在 TiDB Dashboard 中配置了自定义 Prometheus 数据源地址，会报错。

### `tidb-cacert-path`

+ 根 CA 证书文件路径。连接 TiDB 的 SQL 服务时使用 TLS，可以配置此路径。
+ 默认值：`""`

### `tidb-cert-path`

+ SSL 证书文件路径。连接 TiDB 的 SQL 服务时使用 TLS，可以配置此路径。
+ 默认值：`""`

### `tidb-key-path`

+ SSL 私钥文件路径。连接 TiDB 的 SQL 服务时使用 TLS，可以配置此路径。
+ 默认值：`""`

### `public-path-prefix`

+ 当通过反向代理访问 TiDB Dashboard 时，此项设置所有 Web 资源的公共 URL 路径前缀。
+ 默认值：`/dashboard`
+ 在非反向代理环境下不要修改此配置，否则可能导致访问问题。详情请参考[在反向代理后使用 TiDB Dashboard](/dashboard/dashboard-ops-reverse-proxy.md)。

### `enable-telemetry`

> **Warning:**
>
> 从 v8.1.0 起，TiDB Dashboard 中的遥测功能已移除，此配置项不再生效。仅为兼容早期版本而保留。

+ 在 v8.1.0 之前，此配置项控制是否启用 TiDB Dashboard 的遥测收集。
+ 默认值：`false`

## `replication-mode`

与所有 Region 的复制模式相关的配置项。详见[启用 DR 自动同步模式](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode)。

## controller

本节描述内置于 PD 的[资源控制](/tidb-resource-control.md)的配置项。

### `degraded-mode-wait-duration`

+ 触发降级模式的等待时间。降级模式意味着当本地令牌桶（LTB）和全局令牌桶（GTB）丢失时，LTB 会回退到默认资源组配置，不再拥有 GTB 授权令牌，从而确保在网络隔离或异常情况下服务不受影响。
+ 默认值：`0s`
+ 降级模式默认禁用。

### `request-unit`

以下为关于[请求单元（RU）](/tidb-resource-control.md#what-is-request-unit-ru)的配置项。

#### `read-base-cost`

+ 转换读取请求为 RU 的基础系数
+ 默认值：`0.125`

#### `write-base-cost`

+ 转换写入请求为 RU 的基础系数
+ 默认值：`1`

#### `read-cost-per-byte`

+ 转换读取流量为 RU 的基础系数
+ 默认值：`1/(64 * 1024)`
+ 1 RU = 64 KiB 读取字节

#### `write-cost-per-byte`

+ 转换写入流量为 RU 的基础系数
+ 默认值：`1/1024`
+ 1 RU = 1 KiB 写入字节

#### `read-cpu-ms-cost`

+ 转换 CPU 时间为 RU 的基础系数
+ 默认值：`1/3`
+ 1 RU = 3 毫秒 CPU 时间