# ticloud config use

Use the specified profile as the active profile

```shell
ticloud config use <profile-name> [flags]
```

## Examples

Use the "test" profile as the active profile:

```shell
ticloud config use test
```

## Flags

| Flag       | Description   |
|------------|---------------|
| -h, --help | help for edit |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we welcome any contributions.
