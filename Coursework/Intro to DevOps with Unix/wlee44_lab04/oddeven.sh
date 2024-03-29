#!/bin/bash
now=$(date +%M)

if [ `expr $now % 2` -eq 0 ]; then
  echo "The time is even"
else
  echo "The time is odd"
fi
