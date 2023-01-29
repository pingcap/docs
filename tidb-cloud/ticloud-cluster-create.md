---
title: ticloud cluster create
Summary: The reference of `ticloud cluster create`.
---

# ticloud cluster create

Create one cluster in the specified project

```shell
ticloud cluster create [flags]
```

## Examples

Create a cluster in interactive mode:

```shell
ticloud cluster create
```

Create a cluster in non-interactive mode:

```shell
ticloud cluster create --project-id <project-id> --cluster-name <cluster-name> --cloud-provider <cloud-provider> --region <region> --root-password <password> --cluster-type <cluster-type>
```

## Flags

| Flag                    | Description                                                 | Required | Extra                             |
|-------------------------|-------------------------------------------------------------|----------|-----------------------------------|
| --cloud-provider string | Cloud provider, one of [AWS]                                | Yes      | Only work in non-interactive mode |
| --cluster-name string   | Name of the cluster to be created                           | Yes      | Only work in non-interactive mode | 
| --cluster-type string   | Cluster type. Currently, only "SERVERLESS" is supported.     | Yes      | Only work in non-interactive mode | 
| -h, --help              | Get the help information                |   No  |     Work in both non-interactive and interactive modes.     |                                   |
| -p, --project-id string | The ID of the project, in which the cluster will be created | Yes      | Only work in non-interactive mode | 
| -r, --region string     | Cloud region                                                | Yes      | Only work in non-interactive mode | 
| --root-password string  | The root password of the cluster                            | Yes      | Only work in non-interactive mode | 

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
