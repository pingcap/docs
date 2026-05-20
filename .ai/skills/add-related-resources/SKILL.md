---
name: add-related-resources
description: Produces and merges Related resources cards for TiDB docs pages using the RelatedResources and ResourceCard MDX components. Use when the user asks to add or update a related resource card, resource link, blog card, video card, YouTube card, or TiDB Lab card in English, Simplified Chinese, or Japanese Markdown docs.
---

# Add Related Resource Cards to TiDB Docs

## Overview

A "Related resources" section is a final h2 in a TiDB docs page containing a `<RelatedResources>` block with one or more `<ResourceCard />` entries. Each card links to a blog post, YouTube video, or TiDB Lab.

This skill produces those cards correctly for English, Simplified Chinese, and Japanese docs, and merges them into the target file.

## Component syntax

```mdx
## Related resources

<RelatedResources>
  <ResourceCard title="..." type="blog|video|lab" link="..." imgSrc="..." author="..." date="YYYY-MM-DD" duration="..." />
</RelatedResources>
```

Rules:

- Use one `<ResourceCard ... />` per line. Do not wrap attributes.
- Indent cards by two spaces inside `<RelatedResources>`.
- Use double quotes for all attributes and a space before `/>`.
- Keep no blank lines inside `<RelatedResources>`.
- Add one blank line before the heading and one blank line after it when creating the container section.
- Append as the last H2 unless the user gives another location.

## Language heading mapping

Infer language from the target file path and surrounding document language.

| Language | Heading | Duration |
|---|---|---|
| English | `## Related resources` | `8 mins` |
| Simplified Chinese | `## 相关资源` | `8 分钟` |
| Japanese | `## 関連リソース {#related-resources}` | `8 分` |

Japanese headings must include `{#related-resources}`.

## Card attributes

Required for every card: `title`, `type`, `link`, `imgSrc`.

Optional:

- `author`: include only when clearly shown by the source.
- `date`: use `YYYY-MM-DD`; mainly for blogs. Omit for videos/labs unless clearly shown or requested.
- `duration`: include for videos and labs when available; omit for blogs.

Do not invent values. If any required attribute cannot be found, stop and ask the user.

## Source handling

When the user provides only a URL, first run:

```bash
python3 .ai/skills/add-related-resources/scripts/fetch_resource_metadata.py "<url>" --lang en|zh|ja
```

The script emits a JSON card draft with `type`, `title`, `link`, `imgSrc`, optional fields, and warnings. Use it as a helper, not as unquestioned truth: review warnings, verify missing fields, and ask the user before fallbacks or substitutions.

If the script cannot fetch a source or returns missing required fields, use the available web, browser, or shell tools to inspect the page manually. Do not invent values.

### Blogs

Use the blog host that matches the target document language:

| Language | Host |
|---|---|
| English | `https://www.pingcap.com/blog/<slug>` |
| Simplified Chinese | `https://pingkai.cn/tidbcommunity/blog/<slug>` |
| Japanese | `https://pingcap.co.jp/blog/<slug>` |

Extract:

- `title`: visible page title, preferably H1 or `og:title`.
- `imgSrc`: page `og:image`.
- `author`: visible byline.
- `date`: `datePublished` or visible publish date, normalized to `YYYY-MM-DD`.

Japanese blog rules:

- If the JP URL redirects, use the final URL as `link`.
- If the JP URL is 404 or missing, ask before falling back to English or substituting another JP post.
- Do not rewrite `static.pingcap.com/...` image URLs to `static.pingcap.co.jp/...`; use the page's actual `og:image`.

### Videos

Supported URLs: `youtube.com/watch?v=<ID>` and `youtu.be/<ID>`.

Extract:

- `title`: YouTube video title.
- `link`: preserve the user-provided canonical video URL unless substituting with confirmation.
- `imgSrc`: `https://i.ytimg.com/vi/<ID>/hqdefault.jpg`.
- `author`: channel name.
- `duration`: video length rounded to minutes and localized.

Use the same video ID in `link` and `imgSrc`. For Japanese docs, prefer a Japanese-language `PingCAP Japan` video only after confirming substitution with the user.

### Labs

Use the lab URL that matches the target document language:

| Language | URL |
|---|---|
| English | `https://labs.tidb.io/labs/<slug>` |
| Simplified Chinese | `https://labs.pingcap.com/labs/<slug>` |
| Japanese | `https://labs.tidb.io/ja/labs/<slug>` |

Extract:

- `title`: localized lab title from the page or embedded page data. Do not translate manually.
- `imgSrc`: lab cover image, typically `https://lab-static.pingcap.com/...`.
- `duration`: estimated time, localized.

Keep the page's actual image filename, including `_en.png` images used by localized labs. Do not invent `_zh` or `_ja` variants.

## Workflow

1. Identify target file(s), source URL(s), resource type(s), and target language.
2. Read each target file and find the merge location: an existing `Related resources` block, or the end of the file if the container section must be created.
3. For each source URL, run `scripts/fetch_resource_metadata.py` with the target language.
4. Review the JSON draft. Ask the user if a required value is unavailable, a localized URL is missing, or a substitution/fallback is needed.
5. Merge the card into the target file: append to an existing `<RelatedResources>` block, or create the final localized h2 container and place the card inside it.
6. Verify formatting with:

   ```bash
   python3 .ai/skills/add-related-resources/scripts/validate_related_resources.py "<target-file>"
   ```

7. Fix validation errors and rerun the validator until it prints `OK`.

## Examples

English lab:

```mdx
## Related resources

<RelatedResources>
  <ResourceCard title="TiDB SQL Tuning Lab 1: Clustered and Non-Clustered Indexes" type="lab" link="https://labs.tidb.io/labs/dba_307_lab_ff0" imgSrc="https://lab-static.pingcap.com/quick-demo/307-01.png" duration="90 mins" />
</RelatedResources>
```

Chinese lab:

```mdx
## 相关资源

<RelatedResources>
  <ResourceCard title="管理 TiDB 实验 8: 备份与还原" type="lab" link="https://labs.pingcap.com/labs/dba_303_lab_ff7" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch09_en.png" duration="60 分钟" />
</RelatedResources>
```

Japanese mixed cards:

```mdx
## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="管理 TiDB 演習 8: バックアップと復元" type="lab" link="https://labs.tidb.io/ja/labs/dba_303_lab_ff7" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch09_en.png" duration="60 分" />
  <ResourceCard title="3分で分かるNewSQLデータベースのTiDB Cloud" type="video" link="https://www.youtube.com/watch?v=kWrT4Qd1xA0" imgSrc="https://i.ytimg.com/vi/kWrT4Qd1xA0/hqdefault.jpg" author="PingCAP Japan" duration="3 分" />
</RelatedResources>
```

## Common mistakes

- Creating a duplicate container section instead of appending cards to the existing block.
- Omitting `{#related-resources}` from Japanese headings.
- Using `type="Blog"` or `type="YouTube"` instead of `blog`, `video`, or `lab`.
- Using non-ISO dates.
- Formatting English duration as `8 minutes` instead of `8 mins`.
- Omitting the space in Chinese or Japanese durations.
- Silently falling back to English when a localized source page is missing.
- Mismatching YouTube IDs between `link` and `imgSrc`.
