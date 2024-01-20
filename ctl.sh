#!/bin/bash
case $1 in
    build)
        docker build -t mqtt-panel .
        ;;
    run)
        docker run -p 8765:8765 mqtt-panel
        ;;
    *)
        echo "Usage: ./ctl build | run"
        ;;
esac


