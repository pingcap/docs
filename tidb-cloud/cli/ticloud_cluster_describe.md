# ticloud cluster describe

Describe a cluster

```shell
ticloud cluster describe [flags]
```

Or use alias

```shell
ticloud cluster get [flags]
```

## Examples

Get the cluster info in interactive mode:

```shell
ticloud cluster describe
```

Get the cluster info in non-interactive mode:

```shell
ticloud cluster describe --project-id <project-id> --cluster-id <cluster-id>
```

## Flags

| Flag                                            | Description                   | Required | Extra                             |
|-------------------------------------------------|-------------------------------|----------|-----------------------------------|
| -c, --cluster-id string   The ID of the cluster |                               | true     | Only work in non-interactive mode |
| -h, --help                                      | help for describe             |          |                                   |
| -p, --project-id string                         | The project ID of the cluster | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.
