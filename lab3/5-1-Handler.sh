current_value=1

(tail -f pipi) |
 while true; do
    read input
    if [[ $input == "+" ]]; then
        mode="addition"
    elif [[ $input == "*" ]]; then
        mode="multiplication"
    elif [[ $input =~ ^[0-9]+$ ]]; then
      if [[ $mode == "addition" ]]; then
        current_value=$((current_value + input))
      elif [[ $mode == "multiplication" ]]; then
         current_value=$((current_value * input))
      fi
    elif [[ $input == "QUIT" ]]; then
        echo "Плановая остановка."
        pkill -f script5Generator
        break
    else
        echo "Ошибка: неверный ввод."
        echo $input
        pkill -f script5Generator
        break
    fi
 done