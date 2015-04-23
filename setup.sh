#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run using sudo" 2>&1
  exit 1
else
  rm -f /usr/bin/twitch-indicator
  cp apps.twitch-indicator.gschema.xml /usr/share/glib-2.0/schemas
  glib-compile-schemas /usr/share/glib-2.0/schemas
  cp run.py /usr/bin/twitch-indicator
  chmod a+x /usr/bin/twitch-indicator

  mkdir -p /usr/lib/twitch-indicator
  cp icons/*.svg /usr/lib/twitch-indicator/
  cp twitch-indicator.glade /usr/lib/twitch-indicator/
  chmod a+r /usr/lib/twitch-indicator/*.svg
fi
