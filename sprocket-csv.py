#!/usr/bin/python2

# sprocket-csv.py: Utility to generate INI files from the "COG Ore Settings Chart" LibreOffice spreadsheet. 

import csv
import sys
import os
import string

# Whatever output we want, we don't want it to be too close to the prompt.
print 

# First, we create a list to store the records in.
sprocketSpreadsheetFile = []
sprocketRawRecords = []
sprocketCookedRecords = []
sprocketModDatabase = []
previousMod = ""

# Let's make sure the CSV file is present.
#try:
#    if not os.path.isfile(sys.argv[1]):
#        sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": No such file or directory")

# Now, we populate the list with CSV records, each containing the output fields.
with open(sys.argv[1], 'rb') as sprocketSpreadsheetFile:
    rawRecords = csv.reader(sprocketSpreadsheetFile, delimiter='\n', quotechar='"')

    for i in rawRecords:
        string = ""
        for x in range(0, len(i)):
            string += i[x]
        sprocketCookedRecords.append(string.split(';'))
        #sprocketRawRecords.append(i)

    #current=0
    #for i in sprocketRawRecords:
    #    currentString.append = sprocketRawRecords[current]
    #    sprocketCookedRecords.append(currentString.split(';'))
    #    current += 1

# We want to reorder the records to remove extraneous rows.
for row in range(19, len(sprocketCookedRecords)):
    
    sprocketModDatabase.append(sprocketCookedRecords[row])
    
# Newlines can be a problem.  Using \n in the field should fix it if it can be converted to a newline.
def newlineConvert(field):
    fieldOutput = ""
    fieldOutput = field.replace('\\n','\n')
    # for stringCount in range(0, len(stringList)):
    #    fieldOutput += stringList[stringCount]+"\n"
            
    return fieldOutput
    
# Okay, now we have the database firmly stored in memory, it's time to make the template.

# First, the individual ore stanzas.

