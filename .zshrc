export TERM="xterm-256color"



if [ -f ~/.zsh_aliases ]; then
    . ~/.zsh_aliases
fi

if [ -f ~/.zsh_ext ]; then
    . ~/.zsh_ext
fi

# >>> mamba initialize >>>
# !! Contents within this block are managed by 'mamba init' !!
export MAMBA_EXE="/opt/homebrew/bin/micromamba";
export MAMBA_ROOT_PREFIX="/Users/idafna/micromamba";
__mamba_setup="$("$MAMBA_EXE" shell hook --shell zsh --prefix "$MAMBA_ROOT_PREFIX" 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__mamba_setup"
else
    if [ -f "/Users/idafna/micromamba/etc/profile.d/micromamba.sh" ]; then
        . "/Users/idafna/micromamba/etc/profile.d/micromamba.sh"
    else
        export  PATH="/Users/idafna/micromamba/bin:$PATH"  # extra space after export prevents interference from conda init
    fi
fi
unset __mamba_setup
# <<< mamba initialize <<<

source /Users/idafna/.docker/init-zsh.sh || true # Added by Docker Desktop

# Activate default conda environment
m activate base

# Add copilot CLI to path
export PATH=/Users/idafna/.local/bin/:$PATH
export PATH=$PATH:/Users/idafna/.pixi/bin
export PATH=/opt/homebrew/bin:$PATH
export EDITOR=nvim

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

eval "$(starship init zsh)"

# Added by Windsurf
export PATH="/Users/idafna/.codeium/windsurf/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
[ -f $HOME/.sbn_aliases ] && source $HOME/.sbn_aliases
