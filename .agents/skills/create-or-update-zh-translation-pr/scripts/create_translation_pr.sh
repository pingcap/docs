#!/usr/bin/env bash
set -euo pipefail

META_ENV="${1:?usage: create_translation_pr.sh <translation-meta.env> [commit-message]}"
COMMIT_MESSAGE="${2:-}"

source "$META_ENV"

TARGET_FILES=()
while IFS= read -r target_file; do
  [ -n "$target_file" ] || continue
  TARGET_FILES+=("$target_file")
done < "$TARGET_FILES_TXT"

if [ "${#TARGET_FILES[@]}" -eq 0 ]; then
  echo "No target files to stage." >&2
  exit 1
fi

if [ -z "$COMMIT_MESSAGE" ]; then
  if [ -n "${TARGET_TRANSLATION_PR_URL:-}" ]; then
    COMMIT_MESSAGE="docs: sync translation for #$SOURCE_PR_NUMBER"
  else
    COMMIT_MESSAGE="docs: translate #$SOURCE_PR_NUMBER"
  fi
fi

git -C "$TARGET_REPO_DIR" status --short -- "${TARGET_FILES[@]}"
git -C "$TARGET_REPO_DIR" add -- "${TARGET_FILES[@]}"

if git -C "$TARGET_REPO_DIR" diff --cached --quiet; then
  echo "No staged changes for the translation PR." >&2
  exit 1
fi

git -C "$TARGET_REPO_DIR" commit -m "$COMMIT_MESSAGE"
git -C "$TARGET_REPO_DIR" push -u origin "$NEW_BRANCH_NAME"

if [ -n "${TARGET_TRANSLATION_PR_URL:-}" ]; then
  TARGET_PR_URL="$TARGET_TRANSLATION_PR_URL"
  TARGET_PR_NUMBER="${TARGET_PR_URL##*/}"
  UPDATE_PAYLOAD="$(mktemp "${TMPDIR:-/tmp}/translation-pr-update.XXXXXX.json")"
  python3 - <<'PY' "$SOURCE_TITLE" "$TRANSLATION_BODY_MD" "$UPDATE_PAYLOAD"
import json
import pathlib
import sys

title = sys.argv[1]
body_path = pathlib.Path(sys.argv[2])
output_path = pathlib.Path(sys.argv[3])
payload = {
    "title": title,
    "body": body_path.read_text(encoding="utf-8"),
}
output_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
PY
  gh api --method PATCH "repos/$TARGET_REPO_OWNER/$TARGET_REPO_NAME/pulls/$TARGET_PR_NUMBER" \
    --input "$UPDATE_PAYLOAD" >/dev/null
  rm -f "$UPDATE_PAYLOAD"
else
  TARGET_PR_URL="$(
    gh pr create \
      --repo "$TARGET_REPO_OWNER/$TARGET_REPO_NAME" \
      --base "$BASE_BRANCH" \
      --head "$MY_LOGIN:$NEW_BRANCH_NAME" \
      --title "$SOURCE_TITLE" \
      --body-file "$TRANSLATION_BODY_MD"
  )"
  TARGET_PR_NUMBER="${TARGET_PR_URL##*/}"
fi

LABEL_ARGS=()
while IFS= read -r label; do
  [ -n "$label" ] || continue
  LABEL_ARGS+=("-f" "labels[]=$label")
done < "$TRANSLATION_LABELS_TXT"

if [ "${#LABEL_ARGS[@]}" -gt 0 ]; then
  gh api --method POST "repos/$TARGET_REPO_OWNER/$TARGET_REPO_NAME/issues/$TARGET_PR_NUMBER/labels" \
    "${LABEL_ARGS[@]}" >/dev/null
fi

if [ -n "${TARGET_TRANSLATION_PR_URL:-}" ]; then
  printf 'Updated translation PR: %s\n' "$TARGET_PR_URL"
else
  printf 'Created translation PR: %s\n' "$TARGET_PR_URL"
fi
