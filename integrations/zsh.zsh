# Source this file from ~/.zshrc:
#   source /path/to/Youcli/integrations/zsh.zsh

_ai_complete_zsh() {
    local result
    result=$(ai-complete --shell zsh --line "$BUFFER" --cursor "$CURSOR")
    if [ "$?" -eq 0 ] && [ -n "$result" ]; then
        BUFFER="$result"
        CURSOR=${#BUFFER}
    fi
    zle redisplay
}

zle -N _ai_complete_zsh
bindkey '^X^A' _ai_complete_zsh
