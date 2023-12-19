#!/bin/bash

i=1
while [ $i -le 5 ]
do
    app="node$i"
    docker run -d --rm  \
    -p $((i + 4999)):5000 \
    --name=${app} \
    -v "$PWD"/app:/home/nodo/app \
    private-node
    echo $((i + 4999))
    echo "Node $i private completed..."
    i=$((i + 1))
done

    #
