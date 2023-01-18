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
| --cluster-name string   | Name of the cluster to de created                           | Yes      | Only work in non-interactive mode | 
| --cluster-type string   | Cluster type, only support "SERVERLESS" now                 | Yes      | Only work in non-interactive mode | 
| -h, --help              | help for create                                             |          |                                   |
| -p, --project-id string | The ID of the project, in which the cluster will be created | Yes      | Only work in non-interactive mode | 
| -r, --region string     | Cloud region                                                | Yes      | Only work in non-interactive mode | 
| --root-password string  | The root password of the cluster                            | Yes      | Only work in non-interactive mode | 

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.
