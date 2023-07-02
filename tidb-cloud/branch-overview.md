---
title: Branch overview
summary: Learn what is TiDB Serverless Branch.
---

TiDB Serverless allows users to create branches of clusters. By using TiDB Serverless Branch, teams can work in parallel, iterate quickly on new features, troubleshoot issues without impacting the production database, and roll back changes easily if necessary. It aids in the overall development and deployment process while ensuring a high level of stability and reliability for the production database.

## What is a Branch?

A branch refers to a separate instance that contains a diverged copy of data from the cluster. It serves as an isolated environment, allowing users to freely experiment without any concerns about impacting the parent cluster. 

At the point of creation, the data in the branch diverges from the cluster, meaning that subsequent changes made in either the cluster or the branch won't be synchronized. 

To ensure quick and seamless branch creation, TiDB Serverless utilizes a copy-on-write technique for sharing data between the cluster and branches. This process usually completes within several minutes and remains imperceptible to users, not affecting performance for the parent cluster.

## Scenarios

Branches are easy and quick to create and provide isolated data environments. It is beneficial in scenarios where multiple developers or teams need to work independently, test changes, fix bugs, experiment with new features, or roll out updates without disrupting the main production database.

1. Feature Development: It enables developers to work on new features in isolation without affecting the main production database. Each feature can have its own branch, allowing developers to iterate quickly and experiment without impacting other ongoing work.

2. Bug Fixing: Database branching aids in isolating and fixing bugs without introducing new issues to the main database. Developers can create a branch dedicated to fixing a specific bug, test the fix, and then merge it back once verified.

3. Experimentation: While developing new features or making changes, developers can create branches to experiment with different approaches or configurations. This allows them to compare various options, gather data, and make informed decisions before merging changes into the main database.

4. Performance Optimization: Sometimes, database changes are made to enhance performance. With branching, developers can experiment and fine-tune different configurations, indexes, or algorithms in isolated environments to identify the most efficient solution.

5. Testing and Staging: Database branching enables teams to create branches for testing and staging purposes. It ensures a controlled environment for quality assurance, user acceptance testing, or staging customizations before merging them into the main database.

6. Parallel Development: Database branching allows different teams or developers to work on different projects simultaneously. Each project can have its own branch, allowing independent development and experimentation, while still being able to merge changes back into the main database.

## Limitations and Quotas

TiDB Serverless Branch is in Beta version. Currently it is free of charge. 

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless branches by default across all the clusters. You can not create branches under a throttled cluster.

For each branch, 5 GiB storage is allowed. Once the storage is reached, the read and write operations on this branch will be throttled until you reduce the storage.

If you need more quotas, [contact TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

## What's next

- [Learn how to manage branches](./branch-manage.md)
