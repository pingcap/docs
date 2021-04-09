---
title: tiup cluster stop
---

# tiup cluster stop

<<<<<<< Updated upstream
The `tiup cluster stop` command is used to stop all services or some services of the specified cluster.

> **Note:**
> 
> If the core services of a cluster are stopped, the cluster cannot provide services anymore.

## Syntax
=======
命令 `tiup cluster stop` 用于停止指定集群的所有服务或部分服务。

> **注意：**
> 
> 核心服务停止后集群将无法提供服务。

## 语法
>>>>>>> Stashed changes

```sh
tiup cluster stop <cluster-name> [flags]
```

<<<<<<< Updated upstream
``<cluster-name>` is the name of the cluster to operate on. If you forget the cluster name, check it in [tiup cluster list](/tiup/tiup-component-cluster-list.md).

## Options

### -N, --node

Specifies the IDs of the nodes to stop, splitting by commas for multiple nodes. The node IDs are in the first column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command stops all the nodes.

> **Note:**
> 
> If `-R, --role` is also specified, only the services in the intersection of the specified nodes and roles are stopped.

### -R, --role strings

Specifies the roles to stop, splitting by commas for multiple roles. The roles are in the second column of the [tiup cluster display](/tiup/tiup-component-cluster-display.md) table.
Data type: `STRING`
Default: []. If this option is not specified in the command, the command stops all the roles.

> **Note:**
> 
> If `-N, --node` is also specified, only the services in the intersection of the specified nodes and roles are stopped.

### -h, --help

- Prints the help information.
- Data type: `BOOLEAN`
- This option is disabled by default with the `false` value. To enable this option, add this option to the command, and either pass the `true` value or do not pass any value.

## Output

The output contains the stopping logs.
=======
`<cluster-name>` 为要操作的集群名字，如果忘记集群名字可通过[集群列表](/tiup/tiup-component-cluster-list.md)查看。

## 选项

### -N, --node（strings，默认为 []，表示所有节点）

指定要停止的节点，不指定则表示所有节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。

> **注意：**
> 
> 若同时指定了 `-R, --role`，那么将停止它们的交集中的服务。

### -R, --role strings（strings，默认为 []，表示所有角色）

指定要停止的角色，不指定则表示所有角色。该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
> 
> 若同时指定了 `-N, --node`，那么将停止它们的交集中的服务。

### -h, --help（boolean，默认 false）

输出帮助信息。

## 输出

停止服务的日志。
>>>>>>> Stashed changes
