# Ada_Louisiana_Purchase.py
#
# Program to read and analyze storm incidence data for Ada Developers Academy
# application task. This particular program examines storm events from 1957 and 2007,
# identifies those events occurring in CZ_NAME regions not beginning with A, E, I, O, or U,
# further selects those events that occur in states representing the Louisiana Purchase
# territory, and sums the damages (DAMAGE_CROPS and DAMAGE_PROPERTY) for each year for the
# storm events meeting those criteria. The absolute dollar totals for damages in each
# year are printed, along with an inflation-adjusted estimate that expresses 1957 damages
# in "2007 dollars." 
#
# Please note that this program is intended to be used with trimmed versions of the 1957
# and 2007 files, in which the last three columns are removed. This trimming is important
# for the 2007 version because there may be commas in the entries in those columns, which
# would disrupt the file parsing.
#
# ATTRIBUTION:
# Modified from programs Cytof.py and Framingham.py, presented in Stanford GENE 218 course
# (originally used to analyze cell sorting data and data from the Framingham health study),
# Prof. Andy Fire).


# Different rough ways of approximating the Louisiana Purchase territory using modern state.
#
# inAtAllSet = includes all states that have even a tiny corner inside the area of the Louisiana Purchase
# mostlyInSet = includes all states that are fully or mostly inside the area of the Louisiana Purchase
# fullyInSet = includes only those states fully contained within the present-day area of the Louisiana Purchase
#
# States categorized according to Library of Congress: https://www.loc.gov/collections/louisiana-european-explorations-and-the-louisiana-purchase/articles-and-essays/a-question-of-boundaries/

inAtAllSet =  ['NEW MEXICO', 'TEXAS', 'ARKANSAS', 'IOWA', 'MISSOURI', 'NEBRASKA', 'KANSAS', 'OKLAHOMA', 'LOUISIANA', 'MINNESOTA', 'NORTH DAKOTA', 'SOUTH DAKOTA', 'MONTANA', 'WYOMING', 'COLORADO']
mostlyInSet =  ['ARKANSAS', 'IOWA', 'MISSOURI', 'NEBRASKA', 'KANSAS', 'OKLAHOMA', 'LOUISIANA', 'MINNESOTA', 'NORTH DAKOTA', 'SOUTH DAKOTA', 'MONTANA', 'WYOMING', 'COLORADO']
fullyInSet = ['ARKANSAS', 'IOWA', 'MISSOURI', 'NEBRASKA', 'KANSAS', 'OKLAHOMA']

louisianaPurchaseStates = mostlyInSet 	# Choose the set of states to include in the analysis

limitTo1957Types = 1;

## Open source files for 1957 and 2007	

F = open("StormEvents2007_trimmed.csv", mode = "rU")
Headers = F.next().split(",")   #Collect the first line of the file, which holds the headers

F2 = open("1957_trimmed2.csv", mode = "rU")
Headers2 = F2.next().split(",")  #Collect the first line of the file, which holds the headers

# Define a class called event. An event represents a data line from the .CSV file of storm events.
# An event has an attribute corresponding to each header in the file.

class event:
    def __init__(self,L,H):
        for i in range(len(H)):
            setattr(self,H[i],L[i]) #Set attribute corresponding to header element to be the value appr. to the event

#eventsList2007 =[]   # Make a list to contain the event objects created from the 2007 file

damage2007 = 0.0

events2007 = 0

