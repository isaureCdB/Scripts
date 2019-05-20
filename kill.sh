#!/bin/bash
for i in `ps -elf| grep $1 |awk '{print $4}'`; do
	kill -9  $i
done
