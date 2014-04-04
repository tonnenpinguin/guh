#!/bin/bash

if [ -z $2 ]; then
  echo "usage: $0 host deviceClassId"
else
  (echo '{"id":1, "method":"Devices.GetStateTypes", "params":{"deviceClassId":"'$2'"}}'; sleep 1) | nc $1 1234
fi
