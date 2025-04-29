while true; do
  read LINE;
  case $LINE in 
    "+")
      kill -SIGUSR1 $(cat .pid)
      ;;
    "*")
      kill -SIGUSR2 $(cat .pid)
      ;;
    *TERM*)
      kill -SIGTERM $(cat .pid)
      exit 0
      ;;
    *)
  esac
done