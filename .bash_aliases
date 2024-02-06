# General System Utilities
alias c='clear'
alias gh='history|grep'
alias lt='ls --human-readable --size -1 -S --classify'
alias sha='shasum -a 256 '
alias sshrestart='sudo /etc/init.d/ssh restart'

# Network and File Download
alias ping='ping -c 5'
alias wget='wget -c '
alias wgetc='wget --content-disposition '

# Journal and Logging
alias wtf='sudo journalctl --since today -u '
alias wtfy='sudo journalctl --since yesterday -u '

# Systemd Services Management
alias sysdisable='sudo systemctl disable'
alias sysenable='sudo systemctl enable'
alias sysreload='sudo systemctl daemon-reload'
alias sysstart='sudo systemctl start'
alias sysstatus='sudo systemctl status'
alias sysstop='sudo systemctl stop'

# Archive and Compression
alias untar='tar -zxvf '

# Network Testing
alias speed='speedtest-cli --server 2406 --simple'

# Docker Management
alias dcdown='docker-compose down'
alias dcup='docker-compose up'
alias dexec='docker exec -it'
alias dockerclean='docker rm $(docker ps -a -q)'
alias dockerdu='docker system df'
alias dockerls='docker ps -a'
alias docker-rmi-untagged='docker rmi $(docker images | grep "^<none>" | awk "{print \$3}")'
alias dockerstopall='docker stop $(docker ps -a -q)'
alias dlogs='docker logs'

# Development and Git
alias startgit='cd `git rev-parse --show-toplevel` && git checkout master && git pull'
