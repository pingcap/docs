#!/usr/bin/env bash
set -euo pipefail

META_ENV="${1:?usage: create_translation_branch.sh <translation-meta.env>}"
source "$META_ENV"

UPSTREAM_SHA="$(gh api "repos/$TARGET_REPO_OWNER/$TARGET_REPO_NAME/git/ref/heads/$BASE_BRANCH" -q '.object.sha')"
CURRENT_BRANCH="$(git -C "$TARGET_REPO_DIR" branch --show-current || true)"

gh api --method PATCH "repos/$MY_LOGIN/$TARGET_REPO_NAME/git/refs/heads/$BASE_BRANCH" \
  -f sha="$UPSTREAM_SHA" \
  -F force=true >/dev/null

git -C "$TARGET_REPO_DIR" fetch upstream "$BASE_BRANCH"
git -C "$TARGET_REPO_DIR" fetch origin "$BASE_BRANCH"

if gh api "repos/$MY_LOGIN/$TARGET_REPO_NAME/git/ref/heads/$NEW_BRANCH_NAME" >/dev/null 2>&1; then
  git -C "$TARGET_REPO_DIR" fetch origin "$NEW_BRANCH_NAME"
  if [ "$CURRENT_BRANCH" != "$NEW_BRANCH_NAME" ]; then
    git -C "$TARGET_REPO_DIR" checkout -B "$NEW_BRANCH_NAME" "origin/$NEW_BRANCH_NAME"
  fi
  git -C "$TARGET_REPO_DIR" branch --set-upstream-to "origin/$NEW_BRANCH_NAME" "$NEW_BRANCH_NAME" >/dev/null 2>&1 || true
  echo "BRANCH_READY=$NEW_BRANCH_NAME"
  echo "BRANCH_REUSED=1"
  exit 0
fi

gh api --method POST "repos/$MY_LOGIN/$TARGET_REPO_NAME/git/refs" \
  -f ref="refs/heads/$NEW_BRANCH_NAME" \
  -f sha="$UPSTREAM_SHA" >/dev/null

git -C "$TARGET_REPO_DIR" checkout -B "$NEW_BRANCH_NAME" "upstream/$BASE_BRANCH"
git -C "$TARGET_REPO_DIR" branch --set-upstream-to "origin/$NEW_BRANCH_NAME" "$NEW_BRANCH_NAME" >/dev/null 2>&1 || true

echo "BRANCH_READY=$NEW_BRANCH_NAME"
echo "BRANCH_REUSED=0"
