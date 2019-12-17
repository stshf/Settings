
# Executes commands at the start of an interactive session.
#
# Authors:
#   Sorin Ionescu <sorin.ionescu@gmail.com>
#

# Source Prezto.
if [[ -s "${ZDOTDIR:-$HOME}/.zprezto/init.zsh" ]]; then
  source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"
fi

# Customize to your needs...
# path
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_CACHE_HOME="$HOME/.cache"

# list show
alias ls='ls -G'
alias ll='ls -l'
alias lla='ls -a'

# open google chrome
alias ggl='open -a google\ chrome'

# python3 
alias py='python3'

# vim -> nvim
alias vim="nvim"

# scp
alias cpfile="scp -P 60006 -i ~/.ssh/crest "


# path to pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
