---
title: ADMIN SHOW TELEMETRY | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN SHOW TELEMETRY for the TiDB database.
---

# ADMIN SHOW TELEMETRY

The `ADMIN SHOW TELEMETRY` statement shows the information that will be reported back to PingCAP as part of the [telemetry](/telemetry.md) feature.

## Synopsis

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow | 'TELEMETRY' ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

```

## Examples

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY\G
```

```sql
*************************** 1. row ***************************
 TRACKING_ID: 668bdb24-6809-4bd7-85ae-6b450bae5846
 LAST_STATUS: {
  "check_at": "2021-08-10T08:53:26-06:00",
  "is_error": false,
  "error_msg": "",
  "is_request_sent": true
}
DATA_PREVIEW: {
  "hardware": [
    {
      "instanceType": "tidb",
      "listenHostHash": "e04dd0f0307fe94be0efe08015680c521abfb488",
      "listenPort": "4000",
      "cpu": {
        "cache": "512",
        "cpuFrequency": "4950.19MHz",
        "cpuLogicalCores": "24",
        "cpuPhysicalCores": "12"
      },
      "memory": {
        "capacity": "67423232000"
      },
      "disk": {
        "03d82ae39a17e5e3b2ecc5fc74dede9abc9f73e5": {
          "deviceName": "03d82ae39a17e5e3b2ecc5fc74dede9abc9f73e5",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "c37652c7c21bdf4ef0ba1900c80c6d26fffec668",
          "total": "10747904",
          "used": "10747904",
          "usedPercent": "1.00"
        },
        "2118911fcc6beb0216a9caf06af7106580030132": {
          "deviceName": "2118911fcc6beb0216a9caf06af7106580030132",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "c1f9b30495da5cda342ef4b91c400745725c6863",
          "total": "11141120",
          "used": "11141120",
          "usedPercent": "1.00"
        },
        "22cf1f5eb9b0411e77f1973be8154ee92b968a26": {
          "deviceName": "22cf1f5eb9b0411e77f1973be8154ee92b968a26",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "bb76f24cdbebee4aa7cb1d582b2e38adc4c4f237",
          "total": "52953088",
          "used": "52953088",
          "usedPercent": "1.00"
        },
        "238dac19a96f6db409609127d322f4657ab51935": {
          "deviceName": "238dac19a96f6db409609127d322f4657ab51935",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "4a0eadb05aeb3170899d20e1e679453325f38c5d",
          "total": "68026368",
          "used": "68026368",
          "usedPercent": "1.00"
        },
        "50387ccb883449b8ff10afa40f4a8d1ab9afedcc": {
          "deviceName": "50387ccb883449b8ff10afa40f4a8d1ab9afedcc",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "818cb46646d0f357911cf6e963d8f3a8108423c0",
          "total": "11010048",
          "used": "11010048",
          "usedPercent": "1.00"
        },
        "50ac293415317aeed396f0963e7e5f515f8b0336": {
          "deviceName": "50ac293415317aeed396f0963e7e5f515f8b0336",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "22014e4aa243f5b6c473c5bf45cb4a1584f40ddc",
          "total": "227540992",
          "used": "227540992",
          "usedPercent": "1.00"
        },
        "66e6074348b4c67c611eb45ad382af3499eb74c3": {
          "deviceName": "66e6074348b4c67c611eb45ad382af3499eb74c3",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "30b4687f93f6955c52d9abba44663edb35726442",
          "total": "104333312",
          "used": "104333312",
          "usedPercent": "1.00"
        },
        "6ca5d4155e772f009a7393943c37102b697812a5": {
          "deviceName": "6ca5d4155e772f009a7393943c37102b697812a5",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "d40ae3227bae816d716ee3c4bc1921d2159af601",
          "total": "53477376",
          "used": "53477376",
          "usedPercent": "1.00"
        },
        "820614014750be664ca2c6d58e3ad3144f87e562": {
          "deviceName": "820614014750be664ca2c6d58e3ad3144f87e562",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "7501db22deb27706df4de2c49895dcaba071c729",
          "total": "229638144",
          "used": "229638144",
          "usedPercent": "1.00"
        },
        "88bd4315f9425d1133b0bbe1e1aef1dc2c54c328": {
          "deviceName": "88bd4315f9425d1133b0bbe1e1aef1dc2c54c328",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "0e4a8cd479bfa32681025d7002566c8a83a01df1",
          "total": "53477376",
          "used": "53477376",
          "usedPercent": "1.00"
        },
        "8d052a01691284725c7e63b1609236d62d6e8a82": {
          "deviceName": "8d052a01691284725c7e63b1609236d62d6e8a82",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "a871044163bc5284deb13537918895c901985f9f",
          "total": "33947648",
          "used": "33947648",
          "usedPercent": "1.00"
        },
        "960d931d8996ef39ff97603f4236c0207618f53a": {
          "deviceName": "960d931d8996ef39ff97603f4236c0207618f53a",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "cba9e5d5e548e6a8a7ec8061e07502c9ead9cd2c",
          "total": "219152384",
          "used": "219152384",
          "usedPercent": "1.00"
        },
        "9ea192b58417f36c61c1899d007c0da6ab872b2f": {
          "deviceName": "9ea192b58417f36c61c1899d007c0da6ab872b2f",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "9796a47751ec2a115e541da20743a69ae1db2755",
          "total": "188219392",
          "used": "188219392",
          "usedPercent": "1.00"
        },
        "a17ce47987a347c058e98ff9f2322f409a9e4232": {
          "deviceName": "a17ce47987a347c058e98ff9f2322f409a9e4232",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "e531df779491cbedb0c6e709470c6b6b430d354c",
          "total": "68288512",
          "used": "68288512",
          "usedPercent": "1.00"
        },
        "a5b1327fa6e29681966081f3d48ca6ff422a2cc9": {
          "deviceName": "a5b1327fa6e29681966081f3d48ca6ff422a2cc9",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "0e0f9a0a8e95cb9b1b005d9a175859ff0611ed86",
          "total": "104202240",
          "used": "104202240",
          "usedPercent": "1.00"
        },
        "a7303bb0d2bada49c8065ccb9ce7e547cb3da30b": {
          "deviceName": "a7303bb0d2bada49c8065ccb9ce7e547cb3da30b",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "60a417f5ef59bd9f4d2d9b96e858bbb977bed6fb",
          "total": "29229056",
          "used": "29229056",
          "usedPercent": "1.00"
        },
        "b4b223caa62a2e116ad98f0535d1c7b6a06a48fb": {
          "deviceName": "b4b223caa62a2e116ad98f0535d1c7b6a06a48fb",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "d5fc7adaa999ce9911e6b3dc3f240ad273f40be2",
          "total": "33947648",
          "used": "33947648",
          "usedPercent": "1.00"
        },
        "c89dd343c68c40b414ac2662af5514ca9dd0b18c": {
          "deviceName": "c89dd343c68c40b414ac2662af5514ca9dd0b18c",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "23b62a02e0433719dc73d38dd4a6b819609fd2fb",
          "total": "58195968",
          "used": "58195968",
          "usedPercent": "1.00"
        },
        "c91f9090d1fc27c4879dd10ae48d720562503ea0": {
          "deviceName": "c91f9090d1fc27c4879dd10ae48d720562503ea0",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "bf3e80dc2b58bab5ffea7ff73fcc91c41b6a0a13",
          "total": "58195968",
          "used": "58195968",
          "usedPercent": "1.00"
        },
        "caec572597951508e2903ca595b7be9c20dd5232": {
          "deviceName": "caec572597951508e2903ca595b7be9c20dd5232",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "884def20a66360c15d12e24bd9e06e5947a9a36a",
          "total": "52953088",
          "used": "52953088",
          "usedPercent": "1.00"
        },
        "cd4d3d6dd9223d056ddfad7dbc9f4f3468c48a82": {
          "deviceName": "cd4d3d6dd9223d056ddfad7dbc9f4f3468c48a82",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "15eac42063613d9a40052ddfae09f6a07d8ba4b7",
          "total": "129761280",
          "used": "129761280",
          "usedPercent": "1.00"
        },
        "d39c42cc66b7d5db9588607bf70ca79d3d8c32e1": {
          "deviceName": "d39c42cc66b7d5db9588607bf70ca79d3d8c32e1",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "2c56b75bc85f4ef5a59211d1b298f71fe6485a11",
          "total": "129761280",
          "used": "129761280",
          "usedPercent": "1.00"
        },
        "db73d178e793143f28e0ea14d4c24f3adc1436cc": {
          "deviceName": "db73d178e793143f28e0ea14d4c24f3adc1436cc",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "15fecdcb41595730240631df8e13cf6892c348e6",
          "total": "64880640",
          "used": "64880640",
          "usedPercent": "1.00"
        },
        "eb7bd2c0f3e9b87ad9036d1b16aa50ca86824d49": {
          "deviceName": "eb7bd2c0f3e9b87ad9036d1b16aa50ca86824d49",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "9cde550549b84a15e5255030214af0d8a8e70265",
          "total": "229638144",
          "used": "229638144",
          "usedPercent": "1.00"
        },
        "ebadafd66d657439bff20589a5db5d86986969c8": {
          "deviceName": "ebadafd66d657439bff20589a5db5d86986969c8",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "a084e177592d1c761adc0012e4fb8e96c09301c5",
          "total": "64749568",
          "used": "64749568",
          "usedPercent": "1.00"
        },
        "efbddbff80c0374d58c66687009f9510d7d07e7f": {
          "deviceName": "efbddbff80c0374d58c66687009f9510d7d07e7f",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "8520d16fd7d1b9a83820190c551fb41e1b2ff6cf",
          "total": "138018816",
          "used": "138018816",
          "usedPercent": "1.00"
        },
        "f12336c2edc7828cc40824548c34a777170a11ea": {
          "deviceName": "f12336c2edc7828cc40824548c34a777170a11ea",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "ed0cc9f254a974e731434b56e01507f239a4b948",
          "total": "188350464",
          "used": "188350464",
          "usedPercent": "1.00"
        },
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "530337792",
          "freePercent": "0.99",
          "fstype": "vfat",
          "opts": "rw,relatime",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "535805952",
          "used": "5468160",
          "usedPercent": "0.01"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "648760172544",
          "freePercent": "0.70",
          "fstype": "ext4",
          "opts": "rw,relatime",
          "path": "/",
          "total": "982900588544",
          "used": "284140331008",
          "usedPercent": "0.30"
        },
        "nvme1n1": {
          "deviceName": "nvme1n1",
          "free": "602907807744",
          "freePercent": "0.65",
          "fstype": "ext4",
          "opts": "rw,nosuid,nodev,relatime",
          "path": "eaca4760668e918f9ef6666a67bc37b35662e83c",
          "total": "983430832128",
          "used": "330496004096",
          "usedPercent": "0.35"
        }
      }
    },
    {
      "instanceType": "pd",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "2379",
      "cpu": {
        "cache": "512",
        "cpuFrequency": "4950.19MHz",
        "cpuLogicalCores": "24",
        "cpuPhysicalCores": "12"
      },
      "memory": {
        "capacity": "67423232000"
      },
      "disk": {
        "03d82ae39a17e5e3b2ecc5fc74dede9abc9f73e5": {
          "deviceName": "03d82ae39a17e5e3b2ecc5fc74dede9abc9f73e5",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "c37652c7c21bdf4ef0ba1900c80c6d26fffec668",
          "total": "10747904",
          "used": "10747904",
          "usedPercent": "1.00"
        },
        "2118911fcc6beb0216a9caf06af7106580030132": {
          "deviceName": "2118911fcc6beb0216a9caf06af7106580030132",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "c1f9b30495da5cda342ef4b91c400745725c6863",
          "total": "11141120",
          "used": "11141120",
          "usedPercent": "1.00"
        },
        "22cf1f5eb9b0411e77f1973be8154ee92b968a26": {
          "deviceName": "22cf1f5eb9b0411e77f1973be8154ee92b968a26",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "bb76f24cdbebee4aa7cb1d582b2e38adc4c4f237",
          "total": "52953088",
          "used": "52953088",
          "usedPercent": "1.00"
        },
        "238dac19a96f6db409609127d322f4657ab51935": {
          "deviceName": "238dac19a96f6db409609127d322f4657ab51935",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "4a0eadb05aeb3170899d20e1e679453325f38c5d",
          "total": "68026368",
          "used": "68026368",
          "usedPercent": "1.00"
        },
        "50387ccb883449b8ff10afa40f4a8d1ab9afedcc": {
          "deviceName": "50387ccb883449b8ff10afa40f4a8d1ab9afedcc",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "818cb46646d0f357911cf6e963d8f3a8108423c0",
          "total": "11010048",
          "used": "11010048",
          "usedPercent": "1.00"
        },
        "50ac293415317aeed396f0963e7e5f515f8b0336": {
          "deviceName": "50ac293415317aeed396f0963e7e5f515f8b0336",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "22014e4aa243f5b6c473c5bf45cb4a1584f40ddc",
          "total": "227540992",
          "used": "227540992",
          "usedPercent": "1.00"
        },
        "66e6074348b4c67c611eb45ad382af3499eb74c3": {
          "deviceName": "66e6074348b4c67c611eb45ad382af3499eb74c3",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "30b4687f93f6955c52d9abba44663edb35726442",
          "total": "104333312",
          "used": "104333312",
          "usedPercent": "1.00"
        },
        "6ca5d4155e772f009a7393943c37102b697812a5": {
          "deviceName": "6ca5d4155e772f009a7393943c37102b697812a5",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "d40ae3227bae816d716ee3c4bc1921d2159af601",
          "total": "53477376",
          "used": "53477376",
          "usedPercent": "1.00"
        },
        "820614014750be664ca2c6d58e3ad3144f87e562": {
          "deviceName": "820614014750be664ca2c6d58e3ad3144f87e562",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "7501db22deb27706df4de2c49895dcaba071c729",
          "total": "229638144",
          "used": "229638144",
          "usedPercent": "1.00"
        },
        "88bd4315f9425d1133b0bbe1e1aef1dc2c54c328": {
          "deviceName": "88bd4315f9425d1133b0bbe1e1aef1dc2c54c328",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "0e4a8cd479bfa32681025d7002566c8a83a01df1",
          "total": "53477376",
          "used": "53477376",
          "usedPercent": "1.00"
        },
        "8d052a01691284725c7e63b1609236d62d6e8a82": {
          "deviceName": "8d052a01691284725c7e63b1609236d62d6e8a82",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "a871044163bc5284deb13537918895c901985f9f",
          "total": "33947648",
          "used": "33947648",
          "usedPercent": "1.00"
        },
        "960d931d8996ef39ff97603f4236c0207618f53a": {
          "deviceName": "960d931d8996ef39ff97603f4236c0207618f53a",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "cba9e5d5e548e6a8a7ec8061e07502c9ead9cd2c",
          "total": "219152384",
          "used": "219152384",
          "usedPercent": "1.00"
        },
        "9ea192b58417f36c61c1899d007c0da6ab872b2f": {
          "deviceName": "9ea192b58417f36c61c1899d007c0da6ab872b2f",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "9796a47751ec2a115e541da20743a69ae1db2755",
          "total": "188219392",
          "used": "188219392",
          "usedPercent": "1.00"
        },
        "a17ce47987a347c058e98ff9f2322f409a9e4232": {
          "deviceName": "a17ce47987a347c058e98ff9f2322f409a9e4232",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "e531df779491cbedb0c6e709470c6b6b430d354c",
          "total": "68288512",
          "used": "68288512",
          "usedPercent": "1.00"
        },
        "a5b1327fa6e29681966081f3d48ca6ff422a2cc9": {
          "deviceName": "a5b1327fa6e29681966081f3d48ca6ff422a2cc9",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "0e0f9a0a8e95cb9b1b005d9a175859ff0611ed86",
          "total": "104202240",
          "used": "104202240",
          "usedPercent": "1.00"
        },
        "a7303bb0d2bada49c8065ccb9ce7e547cb3da30b": {
          "deviceName": "a7303bb0d2bada49c8065ccb9ce7e547cb3da30b",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "60a417f5ef59bd9f4d2d9b96e858bbb977bed6fb",
          "total": "29229056",
          "used": "29229056",
          "usedPercent": "1.00"
        },
        "b4b223caa62a2e116ad98f0535d1c7b6a06a48fb": {
          "deviceName": "b4b223caa62a2e116ad98f0535d1c7b6a06a48fb",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "d5fc7adaa999ce9911e6b3dc3f240ad273f40be2",
          "total": "33947648",
          "used": "33947648",
          "usedPercent": "1.00"
        },
        "c89dd343c68c40b414ac2662af5514ca9dd0b18c": {
          "deviceName": "c89dd343c68c40b414ac2662af5514ca9dd0b18c",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "23b62a02e0433719dc73d38dd4a6b819609fd2fb",
          "total": "58195968",
          "used": "58195968",
          "usedPercent": "1.00"
        },
        "c91f9090d1fc27c4879dd10ae48d720562503ea0": {
          "deviceName": "c91f9090d1fc27c4879dd10ae48d720562503ea0",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "bf3e80dc2b58bab5ffea7ff73fcc91c41b6a0a13",
          "total": "58195968",
          "used": "58195968",
          "usedPercent": "1.00"
        },
        "caec572597951508e2903ca595b7be9c20dd5232": {
          "deviceName": "caec572597951508e2903ca595b7be9c20dd5232",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "884def20a66360c15d12e24bd9e06e5947a9a36a",
          "total": "52953088",
          "used": "52953088",
          "usedPercent": "1.00"
        },
        "cd4d3d6dd9223d056ddfad7dbc9f4f3468c48a82": {
          "deviceName": "cd4d3d6dd9223d056ddfad7dbc9f4f3468c48a82",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "15eac42063613d9a40052ddfae09f6a07d8ba4b7",
          "total": "129761280",
          "used": "129761280",
          "usedPercent": "1.00"
        },
        "d39c42cc66b7d5db9588607bf70ca79d3d8c32e1": {
          "deviceName": "d39c42cc66b7d5db9588607bf70ca79d3d8c32e1",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "2c56b75bc85f4ef5a59211d1b298f71fe6485a11",
          "total": "129761280",
          "used": "129761280",
          "usedPercent": "1.00"
        },
        "db73d178e793143f28e0ea14d4c24f3adc1436cc": {
          "deviceName": "db73d178e793143f28e0ea14d4c24f3adc1436cc",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "15fecdcb41595730240631df8e13cf6892c348e6",
          "total": "64880640",
          "used": "64880640",
          "usedPercent": "1.00"
        },
        "eb7bd2c0f3e9b87ad9036d1b16aa50ca86824d49": {
          "deviceName": "eb7bd2c0f3e9b87ad9036d1b16aa50ca86824d49",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "9cde550549b84a15e5255030214af0d8a8e70265",
          "total": "229638144",
          "used": "229638144",
          "usedPercent": "1.00"
        },
        "ebadafd66d657439bff20589a5db5d86986969c8": {
          "deviceName": "ebadafd66d657439bff20589a5db5d86986969c8",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "a084e177592d1c761adc0012e4fb8e96c09301c5",
          "total": "64749568",
          "used": "64749568",
          "usedPercent": "1.00"
        },
        "efbddbff80c0374d58c66687009f9510d7d07e7f": {
          "deviceName": "efbddbff80c0374d58c66687009f9510d7d07e7f",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "8520d16fd7d1b9a83820190c551fb41e1b2ff6cf",
          "total": "138018816",
          "used": "138018816",
          "usedPercent": "1.00"
        },
        "f12336c2edc7828cc40824548c34a777170a11ea": {
          "deviceName": "f12336c2edc7828cc40824548c34a777170a11ea",
          "free": "0",
          "freePercent": "0.00",
          "fstype": "squashfs",
          "opts": "ro,nodev,relatime",
          "path": "ed0cc9f254a974e731434b56e01507f239a4b948",
          "total": "188350464",
          "used": "188350464",
          "usedPercent": "1.00"
        },
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "530337792",
          "freePercent": "0.99",
          "fstype": "vfat",
          "opts": "rw,relatime",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "535805952",
          "used": "5468160",
          "usedPercent": "0.01"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "648760172544",
          "freePercent": "0.70",
          "fstype": "ext4",
          "opts": "rw,relatime",
          "path": "/",
          "total": "982900588544",
          "used": "284140331008",
          "usedPercent": "0.30"
        },
        "nvme1n1": {
          "deviceName": "nvme1n1",
          "free": "602907807744",
          "freePercent": "0.65",
          "fstype": "ext4",
          "opts": "rw,nosuid,nodev,relatime",
          "path": "eaca4760668e918f9ef6666a67bc37b35662e83c",
          "total": "983430832128",
          "used": "330496004096",
          "usedPercent": "0.35"
        }
      }
    },
    {
      "instanceType": "tikv",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "20165",
      "cpu": {
        "cpuFrequency": "2306MHz",
        "cpuLogicalCores": "24",
        "cpuPhysicalCores": "12",
        "cpuVendorId": "AuthenticAMD",
        "l1CacheLineSize": "64",
        "l1CacheSize": "32768",
        "l2CacheLineSize": "64",
        "l2CacheSize": "524288",
        "l3CacheLineSize": "64",
        "l3CacheSize": "33554432"
      },
      "memory": {
        "capacity": "69041389568"
      },
      "disk": {
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "530337792",
          "freePercent": "0.99",
          "fstype": "vfat",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "535805952",
          "used": "5468160",
          "usedPercent": "0.01"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "648760172544",
          "freePercent": "0.66",
          "fstype": "ext4",
          "path": "/",
          "total": "982900588544",
          "used": "334140416000",
          "usedPercent": "0.34"
        },
        "nvme1n1": {
          "deviceName": "nvme1n1",
          "free": "602907807744",
          "freePercent": "0.61",
          "fstype": "ext4",
          "path": "eaca4760668e918f9ef6666a67bc37b35662e83c",
          "total": "983430832128",
          "used": "380523024384",
          "usedPercent": "0.39"
        }
      }
    }
  ],
  "instances": [
    {
      "instanceType": "tidb",
      "listenHostHash": "e04dd0f0307fe94be0efe08015680c521abfb488",
      "listenPort": "4000",
      "statusHostHash": "e04dd0f0307fe94be0efe08015680c521abfb488",
      "statusPort": "10080",
      "version": "5.2.0-alpha",
      "gitHash": "15c6541e27838969a874f8bf1ff846db3b69a6bf",
      "startTime": "2021-08-08T20:53:22-06:00",
      "upTime": "40h34m13.09256248s"
    },
    {
      "instanceType": "pd",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "2379",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "2379",
      "version": "5.1.0-alpha",
      "gitHash": "de92ac964a6e170a90235d6047c84ee93967171d",
      "startTime": "2021-08-08T20:53:13-06:00",
      "upTime": "40h34m22.09257495s"
    },
    {
      "instanceType": "tikv",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "20165",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "20180",
      "version": "5.1.0-alpha",
      "gitHash": "8fc1d21bf1d0ce65246d3289c00f63e5250a5d3e",
      "startTime": "2021-08-08T20:53:18-06:00",
      "upTime": "40h34m17.09257664s"
    }
  ],
  "hostExtra": {
    "cpuFlags": [
      "fpu",
      "vme",
      "de",
      "pse",
      "tsc",
      "msr",
      "pae",
      "mce",
      "cx8",
      "apic",
      "sep",
      "mtrr",
      "pge",
      "mca",
      "cmov",
      "pat",
      "pse36",
      "clflush",
      "mmx",
      "fxsr",
      "sse",
      "sse2",
      "ht",
      "syscall",
      "nx",
      "mmxext",
      "fxsr_opt",
      "pdpe1gb",
      "rdtscp",
      "lm",
      "constant_tsc",
      "rep_good",
      "nopl",
      "nonstop_tsc",
      "cpuid",
      "extd_apicid",
      "aperfmperf",
      "pni",
      "pclmulqdq",
      "monitor",
      "ssse3",
      "fma",
      "cx16",
      "sse4_1",
      "sse4_2",
      "movbe",
      "popcnt",
      "aes",
      "xsave",
      "avx",
      "f16c",
      "rdrand",
      "lahf_lm",
      "cmp_legacy",
      "svm",
      "extapic",
      "cr8_legacy",
      "abm",
      "sse4a",
      "misalignsse",
      "3dnowprefetch",
      "osvw",
      "ibs",
      "skinit",
      "wdt",
      "tce",
      "topoext",
      "perfctr_core",
      "perfctr_nb",
      "bpext",
      "perfctr_llc",
      "mwaitx",
      "cpb",
      "cat_l3",
      "cdp_l3",
      "hw_pstate",
      "ssbd",
      "mba",
      "ibrs",
      "ibpb",
      "stibp",
      "vmmcall",
      "fsgsbase",
      "bmi1",
      "avx2",
      "smep",
      "bmi2",
      "erms",
      "invpcid",
      "cqm",
      "rdt_a",
      "rdseed",
      "adx",
      "smap",
      "clflushopt",
      "clwb",
      "sha_ni",
      "xsaveopt",
      "xsavec",
      "xgetbv1",
      "xsaves",
      "cqm_llc",
      "cqm_occup_llc",
      "cqm_mbm_total",
      "cqm_mbm_local",
      "clzero",
      "irperf",
      "xsaveerptr",
      "rdpru",
      "wbnoinvd",
      "arat",
      "npt",
      "lbrv",
      "svm_lock",
      "nrip_save",
      "tsc_scale",
      "vmcb_clean",
      "flushbyasid",
      "decodeassists",
      "pausefilter",
      "pfthreshold",
      "avic",
      "v_vmsave_vmload",
      "vgif",
      "umip",
      "pku",
      "ospke",
      "vaes",
      "vpclmulqdq",
      "rdpid",
      "overflow_recov",
      "succor",
      "smca",
      "fsrm"
    ],
    "cpuModelName": "AMD Ryzen 9 5900X 12-Core Processor",
    "os": "linux",
    "platform": "ubuntu",
    "platformFamily": "debian",
    "platformVersion": "21.04",
    "kernelVersion": "5.11.0-25-generic",
    "kernelArch": "x86_64",
    "virtualizationSystem": "kvm",
    "virtualizationRole": "host"
  },
  "reportTimestamp": 1628623654,
  "trackingId": "668bdb24-6809-4bd7-85ae-6b450bae5846",
  "featureUsage": {
    "txn": {
      "asyncCommitUsed": true,
      "onePCUsed": true,
      "txnCommitCounter": {
        "twoPC": 328,
        "asyncCommit": 0,
        "onePC": 328
      }
    },
    "clusterIndex": {},
    "temporaryTable": false,
    "cte": {
      "nonRecursiveCTEUsed": 0,
      "recursiveUsed": 0,
      "nonCTEUsed": 6
    }
  },
  "windowedStats": [
    {
      "beginAt": "2021-08-10T07:28:27.422979166-06:00",
      "executeCount": 0,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 2238,
        "LTInt": 108
      }
    },
    {
      "beginAt": "2021-08-10T08:28:27.529512647-06:00",
      "executeCount": 0,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 1994,
        "LTInt": 96
      }
    },
    {
      "beginAt": "2021-08-10T09:28:27.64699984-06:00",
      "executeCount": 0,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 1994,
        "LTInt": 96
      }
    },
    {
      "beginAt": "2021-08-10T10:28:27.758379348-06:00",
      "executeCount": 0,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 1746,
        "LTInt": 84
      }
    },
    {
      "beginAt": "2021-08-10T11:28:27.868553646-06:00",
      "executeCount": 0,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 999,
        "LTInt": 48
      }
    },
    {
      "beginAt": "2021-08-10T12:28:27.983255506-06:00",
      "executeCount": 5,
      "tiFlashUsage": {
        "pushDown": 0,
        "exchangePushDown": 0
      },
      "coprCacheUsage": {
        "gte0": 0,
        "gte1": 0,
        "gte10": 0,
        "gte20": 0,
        "gte40": 0,
        "gte80": 0,
        "gte100": 0
      },
      "SQLUsage": {
        "total": 0,
        "type": {}
      },
      "builtinFunctionsUsage": {
        "EQString": 252,
        "LTInt": 12
      }
    }
  ],
  "slowQueryStats": null
}
```


## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Telemetry](/telemetry.md)
* [`tidb_enable_telemetry` System Variable](/system-variables.md#tidb_enable_telemetry-new-in-v402)