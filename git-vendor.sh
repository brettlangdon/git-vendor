#!/bin/sh
#
# git-vendor.sh: manage vendored repos via git-subtree
#
# Copyright (C) 2016 Brett Langdon <me@brett.is>
#
if [ $# -eq 0 ];
then
    set -- -h
fi

OPTS_SPEC="\
git vendor add <repository> <ref>
git vendor list
git vendor update <repository> <ref>
--
"
eval "$(echo "$OPTS_SPEC" | git rev-parse --parseopt -- "$@" || echo exit $?)"

PATH=$PATH:$(git --exec-path)
. git-sh-setup

require_work_tree

while [ $# -gt 0 ]; do
	opt="$1"
	shift
	case "$opt" in
		--) break ;;
		*) die "Unexpected option: $opt" ;;
	esac
done

command="$1"
shift
case "$command" in
    add|list|update) ;;
    *) die "Unknown command '$command'" ;;
esac

cmd_add()
{
    repository="$1"
    ref="$2"
    if [ $# -ne 2 ];
    then
        die "Incorrect options provided: git vendor add <repository> <ref>"
    fi

    dir="vendor/$(echo "$repository" | sed -E 's/^[a-zA-Z]+((:\/\/)|@)//' | sed 's/:/\//' | sed -E 's/\.git$//')"
    message="\
Add '$dir/' from '$repository $ref'

git-subtree-repository: $repository
git-subtree-ref: $ref
"
    git subtree add --prefix "$dir" --message "$message" "$repository" "$ref"
}

cmd_list()
{
    die "Not implemented"
}

cmd_update()
{
    die "Not implemented"
}

"cmd_$command" "$@"
