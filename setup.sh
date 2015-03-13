#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run using sudo" 2>&1
  exit 1
else
  rm -f /usr/bin/twitch-indicator-applet
  cp apps.twitch-indicator-applet.gschema.xml /usr/share/glib-2.0/schemas
  cp run.py /usr/bin/twitch-indicator-applet
  chmod a+x /usr/bin/twitch-indicator-applet

  mkdir -p /usr/lib/twitch-indicator-applet
  cp icons/*.png /usr/lib/twitch-indicator-applet/
  chmod a+r /usr/lib/twitch-indicator-applet/*.png
fi
