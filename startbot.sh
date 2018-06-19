#!/bin/bash
export APP_MODE="prod"
python simple.py "" "4000" &
chmod a+x engines/stockfish9
gunicorn --worker-class eventlet -w 1 server:app