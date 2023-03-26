#!/bin/bash
set -e

Xvfb :99 -screen 0 1024x768x24 -ac -nolisten tcp &

export DISPLAY=:99

exec python nailtracking/broker.py