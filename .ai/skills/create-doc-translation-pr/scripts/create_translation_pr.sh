#!/usr/bin/env bash
set -euo pipefail

META_ENV="${1:?usage: create_translation_pr.sh <translation-meta.env> [commit-message]}"
COMMIT_MESSAGE="${2:-}"

source "$META_ENV"

mapfile -t TARGET_FILES < "$TARGET_FILES_TXT"

if [ "${#TARGET_FILES[@]}" -eq 0 ]; then
  echo "No target files to stage." >&2
  exit 1
fi

if [ -z "$COMMIT_MESSAGE" ]; then
  COMMIT_MESSAGE="docs: translate #$SOURCE_PR_NUMBER"
fi

git -C "$TARGET_REPO_DIR" status --short -- "${TARGET_FILES[@]}"
git -C "$TARGET_REPO_DIR" add -- "${TARGET_FILES[@]}"

if git -C "$TARGET_REPO_DIR" diff --cached --quiet; then
  echo "No staged changes for the translation PR." >&2
  exit 1
fi

git -C "$TARGET_REPO_DIR" commit -m "$COMMIT_MESSAGE"
git -C "$TARGET_REPO_DIR" push -u origin "$NEW_BRANCH_NAME"

TARGET_PR_URL="$(
  gh pr create \
    --repo "$TARGET_REPO_OWNER/$TARGET_REPO_NAME" \
    --base "$BASE_BRANCH" \
    --head "$MY_LOGIN:$NEW_BRANCH_NAME" \
    --title "$SOURCE_TITLE" \
    --body-file "$TRANSLATION_BODY_MD"
)"

while IFS= read -r label; do
  test -n "$label" || continue
  gh pr edit "$TARGET_PR_URL" --repo "$TARGET_REPO_OWNER/$TARGET_REPO_NAME" --add-label "$label"
done < "$TRANSLATION_LABELS_TXT"

printf 'Created translation PR: %s\n' "$TARGET_PR_URL"
