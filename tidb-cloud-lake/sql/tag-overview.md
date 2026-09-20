---
title: Tag
summary: Overview of tag management and assignment in TiDB Cloud Lake.
---

# Tag

Tags let you attach key-value metadata to {{{ .lake }}} objects for data governance, classification, and compliance tracking. You can define tags with optional allowed values, assign them to objects, and query tag assignments through the `TAG_REFERENCES` table function.

## Tag Management

| Command | Description |
|---------|-------------|
| [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) | Creates a new tag with optional allowed values and comment |
| [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md) | Removes a tag (must have no active references) |
| [SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md) | Lists tag definitions |

## Tag Assignment

| Command | Description |
|---------|-------------|
| [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) | Assigns or removes tags on database objects |
| [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md) | Queries tag assignments on a specific object |