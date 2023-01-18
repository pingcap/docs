# ticloud config describe

Describe a specific profile

```shell
ticloud config describe <profileName> [flags]
```

Or use alias

```shell
ticloud config get <profileName> [flags]
```

## Examples

Describe the profile configuration:

```shell
ticloud config describe <profileName>
```

## Flags

| Flag       | Description       |
|------------|-------------------|
| -h, --help | help for describe |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.
