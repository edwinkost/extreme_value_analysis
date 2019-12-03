#!/bin/bash

echo "Arg 0: $0"
echo "Arg 1: $1"
echo "Arg 2: $2"
echo "Arg 3: $3"

for arg in "$@"
do
    echo "$arg"
done

set -x

INP_DIRECTORY=$1
INP_FILE_NAME=$2

OUT_DIRECTORY=$3
OUT_FILE_NAME=${INP_FILE_NAME}

cd ${INP_DIRECTORY}
dmget -a ${INP_FILE_NAME}

mkdir -p ${OUT_DIRECTORY}
cd ${OUT_DIRECTORY}

rsync -r --size-only --progress ${INP_DIRECTORY}/${INP_FILE_NAME} .

# for double checking
rsync -r --size-only --progress ${INP_DIRECTORY}/${INP_FILE_NAME} .

# make the list of tar file
module load p7zip
7za l ${OUT_FILE_NAME} > 7za-l_${OUT_FILE_NAME}.txt

set +x
