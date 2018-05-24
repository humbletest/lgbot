#!/bin/bash
export SIMPLE_ENGINE_NAME="stockfish9"
export SIMPLE_SERVER_URL="http://localhost:4000"
export FLASK_SERVER_URL="http://fhelloworld.herokuapp.com"
python simple.py "" "4000" &
chmod a+x engines/stockfish9
ls engines -l
gunicorn --worker-class eventlet -w 1 server:app