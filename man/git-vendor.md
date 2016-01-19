git-vendor(1) -- manage vendored dependency subtrees
================================

## SYNOPSIS

`git-vendor add <repository> <ref>`

`git-vendor list`

`git-vendor update <dir> <ref>`

## DESCRIPTION

  Manage any repository dependencies under `/vendor/<repository>` with `git-subtree`.

  `git-vendor` is unable to `list` or `update` any dependencies it has not added, the reason is that `git-vendor` adds special commit messages so that it can track existing dependencies.

## COMMANDS

  add &lt;repository&gt; &lt;ref&gt;

  Add a new vendored dependency

  list

  List all existing vendored dependencies and their current version

  update &lt;dir&gt; &lt;ref&gt;

  Update the vendored dependency to a different version


## OPTIONS

  &lt;repository&gt;

  The repository url to vendor. e.g. `https://github.com/<username>/<repo-name>` (supports `http://`, `https://` `git://` and `git@` protocols).

  &lt;ref&gt;

  The ref to vendor. e.g. `master`, `v1.0.2`, etc

  &lt;dir&gt;

  The vendor directory for the dependency. e.g. `vendor/github.com/<username>/<repo-name>`.

## EXAMPLES

  Adding a new dependency:

    $ git vendor add https://github.com/brettlangdon/forge v0.1.4

  Updating an existing dependency:

    $ git vendor update vendor/github.com/brettlangdon/forge v0.1.7

  List all existing dependencies:

    $ git vendor list

## AUTHOR

Written by Brett Langdon <me@brett.is>

## REPORTING BUGS

&lt;<https://github.com/brettlangdon/git-vendor/issues>&gt;

## SEE ALSO

&lt;<https://github.com/brettlangdon/git-vendor>&gt;
