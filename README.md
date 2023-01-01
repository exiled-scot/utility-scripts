# Utilities and Scripts
A collection of utilities and scripts that are not yet worthy of their own repo.

# Table of Contents

[Identify Monitor where the Mouse is Currently](#user-content-identify-mouse)

[Rotate Monitor](#user-content-rotate-monitor)

[Toggle Input](#user-content-toggle-input)

[Vscode to Yasnippet Converter](#user-content-vscode-to-yasnippet-converter)

## Identify Mouse

This is a small script I wrote (with the assistance of OpenAI) to identify where the mouse is currently active. It will eventually become part of a larger script that will manipulate `xrandr` details on the fly. 

## Rotate Monitor

Rotate the laptop screen and the trackpad. Good for reading pdfs.

*TODO* Fix two finger scrolling. *xinput* does not appear to affect gestures.

## Toggle Input

Use *xinput* to toggle the keyboard and trackpad between *enabled* and *disabled* states. Good when using an external keyboard and laying monitors on the keyboard.

*TODO* Add CLI arguments instead of hard-coded device names.

## VSCode to Yasnippet Converter

Convert Vscode snippets, which are json formatted, into Yasnippet snippets. Includes description. Trigger is the same as Vscode and mode specific (shell-mode, dart-mode, etc).

### Usage

``` sh
python3 vscode_snippet_to_yasnippet.py ~/vscode/snippets.json ~/snippets/dart-mode
```
