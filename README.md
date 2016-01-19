git-vendor
==========
A work in progress git command for managing golang vendor dependencies.

`git-vendor` is a wrapper around `git-subtree` commands for checking out and updating vendored dependencies.

`git-vendor` provides the following commands:

* `git vendor add <repository> <ref>` - add a new vendored dependency in `vendor/`
* `git vendor list` - list all current vendored dependencies, their source, and current vendored ref.
* `git vendor update <dir> <ref>` - update a vendored dependency to `<ref>`.

## Installation
Manually:

```bash
git clone https://github.com/brettlangdon/git-vendor
cd ./git-vendor
make
```

One-liner:
```bash
curl -sSL https://git.io/vz8AK | sudo bash /dev/stdin
```

## Example

```bash
$ # Checkout github.com/brettlangdon/forge@v0.1.6 under vendor/github.com/brettlangdon/forge
$ git vendor add https://github.com/brettlangdon/forge v0.1.6
git fetch https://github.com/brettlangdon/forge v0.1.6
warning: no common commits
remote: Counting objects: 405, done.
remote: Total 405 (delta 0), reused 0 (delta 0), pack-reused 404
Receiving objects: 100% (405/405), 68.31 KiB | 0 bytes/s, done.
Resolving deltas: 100% (227/227), done.
From https://github.com/brettlangdon/forge
 * tag               v0.1.6     -> FETCH_HEAD
Added dir 'vendor/github.com/brettlangdon/forge'
$ # List current vendored dependencies
$ git vendor list
vendor/github.com/brettlangdon/forge
	commit:	a7afbba3821d74c5b722c9195b954effa3d7420f
	dir:	vendor/github.com/brettlangdon/forge
	ref:	v0.1.6
	repo:	https://github.com/brettlangdon/forge

$ # Update existing dependency to a newer version
$ git vendor update vendor/github.com/brettlangdon/forge v0.1.7
warning: no common commits
remote: Counting objects: 411, done.
remote: Total 411 (delta 0), reused 0 (delta 0), pack-reused 410
Receiving objects: 100% (411/411), 68.91 KiB | 0 bytes/s, done.
Resolving deltas: 100% (231/231), done.
From https://github.com/brettlangdon/forge
 * tag               v0.1.7     -> FETCH_HEAD
Merge made by the 'recursive' strategy.
 vendor/github.com/brettlangdon/forge/forge_test.go | 2 ++
 vendor/github.com/brettlangdon/forge/scanner.go    | 4 ++++
 vendor/github.com/brettlangdon/forge/test.cfg      | 1 +
 3 files changed, 7 insertions(+)
$ # List current vendored dependencies
$ git vendor list
vendor/github.com/brettlangdon/forge
	commit:	fcaa3c0cf3792fe3ad724c43d6db75f06fc5ecd5
	dir:	vendor/github.com/brettlangdon/forge
	ref:	v0.1.7
	repo:	https://github.com/brettlangdon/forge

```
