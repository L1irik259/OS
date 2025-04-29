echo $$ > .pid

current_value=1

usr1(){
  current_value=$((current_value + 2))
  echo $current_value
}

usr2(){
  current_value=$((current_value * 2))
  echo $current_value
}

sigterm(){
 echo "Получен сигнал SIGTERM, завершаю работу..."
 exit 0
}


trap 'usr1' USR1
trap 'usr2' USR2
trap 'sigterm' SIGTERM
while true; do 
  sleep 1
done