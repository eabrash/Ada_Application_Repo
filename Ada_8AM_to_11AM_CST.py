# Ada_8AM_to_11AM_CST.py
#
# Program to read and analyze storm incidence data for Ada Developers Academy
# application task.
#
# The program converts all times to PST and checks which wind-based storms (Thunderstorm 
# Wind or Tornado type) occurred between 8 AM and 11 AM PST in the 1957 dataset, looking
# at only those events that occurred in localities that do not have a CZ_NAME starting 
# with A, E, I, O, or U.
#
# Note that the 1957 dataset gives only one time value (BEGIN_TIME same as END_TIME) for
# each storm event. This time value is used to check whether each event fell into the 8 AM
# to 11 AM bracket. The program in its present form would not be able to handle the same
# question using the 2007 data, or other data in which a storm is considered to have an
# extent.
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


## Open source files for 1957 and 2007	

F2 = open("1957_trimmed2.csv", mode = "rU")
Headers2 = F2.next().split(",")  #Collect the first line of the file, which holds the headers

# Define a class called event. An event represents a data line from the .CSV file of storm events.
# An event has an attribute corresponding to each header in the file.

class event:
    def __init__(self,L,H):
        for i in range(len(H)):
            setattr(self,H[i],L[i]) #Set attribute corresponding to header element to be the value appr. to the event



eventsList1957 = []	# List of events in 1957 (as event objects)

for L0 in F2:                                     
    L1=L0.strip().split(',')
    #print(L1)
    e = event(L1, Headers2)
    if e.CZ_NAME == "":
			eventsList1957.append(e)    # Handle case where no name is given for locality; these CZ_NAME instances are considered to "not start with a vowel"
    elif e.CZ_NAME[0] != 'A' and e.CZ_NAME[0] != 'E' and e.CZ_NAME[0] != 'I' and e.CZ_NAME[0] != 'O' and e.CZ_NAME[0] != 'U':		##...and if the event does not occur in a CZ_NAME starting with an AEIOU vowel
			eventsList1957.append(e)							

# Convert all timestamps from CST to PST and check if they fall within the range of 8 AM
# to 11 AM PST. This approach is designed specifically for the 1957 file, in which the
# begin and end times of the storm event are always the same. It uses the BEGIN_TIME value
# as the occurrence time of the event. 
#
# Note: This analysis does not take Daylight Savings Time into account/assumes that the
# NOAA already took it into account when converting the occurrence times into CST.
# Daylight savings time was not nationally mandated in 1957 and thus occurred in a
# piecemeal way in different counties and localities, so it would be challenging to
# accurately account for this factor in any case.
#
# Source: http://www.webexhibits.org/daylightsaving/e.html

eventsInWindow = 0

for e in eventsList1957:

	if e.EVENT_TYPE == "Thunderstorm Wind" or e.EVENT_TYPE == "Tornado":	# If event is a wind-based storm

		# Note: there are two events that are not marked as CST. One is marked "unknown"
		# but is Oklahoma and occurs just before midnight. This event is likely CST and
		# would not be within the desired window in any likely scenario. The other is
		# marked "PST" but is in Hawaii. If the time is actually in PST, it is outside
		# of the desired window (11:20 AM). If it is actually in Hawaii time (HST), it
		# would still be out of the desired window. Therefore, these data points are
		# excluded from the analysis.
		
		if e.CZ_TIMEZONE == 'CST':
			pacTime = int(e.BEGIN_TIME)-200
			if pacTime >= 800 and pacTime <= 1100:
				#print e.EVENT_ID + " " + e.BEGIN_TIME + " " + e.CZ_TIMEZONE + ", pacTime = " + str(pacTime)
				eventsInWindow = eventsInWindow + 1
				
print "Number of events between 8 AM and 11 AM PST in 1957: " + str(eventsInWindow)

F2.close()

