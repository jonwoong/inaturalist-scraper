#!/bin/bash

INPUT_FILENAME=$1
command="scrapy crawl inaturalist -a ${INPUT_FILENAME} -o ${INPUT_FILENAME}"
run=$(eval "$command")
echo "$run"