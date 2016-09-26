#!/bin/sh

mv $1/positive/*.$3 $2/JPEGImages
mv $1/negative/*.$3 $2/JPEGImages
mv $1/positive/annotations/*.xml $2/Annotations
mv $1/negative/annotations/*.xml $2/Annotations
cut -d' ' -f1 $1/positive_label.txt > $4_trainval.txt
cut -d' ' -f1 $1/negative_label.txt > $4_train.txt
