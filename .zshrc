#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

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
source /opt/homebrew/opt/spaceship/spaceship.zsh

source /Users/idafna/.docker/init-zsh.sh || true # Added by Docker Desktop

# Activate default conda environment
m activate base

# Add copilot CLI to path
export PATH=/Users/idafna/copilot-cli/node_modules/.bin/github-copilot-cli:$PATH

