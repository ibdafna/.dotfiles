alias lll="ls -alt"
alias rshl="source ~/.bashrc"
alias k="kubectl"
alias n="nvim"

# Cleanup
alias gcb="git branch | grep -v 'main\|master' | xargs git branch -D"

drm() {
  command -v docker >/dev/null 2>&1 || return 0
  docker rm -vf $(docker ps -aq)
}

drmi() {
  command -v docker >/dev/null 2>&1 || return 0
  docker rmi -f $(docker images -aq)
}

# Very personal
alias mc="mv"
alias fir="git"
