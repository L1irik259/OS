#!/bin/bash

if [ -z "$1" ]; then
    echo "Нужно указать N"
    exit 1
fi

N=$1
arr=()
step=0

while true; do
    arr+=(1 2 3 4 5 6 7 8 9 10)

    ((step++))

    if (( ${#arr[@]} > N )); then
        echo "$$" >> "finished.log"
        exit 0
    fi

    if ((step % 100000 == 0)); then
        echo "Step $step: Array size is ${#arr[@]}"
    fi
done