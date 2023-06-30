---
title: Branch overview
summary: Learn what is TiDB Cloud branch.
---

## TiDB Cloud Branch Overview

> **Note:**
>
> Branch is in public beta now, try it without any extra charge.

TiDB Cloud provides branch feature that enables you branch your serverless cluster in the same way that you branch your code.

Branch is the resource under **serverless cluster**, it has the following features:

1. Branch is a copy-on-write clone of the original cluster, including the schema and data.
2. Branch is isolated from the original cluster, changes to your branch will not affect the original cluster.

## Scenarios

Branch is gaining popularity in the realm of serverless databases. TiDB Cloud's branch feature allows you to seamlessly integrate with variety development workflows. The following are some typical scenarios:

- **Develop**: Create a branch for every developer without worrying about the data conflict.
- **Test**: Create a branch to test your every bugfix or feature without building testing data.
- **Deploy**: Deploy your testing,staging environments using the branches of the production cluster. What's more, deploy personal environments for every Git branch or pull request.

## What's next

- [Learn how to manage branches](./branch-manage.md)
