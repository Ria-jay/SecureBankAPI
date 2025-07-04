#!/bin/bash

curl -v -X POST http://127.0.0.1:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  --data-raw "{
    \"streams\": [{
      \"stream\": {
        \"job\": \"test\"
      },
      \"values\": [
        [\"$(date +%s%N)\", \"hello from Loki test log\"]
      ]
    }]
  }"

echo -e "\n[+] Done sending."
