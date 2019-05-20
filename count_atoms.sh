#!/bin/bash

awk '$1=="ATOM"||$1=="HETATM"{i++}$1=="MODEL"&&$2=="2"{print i; exit}END{print i}' $1
