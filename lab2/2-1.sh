if ! id -u "root" &>/dev/null; then
    echo "Ошибка: пользователь 'user' не существует" >&2
    exit 1
fi
count=$(ps -u user --no-headers | wc -l)
echo "Количество процессов пользователя user: $count" > answer-1.txt
ps -u root -o pid= -o comm= | awk '{print $1 ":" $2}' >> answer-1.txt