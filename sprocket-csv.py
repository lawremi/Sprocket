#!/usr/bin/python2

# sprocket-csv.py: Utility to generate INI files from the "COG Ore Settings Chart" LibreOffice spreadsheet. 

import csv
import sys
from collections import OrderedDict
from pprint import pprint

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

# Read in the input CSV file.
#
# The result is a list of dicts, one dict per row.
#
# For example, to get the ore name of the first row, do:
#    records[0]['Ore.Name.'] # returns "Clay"
with open(sys.argv[1], 'rb') as f:
    csv_reader = csv.reader(f)
    header = csv_reader.next()  # Pop first row
    rows = list(csv_reader)  # All remaining rows
    records = [OrderedDict(zip(header, row)) for row in rows]

# Newlines can be a problem.  Using \n in the field should fix it if it can be converted to a newline.
def newlineConvert(field):
    fieldOutput = ""
    fieldOutput = field.replace('\\n','\n')
    # for stringCount in range(0, len(stringList)):
    #    fieldOutput += stringList[stringCount]+"\n"

    return fieldOutput

# Okay, now we have the database firmly stored in memory, it's time to make the template.

# First, the individual ore stanzas.

def oreStanza(row):
    row = row.values()
    global previousMod

    stanzaOutput = ""

    if row[0] != previousMod:
        stanzaOutput += "\n\n\n\n\n\n"
        stanzaOutput += "\n# ---- "+row[0]+" ----\n"
        previousMod = row[0]
    stanzaOutput += "["+row[1]+"]\n"
    if row[2] == "Veins":
        stanzaOutput += "Distribution Presets: "+row[3]+", "+row[4]+", Vanilla\n"
    elif row[2] == "Clouds":
        stanzaOutput += "Distribution Presets: "+row[4]+", "+row[3]+", Vanilla\n"
    else:
        stanzaOutput += "Distribution Presets: Vanilla, "+row[3]+", "+row[4]+"\n"
    if row[28]:
        stanzaOutput += "Seed: "+row[28]+"\n"
    if row[29] != "Overworld":
        stanzaOutput += "Dimensions: "+row[29]+"\n"
    stanzaOutput += "Wireframe Color: "+row[27]+"\n"
    stanzaOutput += "Bounding Box Color: "+row[27]+"\n"
    stanzaOutput += "Blocks: "+row[31]+"\n"
    stanzaOutput += "Replaces: "+row[32]+"\n"
    stanzaOutput += "Height: "+row[18]+", "+row[19]+", "+row[30]+", base\n"

    maxSizeString = row[8]
    maxSize = float(maxSizeString)*2
    minSize = maxSize/3

    sizeRngCalc = (maxSize - minSize)/2
    sizeAvgCalc = sizeRngCalc + minSize

    sizeAvg = round(sizeAvgCalc,3)
    sizeRng = round(sizeRngCalc,2)

    stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"

    maxFreqString = row[9]
    maxFreq = float(maxFreqString)*2
    minFreq = maxFreq/3

    freqRngCalc = (maxFreq - minFreq)/2
    freqAvgCalc = freqRngCalc + minFreq

    freqAvg = round(freqAvgCalc,3)
    freqRng = round(freqRngCalc,2)

    stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
    stanzaOutput += "Vein Motherlode Frequency: "+row[11]+" * _default_, "+row[11]+" * _default_, normal, base\n"
    if row[12] != "none":
        stanzaOutput += "Vein Motherlode Size: "+row[12]+" * _default_, "+row[12]+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
    if row[13] != "none":
        if row[13] != "default":
            stanzaOutput += "Vein Branch Length: "+row[13]+" * _default_, "+row[13]+" * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: "+row[14]+" * _default_, "+row[14]+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
    stanzaOutput += "Cloud Frequency: "+row[16]+" * _default_, "+row[16]+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Radius: "+row[17]+" * _default_, "+row[17]+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Thickness: "+row[17]+" * _default_, "+row[17]+" * _default_, normal, base\n"
    stanzaOutput += newlineConvert(row[33])+"\n"
    if row[35]:
        stanzaOutput += "# "+row[35]+"\n"
    stanzaOutput += "\n"

    ### Next, for the mountains.

    if row[24] != "0":
      stanzaOutput += "[Mountain "+row[1]+"]\n"
      if row[2] == "Veins":
          stanzaOutput += "Distribution Presets: "+row[3]+", "+row[4]+", Vanilla\n"
      elif row[2] == "Clouds":
          stanzaOutput += "Distribution Presets: "+row[4]+", "+row[3]+", Vanilla\n"
      else:
          stanzaOutput += "Distribution Presets: Vanilla, "+row[3]+", "+row[4]+"\n"
      if row[28]:
          stanzaOutput += "Seed: "+row[28]+"\n"
      if row[29] != "Overworld":
          stanzaOutput += "Dimensions: "+row[29]+"\n"
      stanzaOutput += "Wireframe Color: "+row[27]+"\n"
      stanzaOutput += "Bounding Box Color: "+row[27]+"\n"
      stanzaOutput += "Blocks: "+row[31]+"\n"
      stanzaOutput += "Replaces: "+row[32]+"\n"
      stanzaOutput += "Height: "+row[24]+", "+row[25]+", "+row[30]+", base\n"

      maxSizeString = row[8]
      maxSize = float(maxSizeString)*2
      minSize = maxSize/3

      sizeRngCalc = (maxSize - minSize)/2
      sizeAvgCalc = sizeRngCalc + minSize

      sizeAvg = round(sizeAvgCalc,3)
      sizeRng = round(sizeRngCalc,2)

      stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"

      maxFreqString = row[9]
      maxFreq = float(maxFreqString)*2
      minFreq = maxFreq/3

      freqRngCalc = (maxFreq - minFreq)/2
      freqAvgCalc = freqRngCalc + minFreq

      freqAvg = round(freqAvgCalc,3)
      freqRng = round(freqRngCalc,2)

      stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
      stanzaOutput += "Vein Motherlode Frequency: "+row[11]+" * _default_, "+row[11]+" * _default_, normal, base\n"
      if row[12] != "none":
          stanzaOutput += "Vein Motherlode Size: "+row[12]+" * _default_, "+row[12]+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
      if row[13] != "none":
          if row[13] != "default":
              stanzaOutput += "Vein Branch Length: "+row[13]+" * _default_, "+row[13]+" * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: "+row[14]+" * _default_, "+row[14]+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
      stanzaOutput += "Cloud Frequency: "+row[16]+" * _default_, "+row[16]+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Radius: "+row[17]+" * _default_, "+row[17]+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Thickness: "+row[17]+" * _default_, "+row[17]+" * _default_, normal, base\n"
      if row[33]:
          stanzaOutput += newlineConvert(row[33])+"\n"
      if row[34]:
          stanzaOutput += newlineConvert(row[34])+"\n"
      if row[35]:
          stanzaOutput += "# "+row[35]+"\n"

    return stanzaOutput

# Then, we call it until everything is done.

for row in records:
    print(oreStanza(row))