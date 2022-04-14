---
title: A Test File
summary: This is a test file for 14 Vale rules.
---

# A Test File

This is a test file for 14 Vale rules.

## AMAP

12PM, 5 AM, 10 pm.

## Em Dash

This is an em dash — don't put spaces around it.

## En Dash

This is an en dash–don't use it.

## Exclamation

Don't use exclamation!

## Gender

don't use he/she, s/he, or (s)he.

## Gender Bias

don't use waitress.

## Heading Punctuation.

## Latin

Don't use etc.

## Ly Hyphens

This is an actively-maintained repository.

## Optional Plurals

Don't use version(s).

## Ordinal

This is the 11th rule.

## Slang

tl;dr (too long; didn't read).

## Spacing

Use one space around punctuation.  Don't use two spaces.

Use one space around punctuation.Don't use zero space.

## Units

Don't Write units like this: 10kB.

## Reject words

Don't write ambiguous words like these:

- a lot
- lots of
- many
- much
- Enough
- Sufficient
- A large number of
- a large volume of

## Test scoping

Test if the vale linter can skip code spans and code blocks.

Test code spans: <http:waitress>, <code>10kB</code>, `1h`.

Test code blocks:

<pre><code>

This is an actively-maintained repository.
Don't use version(s).
Don't use "a lot of".
This is the 11th rule.

</code></pre>

```
This is an actively-maintained repository.
Don't use version(s).
This is the 11th rule.
```

```shell
This is an actively-maintained repository.
Don't use version(s).
This is the 11th rule.
```
