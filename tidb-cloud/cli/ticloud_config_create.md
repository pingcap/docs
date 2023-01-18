# ticloud config create

Configure a user profile to store settings

```shell
ticloud config create [flags]
```

## Examples

To configure a new user profile in interactive mode:

```shell
ticloud config create
```

To configure a new user profile in non-interactive mode:

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## Flags

| Flag                  | Description                                   | Required | Extra                             |
|-----------------------|-----------------------------------------------|----------|-----------------------------------|
| -h, --help            | help for create                               |          |                                   |
| --private-key string  | the private key of the TiDB Cloud API         | true     | Only work in non-interactive mode |
| --profile-name string | the name of the profile, must not contain '.' | true     | Only work in non-interactive mode |
| --public-key string   | the public key of the TiDB Cloud API          | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.
