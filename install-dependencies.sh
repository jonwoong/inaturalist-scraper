#!/bin/bash

sudo easy_install pip
pip install pandas
pip install scrapy
pip install selenium
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap caskroom/cask
brew cask install chromedriver