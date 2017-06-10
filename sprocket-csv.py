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
    global previousMod

    stanzaOutput = ""

    if row['Mod.Name.'] != previousMod:
        stanzaOutput += "\n\n\n\n\n\n"
        stanzaOutput += "\n# ---- "+row['Mod.Name.']+" ----\n"
        previousMod = row['Mod.Name.']
    stanzaOutput += "["+row['Ore.Name.']+"]\n"
    if row['Preferred.Preset'] == "Veins":
        stanzaOutput += "Distribution Presets: "+row['Vein.Preset.']+", "+row['Cloud.Preset']+", Vanilla\n"
    elif row['Preferred.Preset'] == "Clouds":
        stanzaOutput += "Distribution Presets: "+row['Cloud.Preset']+", "+row['Vein.Preset.']+", Vanilla\n"
    else:
        stanzaOutput += "Distribution Presets: Vanilla, "+row['Vein.Preset.']+", "+row['Cloud.Preset']+"\n"
    if row['Seed']:
        stanzaOutput += "Seed: "+row['Seed']+"\n"
    if row['Dimension'] != "Overworld":
        stanzaOutput += "Dimensions: "+row['Dimension']+"\n"
    stanzaOutput += "Wireframe Color: "+row['Debugging.Color']+"\n"
    stanzaOutput += "Bounding Box Color: "+row['Debugging.Color']+"\n"
    stanzaOutput += "Blocks: "+row['Block.ID.s.']+"\n"
    stanzaOutput += "Replaces: "+row['Replaces']+"\n"
    stanzaOutput += "Height: "+row['Average.']+", "+row['Range.']+", "+row['Distribution.Type']+", base\n"

    maxSizeString = row['Standard.Size.']
    maxSize = float(maxSizeString)*2
    minSize = maxSize/3

    sizeRngCalc = (maxSize - minSize)/2
    sizeAvgCalc = sizeRngCalc + minSize

    sizeAvg = round(sizeAvgCalc,3)
    sizeRng = round(sizeRngCalc,2)

    stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"

    maxFreqString = row['Standard.Frequency.']
    maxFreq = float(maxFreqString)*2
    minFreq = maxFreq/3

    freqRngCalc = (maxFreq - minFreq)/2
    freqAvgCalc = freqRngCalc + minFreq

    freqAvg = round(freqAvgCalc,3)
    freqRng = round(freqRngCalc,2)

    stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
    stanzaOutput += "Vein Motherlode Frequency: "+row['Frequency']+" * _default_, "+row['Frequency']+" * _default_, normal, base\n"
    if row['Motherlode.Size'] != "none":
        stanzaOutput += "Vein Motherlode Size: "+row['Motherlode.Size']+" * _default_, "+row['Motherlode.Size']+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
    if row['Branch.Length'] != "none":
        if row['Branch.Length'] != "default":
            stanzaOutput += "Vein Branch Length: "+row['Branch.Length']+" * _default_, "+row['Branch.Length']+" * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: "+row['Segment.Radius']+" * _default_, "+row['Segment.Radius']+" * _default_, normal, base\n"
    else:
        stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
        stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
    stanzaOutput += "Cloud Frequency: "+row['Frequency.1']+" * _default_, "+row['Frequency.1']+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Radius: "+row['Radius...Thickness']+" * _default_, "+row['Radius...Thickness']+" * _default_, normal, base\n"
    stanzaOutput += "Cloud Thickness: "+row['Radius...Thickness']+" * _default_, "+row['Radius...Thickness']+" * _default_, normal, base\n"
    stanzaOutput += newlineConvert(row['Extra.Sprocket.Settings'])+"\n"
    if row['Notes.']:
        stanzaOutput += "# "+row['Notes.']+"\n"
    stanzaOutput += "\n"

    ### Next, for the mountains.

    if row['Mountain.Avg.'] != "0":
      stanzaOutput += "[Mountain "+row['Ore.Name.']+"]\n"
      if row['Preferred.Preset'] == "Veins":
          stanzaOutput += "Distribution Presets: "+row['Vein.Preset.']+", "+row['Cloud.Preset']+", Vanilla\n"
      elif row['Preferred.Preset'] == "Clouds":
          stanzaOutput += "Distribution Presets: "+row['Cloud.Preset']+", "+row['Vein.Preset.']+", Vanilla\n"
      else:
          stanzaOutput += "Distribution Presets: Vanilla, "+row['Vein.Preset.']+", "+row['Cloud.Preset']+"\n"
      if row['Seed']:
          stanzaOutput += "Seed: "+row['Seed']+"\n"
      if row['Dimension'] != "Overworld":
          stanzaOutput += "Dimensions: "+row['Dimension']+"\n"
      stanzaOutput += "Wireframe Color: "+row['Debugging.Color']+"\n"
      stanzaOutput += "Bounding Box Color: "+row['Debugging.Color']+"\n"
      stanzaOutput += "Blocks: "+row['Block.ID.s.']+"\n"
      stanzaOutput += "Replaces: "+row['Replaces']+"\n"
      stanzaOutput += "Height: "+row['Mountain.Avg.']+", "+row['Mountain.Range.']+", "+row['Distribution.Type']+", base\n"

      maxSizeString = row['Standard.Size.']
      maxSize = float(maxSizeString)*2
      minSize = maxSize/3

      sizeRngCalc = (maxSize - minSize)/2
      sizeAvgCalc = sizeRngCalc + minSize

      sizeAvg = round(sizeAvgCalc,3)
      sizeRng = round(sizeRngCalc,2)

      stanzaOutput += "Standard Size: "+str(sizeAvg)+" * oreSize, "+str(sizeRng)+" * oreSize, normal, base\n"

      maxFreqString = row['Standard.Frequency.']
      maxFreq = float(maxFreqString)*2
      minFreq = maxFreq/3

      freqRngCalc = (maxFreq - minFreq)/2
      freqAvgCalc = freqRngCalc + minFreq

      freqAvg = round(freqAvgCalc,3)
      freqRng = round(freqRngCalc,2)

      stanzaOutput += "Standard Frequency: "+str(freqAvg)+" * oreFreq, "+str(freqRng)+" * oreFreq, normal, base\n"
      stanzaOutput += "Vein Motherlode Frequency: "+row['Frequency']+" * _default_, "+row['Frequency']+" * _default_, normal, base\n"
      if row['Motherlode.Size'] != "none":
          stanzaOutput += "Vein Motherlode Size: "+row['Motherlode.Size']+" * _default_, "+row['Motherlode.Size']+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base\n"
      if row['Branch.Length'] != "none":
          if row['Branch.Length'] != "default":
              stanzaOutput += "Vein Branch Length: "+row['Branch.Length']+" * _default_, "+row['Branch.Length']+" * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: "+row['Segment.Radius']+" * _default_, "+row['Segment.Radius']+" * _default_, normal, base\n"
      else:
          stanzaOutput += "Vein Branch Length: 0 * _default_, 0 * _default_, normal, base\n"
          stanzaOutput += "Vein Segment Radius: 0 * _default_, 0 * _default_, normal, base\n"
      stanzaOutput += "Cloud Frequency: "+row['Frequency.1']+" * _default_, "+row['Frequency.1']+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Radius: "+row['Radius...Thickness']+" * _default_, "+row['Radius...Thickness']+" * _default_, normal, base\n"
      stanzaOutput += "Cloud Thickness: "+row['Radius...Thickness']+" * _default_, "+row['Radius...Thickness']+" * _default_, normal, base\n"
      if row['Extra.Sprocket.Settings']:
          stanzaOutput += newlineConvert(row['Extra.Sprocket.Settings'])+"\n"
      if row['Extra.Sprocket.Mountain.Settings']:
          stanzaOutput += newlineConvert(row['Extra.Sprocket.Mountain.Settings'])+"\n"
      if row['Notes.']:
          stanzaOutput += "# "+row['Notes.']+"\n"

    return stanzaOutput

# Then, we call it until everything is done.

for row in records:
    print(oreStanza(row))