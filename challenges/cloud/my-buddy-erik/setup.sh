#!/bin/sh

set -eu

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <REMOTE_URL>"
    echo "This script sets up a remote GitHub repository for the challenge."
    echo "REMOTE_URL should be an SSH url for authentication purposes."
    exit 1
fi

tarball="git.tar"
remote_url="$1"

rootdir="$(pwd)"
cleanup() {
    cd "$rootdir"
    rm -rf repo worktree
}
trap cleanup EXIT

mkdir repo
tar -xf $tarball -C repo
git clone repo worktree

cd worktree

git switch original
git switch fixed
git remote set-url origin "$remote_url"
git switch main

# first push doesn't list commits, it's a CreateEvent
git reset --hard "$(git rev-list --max-parents=0 original)"
git push

git reset --hard original
git push -f

git reset --hard fixed
git push -f

cd ..
# cleanup() is called on EXIT