def oreStanza(recordIndex):
    global previousMod
    
    stanzaOutput = ""
    
    if sprocketModDatabase[recordIndex][0] != previousMod:
        stanzaOutput += "\n\n\n\n\n\n"
        stanzaOutput += "\n# ---- "+sprocketModDatabase[recordIndex][0]+" ----\n"
        previousMod = sprocketModDatabase[recordIndex][0]
    stanzaOutput += "["+sprocketModDatabase[recordIndex][1]+"]\n"
    if sprocketModDatabase[recordIndex][2] == "Veins":
        stanzaOutput += "Distribution Presets: "+sprocketModDatabase[recordIndex][3]+", "+sprocketModDatabase[recordIndex][4]+", Vanilla\n"
    elif sprocketModDatabase[recordIndex][2] == "Clouds":
        stanzaOutput += "Distribution Presets: "+sprocketModDatabase[recordIndex][4]+", "+sprocketModDatabase[recordIndex][3]+", Vanilla\n"
    else:
        stanzaOutput += "Distribution Presets: Vanilla, "+sprocketModDatabase[recordIndex][3]+", "+sprocketModDatabase[recordIndex][4]+"\n"
    if sprocketModDatabase[recordIndex][28]:
        stanzaOutput += "Seed: "+sprocketModDatabase[recordIndex][28]+"\n"
    if sprocketModDatabase[recordIndex][29] != "Overworld":
        stanzaOutput += "Dimensions: "+sprocketModDatabase[recordIndex][29]+"\n"
    stanzaOutput += "Wireframe Color: "+sprocketModDatabase[recordIndex][27]+"\n"
    stanzaOutput += "Bounding Box Color: "+sprocketModDatabase[recordIndex][27]+"\n"
    stanzaOutput += "Blocks: "+sprocketModDatabase[recordIndex][31]+"\n"
    stanzaOutput += "Replaces: "+sprocketModDatabase[recordIndex][32]+"\n"
    stanzaOutput += "Height: "+sprocketModDatabase[recordIndex][18]+", "+sprocketModDatabase[recordIndex][19]+", "+sprocketModDatabase[recordIndex][30]+", base\n"
    
    maxSizeString = sprocketModDatabase[recordIndex][8]
    maxSize = float(maxSizeString)*2
    minSize = maxSize/3
    
    sizeRngCalc = (maxSize - minSize)/2
    sizeAvgCalc = sizeRngCalc + minSize
    
    sizeAvg = round(sizeAvgCalc,3)
    sizeRng = round(sizeRngCalc,2)
    
    stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"
    
    maxFreqString = sprocketModDatabase[recordIndex][9]
    maxFreq = float(maxFreqString)*2
    minFreq = maxFreq/3
    
    freqRngCalc = (maxFreq - minFreq)/2
    freqAvgCalc = freqRngCalc + minFreq
    
    freqAvg = round(freqAvgCalc,3)
    freqRng = round(freqRngCalc,2)
    
    stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
    stanzaOutput += "Vein Motherlode Frequency: "+sprocketModDatabase[recordIndex][11]+" * _default_, "+sprocketModDatabase[recordIndex][11]+" * _default_, normal, base\n"
    if sprocketModDatabase[recordIndex][12] != "none":
        stanzaOutput += "Vein Motherlode Size: "+sprocketModDatabase[recordIndex][12]+" * _default_, "+sprocketModDatabase[recordIndex][12]+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
    if sprocketModDatabase[recordIndex][13] != "none":
        if sprocketModDatabase[recordIndex][13] != "default":
            stanzaOutput += "Vein Branch Length: "+sprocketModDatabase[recordIndex][13]+" * _default_, "+sprocketModDatabase[recordIndex][13]+" * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: "+sprocketModDatabase[recordIndex][14]+" * _default_, "+sprocketModDatabase[recordIndex][14]+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
    stanzaOutput += "Cloud Frequency: "+sprocketModDatabase[recordIndex][16]+" * _default_, "+sprocketModDatabase[recordIndex][16]+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Radius: "+sprocketModDatabase[recordIndex][17]+" * _default_, "+sprocketModDatabase[recordIndex][17]+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Thickness: "+sprocketModDatabase[recordIndex][17]+" * _default_, "+sprocketModDatabase[recordIndex][17]+" * _default_, normal, base\n"
    stanzaOutput += newlineConvert(sprocketModDatabase[recordIndex][33])+"\n"
    if sprocketModDatabase[recordIndex][35]:
        stanzaOutput += "# "+sprocketModDatabase[recordIndex][35]+"\n"
    stanzaOutput += "\n"
        
    ### Next, for the mountains.
    
    if sprocketModDatabase[recordIndex][24] != "0":
      stanzaOutput += "[Mountain "+sprocketModDatabase[recordIndex][1]+"]\n"
      if sprocketModDatabase[recordIndex][2] == "Veins":
          stanzaOutput += "Distribution Presets: "+sprocketModDatabase[recordIndex][3]+", "+sprocketModDatabase[recordIndex][4]+", Vanilla\n"
      elif sprocketModDatabase[recordIndex][2] == "Clouds":
          stanzaOutput += "Distribution Presets: "+sprocketModDatabase[recordIndex][4]+", "+sprocketModDatabase[recordIndex][3]+", Vanilla\n"
      else:
          stanzaOutput += "Distribution Presets: Vanilla, "+sprocketModDatabase[recordIndex][3]+", "+sprocketModDatabase[recordIndex][4]+"\n"
      if sprocketModDatabase[recordIndex][28]:
          stanzaOutput += "Seed: "+sprocketModDatabase[recordIndex][28]+"\n"
      if sprocketModDatabase[recordIndex][29] != "Overworld":
          stanzaOutput += "Dimensions: "+sprocketModDatabase[recordIndex][29]+"\n"
      stanzaOutput += "Wireframe Color: "+sprocketModDatabase[recordIndex][27]+"\n"
      stanzaOutput += "Bounding Box Color: "+sprocketModDatabase[recordIndex][27]+"\n"
      stanzaOutput += "Blocks: "+sprocketModDatabase[recordIndex][31]+"\n"
      stanzaOutput += "Replaces: "+sprocketModDatabase[recordIndex][32]+"\n"
      stanzaOutput += "Height: "+sprocketModDatabase[recordIndex][24]+", "+sprocketModDatabase[recordIndex][25]+", "+sprocketModDatabase[recordIndex][30]+", base\n"
      
      maxSizeString = sprocketModDatabase[recordIndex][8]
      maxSize = float(maxSizeString)*2
      minSize = maxSize/3
      
      sizeRngCalc = (maxSize - minSize)/2
      sizeAvgCalc = sizeRngCalc + minSize
      
      sizeAvg = round(sizeAvgCalc,3)
      sizeRng = round(sizeRngCalc,2)
      
      stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"
      
      maxFreqString = sprocketModDatabase[recordIndex][9]
      maxFreq = float(maxFreqString)*2
      minFreq = maxFreq/3
      
      freqRngCalc = (maxFreq - minFreq)/2
      freqAvgCalc = freqRngCalc + minFreq
      
      freqAvg = round(freqAvgCalc,3)
      freqRng = round(freqRngCalc,2)
      
      stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
      stanzaOutput += "Vein Motherlode Frequency: "+sprocketModDatabase[recordIndex][11]+" * _default_, "+sprocketModDatabase[recordIndex][11]+" * _default_, normal, base\n"
      if sprocketModDatabase[recordIndex][12] != "none":
          stanzaOutput += "Vein Motherlode Size: "+sprocketModDatabase[recordIndex][12]+" * _default_, "+sprocketModDatabase[recordIndex][12]+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
      if sprocketModDatabase[recordIndex][13] != "none":
          if sprocketModDatabase[recordIndex][13] != "default":
              stanzaOutput += "Vein Branch Length: "+sprocketModDatabase[recordIndex][13]+" * _default_, "+sprocketModDatabase[recordIndex][13]+" * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: "+sprocketModDatabase[recordIndex][14]+" * _default_, "+sprocketModDatabase[recordIndex][14]+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
      stanzaOutput += "Cloud Frequency: "+sprocketModDatabase[recordIndex][16]+" * _default_, "+sprocketModDatabase[recordIndex][16]+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Radius: "+sprocketModDatabase[recordIndex][17]+" * _default_, "+sprocketModDatabase[recordIndex][17]+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Thickness: "+sprocketModDatabase[recordIndex][17]+" * _default_, "+sprocketModDatabase[recordIndex][17]+" * _default_, normal, base\n"
      if sprocketModDatabase[recordIndex][33]:
          stanzaOutput += newlineConvert(sprocketModDatabase[recordIndex][33])+"\n"
      if sprocketModDatabase[recordIndex][34]:
          stanzaOutput += newlineConvert(sprocketModDatabase[recordIndex][34])+"\n"
      if sprocketModDatabase[recordIndex][35]:
          stanzaOutput += "# "+sprocketModDatabase[recordIndex][35]+"\n"
      
    return stanzaOutput
  

#for i in range(0, len(sprocketModDatabase[10])):
#    print str(i)+": "+sprocketModDatabase[10][i]

#print oreStanza(0)

# Then, we call it until everything is done.



for i in range (0, len(sprocketModDatabase)):
    #print i
    #print "\n"
    print oreStanza(i)
    
