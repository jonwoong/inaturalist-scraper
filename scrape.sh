#!/bin/bash

build_url_command="python generate-url-list.py"
run_build_url=$(eval "$build_url_command")
echo "$run_build_url"
sleep .5
scrape_command="scrapy crawl inaturalist"
run_scrape=$(eval "$scrape_command")
echo "$run_scrape"