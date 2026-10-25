#!/usr/bin/env bash
set -e

# Keep the checkout separate from other users' files in the system temp area.
# The trap removes this directory after success or failure.
install_dir=$(mktemp -d "${TMPDIR:-/tmp}/git-vendor.XXXXXX")
trap 'rm -rf "$install_dir"' EXIT

git clone https://github.com/brettlangdon/git-vendor "$install_dir" &> /dev/null
cd "$install_dir"
make install
