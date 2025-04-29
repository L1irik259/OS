for pid in $(ls /proc | grep -E '^[0-9]+$'); do
        ppid=$(cat "/proc/$pid/status" | grep "PPid:" | cut -d':' -f2- | awk '{print $1}')
        runtime=$(cat "/proc/$pid/sched" | grep "se.sum_exec_runtime" | cut -d':' -f2- | awk '{print $1}')
        switches=$(cat "/proc/$pid/sched" | grep "nr_switches" | cut -d':' -f2- | awk '{print $1}')
        ART=$(bc <<<"scale=3;$runtime/$switches")
        echo "$pid:$ppid:$ART" >>tmp
done

sort -t ':' -k2n tmp |
        awk -F":" '{print "Process_ID=" $1 " : ""Parent_ProcessID=" $2 " : ""Average_Running_Time=" $3}' >>sorted
rm tmp