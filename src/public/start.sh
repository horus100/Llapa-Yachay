#!/bin/bash

        app="public"
        docker run -d --rm \
        -p $((5005)):5000 \
        --name=${app} \
        -v "$PWD"/app:/home/nodo/app \
        public-node
        echo $((5005))
        echo "public node completed..."

        