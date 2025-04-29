./worker.sh & pid1=$!
./worker.sh & pid2=$!
./worker.sh & pid3=$!

echo "Запущены процессы: $pid1, $pid2, $pid3"