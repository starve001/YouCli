# Source this file from ~/.bashrc:
#   source /path/to/Youcli/integrations/bash.sh

_ai_complete_bash() {
    local result status
    result=$(ai-complete --shell bash --line "$READLINE_LINE" --cursor "$READLINE_POINT")
    status=$?
    if [ "$status" -eq 0 ] && [ -n "$result" ]; then
        READLINE_LINE="$result"
        READLINE_POINT=${#READLINE_LINE}
    fi
}

# Ctrl+G is a single shortcut that works reliably in Windows Terminal/WSL.
bind -x '"\C-g":_ai_complete_bash'
# Keep the two-key shortcut for users who prefer it.
bind -x '"\C-x\C-a":_ai_complete_bash'
