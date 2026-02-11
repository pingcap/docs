---
title: 使用 TiDB Cloud Starter 搭配 AI 工具
summary: 了解如何将 TiDB Cloud Starter 集群连接到支持 Model Context Protocol (MCP) 的 AI 驱动开发工具，如 Cursor、Claude Code、VS Code 和 Windsurf。
---

# 使用 TiDB Cloud Starter 搭配 AI 工具

本文介绍如何将 TiDB Cloud Starter 集群连接到支持 Model Context Protocol (MCP) 的 AI 驱动开发工具，如 Cursor、Claude Code、Visual Studio Code (VS Code) 和 Windsurf。

通过将 TiDB Cloud Starter 集群配置为 MCP 服务器，你可以让开发工具中的 AI 助手查询你的数据库 schema，理解你的数据模型，并生成具备上下文感知的代码建议。

## 开始之前

完成本指南，你需要准备以下内容：

- 一个 TiDB Cloud Starter 集群。如果你还没有，可以[创建一个 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 已安装 [Python 3.11 或更高版本](https://www.python.org/downloads/)。
- 已安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)。
- 一个支持 MCP 的 AI 开发工具，例如：

    - [Cursor](https://cursor.com)
    - [Claude Code](https://claude.com/product/claude-code)
    - [Visual Studio Code](https://code.visualstudio.com)
    - [Windsurf](https://windsurf.com)

## 连接到 AI 工具

在 TiDB Cloud 中创建 TiDB Cloud Starter 集群后，按照以下步骤将其连接到你的 AI 工具。

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。然后，点击右上角的 **Use with AI Tools**。
2. 在 **Access `your_cluster_name` with AI tools** 对话框中，选择你希望 AI 工具访问的 **Branch** 和 **Database**。
3. 确认你已满足所有 **Prerequisites**（前置条件）。如未满足，请按照屏幕提示安装所需依赖。
4. 配置密码：

    - 如果你尚未设置密码，点击 **Generate Password** 生成一个随机密码。

        生成的密码不会再次显示，请将密码保存在安全的位置。

    - 如果你已设置密码，在 **Enter the password for easy setup** 字段中输入你的密码。
    - 如果你忘记了密码，在 **Prerequisites** 部分点击 **Reset password** 生成新密码。

        注意，重置密码会断开所有现有 root 用户会话。

5. 选择你的 AI 工具对应的标签页：**Cursor**、**Claude Code**、**VS Code** 或 **Windsurf**。
6. 按照所选工具的步骤完成设置。

    更多信息，参见 [特定工具设置](#tool-specific-setup)。

## 特定工具设置

### Cursor

要将 Cursor 配置为 TiDB 的 MCP 客户端，你可以使用以下任一方法：

- **方法 1**：在 [TiDB Cloud 控制台](https://tidbcloud.com) 的 **Access `your_cluster_name` with AI tools** 对话框中，点击 **Add to Cursor** 启动 Cursor，然后点击 **Install**。
- **方法 2**：手动将以下配置添加到你的 `.cursor/mcp.json` 文件中：

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "command": "uvx --from pytidb[mcp] tidb-mcp-server",
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Claude Code

要将 Claude Code 配置为 TiDB 的 MCP 客户端，你可以使用以下任一方法：

- **方法 1**：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的 **Access `your_cluster_name` with AI tools** 对话框中复制设置命令，并在终端中运行：

    ```bash
    claude mcp add --transport stdio TiDB \
      --env TIDB_HOST='<YOUR_TIDB_HOST>' \
      --env TIDB_PORT=<YOUR_TIDB_PORT> \
      --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
      --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
      --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
      -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
    ```

- **方法 2**：将以下配置添加到你的项目级 `.mcp.json` 文件中。更多信息，参见 [Claude Code 文档](https://code.claude.com/docs/en/mcp#project-scope)。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### VS Code

要将 VS Code 配置为 TiDB 的 MCP 客户端，你可以使用以下任一方法：

- **方法 1**：在 [TiDB Cloud 控制台](https://tidbcloud.com/) 的 **Access `your_cluster_name` with AI tools** 对话框中，点击 **Add to VS Code** 启动 VS Code，然后点击 **Install**。
- **方法 2**：将以下配置添加到你的 `.vscode/mcp.json` 文件中：

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Windsurf

要将 TiDB MCP 插件添加到 Windsurf，请按如下方式更新你的 `mcp_config.json` 文件。更多信息，参见 [Windsurf 文档](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin)。

```json
{
  "mcpServers": {
    "TiDB": {
      "command": "uvx",
      "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
      "env": {
        "TIDB_HOST": "<YOUR_TIDB_HOST>",
        "TIDB_PORT": "<YOUR_TIDB_PORT>",
        "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
        "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
        "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
      }
    }
  }
}
```

## 另请参阅

- [试用 TiDB + 向量检索](/ai/quickstart-via-python.md)
- [开发者指南总览](https://docs.pingcap.com/developer/)