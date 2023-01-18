# ticloud config delete

Delete a profile

```shell
ticloud config delete <profile-name> [flags]
```

Or use alias

```shell
ticloud config rm <profile-name> [flags]
```

## Examples

Delete a profile configuration:

```shell
ticloud config delete <profile-name>
```

## Flags

| Flag       | Description                           |
|------------|---------------------------------------|
| --force    | Delete a profile without confirmation |
| -h, --help | help for delete                       |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we welcome any contributions.
