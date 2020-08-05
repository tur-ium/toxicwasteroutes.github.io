'''
Basel Brush - A program for gently "scraping" data from the Basel convention website, in order to fight toxic waste.

Archives data from Table 4, which shows exports of waste.

TODO:
- Get Import data

'''

import pandas as pd
import urllib.request, urllib.error
import re


country_codes = ""
ccs = []
participants = ""
signatories_df = ""

def run_it():
	global ccs
	global participants
	global signatories_df
	#Load country codes
	country_codes = pd.read_csv("country_codes_wikipedia.csv",header=0)
	country_codes = country_codes.apply(lambda x: x.astype(str).str.replace(" ","").str.upper())
	print(country_codes)
	ntables = 6
	ccs = country_codes["Code"].to_list()
	
	#Load Signatories to the Basel Convention
	signatories_df = pd.read_csv("basel_signatories.csv",header=0)
	signatories_df = signatories_df.apply(lambda x: x.astype(str).str.upper().str.strip())
	participants = signatories_df.Participant.replace(to_replace='[\d ,]', value='',regex=True).tolist()

	print(participants)
	print("\n Basel Convention members, and their 2 letter codes used by the Basel Convention (as well as internet domain names), are: \n", country_codes[country_codes["Country name (using title case)"].isin(participants)])
	
	for participant in participants:
		print("Searching for data for {0}".format(participant))
		
		cc = country_codes[country_codes["Country name (using title case)"]==participant].iloc[0]["Code"] #Country code
		#GET DATA REMOTELY
		
		#Export data
		#url = "http://ers.basel.int//ERS-Extended/ExcelFiles/Temp/ERS_Basel_2018-{0}-BC-Table4.xlsx".format(cc)
		#Generation
		for n in range(1,ntables+1):
			print("Table {0}".format(n))
			url = "http://ers.basel.int//ERS-Extended/ExcelFiles/Temp/ERS_Basel_2018-{0}-BC-Table{1}.xlsx".format(cc,n)
			try:
				data = urllib.request.urlopen(url).read()
				file = open("ERS_Basel_2018-{0}-BC-Table{1}.xlsx".format(cc,n),"wb")
				file.write(data)
				file.close()
				cc_data = pd.read_excel(data,sheet_name="BC-Table{0}".format(n),header=2)
			except urllib.error.HTTPError as e:
				print("{0} does not report Table {1}, or it is not available at {2}".format(participant,n,url))
			
			#READ SAVED DATA
			'''
			try:
				fname = "ERS_Basel_2018-{0}-BC-Table4.xlsx".format(cc)
				file = open(fname,"rb")
				cc_data = pd.read_excel(file,sheet_name="BC-Table4",header=2)
				file.close()
				if(participant=="CHINA"):
					print("SHOWING DATA FOR CHINA (SINCE IT IS A LARGE WASTE PROCESSOR)")
					print(cc_data)
			except IOError:
				print("{0} does not report this information, or it is has not been downloaded. The filename expected is {1}".format(participant,fname))
		'''
#	print(cc_data[cc_data["Country of destination"]=="BE"])
