---
title: AI-Powered Features
---

import SearchSVG from '@site/static/img/icon/search.svg'
import LanguageFileParse from '@site/src/components/LanguageDocs/file-parse'
import AITip from '@site/docs/fragment/ai-tip.md'

<LanguageFileParse
cn={<AITip />}
/>

With the inclusion of AI-powered features, Databend Cloud allows you to engage in natural language conversations to receive help, assistance, and solutions. These AI-powered features are enabled by default, but you can disable them if desired by navigating to **Manage** > **Settings**.

### AI Chat for Assistance

AI Chat enables natural language interactions, allowing for intuitive information retrieval and streamlined problem-solving.

To launch an AI-Chat:

1. Click the magnifying glass icon <SearchSVG/> located in the sidebar to open the search box.

2. Switch to the **Chat** tab.

3. Enter your question.

![Alt text](@site/static/img/documents/worksheet/ai-chat.gif)

### AI-Powered SQL Assistant

AI assistance is available for editing SQL statements within worksheets. You don't need to write your SQL from scratch — AI can generate it for you.

To involve AI when editing a SQL statement, simply type "/" at the beginning of a new line and input your query, like "return current time":

![Alt text](@site/static/img/documents/worksheet/ai-worksheet-1.gif)

You can also get AI assistance for an existing SQL statement. To do so, highlight your SQL and click **Edit** to specify your desired changes or request further help. Alternatively, click **Chat** to engage in a conversation with AI for more comprehensive support.

![Alt text](@site/static/img/documents/worksheet/ai-worksheet-2.gif)
