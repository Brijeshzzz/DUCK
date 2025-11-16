#!/bin/bash
for i in {1..5}; do
  echo "Capture run $i"
  python3 main.py
  sleep 300
 done
