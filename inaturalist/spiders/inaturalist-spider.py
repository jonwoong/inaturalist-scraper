########## INFORMATION ##########
# In the file "inputs.py" you can:
# 	Provide the name of your csv file 
# 	Toggle whether or not to download images to the "images" folder
# 	Toggle whether or not to update the csv file

########## HEADERS ##########

import os
import sys
from sys import platform
from os.path import dirname as up 

path_to_project_folder = up(up(up(__file__)))
sys.path.append(path_to_project_folder)

from inputs import * # user defined

import urllib
from urllib import URLopener # used to download images

import pandas 
from pandas import DataFrame, read_csv # used to extract column data from excel file

import scrapy # used to create web crawlers
from scrapy import Spider

import selenium # used to load web pages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

########## CONSTANTS ##########

chromedriver_options = webdriver.ChromeOptions()
chromedriver_options.add_argument("headless")

excel_file = read_csv(EXCEL_FILENAME) # obtain contents of csv file
species_names = excel_file.Name.tolist() # obtain Name column
page_urls = excel_file.occurrenceid.tolist() # obtain occurrenceid column

observation_numbers = [] # list of all unique numbers at the end of "inturalist.org/observations/"
for url in page_urls: # build the list of observation numbers using occurrenceid column
	observation_numbers.append(url.split("/")[-1])

observation_name_dict = dict(zip(observation_numbers, species_names)) # create dictionary, key=obvservation number, value=a Name

########## SPIDER ##########

class InaturalistSpider(Spider):
	name = "inaturalist" # name of spider

	with open("url-list.txt", "rt") as url_file:
		start_urls = [url.strip() for url in url_file.readlines()] # fetch all urls from url-list.txt

	def __init__(self):
		#self.driver = webdriver.Chrome(path_to_project_folder + "/drivers/chromedriver-pc", chrome_options=chromedriver_options) # chrome is used as a headless web-browser
		self.driver = webdriver.Chrome(path_to_project_folder + "/drivers/chromedriver-mac", chrome_options=chromedriver_options) # chrome is used as a headless web-browser

	def parse(self, response):
		global excel_file
		species_name = observation_name_dict[str(response.url).strip().split("/")[-1]] # look up species name in our dictionary by using observation number as key
		
		self.driver.get(response.url) # load an observation page in selenium
		
		try: # try to load webpage
			image_elements = WebDriverWait(self.driver,5).until(expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@class='image-gallery-image']/img"))) # scrape images of species

			image = URLopener() # create a blank URLopener object to later download image(s) 
			
			image_urls = [] # list of urls, scraped from image elements
			for image_element in image_elements: # build image_urls
				image_url = image_element.get_attribute("src") # extract src attribtue from image element (the image url)
				image_urls.append(image_url) # add extracted url to image_urls

			number_of_images = len(image_urls) # calculate total number of images for an observation
		
			if number_of_images > 1: # if there are multiple images for one observation page
				for index in range(number_of_images): # loop over all images
					indexed_species_name = species_name + '-0' + str(index+1) # create string that looks like "species_name-0x" where x is >= 1
					
					if DOWNLOAD_IMAGES:
						image.retrieve(image_urls[index].replace("large","original"), "images/" + indexed_species_name + ".jpg") # download the image, save it as "species_name-0x.jpeg"

					if UPDATE_CSV:
						species_row = DataFrame() # initialize new row to hold "species-0x" data
						species_row = excel_file.loc[excel_file['Name']==species_name] # fetch row corresponding to this species
						species_row.iloc[0,0] = indexed_species_name # change Name field to "species-0x"

						species_row.to_csv(EXCEL_FILENAME, header=None, mode='a', index=False, sep=',', encoding='utf-8') # add the new row to original csv file

				if UPDATE_CSV:
					excel_file = read_csv(EXCEL_FILENAME) # refresh excel_file by reading in newly added rows "species-0x"
					species_index = excel_file.index[excel_file['Name']==species_name][0] # get index of row to eliminate "species"
					excel_file.drop(species_index).to_csv(EXCEL_FILENAME, index=False) # remove original species row

			if DOWNLOAD_IMAGES:
				if number_of_images == 1: # if there is only one image for one observation
					image.retrieve(str(image_urls[0]).replace("large","original"), "images/" + species_name + ".jpg") # download the image, save it as "species_name.jpeg"

		except TimeoutException: # in the case of a timeout
			# add species url to exception list
			with open("exception-url-list.txt",'a') as url_file:
				url_file.write(str(response.url) + '\n')

			if UPDATE_CSV and DELETE_FAILURES:
				# delete a species row
				excel_file = excel_file.read_csv(EXCEL_FILENAME)
				species_index = excel_file.index[excel_file['Name']==species_name][0] # get index of row to eliminate "species"
				excel_file.drop(species_index).to_csv(EXCEL_FILENAME, index=False) # remove original species row

		yield


