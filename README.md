git-vendor
==========
A git command for managing vendored dependencies.

`git-vendor` is a wrapper around `git-subtree` commands for checking out and updating vendored dependencies.

By default `git-vendor` conforms to the pattern used for vendoring golang dependencies:

* Dependencies are stored under `vendor/` directory in the repo.
* Dependencies are stored under the fully qualified project path.
    * e.g. `https://github.com/brettlangdon/forge` will be stored under `vendor/github.com/brettlangdon/forge`.

## Usage
See https://brettlangdon.github.io/git-vendor for the current MAN page documentation.

`git-vendor` provides the following commands:

* `git vendor add [--prefix <dir>] <name> <repository> [<ref>]` - add a new vendored dependency.
* `git vendor list [<name>]` - list current vendored dependencies, their source, and current vendored ref.
* `git vendor update <name> [<ref>]` - update a vendored dependency.

## Installation
Manually:

```bash
git clone https://github.com/brettlangdon/git-vendor
cd ./git-vendor
make
```

One-liner:
```bash
curl -sSL https://git.io/vzN5m | sudo bash /dev/stdin
```

[Homebrew](http://brew.sh) (thanks to @liamstask):
```bash
brew install git-vendor
```

## Example

```bash
$ # Checkout github.com/brettlangdon/forge@v0.1.6 under vendor/github.com/brettlangdon/forge
$ git vendor add forge https://github.com/brettlangdon/forge v0.1.6
+ git subtree add --prefix vendor/github.com/brettlangdon/forge --message 'Add "forge" from "https://github.com/brettlangdon/forge@v0.1.6"

git-vendor-name: forge
git-vendor-dir: vendor/github.com/brettlangdon/forge
git-vendor-repository: https://github.com/brettlangdon/forge
git-vendor-ref: v0.1.6
' https://github.com/brettlangdon/forge v0.1.6 --squash
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
forge@v0.1.6:
	name:	forge
	dir:	vendor/github.com/brettlangdon/forge
	repo:	https://github.com/brettlangdon/forge
	ref:	v0.1.6
	commit:	3335840c5f0ad9e821006588f1b16a3385d9c318

$ # Update existing dependency to a newer version
$ git vendor update forge v0.1.7
From https://github.com/brettlangdon/forge
 * tag               v0.1.7     -> FETCH_HEAD
Merge made by the 'recursive' strategy.
 vendor/github.com/brettlangdon/forge/forge_test.go | 2 ++
 vendor/github.com/brettlangdon/forge/scanner.go    | 4 ++++
 vendor/github.com/brettlangdon/forge/test.cfg      | 1 +
 3 files changed, 7 insertions(+)

$ # List current vendored dependencies
$ git vendor list
forge@v0.1.7:
	name:	forge
	dir:	vendor/github.com/brettlangdon/forge
	repo:	https://github.com/brettlangdon/forge
	ref:	v0.1.7
	commit:	071c5f108e0af39bf67a87fc766ea9bfb72b9ee7

```
