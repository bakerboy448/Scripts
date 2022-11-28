# WTF Service
alias wtf='sudo journalctl --since today -u '
alias wtfy='sudo journalctl --since yesterday -u '
#Useful
alias untar='tar -zxvf '
alias wget='wget -c '
alias sha='shasum -a 256 '
alias ping='ping -c 5'
alias speed='speedtest-cli --server 2406 --simple'
alias wgetc='wget --content-disposition '
alias lt='ls --human-readable --size -1 -S --classify'
alias c='clear'
alias gh='history|grep'
# Systemd alias
alias sysstatus='sudo systemctl status'
alias sysenable='sudo systemctl enable'
alias sysdisable='sudo systemctl disable'
alias sysstart='sudo systemctl start'
alias sysstop='sudo systemctl stop'
alias sysreload='sudo systemctl daemon-reload'
alias sshrestart='# /etc/init.d/ssh restart'
alias systatus='sysstatus'
alias systart='sysstart'
alias systop='sysstop'
alias syreload='sysreload'
# Git Aliases
alias startgit='cd `git rev-parse --show-toplevel` && git checkout master && git pull'