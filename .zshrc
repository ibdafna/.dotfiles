export TERM="xterm-256color"

for dir in "$HOME/bin" "$HOME/.local/bin" "$HOME/.pixi/bin" "/opt/homebrew/bin"; do
    if [ -d "$dir" ]; then
        export PATH="$dir:$PATH"
    fi
done

if [ -f "$HOME/.zsh_aliases" ]; then
    . "$HOME/.zsh_aliases"
fi

if [ -f "$HOME/.zsh_ext" ]; then
    . "$HOME/.zsh_ext"
fi

# Used for git ops
export EDITOR=nvim

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
[ -f "$HOME/.sbn_aliases" ] && source "$HOME/.sbn_aliases"

if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi
