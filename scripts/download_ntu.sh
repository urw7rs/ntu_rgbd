#!/bin/bash

export OPENSSL_CONF=openssl.cnf 

curl -LOJZ --cookie $(pwd)/cookies.txt "https://rose1.ntu.edu.sg/dataset/actionRecognition/download/[125-158]"
