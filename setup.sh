#!/bin/bash

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run using sudo" 2>&1
  exit 1
else
  cp apps.twitch-indicator-applet.gschema.xml /usr/share/glib-2.0/schemas
fi
