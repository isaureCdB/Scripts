#!/bin/bash
sed -e "s/\]\,\ \[/\n/g" $1 > matrix_$1
sed -i -e "s/\,//g" matrix_$1
sed -i -e "s/\[\[//g" matrix_$1
sed -i -e "s/\]\]//g" matrix_$1
