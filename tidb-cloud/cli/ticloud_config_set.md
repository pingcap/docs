# ticloud config set

Configure specific properties of the active profile

## Synopsis

Configure specific properties of the active profile.
Available properties : [public-key private-key api-url].

| Property    | Description                                                     |
|-------------|-----------------------------------------------------------------|
| public-key  | the public key of the TiDB Cloud API                            |
| private-key | the private key of the TiDB Cloud API                           |
| api-url     | the host of TiDB Cloud API, default `https://api.tidbcloud.com` |

If using -P flag, the config in the specific profile will be set.
If not, the config in the active profile will be set

```shell
ticloud config set <property-name> <value> [flags]
```

## Examples

Set the value of the public-key in active profile:

```shell
ticloud config set public-key <public-key>
```

Set the value of the public-key in the specific profile "test":

```shell
ticloud config set public-key <public-key> -P test
```

Set the API host:

```shell
ticloud config set api-url https://api.tidbcloud.com
```

<Note>Usually you don't need to set up the TiDB Cloud API url, the default value is `https://api.tidbcloud.com`.</Note>

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
