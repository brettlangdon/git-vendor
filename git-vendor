#!/bin/sh
#
# git-vendor.sh: manage vendored repos via git-subtree
#
# Copyright (c) 2016 Brett Langdon <me@brett.is>
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

vendor_dirs_from_log()
{
    dir=
    git log --grep="^git-vendor-dir: vendor/.*\$" \
	--pretty=format:'START %H%n%s%n%n%b%nEND%n' HEAD |
	while read a b junk; do
	    case "$a" in
		START) ;;
		git-vendor-dir:) dir="$b" ;;
		END)
                    echo "$dir"
                    dir=
                    ;;
	    esac
	done
}

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

git-vendor-dir: $dir
git-vendor-repository: $repository
git-vendor-ref: $ref
"
    git subtree add --prefix "$dir" --message "$message" "$repository" "$ref" --squash
}

cmd_list()
{
    vendorDirs=($(vendor_dirs_from_log | sort -u))
    for dir in "${vendorDirs[@]}";
    do
    git log -1 --grep="^git-vendor-dir: $dir\$" \
	--pretty=format:'START %H%n%s%n%n%b%nEND%n' HEAD |
	while read a b junk; do
	    case "$a" in
		START) commit="$b" ;;
                git-vendor-dir:) dir="$b" ;;
                git-vendor-ref:) ref="$b" ;;
		git-vendor-repository:) repository="$b" ;;
		END)
                    if [[ ! -z "$repository" ]];
                    then
                        echo "$dir"
                        echo "\tcommit:\t$commit"
                        echo "\tdir:\t$dir"
                        echo "\tref:\t$ref"
                        echo "\trepo:\t$repository"
                        echo ""
                    fi
                    dir=
                    ref=
                    commit=
                    repository=
                    ;;
	    esac
	done
    done;

}

cmd_update()
{
    dir="$1"
    ref="$2"
    git log --grep="^git-vendor-dir: $dir\$" \
	--pretty=format:'START %H%n%s%n%n%b%nEND%n' HEAD |
	while read a b junk; do
	    case "$a" in
		START) ;;
		git-vendor-repository:) repository="$b" ;;
		END)
                    if [[ ! -z "$repository" ]];
                    then
                        message="\
Update '$dir/' from '$repository $ref'

git-vendor-dir: $dir
git-vendor-repository: $repository
git-vendor-ref: $ref
"
                        git subtree pull --prefix "$dir" --message "$message" "$repository" "$ref" --squash
                        break
                    fi
                    ;;
	    esac
	done
}

"cmd_$command" "$@"
