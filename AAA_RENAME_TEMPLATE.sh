#!/usr/bin/env bash
#
# AAA_RENAME_TEMPLATE.sh
#
# One-shot setup for this template. Prompts for the new module/dist/repo names,
# rewrites every reference, renames the package dir, drops template-only files,
# resyncs the venv, rebuilds the frontend, and re-inits git with a fresh initial commit.
#
# Run once from the repo root, then this script deletes itself.

set -euo pipefail

cd "$(dirname "$0")"
SCRIPT_NAME="$(basename "$0")"

# --- placeholders in this template ------------------------------------------
OLD_MODULE="my_cool_app"
OLD_DIST="my-cool-app"
OLD_REPO="kism/fastapi-boilerplate"

# --- helpers ---------------------------------------------------------------
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

prompt() {
	# prompt <varname> <message> <regex> <default>
	local __var=$1 __msg=$2 __re=$3 __default=${4:-} __val
	while :; do
		if [ -n "$__default" ]; then
			read -r -p "$__msg [$__default]: " __val
			__val=${__val:-$__default}
		else
			read -r -p "$__msg: " __val
		fi
		if [ -z "$__val" ]; then
			echo "  value required" >&2
		elif ! printf '%s' "$__val" | grep -Eq "$__re"; then
			echo "  '$__val' does not match $__re" >&2
		else
			printf -v "$__var" '%s' "$__val"
			return 0
		fi
	done
}

# --- sanity checks -------------------------------------------------------
command -v git >/dev/null || die "git not found"
command -v perl >/dev/null || die "perl not found"
[ -d .git ] || die "not a git repo (run from the template root)"
git grep -q "$OLD_MODULE" -- . ":(exclude)$SCRIPT_NAME" \
	|| die "no '$OLD_MODULE' references found - already renamed?"

# --- gather variables --------------------------------------------------
echo "Renaming this template. Answer three prompts:"
echo
prompt NEW_MODULE "Python module name (snake_case)"       '^[a-z][a-z0-9_]*$'
prompt NEW_DIST   "Package / dist name (kebab-case)"      '^[a-z][a-z0-9-]*$' "${NEW_MODULE//_/-}"
prompt NEW_REPO   "GitHub repo (<user>/<repo>)"           '^[^/[:space:]]+/[^/[:space:]]+$'

echo
echo "  module : $OLD_MODULE  ->  $NEW_MODULE"
echo "  dist   : $OLD_DIST  ->  $NEW_DIST"
echo "  repo   : $OLD_REPO  ->  $NEW_REPO"
echo
read -r -p "Proceed? This rewrites files and wipes git history. [y/N]: " ans
case "$ans" in
	[yY] | [yY][eE][sS]) ;;
	*) die "aborted" ;;
esac

# --- rewrite references ------------------------------------------------
# names are passed through the environment so perl never parses them as code
export OLD_MODULE OLD_DIST OLD_REPO NEW_MODULE NEW_DIST NEW_REPO
# shellcheck disable=SC2016  # the single-quoted body below is perl, not shell
git grep -lz -e "$OLD_MODULE" -e "$OLD_DIST" -e "$OLD_REPO" \
		-- . ":(exclude)$SCRIPT_NAME" \
	| xargs -0 perl -pi -e '
		s{\Q$ENV{OLD_MODULE}\E}{$ENV{NEW_MODULE}}g;
		s{\Q$ENV{OLD_DIST}\E}{$ENV{NEW_DIST}}g;
		s{\Q$ENV{OLD_REPO}\E}{$ENV{NEW_REPO}}g;
	'

# --- rename the package dir ------------------------------------------
if [ "$NEW_MODULE" != "$OLD_MODULE" ]; then
	git mv "src/$OLD_MODULE" "src/$NEW_MODULE"
fi

# --- drop template-only bits ----------------------------------------
rm -f .github/workflows/dependabot_automerge.yml

# --- strip the "Using this template" section from the README --------
if [ -f README.md ]; then
	perl -0pi -e 's/^## Using this template\b.*?^Then delete this section\.\n\n//ms' README.md
fi

# --- resync the environment ---------------------------------------
rm -rf .venv ./*.egg-info src/*.egg-info
if command -v uv >/dev/null; then
	uv sync --all-groups
else
	echo "note: uv not found - run 'uv sync --all-groups' yourself" >&2
fi

# --- rebuild the frontend (openapi.json carries the dist name) -----
if command -v pnpm >/dev/null && command -v uv >/dev/null; then
	pnpm install
	pnpm run all
else
	echo "note: pnpm/uv not found - run 'pnpm install && pnpm run all' yourself" >&2
fi

# --- fresh git history ------------------------------------------
rm -f "$SCRIPT_NAME"
rm -rf .git
git init -q
git add -A
git commit -qm "Initial commit"

echo
echo "Done. '$NEW_MODULE' is ready. Set the remote with:"
echo "  git remote add origin git@github.com:$NEW_REPO.git"
