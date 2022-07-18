#!/bin/bash

set -e

mkdir $1/skeletons
echo "$1/nturgbd_skeletons_s001_to_s017.zip $1/nturgbd_skeletons_s018_to_s032.zip" \
    | xargs -n 1 -P 2 unzip -d $1/skeletons

echo $1/skeletons/nturgb+d_skeletons/* | xargs mv -t $1/skeletons --
rmdir $1/skeletons/nturgb+d_skeletons
