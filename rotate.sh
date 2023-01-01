#!/usr/bin/env sh

# rotate_desktop.sh
#
# Rotates modern Linux desktop screen and input devices to match. Handy for
# convertible notebooks. Call this script from panel launchers, keyboard
# shortcuts, or touch gesture bindings (xSwipe, touchegg, etc.).
#
# Using transformation matrix bits taken from:
#   https://wiki.ubuntu.com/X/InputCoordinateTransformation
#
# Forked from https://gist.github.com/mildmojo/48e9025070a2ba40795c
# Configured to use with a Lenovo Yoga 260 (names taken from `xinput` output).
# If the rotation position ($1) is ommited, the script toggles through the different states: inverted, left, right, normal

TOUCHPAD='PIXA3854:00 093A:0274 Touchpad'
TRANSFORM='Coordinate Transformation Matrix'
NORMAL="Coordinate Transformation Matrix (142): 1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000"
INVERTED="Coordinate Transformation Matrix (142): -1.000000, 0.000000, 1.000000, 0.000000, -1.000000, 1.000000, 0.000000, 0.000000, 1.000000"
LEFT="Coordinate Transformation Matrix (142): 0.000000, -1.000000, 1.000000, 1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000"
RIGHT="Coordinate Transformation Matrix (142): 0.000000, 1.000000, 0.000000, -1.000000, 0.000000, 1.000000, 0.000000, 0.000000, 1.000000"

function do_rotate
{
  xrandr --output $1 --rotate $2

  TRANSFORM='Coordinate Transformation Matrix'

  case "$2" in
    normal)
      [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 1 0 0 0 1 0 0 0 1
      ;;
    inverted)
      [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" -1 0 1 0 -1 1 0 0 1
      ;;
    left)
      [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 0 -1 1 1 0 0 0 0 1
      ;;
    right)
      [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 0 1 0 -1 0 1 0 0 1
      ;;
  esac
}

XDISPLAY=`xrandr --current | grep primary | sed -e 's/ .*//g'`
state=`xrandr --query --verbose | grep " connected" | cut -d ' ' -f 6`

if [ $state = 'normal' ]; then
  state=right
elif [ $state = 'right' ]; then
  state=inverted
elif [ $state = 'inverted' ]; then
  state=left
else
    state=normal
fi

do_rotate $XDISPLAY $state
