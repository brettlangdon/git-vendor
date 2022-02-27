git-vendor(1) -- manage vendored dependency subtrees
================================

## SYNOPSIS

`git-vendor add [--prefix <dir>] <name> <repository> [<ref>]`

`git-vendor list [<name>]`

`git-vendor remove <name>`

`git-vendor update <name> [<ref>]`

`git-vendor upstream <name> [<ref>]`

## DESCRIPTION

  Manage any repository dependencies with `git-subtree`.

  `git-vendor` follows the same vendoring pattern that is used in the Go community. Dependencies are stored under `vendor/<repository_uri>`. For example, the dependency of `https://github.com/brettlangdon/forge.git` will be stored under `vendor/github.com/brettlangdon/forge` by default.

  `git-vendor` is unable to `list`, `update` or `upstream` any dependencies it has not added, the reason is that `git-vendor` adds special commit messages so that it can track existing dependencies.

## COMMANDS

  add [--prefix &lt;dir&gt;] &lt;name&gt; &lt;repository&gt; [&lt;ref&gt;]

  Add a new vendored dependency

  list [&lt;name&gt;]

  List all existing vendored dependencies and their current version. Limit show dependency to `<name>` if provided.

  remove &lt;name&gt;

  Remove the named vendored dependency.

  update &lt;dir&gt; &lt;ref&gt;

  Update the vendored dependency to a different version.

  upstream &lt;dir&gt; &lt;ref&gt;

  Push the vendored dependency changes to the source repository.


## OPTIONS

  --prefix &lt;dir&gt;

  Directory to pull dependencies in under (e.g. `vendor` or `third_party`, etc). [default: `vendor`]

  &lt;name&gt;

  A name to provide the vendored dependency to use when listing/updating/pushing.

  &lt;repository&gt;

  The repository url to vendor. e.g. `https://github.com/<username>/<repo-name>` (supports `http://`, `https://` `git://` and `git@` protocols).

  &lt;ref&gt;

  The ref to vendor. e.g. `master`, `v1.0.2`, etc. [default: `master`]

## EXAMPLES

  Adding a new dependency at a specific git tagged version:

    $ git vendor add forge https://github.com/brettlangdon/forge v0.1.4

  Adding a new dependency under a different directory than `vendor/`:

    $ git vendor add --prefix third_party forge https://github.com/brettlangdon/forge

  Updating an existing dependency to a specific git tagged version:

    $ git vendor update forge  v0.1.7

  Updating a dependency to `master`:

    $ git vendor update forge

  Upstream changes to the source repository to `master`:

    $ git vendor upstream forge

  Upstream changes to the source repository to a (new) branch my_changes:

    $ git vendor upstream forge my_changes

  Upstream changes to another repository to `master`:

    $ git vendor upstream forge --repo https://github.com/user/another.git

  Upstream changes to another repository to a (new) branch my_changes:

    $ git vendor upstream forge my_changes --repo https://github.com/user/another.git

  Removing a dependency:

    $ git vendor remove forge

  List all existing dependencies:

    $ git vendor list

## AUTHOR

Written by Brett Langdon <me@brett.is>

## REPORTING BUGS

&lt;<https://github.com/brettlangdon/git-vendor/issues>&gt;

## SEE ALSO

&lt;<https://github.com/brettlangdon/git-vendor>&gt;
