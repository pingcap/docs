---
title: 管理 Endpoint
summary: 了解如何在 TiDB Cloud 控制台中创建、开发、测试、部署和删除 Data App 中的 endpoint。
---

# 管理 Endpoint

Data Service（测试版）中的 endpoint 是一个可自定义的 Web API，用于执行 SQL 语句。你可以为 SQL 语句指定参数，例如 `WHERE` 子句中使用的值。当 client 调用 endpoint 并在 request URL 中提供参数值时，endpoint 会使用提供的参数执行 SQL 语句，并将结果作为 HTTP response 的一部分 return。

本文档介绍如何在 TiDB Cloud 控制台的 Data App 中管理你的 endpoint。

## 开始之前

- 在创建 endpoint 之前，请确保以下条件：

    - 你已创建 cluster 和 Data App。更多信息，参见 [创建 Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app)。
    - endpoint 将要操作的数据库、表和列已存在于目标 cluster 中。

- 在调用 endpoint 之前，请确保你已在 Data App 中创建 API key。更多信息，参见 [创建 API key](/tidb-cloud/data-service-api-key.md#create-an-api-key)。

## 创建 endpoint

在 Data Service 中，你可以自动生成 endpoint、手动创建 endpoint，或添加预定义的系统 endpoint。

> **提示：**
>
> 你也可以在 SQL Editor 中通过 SQL 文件创建 endpoint。更多信息，参见 [通过 SQL 文件生成 endpoint](/tidb-cloud/explore-data-with-chat2query.md#generate-an-endpoint-from-a-sql-file)。

### 自动生成 endpoint

在 TiDB Cloud Data Service 中，你可以按如下方式一次性自动生成一个或多个 endpoint：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板中，定位到目标 Data App，点击 App 名称右侧的 **+**，然后点击 **Autogenerate Endpoint**。此时会弹出 endpoint 生成对话框。
3. 在对话框中，执行以下操作：

    1. 选择要生成 endpoint 的目标 cluster、数据库和表。

        > **注意：**
        >
        > **Table** 下拉列表仅包含至少有一个列的用户自定义表，不包括系统表和没有列定义的表。

    2. 选择至少一个 HTTP operation（如 `GET (Retrieve)`、`POST (Create)` 和 `PUT (Update)`）用于生成 endpoint。

        对于你选择的每个 operation，TiDB Cloud Data Service 都会生成一个对应的 endpoint。如果你选择了批量 operation（如 `POST (Batch Create)`），生成的 endpoint 允许你在单个 request 中操作多行数据。

        如果你选择的表包含 [向量数据类型](/ai/reference/vector-search-data-types.md)，你可以启用 **Vector Search Operations** 选项，并选择一个向量距离 function，以生成一个基于所选距离 function 自动计算向量距离的向量检索 endpoint。支持的 [向量距离 function](/ai/reference/vector-search-functions-and-operators.md) 包括：

        - `VEC_L2_DISTANCE`（默认）：计算两个向量之间的 L2 距离（欧氏距离）。
        - `VEC_COSINE_DISTANCE`：计算两个向量之间的余弦距离。
        - `VEC_NEGATIVE_INNER_PRODUCT`：使用两个向量内积的相反数计算距离。
        - `VEC_L1_DISTANCE`：计算两个向量之间的 L1 距离（曼哈顿距离）。
       
    3. （可选）为 operation 配置 timeout 和 tag。所有生成的 endpoint 会自动继承已配置的属性，后续可根据需要修改。
    4. （可选）**Auto-Deploy Endpoint** 选项（默认禁用）用于控制是否直接部署生成的 endpoint。启用后，将跳过草稿审核流程，生成的 endpoint 会立即部署，无需进一步人工审核或批准。

4. 点击 **Generate**。

    生成的 endpoint 会显示在 endpoint 列表的顶部。

5. 检查新生成 endpoint 的名称、SQL 语句、属性和参数。

    - Endpoint 名称：生成的 endpoint 名称格式为 `/<所选表名>`，请求 method（如 `GET`、`POST`、`PUT`）显示在 endpoint 名称前。例如，若所选表名为 `sample_table`，所选 operation 为 `POST (Create)`，则生成的 endpoint 显示为 `POST /sample_table`。

        - 若选择了批量 operation，TiDB Cloud Data Service 会在生成的 endpoint 名称后追加 `/bulk`。例如，所选表名为 `/sample_table`，所选 operation 为 `POST (Batch Create)`，则生成的 endpoint 显示为 `POST /sample_table/bulk`。
        - 若选择了 `POST (Vector Similarity Search)`，TiDB Cloud Data Service 会在生成的 endpoint 名称后追加 `/vector_search`。例如，所选表名为 `/sample_table`，所选 operation 为 `POST (Vector Similarity Search)`，则生成的 endpoint 显示为 `POST /sample_table/vector_search`。
        - 若已存在相同请求 method 和 endpoint 名称的 endpoint，TiDB Cloud Data Service 会在生成的 endpoint 名称后追加 `_dump_<随机字母>`。例如，`/sample_table_dump_EUKRfl`。

    - SQL 语句：TiDB Cloud Data Service 会根据表列规范和所选 endpoint operation 自动为生成的 endpoint 编写 SQL 语句。你可以点击 endpoint 名称，在页面中间区域查看其 SQL 语句。
    - Endpoint 属性：TiDB Cloud Data Service 会根据你的选择自动配置 endpoint 路径、请求 method、timeout 和 tag。你可以在页面右侧面板查看属性。
    - Endpoint 参数：TiDB Cloud Data Service 会自动为生成的 endpoint 配置参数。你可以在页面右侧面板查看参数。

6. 如果你想修改生成 endpoint 的详细信息（如名称、SQL 语句、属性或参数），请参考 [开发 endpoint](#deploy-an-endpoint) 中的说明。

### 手动创建 endpoint

要手动创建 endpoint，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板中，定位到目标 Data App，点击 App 名称右侧的 **+**，然后点击 **Create Endpoint**。
3. 如有需要，修改默认名称。新创建的 endpoint 会添加到 endpoint 列表顶部。
4. 按照 [开发 endpoint](#develop-an-endpoint) 中的说明配置新 endpoint。

### 添加预定义系统 endpoint

Data Service 提供了一个包含预定义系统 endpoint 的 endpoint 库，你可以直接将其添加到 Data App，减少 endpoint 开发工作量。目前该库仅包含 `/system/query` endpoint，你只需在预定义的 `sql` 参数中传入 SQL 语句，即可 execute 任意 SQL 语句。

要将预定义系统 endpoint 添加到 Data App，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。

2. 在左侧面板中，定位到目标 Data App，点击 App 名称右侧的 **+**，然后点击 **Manage Endpoint Library**。

    此时会弹出 endpoint 库管理对话框。目前对话框中仅提供 **Execute Query**（即 `/system/query` endpoint）。

3. 要将 `/system/query` endpoint 添加到 Data App，请将 **Execute Query** 开关切换为 **Added**。

    > **提示：**
    >
    > 若要从 Data App 移除已添加的预定义 endpoint，请将 **Execute Query** 开关切换为 **Removed**。

4. 点击 **Save**。

    > **注意：**
    >
    > - 点击 **Save** 后，添加或移除的 endpoint 会立即部署到生产环境，添加的 endpoint 立即可访问，移除的 endpoint 立即不可访问。
    > - 若当前 App 已存在相同 path 和 method 的非预定义 endpoint，则系统 endpoint 创建会失败。

    添加的系统 endpoint 会显示在 endpoint 列表的顶部。

5. 检查新 endpoint 的名称、SQL 语句、属性和参数。

    > **注意：**
    >
    > `/system/query` endpoint 功能强大且通用，但也可能具有破坏性。请谨慎使用，并确保 query 安全且经过充分考虑，以防止意外后果。

    - Endpoint 名称：endpoint 名称和路径为 `/system/query`，请求 method 为 `POST`。
    - SQL 语句：`/system/query` endpoint 不自带任何 SQL 语句。你可以在页面中间的 SQL editor 中编写所需 SQL 语句。注意，在 `/system/query` endpoint 的 SQL editor 中编写的 SQL 语句会保存在 SQL editor 中，便于后续开发和测试，但不会保存在 endpoint 配置中。
    - Endpoint 属性：在页面右侧的 **Properties** 标签页中可以查看 endpoint 属性。与其他自定义 endpoint 不同，系统 endpoint 仅支持自定义 `timeout` 和 `max rows` 属性。
    - Endpoint 参数：在页面右侧的 **Params** 标签页中可以查看 endpoint 参数。`/system/query` endpoint 的参数为自动配置，且不可修改。

## 开发 endpoint

对于每个 endpoint，你可以编写要在 TiDB cluster 上 execute 的 SQL 语句、为 SQL 语句定义参数，或管理名称和版本。

> **注意：**
>
> 如果你已将 Data App 连接到 GitHub 并启用 **Auto Sync & Deployment**，也可以通过 GitHub 修改 endpoint 配置。你在 GitHub 上的任何修改都会自动部署到 TiDB Cloud Data Service。更多信息，参见 [通过 GitHub 自动部署](/tidb-cloud/data-service-manage-github-connection.md)。

### 配置属性

在 endpoint 详情页右侧面板中，点击 **Properties** 标签页可查看和配置 endpoint 的属性。

#### 基本属性

- **Path**：用户访问 endpoint 时使用的路径。

    - 路径长度必须小于 64 个字符。
    - 请求 method 与路径的组合在同一个 Data App 内必须唯一。
    - 路径仅允许字母、数字、下划线（`_`）、斜杠（`/`）以及用大括号包裹的参数（如 `{var}`）。每个路径必须以斜杠（`/`）开头，并以字母、数字或下划线（`_`）结尾。例如，`/my_endpoint/get_id`。
    - 用 `{ }` 包裹的参数仅允许字母、数字和下划线（`_`），且每个参数必须以字母或下划线（`_`）开头。

    > **注意：**
    >
    > - 路径中每个参数必须单独占一级，不支持前缀或后缀。
    >
    >    合法路径：```/var/{var}``` 和  ```/{var}```
    >
    >    非法路径：```/var{var}``` 和 ```/{var}var```
    >
    > - 拥有相同 method 和前缀的路径可能会发生 conflict，例如：
    >
    >    ```GET /var/{var1}```
    >
    >    ```GET /var/{var2}```
    >
    >   这两条路径会 conflict，因为 `GET /var/123` 能同时匹配。
    >
    > - 带参数的路径优先级低于不带参数的路径。例如：
    >
    >    ```GET /var/{var1}```
    >
    >    ```GET /var/123```
    >
    >   这两条路径不会 conflict，因为 `GET /var/123` 优先匹配。
    >
    > - 路径参数可直接在 SQL 中使用。更多信息，参见 [配置参数](#configure-parameters)。

- **Endpoint URL**：（只读）默认 URL 会根据对应 cluster 所在 region、Data App 的 service URL 及 endpoint 路径自动生成。例如，若 endpoint 路径为 `/my_endpoint/get_id`，则 endpoint URL 为 `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`。如需为 Data App 配置自定义域名，参见 [Data Service 自定义域名](/tidb-cloud/data-service-custom-domain.md)。

- **Request Method**：endpoint 的 HTTP method。支持以下 method：

    - `GET`：用于 query 或 retrieve 数据，如 `SELECT` 语句。
    - `POST`：用于插入或创建数据，如 `INSERT` 语句。
    - `PUT`：用于 update 或修改数据，如 `UPDATE` 语句。
    - `DELETE`：用于删除数据，如 `DELETE` 语句。

- **Description**（可选）：endpoint 的描述信息。

#### 高级属性

- **Timeout(ms)**：endpoint 的 timeout，单位为毫秒。
- **Max Rows**：endpoint 可操作或 return 的最大行数。
- **Tag**：用于标识一组 endpoint 的 tag。
- **Pagination**：仅当请求 method 为 `GET` 且 endpoint 的最后一条 SQL 语句为 `SELECT` 操作时可用。启用 **Pagination** 后，你可以在调用 endpoint 时通过 query 参数指定 `page` 和 `page_size` 实现结果分页，例如：`https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id?page=<Page Number>&page_size=<Page Size>`。更多信息，参见 [调用 endpoint](#call-an-endpoint)。

    > **注意：**
    >
    > - 如果 request 中未包含 `page` 和 `page_size` 参数，则默认行为是单页 return **Max Rows** 属性指定的最大行数。
    > - `page_size` 必须小于等于 **Max Rows** 属性，否则会 return 错误。

- **Cache Response**：仅当请求 method 为 `GET` 时可用。启用 **Cache Response** 后，TiDB Cloud Data Service 可在指定的 TTL（time-to-live）期间 cache 你的 `GET` 请求返回的 response。
- **Time-to-live(s)**：仅在启用 **Cache Response** 时可用。用于指定 cache response 的 TTL（秒）。在 TTL 期间，若再次发起相同的 `GET` 请求，Data Service 会直接 return cache response，而不是再次从目标数据库获取数据，从而提升 query performance。
- **Batch Operation**：仅当请求 method 为 `POST` 或 `PUT` 时可见。启用 **Batch Operation** 后，你可以在单个 request 中操作多行数据。例如，你可以在一次 `POST` 请求中，通过在 curl 命令的 `--data-raw` 选项的 `items` 字段中放入数据对象数组，插入多行数据，具体见 [调用 endpoint](#call-an-endpoint)。

    > **注意：**
    >
    > 启用 **Batch Operation** 的 endpoint 支持数组和对象两种 request body 格式：`[{dataObject1}, {dataObject2}]` 和 `{items: [{dataObject1}, {dataObject2}]}`。为更好兼容其他系统，推荐使用对象格式 `{items: [{dataObject1}, {dataObject2}]}`。

### 编写 SQL 语句

在 endpoint 详情页的 SQL editor 中，你可以为 endpoint 编写并运行 SQL 语句。你也可以直接输入 `--` 加指令，让 AI 自动生成 SQL 语句。

1. 选择 cluster。

    > **注意：**
    >
    > 仅显示已关联到 Data App 的 cluster。要管理已关联的 cluster，参见 [管理已关联 cluster](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)。

    在 SQL editor 上方，从下拉列表中选择你希望 execute SQL 语句的 cluster。然后，你可以在右侧面板的 **Schema** 标签页查看该 cluster 的所有数据库。

2. 根据 endpoint 类型，选择数据库：

    - 预定义系统 endpoint：在 SQL editor 上方，从下拉列表中选择目标数据库。
    - 其他 endpoint：在 SQL editor 中通过 SQL 语句指定目标数据库。例如，`USE database_name;`。

3. 编写 SQL 语句。

    在 SQL editor 中，你可以编写如表关联查询、复杂查询、aggregate function 等语句。你也可以直接输入 `--` 加指令，让 AI 自动生成 SQL 语句。

    若要定义参数，可以在 SQL 语句中以变量占位符形式插入，如 `${ID}`。例如，`SELECT * FROM table_name WHERE id = ${ID}`。然后，你可以点击右侧面板的 **Params** 标签页，修改参数定义和测试值。更多信息，参见 [参数](#configure-parameters)。

    定义数组参数时，参数会在 SQL 语句中自动转换为用逗号分隔的多个值。为确保 SQL 语句有效，你需要在某些 SQL 语句（如 `IN`）中为参数加括号（`()`）。例如，定义数组参数 `ID`，测试值为 `1,2,3`，应使用 `SELECT * FROM table_name WHERE id IN (${ID})` 进行查询。

    > **注意：**
    >
    > - 参数名大小写敏感。
    > - 参数不能用作表名或列名。

4. 运行 SQL 语句。

    如果 SQL 语句中包含参数，请确保已在右侧 **Params** 标签页为参数设置测试值或默认值，否则会 return 错误。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果 editor 中只有一条语句，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 运行。

    - 如果 editor 中有多条语句，想顺序运行其中一条或多条，将光标放在目标语句上或用光标选中目标语句的行，然后按 **⌘ + Enter** 或点击 **Run**。

    - 要顺序运行 editor 中所有语句，按 **⇧ + ⌘ + Enter**，或用光标选中所有语句的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果 editor 中只有一条语句，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 运行。

    - 如果 editor 中有多条语句，想顺序运行其中一条或多条，将光标放在目标语句上或用光标选中目标语句的行，然后按 **Ctrl + Enter** 或点击 **Run**。

    - 要顺序运行 editor 中所有语句，按 **Shift + Ctrl + Enter**，或用光标选中所有语句的行后点击 **Run**。

    </div>
    </SimpleTab>

    运行后，你可以在页面底部的 **Result** 标签页立即看到 query 结果。

    > **注意：**
    >
    > 返回结果大小限制为 8 MiB。

### 配置参数

在 endpoint 详情页右侧面板，点击 **Params** 标签页可查看和管理 endpoint 使用的参数。

在 **Definition** 区域，你可以查看和管理参数的以下属性：

- 参数名：只能包含字母、数字和下划线（`_`），且必须以字母或下划线（`_`）开头。**不要**使用 `page` 和 `page_size` 作为参数名，这两个名称为 request 结果分页保留。
- **Required**：指定参数在 request 中是否必填。对于路径参数，该配置为必填且不可修改。其他参数默认非必填。
- **Type**：指定参数的数据 type。对于路径参数，仅支持 `STRING` 和 `INTEGER`。其他参数支持 `STRING`、`NUMBER`、`INTEGER`、`BOOLEAN` 和 `ARRAY`。

    使用 `STRING` type 参数时，无需添加引号（`'` 或 `"`）。例如，`foo` 对于 `STRING` type 有效，处理为 `"foo"`，而 `"foo"` 会被处理为 `"\"foo\""`。

- **Enum Value**：（可选）指定参数的有效值，仅当参数 type 为 `STRING`、`INTEGER` 或 `NUMBER` 时可用。

    - 若该字段为空，参数可为指定 type 的任意值。
    - 若要指定多个有效值，可用逗号（`,`）分隔。例如，type 设为 `STRING`，该字段为 `foo, bar`，则参数值只能为 `foo` 或 `bar`。

- **ItemType**：指定 `ARRAY` type 参数的元素 type。
- **Default Value**：指定参数的默认值。

    - 对于 `ARRAY` type，多个值需用逗号（`,`）分隔。
    - 确保该值可转换为参数的 type，否则 endpoint 会 return 错误。
    - 若未为参数设置测试值，则测试 endpoint 时会使用默认值。
- **Location**：参数的位置。该属性不可修改。
    - 路径参数该属性为 `Path`。
    - 其他参数，若请求 method 为 `GET` 或 `DELETE`，该属性为 `Query`；若请求 method 为 `POST` 或 `PUT`，该属性为 `Body`。

在 **Test Values** 区域，你可以查看和设置测试参数。这些值会在测试 endpoint 时作为参数值。确保该值可转换为参数的 type，否则 endpoint 会 return 错误。

### 重命名

要重命名 endpoint，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 找到要重命名的 endpoint，点击 **...** > **Rename**，输入新名称。

> **注意：**
>
> 预定义系统 endpoint 不支持重命名。

## 测试 endpoint

要测试 endpoint，请执行以下步骤：

> **提示：**
>
> 如果你已将 Data App 导入 Postman，也可以在 Postman 中测试 Data App 的 endpoint。更多信息，参见 [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)。

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 点击要测试的 endpoint 名称以查看详情。
4. （可选）若 endpoint 包含参数，需在测试前设置测试值。

    1. 在 endpoint 详情页右侧，点击 **Params** 标签页。
    2. 展开 **Test Values** 区域，为参数设置测试值。

        若未为参数设置测试值，则使用默认值。

5. 点击右上角的 **Test**。

    > **提示：**
    >
    > 你也可以按 <kbd>F5</kbd> 测试 endpoint。

测试完成后，你可以在页面底部看到 JSON 格式的 response。关于 JSON response 的详细信息，参见 [endpoint 的 response](#response)。

## 部署 endpoint

> **注意：**
>
> 如果你已将 Data App 连接到 GitHub 并启用 **Auto Sync & Deployment**，你在 GitHub 上对 Data App 的任何修改都会自动部署到 TiDB Cloud Data Service。更多信息，参见 [通过 GitHub 自动部署](/tidb-cloud/data-service-manage-github-connection.md)。

要部署 endpoint，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 找到要部署的 endpoint，点击 endpoint 名称查看详情，然后点击右上角的 **Deploy**。
4. 若 Data App 启用了 **Review Draft**，会弹出对话框供你审核所做修改。你可以根据审核决定是否放弃修改。
5. 点击 **Deploy** 确认部署。若部署成功，会提示 **Endpoint has been deployed**。

    在 endpoint 详情页右侧面板，你可以点击 **Deployments** 标签页查看部署历史。

## 调用 endpoint

你可以通过发送 HTTPS request 调用 endpoint 的未部署草稿版本或已部署线上版本。

> **提示：**
>
> 如果你已将 Data App 导入 Postman，也可以在 Postman 中调用 Data App 的 endpoint。更多信息，参见 [在 Postman 中运行 Data App](/tidb-cloud/data-service-postman-integration.md)。

### 前提条件

调用 endpoint 前，你需要创建 API key。更多信息，参见 [创建 API key](/tidb-cloud/data-service-api-key.md#create-an-api-key)。

### Request

TiDB Cloud Data Service 会生成代码示例，帮助你调用 endpoint。获取代码示例的步骤如下：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 找到要调用的 endpoint，点击 **...** > **Code Example**。此时会弹出 **Code Example** 对话框。

    > **提示：**
    >
    > 你也可以点击 endpoint 名称查看详情，然后在右上角点击 **...** > **Code Example**。

4. 在对话框中，选择你要调用 endpoint 的环境和认证方式，然后复制代码示例。

    > **注意：**
    >
    > - 代码示例会根据 endpoint 的属性和参数生成。
    > - 目前 TiDB Cloud Data Service 仅提供 curl 代码示例。

    - 环境：根据需要选择 **Test Environment** 或 **Online Environment**。**Online Environment** 仅在你部署 endpoint 后可用。
    - 认证方式：选择 **Basic Authentication** 或 **Digest Authentication**。
        - **Basic Authentication** 以 base64 编码文本形式传输 API key。
        - **Digest Authentication** 以加密形式传输 API key，更加安全。

      与 **Basic Authentication** 相比，**Digest Authentication** 的 curl 代码多了一个 `--digest` 选项。

    以下是启用 **Batch Operation** 并使用 **Digest Authentication** 的 `POST` 请求 curl 代码示例：

    <SimpleTab>
    <div label="Test Environment">

    调用 endpoint 草稿版本时，需要添加 `endpoint-type: draft` header：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
     --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
     --header 'content-type: application/json'\
     --header 'endpoint-type: draft'
     --data-raw '{
      "items": [
        {
          "age": "${age}",
          "career": "${career}"
        }
      ]
    }'
    ```

    </div>

    <div label="Online Environment">

    你必须先部署 endpoint，才能查看线上环境的代码示例。

    调用当前线上版本 endpoint，使用如下命令：

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
     --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
     --header 'content-type: application/json'\
     --data-raw '{
      "items": [
        {
          "age": "${age}",
          "career": "${career}"
        }
      ]
    }'
    ```

    </div>
    </SimpleTab>

    > **注意：**
    >
    > - 通过请求区域域名 `<region>.data.tidbcloud.com`，你可以直接访问 TiDB cluster 所在 region 的 endpoint。
    > - 你也可以不指定 region，直接请求 global 域名 `data.tidbcloud.com`。此时 TiDB Cloud Data Service 会在内部将请求重定向到目标 region，但可能会带来额外的 latency。如果选择此方式，调用 endpoint 时请确保在 curl 命令中添加 `--location-trusted` 选项。

5. 将代码示例粘贴到你的应用中，根据需要修改后运行。

    - 你需要将 `<Public Key>` 和 `<Private Key>` 占位符替换为你的 API key。更多信息，参见 [管理 API key](/tidb-cloud/data-service-api-key.md)。
    - 若 endpoint 的请求 method 为 `GET` 且已启用 **Pagination**，你可以通过修改 `page=<Page Number>` 和 `page_size=<Page Size>` 的值实现结果分页。例如，获取第 2 页且每页 10 条数据时，使用 `page=2` 和 `page_size=10`。
    - 若 endpoint 的请求 method 为 `POST` 或 `PUT`，请根据要操作的数据行填写 `--data-raw` 选项。

        - 对于启用 **Batch Operation** 的 endpoint，`--data-raw` 选项接受一个包含 `items` 字段的对象，`items` 字段为数据对象数组，可一次操作多行数据。
        - 对于未启用 **Batch Operation** 的 endpoint，`--data-raw` 选项仅接受一个数据对象。

    - 若 endpoint 包含参数，调用 endpoint 时需指定参数值。

### Response

调用 endpoint 后，你可以看到 JSON 格式的 response。更多信息，参见 [Data Service 的 response 和状态码](/tidb-cloud/data-service-response-and-status-code.md)。

## 下线 endpoint

> **注意：**
>
> 如果你已将 [Data App 连接到 GitHub](/tidb-cloud/data-service-manage-github-connection.md) 并启用 **Auto Sync & Deployment**，下线该 Data App 的 endpoint 也会删除 GitHub 上该 endpoint 的配置。

要下线 endpoint，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 找到要下线的 endpoint，点击 **...** > **Undeploy**。
4. 点击 **Undeploy** 确认下线。

## 删除 endpoint

> **注意：**
>
> 删除 endpoint 前，请确保该 endpoint 未上线，否则无法删除。下线 endpoint，参见 [下线 endpoint](#undeploy-an-endpoint)。

要删除 endpoint，请执行以下步骤：

1. 进入你的项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧面板，点击目标 Data App 名称以查看其 endpoint。
3. 点击要删除的 endpoint 名称，然后在右上角点击 **...** > **Delete**。
4. 点击 **Delete** 确认删除。