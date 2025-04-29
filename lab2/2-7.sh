declare -A bytesRead

for pid in $(ls /proc | grep -E '^[0-9]+$'); do
        io_file="/proc/$pid/io"

        if [ -f "$io_file" ]; then
                bytes_read=$(grep "read_bytes" "$io_file" | awk '{print $2}')
                bytesRead["$pid"]=$bytes_read
        fi
done

sleep 60

for pid in $(ls /proc | grep -E '^[0-9]+$'); do
        io_file="/proc/$pid/io"

        if [ -f "$io_file" ]; then
                bytes_read=$(grep "read_bytes" "$io_file" | awk '{print $2}')
                current_bytes=${bytesRead["$pid"]}
                bytesRead["$pid"]=$((current_bytes - bytes_read))
        fi
done

sorted=($(for key in "${!bytesRead[@]}"; do
        echo "$key ${bytesRead[$key]}"
done | sort -rn -k2))