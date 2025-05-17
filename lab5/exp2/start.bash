#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ]; then
    echo "Нужно указать N и K"
    exit 1
fi

N=$1
K=$2

counter=0

while [ "$counter" -lt "$K" ]; do
    ./newmem.bash "$N" > "exp_2_report$counter.log" 2>&1 &
    sleep 1
    ((counter++))
done