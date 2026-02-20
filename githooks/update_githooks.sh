#!/usr/bin/env bash
# Update our githooks.

REPO_ROOT=$(git rev-parse --show-toplevel)
src_dir="${REPO_ROOT}/githooks/"
dest_dir="${REPO_ROOT}/.git/hooks"

cp $src_dir/* $dest_dir