#!/bin/bash

docker network inspect bridge | jq '.[0].Containers'
# sudo apt install jq
