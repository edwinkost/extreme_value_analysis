#!/bin/bash

echo "Arg 0: $0"
echo "Arg 1: $1"
echo "Arg 2: $2"

for arg in "$@"
do
    echo "$arg"
done

