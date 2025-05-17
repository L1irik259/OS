#!/bin/bash

PID_FILE=".pid"

echo $$ > "$PID_FILE"

arr=()
step=0

while true; do
    ((step++))

    arr+=(1 2 3 4 5 6 7 8 9 10)

    if ((step % 100000 == 0)); then
        echo "Step $step: Array size ${#arr[@]}" >> report.log
    fi
done
