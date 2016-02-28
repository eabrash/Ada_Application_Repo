# Ada_Storm_Free_Counties.py
#
# Program to read and analyze storm incidence data for Ada Developers Academy
# application task. Specifically, determines how many and which counties in Washington
# State did not have a reported storm event in 2007. Only considers entities that are of
# CZ_TYPE C (county) and whose CZ_NAME does not start with A, E, I, O, or U.
#
# The program could potentially be improved by taking into account the entries of CZ_TYPE Z 
# (zones), which are not included in the present analysis. Zones do map to counties, as 
# described in the document http://www.nws.noaa.gov/geodata/catalog/wsom/data/bp10nv15.dbx.
# However, one zone may map to multiple counties, and the actual storm might or might
# not have touched all of the counties within the zone. The actual counties affected in a
# zone event could be inferred to some degree using the latitude/longitude data for the
# storm's beginning and end, but it's unclear whether adding zones would tend to make the
# estimation of unaffected counties more accurate. (It would, however, make it more
# conservative.)
#
# Please note that this program is intended to be used with trimmed version of the
# 2007 file, in which the last three columns are removed. This trimming is important
# for the 2007 version because there may be commas in the entries in those columns, which
# would disrupt the file parsing.
#
# Depends on a .csv file of all counties in Washington state ("Washington_Counties.csv").
#
# ATTRIBUTION:
# Modified from programs Cytof.py and Framingham.py, presented in Stanford GENE 218 course
# (originally used to analyze cell sorting data and data from the Framingham health study),
# Prof. Andy Fire).


counties = []	# To store names of WA counties

countiesFile = open("Washington_Counties.csv", mode = "rU")		#Open file of county names.

# Make a list of WA counties

for line in countiesFile:
	counties.append(line.strip())
	
countiesFile.close()
	
# Open the 2007 storm events file for reading

F = open("StormEvents2007_trimmed.csv", mode = "rU")
Headers = F.next().split(",")   #Collect the first line of the file, which holds the headers

# Define a class called event. An event represents a data line from the .CSV file of storm events.
# An event has an attribute corresponding to each file header.

class event:
    def __init__(self,L,H):
        for i in range(len(H)):
            setattr(self,H[i],L[i]) #Set attribute corresponding to header element to be the value appr. to the event


eventsList=[]   # Make a list to contain the event objects created from the file
representedCounties = []	# Make a list to contain the WA counties represented in the file

# Add an event object to the list for each row in the file

for L0 in F:                                     
    L1=L0.strip().split(',')
    #print(L1)
    e = event(L1, Headers)
    
    # Do not append any event that occurs in a CZ_NAME that begins with a vowel (AEIOU, Y not considered a vowel here)
    
    if e.CZ_NAME[0] != 'A' and e.CZ_NAME[0] != 'E' and e.CZ_NAME[0] != 'I' and e.CZ_NAME[0] != 'O' and e.CZ_NAME[0] != 'U':
    	if e.STATE == 'WASHINGTON':		#If event is in WA
    		if e.CZ_TYPE == 'C' and e.CZ_NAME not in representedCounties:	# If event is in a county and the county's not yet in the list
    			representedCounties.append(e.CZ_NAME)						# Add the county name to the list
    
stormFreeCounties = []

for county in counties:
	
	# This long filter ensures that the storm data (which is filtered to eliminate CZ names starting with vowels) is
	# checked only for counties that don't start with a vowel.
	if county[0] != 'A' and county[0] != 'E' and county[0] != 'I' and county[0] != 'O' and county[0] != 'U' and county not in representedCounties:
		stormFreeCounties.append(county)

i = 0

print 'Storm-free counties, 2007:'

for county in stormFreeCounties:
	print (county)
	i = i + 1

print 'Number of storm-free counties: '
print i

F.close()