for L0 in F:                                     
    L1=L0.strip().split(',')
    e = event(L1, Headers)
    
    if e.CZ_NAME[0] != 'A' and e.CZ_NAME[0] != 'E' and e.CZ_NAME[0] != 'I' and e.CZ_NAME[0] != 'O' and e.CZ_NAME[0] != 'U': # Consider only events whose CZ_NAME does not start with A, E, I, O, or U
    	if e.STATE in louisianaPurchaseStates and (e.EVENT_TYPE == "Tornado" or e.EVENT_TYPE == "Thunderstorm Wind" or e.EVENT_TYPE == "Hail"):	# If the event is in the set of states defined as Louisiana Purchase territory states, and one of the 3 types found in the 1957 dataset
    		if not e.DAMAGE_PROPERTY == "":		#Some spaces are blank for this field in 2007 sheet; treated as zeroes
    			if e.DAMAGE_PROPERTY[len(e.DAMAGE_PROPERTY)-1] == 'K':
    				damage2007 = damage2007 + float(e.DAMAGE_PROPERTY[0:len(e.DAMAGE_PROPERTY)-1])*1000	# This syntax removes the "K" indicating thousands and converts to dollars
    			elif e.DAMAGE_PROPERTY[len(e.DAMAGE_PROPERTY)-1] == 'M':
    			    damage2007 = damage2007 + float(e.DAMAGE_PROPERTY[0:len(e.DAMAGE_PROPERTY)-1])*1000000	# This syntax removes the "M" indicating millions and multiplies to give result that is in dollars
    		if not e.DAMAGE_CROPS == "":		#Some spaces are blank for this field in 2007 sheet; treated as zeroes
    			if e.DAMAGE_CROPS[len(e.DAMAGE_CROPS)-1] == 'K':
    				damage2007 = damage2007 + float (e.DAMAGE_CROPS[0:len(e.DAMAGE_CROPS)-1])*1000
    			elif e.DAMAGE_CROPS[len(e.DAMAGE_CROPS)-1] == 'M':
    				damage2007 = damage2007 + float (e.DAMAGE_CROPS[0:len(e.DAMAGE_CROPS)-1])*1000000		   
    				 			
    		events2007 = events2007 + 1

print "Damage in 2007 = " + str(damage2007) + " dollars"
print "Number of events in Louisiana Purchase territory in 2007: " + str(events2007) + "\n"


damage1957 = 0.0

events1957 = 0

for L0 in F2:                                     
    L1=L0.strip().split(',')
    #print(L1)
    e = event(L1, Headers2)
    if e.CZ_NAME == "" or (e.CZ_NAME[0] != 'A' and e.CZ_NAME[0] != 'E' and e.CZ_NAME[0] != 'I' and e.CZ_NAME[0] != 'O' and e.CZ_NAME[0] != 'U'):		##...and if the event does not occur in a CZ_NAME starting with an AEIOU vowel
    	if e.STATE in louisianaPurchaseStates:
    		if not e.DAMAGE_PROPERTY == "":		#Some spaces are blank for this field in 2007 sheet; treated as zeroes
    			if e.DAMAGE_PROPERTY[len(e.DAMAGE_PROPERTY)-1] == 'K':
    				damage1957 = damage1957 + float(e.DAMAGE_PROPERTY[0:len(e.DAMAGE_PROPERTY)-1])*1000	# This syntax removes the "K" and multiplies by 1000 and converts the string to a float
    			elif e.DAMAGE_PROPERTY[len(e.DAMAGE_PROPERTY)-1] == 'M':
    			    damage1957 = damage1957 + float(e.DAMAGE_PROPERTY[0:len(e.DAMAGE_PROPERTY)-1])*1000000	# This syntax removes the "M" and multiplies by 1000000to give result that is in dollars
    		
    		if not e.DAMAGE_CROPS == "":		#Some spaces are blank for this field in 2007 sheet; treated as zeroes
    			if e.DAMAGE_CROPS[len(e.DAMAGE_CROPS)-1] == 'K':
    				damage1957 = damage1957 + float (e.DAMAGE_CROPS[0:len(e.DAMAGE_CROPS)-1])*1000
    			elif e.DAMAGE_CROPS[len(e.DAMAGE_CROPS)-1] == 'M':
    				damage1957 = damage1957 + float (e.DAMAGE_CROPS[0:len(e.DAMAGE_CROPS)-1])*1000000
 
    		events1957 = events1957 + 1

print "Damage in 1957 = " + str(damage1957)	+ " dollars"
print "Number of events in Louisiana Purchase territory in 1957: " + str(events1957) + "\n"

# Adjust calculated values for inflation: http://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=1957&year2=2007
# $1 in 1957 is equivalent to $7.38 in 2007 in terms of buying power.

print "In 2007 dollars, the 1957 damage is worth: " + str(damage1957 * 7.38) + " dollars"

F.close()
F2.close()

