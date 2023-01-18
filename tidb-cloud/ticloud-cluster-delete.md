# ticloud cluster delete

Delete a cluster from your project

```shell
ticloud cluster delete [flags]
```

Or use alias

```shell
ticloud cluster rm [flags]
```

## Examples

Delete a cluster in interactive mode:

```shell
ticloud cluster delete
```

Delete a cluster in non-interactive mode:
    
```shell
ticloud cluster delete --project-id <project-id> --cluster-id <cluster-id>
```

## Flags

| Flag                    | Description                                 | Required | Extra                             |
|-------------------------|---------------------------------------------|----------|-----------------------------------|
| -c, --cluster-id string | The ID of the cluster to be deleted         | true     | Only work in non-interactive mode |
| --force                 | Delete a cluster without confirmation       | false    | Work in both modes                |
| -h, --help              | help for delete                             |          |                                   |
| -p, --project-id string | The project ID of the cluster to be deleted | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we welcome any contributions.
