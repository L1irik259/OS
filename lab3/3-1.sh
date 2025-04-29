mkdir ~/test && echo "catalog test was created successfully" >> ~/report && touch ~/test/$(date +%Y-%m-%d_%H-%M-%S)

ping net_nikogo.ru > /dev/null || echo "$(date +"%Y-%m-%d %H:%M:%S") Want full" >> ~/report