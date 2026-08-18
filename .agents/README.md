# Agent Collaboration Guide

This directory stores repo-local guidance for AI agents working in `pingcap/docs`.

## Structure

- `.agents/skills/`: workflow-specific instructions for recurring tasks in this repo

## Current skills

- `.agents/skills/docs-pr-metadata-guard/`: guard PR template structure when creating or editing pull requests, such as version checkboxes, required sections, HTML comments, related-link fields, and cherry-pick conventions

## How to use it

Use progressive loading so the task stays grounded but efficient:

1. Load a skill only when the task matches that workflow.
2. Validate the files you changed with the repo's existing checks when practical.

Keep the task grounded in the existing repository rules, templates, scripts, and workflows.
