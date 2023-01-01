#!/bin/bash

function toggle_device () {

    enabled=$(xinput list-props "$1" | awk '/^\tDevice Enabled \([0-9]+\):\t[01]/ {print $NF}')
    case $enabled in
        0)
            xinput enable "$1"
            echo "$1 enabled"
            ;;
        1)
            xinput disable "$1"
            echo "$1 disabled"
            ;;
        *)
            echo
            xinput list --name-only
            ;;
    esac
}
KEYBOARD='AT Translated Set 2 keyboard'
TRACKPAD='PIXA3854:00 093A:0274 Touchpad'
toggle_device "$KEYBOARD"
toggle_device "$TRACKPAD"
