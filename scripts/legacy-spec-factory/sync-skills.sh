#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT/skills"

usage() {
  cat <<'USAGE'
Usage:
  scripts/sync-skills.sh [--target all|claude|opencode|agents|codex] [--skill name] [--check]

Copies canonical skills from skills/<name>/ into runtime adapter folders.
Adapter-only files named *.adapter.md or placed under runtime-overrides/ are
preserved during sync and ignored during drift checks.

Targets:
  claude    .claude/skills
  opencode  .opencode/skills
  agents    .agents/skills
  codex     .codex/skills
  all       all targets

Options:
  --skill   sync or check one skill directory by name
  --check   report drift without copying
USAGE
}

target="all"
check="no"
skill_filter=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      target="${2:-}"
      shift 2
      ;;
    --check)
      check="yes"
      shift
      ;;
    --skill)
      skill_filter="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "No canonical skills directory found: $SOURCE_DIR" >&2
  exit 1
fi

target_dirs=()
case "$target" in
  claude) target_dirs+=("$ROOT/.claude/skills") ;;
  opencode) target_dirs+=("$ROOT/.opencode/skills") ;;
  agents) target_dirs+=("$ROOT/.agents/skills") ;;
  codex) target_dirs+=("$ROOT/.codex/skills") ;;
  all)
    target_dirs+=("$ROOT/.claude/skills")
    target_dirs+=("$ROOT/.opencode/skills")
    target_dirs+=("$ROOT/.agents/skills")
    target_dirs+=("$ROOT/.codex/skills")
    ;;
  *)
    echo "Invalid target: $target" >&2
    usage
    exit 2
    ;;
esac

shopt -s nullglob
if [[ -n "$skill_filter" ]]; then
  if [[ ! -d "$SOURCE_DIR/$skill_filter" ]]; then
    echo "No such skill: $skill_filter" >&2
    exit 1
  fi
  skill_dirs=("$SOURCE_DIR/$skill_filter")
else
  skill_dirs=("$SOURCE_DIR"/*)
fi

if [[ ${#skill_dirs[@]} -eq 0 ]]; then
  echo "No skills found under $SOURCE_DIR"
  exit 0
fi

status=0

for skill_dir in "${skill_dirs[@]}"; do
  [[ -d "$skill_dir" ]] || continue
  skill_name="$(basename "$skill_dir")"
  if [[ ! -f "$skill_dir/SKILL.md" ]]; then
    echo "Skipping $skill_name: missing SKILL.md" >&2
    status=1
    continue
  fi

  for target_dir in "${target_dirs[@]}"; do
    dest="$target_dir/$skill_name"
    if [[ "$check" == "yes" ]]; then
      if [[ ! -d "$dest" ]]; then
        echo "DRIFT missing: $dest"
        status=1
      elif ! diff -qr \
        -x '.DS_Store' \
        -x '__pycache__' \
        -x '*.adapter.md' \
        -x 'runtime-overrides' \
        -x '.runtime' \
        "$skill_dir" "$dest" >/dev/null; then
        echo "DRIFT changed: $dest"
        status=1
      else
        echo "OK: $dest"
      fi
    else
      mkdir -p "$dest"
      rsync -a --delete \
        --exclude '.DS_Store' \
        --exclude '__pycache__/' \
        --exclude '*.adapter.md' \
        --exclude 'runtime-overrides/' \
        --exclude '.runtime/' \
        "$skill_dir/" "$dest/"
      echo "Synced $skill_name -> $dest"
    fi
  done
done

exit "$status"
