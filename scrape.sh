#!/bin/bash

python generate-url-list.py
scrapy crawl inaturalist

$SHELL