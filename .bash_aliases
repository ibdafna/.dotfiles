alias m="micromamba"
alias lll="ls -alt"
alias rshl="source ~/.bashrc"
alias k="kubectl"
alias n="nvim"

# Cleanup
alias drm="docker rm -vf $(docker ps -aq)"
alias drmi="docker rmi -f $(docker images -aq)"
alias gcb="git branch | grep -v 'main\|master' | xargs git branch -D"

# Very personal
alias mc="mv"
alias fir="git"

# Convenience
alias ghc="/home/idafna/ghcopilot/node_modules/.bin/github-copilot-cli"

# Conda classic
alias conda="/home/idafna/micromamba/envs/theia/bin/conda"
