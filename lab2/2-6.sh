maxMem=0
maxPid=0
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
        memory=$(cat "/proc/$pid/status" | grep "VmSize" | cut -d':' -f2 | awk '{print $1}')
        if [[ "$memory" -gt "$maxMem" ]]; then
                maxMem=$memory
                maxPid=$pid
        fi
done

echo "$pid":"$maxMem"
