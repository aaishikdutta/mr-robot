#!/bin/zsh

VENV_PYTHON="$(dirname "$0")/../venv/bin/python"
SCRIPT_PATH="$(dirname "$0")/../mr_robot/copilot.py"

POSTDISPLAY_FILE=$(mktemp)
BUFFER_FILE=$(mktemp)
MAIN_PID=$$

function ask_copilot() {
    
    POSTDISPLAY=$'\nasking copilot..'
    {
        response=$($VENV_PYTHON $SCRIPT_PATH 2>&1 $BUFFER)
        if [ $? -ne 0 ]
        then   
            echo "[FAIL]: $response" >  $POSTDISPLAY_FILE
        else
            echo "$response" > $BUFFER_FILE
            echo "done" > $POSTDISPLAY_FILE
        fi
        kill -SIGUSR1 $MAIN_PID

    } &|

}

zle -N ask_copilot
bindkey "^K" ask_copilot

function update_buffer() {
    postdisplay_tmp="$(cat $POSTDISPLAY_FILE)"
    buffer_tmp="$(cat $BUFFER_FILE)"
    
    if [[ $postdisplay_tmp == "done" ]] 
    then
        BUFFER="${buffer_tmp}"
        POSTDISPLAY=""

        zle _zsh_highlight__zle-line-finish
    
    else 
        POSTDISPLAY=$'\n'"$postdisplay_tmp"
    fi
    rm -f "$BUFFER_FILE" # Clean up the BUFFER_FILE
    rm -f "$POSTDISPLAY_FILE"
    zle reset-prompt
}

zle -N update_buffer

function on_copilot_done_trap() {
  zle update_buffer
}

trap 'on_copilot_done_trap' SIGUSR1