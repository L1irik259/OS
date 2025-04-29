amount=()

awk -F: '{sub("Parent_ProcessID=","",$2); sub("Average_Running_Time=","",$3); print $2, $3}' sorted |
        awk -F" " '{sum[$1]+=$2; amount[$1]++} END {for (i in sum){ amount[i]=sum[i]/amount[i]; print(i, amount[i])}};'>
while IFS= read -r line; do
        key=${line%% *}
        value=${line#* }
        amount[$key]=$value
done <temp_file

rm temp_file
while IFS=: read -r f1 f2 rest; do

        if [[ $f2 == " Parent_ProcessID= " ]]; then
                continue
        fi

        if [[ $f2 != $prev ]]; then
                echo "${prev} is ${amount[$prev]}" >>newSorted
        fi
        echo "$f1:$f2:$rest" >>newSorted
        prev=$f2
done <sorted
