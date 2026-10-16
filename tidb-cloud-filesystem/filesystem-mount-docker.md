---
title: 在 Docker 中挂载文件系统
summary: 通过启用 FUSE 和所需的容器权限，在 Linux 主机上的 Docker 容器内挂载文件系统。
---

# 在 Docker 中挂载文件系统

要在 Docker 容器内挂载来自 TiDB Cloud Filesystem 的文件系统，容器必须能够访问 Linux 主机上的 FUSE。除了需要在容器内安装 `fuse3` 之外，还需要暴露 `/dev/fuse`，并授予容器创建挂载的权限。

本文档介绍如何在 Linux 主机上使用 Docker 和 Docker Compose。如果你的环境不提供 FUSE 访问能力，或不允许所需的容器权限，请改用直接的 `ti fs` 命令，例如 `copy-file`、`read-file` 和 `list-files`。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

开始之前，请确保：

- 使用 Linux Docker 主机，并且 `/dev/fuse` 可用。
- 具有启动容器的权限，且该容器能够访问 `/dev/fuse`，并具备创建挂载所需的能力。
- 已拥有某个现有文件系统的文件系统 Token 和 Region 代码。参见[访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。

Docker Desktop 以及托管式容器环境或沙箱环境，可能不会暴露 `/dev/fuse`，也可能不允许所需的权限。

> **Warning:**
>
> 本文档中的示例会为容器授予 `SYS_ADMIN`，并通过 `apparmor=unconfined` 禁用其 AppArmor 配置。这些设置会使容器拥有比标准 Docker 容器更高的权限。
>
> 仅在你的环境安全策略允许的情况下使用这些设置。除非你的环境提供了适当的额外隔离边界，否则不要使用这些权限运行不受信任的代码。范围受限 Token 可以限制对文件系统数据的访问，但无法降低 Docker 授予容器的权限。

## 为容器提供文件系统访问能力 {#provide-file-system-access-to-the-container}

在 Docker 主机上，设置文件系统 Token 和 Region 代码：

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

请将文件系统 Token 视为 Secret。不要将其写入 Dockerfile，也不要将其提交到源代码管理系统中。

下面的 Docker 和 Docker Compose 示例会将这些环境变量从主机传递到容器中。

## 启动容器 {#start-the-container}

选择 Docker 或 Docker Compose 其中一种方式。

### 使用 Docker {#use-docker}

在 Docker 主机上，启动一个可交互的 Ubuntu 容器，并使其能够访问 FUSE：

```bash
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  ubuntu:24.04 bash
```

该命令会执行以下操作：

- 将主机的 `/dev/fuse` 设备暴露给容器；
- 授予创建挂载所需的能力；以及
- 将文件系统 Token 和 Region 代码传递到容器中。

容器启动后，继续执行[在容器内安装并挂载](#install-and-mount-inside-the-container)。

### 使用 Docker Compose {#use-docker-compose}

或者，也可以在 Docker 主机上创建如下 `compose.yaml` 文件：

```yaml
services:
  agent:
    image: ubuntu:24.04
    command: ["sleep", "infinity"]
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN:?Set TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE:?Set TI_REGION_CODE}
```

启动容器并进入其 shell：

```bash
docker compose up -d
docker compose exec agent bash
```

然后在容器内继续执行下面的步骤。

## 在容器内安装并挂载 {#install-and-mount-inside-the-container}

以下步骤在容器内执行。它们使用前面示例中的 `ubuntu:24.04` 镜像，该镜像默认以 `root` 身份运行。

1. 安装 `fuse3` 以及安装 `ti` 所需的工具：

    ```bash
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl fuse3
    ```

2. 安装 TiDB Cloud CLI：

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

3. 将 `ti` 添加到当前 shell，并为挂载创建一个本地目录：

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    mkdir -p "$HOME/workspace"
    ```

4. 挂载文件系统：

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    在 Linux 上，`ti` 默认使用 FUSE。命令成功后，你可以通过 `$HOME/workspace` 访问该文件系统。如果挂载启动失败，请检查 `ti` 报告的诊断日志路径。

    如果你的文件系统 Token 仅授予对特定远程路径的访问权限，请使用以下命令替代前面的挂载命令：

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace"
    ```

    在此示例中，远程 `/workspace` 目录会成为本地挂载的根目录。更多信息，参见[仅挂载文件系统的一部分](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system)。

    若要防止通过本地挂载进行写入，请在挂载命令中添加 `--read-only`。例如，将文件系统根目录以只读方式挂载：

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --read-only
    ```

    `--read-only` 选项仅影响此本地挂载。若要在文件系统服务层面强制只读访问，请使用具有只读权限的范围受限 Token。

5. 验证你是否可以访问已挂载的文件系统：

    ```bash
    ls "$HOME/workspace"
    ```

请以同一个操作系统用户运行挂载以及访问该挂载的应用程序。如果你的应用镜像使用非 root 用户，请在构建镜像时安装所需软件包，并在运行时以应用用户身份创建挂载。

## 在不卸载的情况下刷写 FUSE 写入 {#flush-fuse-writes-without-unmounting}

如果你需要在保持挂载运行的同时，让待处理的写入到达文件系统，请先停止应用程序向相关文件写入，并关闭这些文件。然后在容器内对刷写挂载：

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

刷写成功表示待处理的写入已到达文件系统，同时挂载仍保持运行。如果刷写超时或返回错误，请保持容器和 Docker 主机可用，解决错误，并在停止或删除容器之前验证文件。有关命令语法，请参见 [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md)。

## 安全地下线容器 {#stop-the-container-safely}

在下线或移除容器之前：

1. 在容器内，下线正在向已挂载目录写入数据的应用程序，并关闭已打开的文件。

2. 卸载文件系统：

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    在下线或移除容器之前，请等待卸载成功。成功的 FUSE 卸载会刷新待处理的写入。

3. 下线容器：

    - 如果你使用 `docker run --rm -it` 启动容器，请在卸载成功后退出 shell：

        ```bash
        exit
        ```

        由于容器是使用 `--rm` 启动的，Docker 会自动将其移除。

    - 如果你使用的是 Docker Compose，请先退出容器 shell，然后在 Docker 主机上运行以下命令：

        ```bash
        docker compose down
        ```

下线或移除容器不会删除远程文件系统或其中的数据。

> **Warning:**
>
> 如果卸载失败，请不要下线或移除容器。待处理的写入可能仍然只存在于容器内部。请保持容器继续运行，解决错误，并先验证所需文件已经写入文件系统。

## 接下来做什么 {#what-s-next}

- [挂载 Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) 了解只读挂载、挂载 layer 或 checkpoint，以及其他常见挂载选项。
- [在多台机器之间共享 Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md) 以便让其他用户或环境访问同一个文件系统。
- [管理 Filesystem Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md) 以将访问限制到特定路径和操作。