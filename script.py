#!/usr/bin/env python
#coding: utf8 

#get the list of the scanned election results papers ( proces verbaux )
# sudo apt-get install python-setuptools
# easy_install beautifulsoup4

import urllib2
from bs4 import BeautifulSoup
from string import maketrans
from string import whitespace
import csv
import time
import json
import os #for the se of wget command to download the files

 
source_url = "http://www.isie.tn/index.php/fr/302-proces-verbaux-de-depouillement-pour-les-elections-presidentielle.html"
# using urllib2 to read the remote html page
html = urllib2.urlopen(source_url).read()
#using BeautifulSoup library for pulling data out of HTML
soup = BeautifulSoup(html)
#gettting all the disticts represented by a directory tree
main_directory =soup.find('ul', class_="php-file-tree")

#Etranger directory  then tunisia directory 

countries = main_directory.find_all('li', recursive=False)
for country in countries :
	country_link = country.findChild('a');
	country_name = country_link.contents[0].encode('utf-8').strip().replace(' ', '_')

 	if not os.path.exists(country_name):
		os.makedirs(country_name)

	district_directory= country.findChild('ul',recursive=False)
	if district_directory == None :
		print "data unavailable, Level: country , name:"+country_name
	else:
		districts = district_directory.find_all('li', recursive=False)
		# we have two different structures for the  file tree , the easiest way is the treat them differently 
		if country_name == "Etranger":
			for pv in  districts:
				pv_link = pv.findChild('a', href=True)
				pv_ref = pv_link['href']
				file_link = "http://isie.tn"+ pv_ref 
				fullurl = urllib2.quote(file_link.encode('utf-8'), safe="%/:=&?~#+!$,;'@()*[]")
				download_command= "wget -P " + country_name + " " + fullurl
				os.system(download_command)
		else:
				#Processing the tunisia file tree   
			for district in districts:
				district_link = district.findChild('a');
				district_name = district_link.contents[0].encode('utf-8').strip().replace(' ', '_')
				print district_name
  				if not os.path.exists(country_name+ "/" + district_name):
					os.makedirs(country_name+ "/" + district_name)
					#find files list 
					files_directory= district.findChild('ul',recursive=False)
					if files_directory == None :
						print "Error:data unavailable, Level: district , name:"+ district_name
					else:
						files = files_directory.find_all('li', class_='pft-file', recursive=False)

						# pv stands for Proces Verbal which in english means protocol -- in election lexique 
						for pv in  files:
							pv_link = pv.findChild('a', href=True)
							pv_ref = pv_link['href']
							file_link = "http://isie.tn"+ pv_ref 
							fullurl = urllib2.quote(file_link.encode('utf-8'), safe="%/:=&?~#+!$,;'@()*[]")
							download_path= country_name+ "/" + district_name
							download_command= "wget -P " + download_path + " " + fullurl
							os.system(download_command)




	







	

