#!/usr/bin/python

# Sprocket.py: A configuration generator for the Custom Ore Generation:
#              First Revival add-on for Minecraft.  The program reads
#              the mod's name and list of ores from a simple file, and
#              then generates the xml configuration file that can be
#              inserted into COG for play.  Keep in mind that the
#              generated file is *basic*, this was designed to make
#              clean files for further refinement without all the
#              tedious searching for missing brackets or broken 
#              elements.

# UPDATE - 4/11/2015 - Script completely rewritten for more options and
#              flexibility.  

import random
import ConfigParser
import json
import sys
import os
import textwrap
import string

def randomHexNumber(length):
    return ''.join([random.choice('0123456789ABCDEF') for x in range(length)])

def indentText(level):
    spaceHolder = ""
    for i in range (0, level):
        spaceHolder += "    "
        
    return spaceHolder

# Initialize variables

errorCondition = ""

try:
    if not os.path.isfile(sys.argv[1]):
        sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": No such file or directory")
except IndexError:
	print "\n  Sprocket is designed to take an INI file and convert it into an"
	print "  XML file in the current directory.\n"
	print "USAGE:"
	print os.path.basename(sys.argv[0])+" <oregen file>\n"
	print "       or\n"
	print "python "+os.path.basename(sys.argv[0])+" <oregen file> \n"
	errorCondition=1
	sys.exit()

configFile = sys.argv[1]
   

modName = ""        # This is the mod name component for variable names
modPrefix = ""      # This comes before the ore name in variable names
                    #     (tic, mtlg)

# Initialize Ore Options
oreName = []                  # The name of this specific Ore
oreConfigName = []            # Ore name without the spaces
oreWorld = []                 # The world the ore spawns in
                              #    (Overworld, Nether, End)
oreBlock = []                 # The ore's actual block id
oreExtra = []                 # Comma separated list in name:meta format
oreMeta = []                  #  The meta number, if not 0
oreReplace = []               # The block the ore replaces
OreAdjacentAbove = []         # Ore is adjacent above which block?
OreAdjacentBelow = []         # Ore is adjacent below which block?
OreAdjacentBeside = []        # Ore is adjacent beside which block?
orePipe = []                  # Content of pipe distribution
                              #    (usually lava)
oreDistributions = []         # Comma-separated list of distribution
                              #    options.
oreDistType = []              # Pick distribution pattern
oreWireframe = []             # Wireframe color (web code)
oreHeight = []                # Center level for ore distributions
oreRange = []                 # Level range between lowest and highest
                              #    point
oreClampHigh = []             # Top possible level for ore
oreClampLow = []              # Bottom possible level for ore
oreFrequency = []             # Ore Frequency Multiplier
oreCloudFrequency = []        # Frequency Multiplier for Clouds
oreVeinFrequency = []         # Frequency Multiplier for Veins
oreStdFrequency = []          # Frequency Multiplier for Standard 
oreSize = []                  # Ore Size Multiplier
oreCloudSize = []             # Size Multiplier for Clouds
oreVeinSize = []              # Size Multiplier for Veins
oreStdSize = []               # Size Multiplier for Standard 
oreStdHeight = []             # Height for Standard Distributions
                              #   Overrides Main Height Value
oreStdRange = []              # Range for Standard Distributions
                              #   Overrides Main Range Value
oreVeinHeight = []            # Height for Vein Distributions
                              #   Overrides Main Range Value
oreVeinRange = []             # Range for Vein Distributions
                              #   Overrides Main Range Value
oreCloudHeight = []           # Height for Cloud Distributions
                              #   Overrides Main Range Value
oreCloudRange = []            # Range for Cloud Distributions
                              #   Overrides Main Range Value
oreDensity = []               # Ore Density Multiplier
oreCloudDensity = []          # Density Multiplier for Clouds
oreVeinDensity = []           # Density Multiplier for Veins
oreVeinBranchFrequency = []   # Ore Veins Branch Frequency
oreVeinBranchLengthAvg = []   # Ore Veins Branch Length Average
oreVeinBranchLengthRange = [] # Ore Veins Branch Length Range
oreVeinBranchHeight = []      # Ore Veins Branch Height Limit
oreVeinBranchInclineAvg = []  # Ore Veins Branch Inclination Average
oreVeinBranchInclineRange = []# Ore Veins Branch Inclination Range
oreVeinSegmentRadiusAvg = []  # Ore Veins Segment Radius Average
oreVeinSegmentRadiusRange = []# Ore Veins Segment Radius Range
oreVeinSegmentAngleAvg = []   # Ore Veins Segment Angle Average
oreVeinSegmentAngleRange = [] # Ore Veins Segment Angle Range
oreVeinSegmentPitchAvg = []   # Ore Veins Segment Pitch Average
oreVeinSegmentPitchRange = [] # Ore Veins Segment Pitch Range
oreCloudThickness = []        # Thickness Multiplier for Clouds
oreBiomes = []                # Ores only spawn in these biomes
oreAvoid = []                 # Ores will not spawn in these biomes
orePreferBiomes = []          # Ores spawn extra in these biomes
oreNoPreferBiomes = []        # Ores won't spawn extra in these biomes
orePreMultiplier = []         # "Prefers" Multiplier
oreScale = []                 # COG Surface Scaling
oreActive = []                # Is ore distribution active by default?
oreSeed = []                  # Pick a distribution seed
oreSubstitution = []          # Do we remove this ore before generating?
                              #   Useful if mod's oregen can be turned
                              #   off.


oreList = ""
indentLine=0

# Open a configuration file for reading, and prepare defaults.
Config = ConfigParser.SafeConfigParser(
    defaults={'Block':'MISSING',
              'Extra':'MISSING',
              'World':'Overworld',
              'Meta':'0',
              'Replace':'minecraft:stone',
              'Adjacent Above':'MISSING',
              'Adjacent Below':'MISSING',
              'Adjacent Beside':'MISSING',
              'Pipe':'minecraft:lava',
              'Distribution':'Vanilla',
              'Distribution Type':'normal',
              'Biomes':'ALL',
              'Avoid':'NONE',
              'Prefers':'NONE',
              'Prefers Not':'NONE',
              'Prefers Multiplier':'2',
              'Scale':'SeaLevel',
              'Active':'Yes',
              'Substitute':'Yes',
              'Seed':randomHexNumber(4),
              'Wireframe':randomHexNumber(6),
              'Height':'_default_',
              'Range':'_default_',
              'Min Height':'0',
              'Max Height':'0',
              'Density':'1',
              'Frequency':'1',
              'Size':'1',
              'Standard Frequency':'1',
              'Standard Height':'0',
              'Standard Range':'0',
              'Standard Size':'1',
              'Vein Frequency':'1',
              'Vein Size':'1',
              'Vein Height':'0',
              'Vein Range':'0',
              'Vein Density':'1',
              'Vein Branch Frequency':'1',
              'Vein Branch Height Limit':'0',
              'Vein Branch Inclination Average':'0',
              'Vein Branch Inclination Range':'0',
              'Vein Branch Length Average':'1',
              'Vein Branch Length Range':'1',
              'Vein Segment Angle Average':'0',
              'Vein Segment Angle Range':'0',
              'Vein Segment Pitch Average':'0',
              'Vein Segment Pitch Range':'0',
              'Vein Segment Radius Average':'1',
              'Vein Segment Radius Range':'1',
              'Cloud Frequency':'1',
              'Cloud Size':'1',
              'Cloud Height':'0',
              'Cloud Range':'0',
              'Cloud Density':'1',
              'Cloud Thickness':'1'
    })
Config.read(configFile)

# Get the mod's name in three forms, one for mod-specific variables,
# one for display in strings, and a prefix to use for ore variables.
try:
    modName = Config.get('Mod', 'Name')  # "My Mod 2"
except ConfigParser.NoSectionError:
	print "No [Mod] section found."
	errorCondition=1
	sys.exit(""+os.path.basename(sys.argv[1])+": nothing written due to errors\n")
except ConfigParser.NoOptionError:
    print "No mod name found."
    errorCondition=1

try:
    modPrefix = Config.get('Mod', 'Prefix') # "mmd2"
except ConfigParser.NoOptionError:
    print "No mod prefix found."
    errorCondition=1

try:
    modDetect = Config.get('Mod', 'Detect') # "MyMod"
except ConfigParser.NoOptionError:
    print "No ModID to detect was found."
    errorCondition=1

# If errors occurred at this point, don't go any further.
if errorCondition:
    sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": nothing written due to errors\n")

print "Generating configuration for "+modName+"."
                    
modConfigName=modName.replace(" ", "")

oreName = Config.sections()
oreName.pop(0) # The first section is not an ore, it's the mod's
               # settings.  It needs to go.

oreCount = 0

# Creating a set of lists for the options; memory access is always
# faster than disk access.


for currentOre in oreName:
    oreConfigName.append(oreName[oreCount].replace(" ", ""))
    oreBlock.append(Config.get(currentOre, 'Block'))
    oreExtra.append(Config.get(currentOre, 'Extra'))
    oreWorld.append(Config.get(currentOre, 'World'))
    oreMeta.append(Config.get(currentOre, 'Meta'))
    oreReplace.append(Config.get(currentOre, 'Replace'))
    OreAdjacentAbove.append(Config.get(currentOre, 'Adjacent Above'))
    OreAdjacentBelow.append(Config.get(currentOre, 'Adjacent Below'))
    OreAdjacentBeside.append(Config.get(currentOre, 'Adjacent Beside'))
    orePipe.append(Config.get(currentOre, 'Pipe'))
    oreDistributions.append(Config.get(currentOre, 'Distributions'))
    oreDistType.append(Config.get(currentOre, 'Distribution Type'))
    oreWireframe.append(Config.get(currentOre, 'Wireframe'))
    oreHeight.append(Config.get(currentOre, 'Height'))
    oreRange.append(Config.get(currentOre, 'Range'))
    oreClampHigh.append(Config.get(currentOre, 'Max Height'))
    oreClampLow.append(Config.get(currentOre, 'Min Height'))
    oreFrequency.append(Config.get(currentOre, 'Frequency'))
    oreStdFrequency.append(Config.get(currentOre, 'Standard Frequency'))
    oreVeinFrequency.append(Config.get(currentOre, 'Vein Frequency'))
    oreCloudFrequency.append(Config.get(currentOre, 'Cloud Frequency'))
    oreStdHeight.append(Config.get(currentOre, 'Standard Height'))
    oreStdRange.append(Config.get(currentOre, 'Standard Range'))
    oreVeinHeight.append(Config.get(currentOre, 'Vein Height'))
    oreVeinRange.append(Config.get(currentOre, 'Vein Range'))
    oreCloudHeight.append(Config.get(currentOre, 'Cloud Height'))
    oreCloudRange.append(Config.get(currentOre, 'Cloud Range'))
    oreSize.append(Config.get(currentOre, 'Size'))
    oreStdSize.append(Config.get(currentOre, 'Standard Size'))
    oreVeinSize.append(Config.get(currentOre, 'Vein Size'))
    oreCloudSize.append(Config.get(currentOre, 'Cloud Size'))
    oreDensity.append(Config.get(currentOre, 'Density'))
    oreCloudDensity.append(Config.get(currentOre, 'Cloud Density'))
    oreVeinDensity.append(Config.get(currentOre, 'Vein Density'))
    oreVeinBranchFrequency.append(Config.get(currentOre, 'Vein Branch Frequency'))
    oreVeinBranchHeight.append(Config.get(currentOre, 'Vein Branch Height Limit'))
    oreVeinBranchLengthAvg.append(Config.get(currentOre, 'Vein Branch Length Average'))
    oreVeinBranchLengthRange.append(Config.get(currentOre, 'Vein Branch Length Range'))
    oreVeinBranchInclineAvg.append(Config.get(currentOre, 'Vein Branch Inclination Average'))
    oreVeinBranchInclineRange.append(Config.get(currentOre, 'Vein Branch Inclination Range'))
    oreVeinSegmentRadiusAvg.append(Config.get(currentOre, 'Vein Segment Radius Average'))
    oreVeinSegmentRadiusRange.append(Config.get(currentOre, 'Vein Segment Radius Range'))
    oreVeinSegmentAngleAvg.append(Config.get(currentOre, 'Vein Segment Angle Average'))
    oreVeinSegmentAngleRange.append(Config.get(currentOre, 'Vein Segment Angle Range'))
    oreVeinSegmentPitchAvg.append(Config.get(currentOre, 'Vein Segment Pitch Average'))
    oreVeinSegmentPitchRange.append(Config.get(currentOre, 'Vein Segment Pitch Range'))
    oreCloudThickness.append(Config.get(currentOre, 'Cloud Thickness'))
    oreBiomes.append(Config.get(currentOre, 'Biomes'))
    oreAvoid.append(Config.get(currentOre, 'Avoid'))
    orePreferBiomes.append(Config.get(currentOre, 'Prefers'))
    oreNoPreferBiomes.append(Config.get(currentOre, 'Prefers Not'))
    orePreMultiplier.append(Config.get(currentOre, 'Prefers Multiplier'))
    oreScale.append(Config.get(currentOre, 'Scale'))
    oreActive.append(Config.get(currentOre, 'Active'))
    oreSubstitution.append(Config.get(currentOre, 'Substitute'))
    oreSeed.append(Config.get(currentOre, 'Seed'))
    
    
    # Check to make sure the Block value is valid.
    if Config.get(currentOre, 'Block') == 'MISSING':
        print('Error: The \'['+currentOre+']\' section is missing a block name.')
        errorCondition = 'T'
    
    oreCount += 1

# Let's make sure there is any reason to continue the generation.
if oreCount == 0:
    print('Error: There are no ores to configure.')
    errorCondition = 'T'

# All ore data has been imported from the configuration file.  Now we 
# need to generate the actual XML configuration.

# First, we'll set up the variables that will hold the generated text
# until everything is ready to be written to the new file.
headerTemplate = ""
controlsTemplate = []
oreConfigTemplate = []

########################## IS DISTRIBUTION ACTIVE? ###################
# Return nothing if distribution is active; the default distribution
# will be the first one configured.  If the distribution is active,
# then "default='none'" will be returned.

def ifDistActive(oreSelect):
    if (oreActive[oreSelect] == "no") or (oreActive[oreSelect] == "No"):
        return " default='none'"
    else:
        return " "

########################## MAKE CONFIG HEADING #######################

def headerGen():
    oreList = ", ".join(oreName)
    fmtOreList = "\r\n".join(textwrap.wrap(oreList, 70))
    return "\n\
<!-- ================================================================ \n\
\n\
Custom Ore Generation:   "+modName+" Module\n\n\
Generates: \n"+fmtOreList+"\n\
\n\
================================================================ -->\n\n"

##################### BIOME LISTING ###########################
# This limits ore generation to specific biomes, based on the
# Forge Biome Dictionary.

def biomeSet(biome):
    global indentLine
    biomeCommand = indentText(indentLine)+"<BiomeType name='"+biome+"'/>\n"
    
    return biomeCommand

def biomeAvoid(biome):
    biomeCommand = indentText(indentLine)+"<BiomeType name='"+biome+"' weight='-1'/>\n"
    
    return biomeCommand


def biomeList(currentBiomeList):
    biomeList = currentBiomeList.split(',')
    biomeCommandList = ""
    
    for biomeSelect in range (0, len(biomeList)):
        biomeCommandList += biomeSet(biomeList[biomeSelect])
        if biomeList[biomeSelect] == "ALL":
            biomeCommandList = ""
    
    return biomeCommandList


def biomeAvoidList(currentBiomeList):
    biomeList = currentBiomeList.split(',')
    biomeCommandList = ""
    
    for biomeSelect in range (0, len(biomeList)):
        biomeCommandList += biomeAvoid(biomeList[biomeSelect])
        if biomeList[biomeSelect] == "NONE":
            biomeCommandList = ""
    
    return biomeCommandList

####################### Block Replacement ##########################
# This allows a block to replace multiple blocks.

def replaceSet(replace):
    global indentLine
    replaceCommand = indentText(indentLine)+"<Replaces block='"+replace+"'/>\n"
    
    return replaceCommand

def replaceList(currentReplaceList):
    replaceList = currentReplaceList.split(',')
    replaceCommandList = ""
    
    for replaceSelect in range (0, len(replaceList)):
        replaceCommandList += replaceSet(replaceList[replaceSelect])
    
    return replaceCommandList
    
def firstReplace(currentReplaceList):
    replaceList = currentReplaceList.split(',')
    
    return replaceList[0]
    
######################## Block Adjacency ###########################

def adjacentAboveSet(adjacentTo):
    global indentLine
    replaceCommand = indentText(indentLine)+"<PlacesAbove block='"+adjacentTo+"'/>\n"
    
    return replaceCommand
    
    
def adjacentBelowSet(adjacentTo):
    global indentLine
    replaceCommand = indentText(indentLine)+"<PlacesBelow block='"+adjacentTo+"'/>\n"
    
    return replaceCommand
    
    
def adjacentBesideSet(adjacentTo):
    global indentLine
    replaceCommand = indentText(indentLine)+"<PlacesBeside block='"+adjacentTo+"'/>\n"
    
    return replaceCommand
    
################## CHOOSE DISTRIBUTION OPTIONS #####################

def distributionControlGen(currentOreDistBase):
    global indentLine
    currentOreDist = currentOreDistBase.replace(" ", "")
    if currentOreDist == 'Substitute': # uses StandardGen
        optionText = indentText(indentLine)+"<Choice value='substituteGen' displayValue='Substitute'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Simple substitution.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
    elif currentOreDist == 'Vanilla': # uses StandardGen
        optionText = indentText(indentLine)+"<Choice value='vanillaStdGen' displayValue='Vanilla'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Vanilla-style clusters.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
        
    elif currentOreDist == 'LayeredVeins': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='layeredVeins' displayValue='Layered Veins'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Layered Veins.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
               
    elif currentOreDist == 'VerticalVeins': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='verticalVeins' displayValue='Vertical Veins'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Vertical Veins.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
               
    elif currentOreDist == 'SmallDeposits': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='smallDeposits' displayValue='Small Deposits'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Small Deposits.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
        
    elif currentOreDist == 'Geodes': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='geodes' displayValue='Geodes'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Geodes.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
        
    elif currentOreDist == 'HugeVeins': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='hugeVeins' displayValue='Huge Veins'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Huge Veins.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
        
    elif currentOreDist == 'SparseVeins': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='sparseVeins' displayValue='Sparse Veins'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Sparse Veins.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText

    elif currentOreDist == 'PipeVeins': # uses Veins
        optionText = indentText(indentLine)+"<Choice value='pipeVeins' displayValue='Pipe Veins'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Pipe Veins.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText

#    elif currentOreDist == 'CompoundVeins': # uses Veins
#        optionText = indentText(indentLine)+"<Choice value='compoundVeins' displayValue='Compound Veins'>\n"
#        indentLine += 1
#        optionText += indentText(indentLine)+"<Description>\n"
#        indentLine += 1
#        optionText += indentText(indentLine)+"Compound Veins.\n"
#        indentLine -= 1
#        optionText += indentText(indentLine)+"</Description>\n"
#        indentLine -= 1
#        optionText += indentText(indentLine)+"</Choice>\n"
#        return optionText
        
    elif currentOreDist == 'StrategicCloud': # uses Cloud
        optionText = indentText(indentLine)+"<Choice value='strategicCloud' displayValue='Clouds'>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        optionText += indentText(indentLine)+"Strategic Clouds.\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Description>\n"
        indentLine -= 1
        optionText += indentText(indentLine)+"</Choice>\n"
        return optionText
        
    else:
        print "There is no '"+currentOreDist+"' distribution!"
        errorCondition = 'T'

################### CONFIGURATION SETUP ##############################
# Assembles the configuration section for in-game setup.

def controlsGen(currentOreGen):
    global indentLine
    
    oreConfigName=modPrefix+oreName[currentOreGen]
    oreConfigName=oreConfigName.replace(" ", "")
    
    # Opening
    configScriptOpen = indentText(indentLine)+"<OptionChoice name='"+oreConfigName+"Dist'"+ifDistActive(currentOreGen)+" displayState='shown' displayGroup='group"+modConfigName+"'> \n"
    indentLine += 1
    configScriptOpen += indentText(indentLine)+"<Description> Controls how "+oreName[currentOreGen]+" is generated </Description> \n"
    configScriptOpen += indentText(indentLine)+"<DisplayName>"+modName+" "+oreName[currentOreGen]+"</DisplayName>\n"
    
    # Actual Configuration List
    # Start with an empty script
    configScriptList = ""
    
    # The list of ore distributions will determine available options.
    distributionList = oreDistributions[currentOreGen]
    distributionList = distributionList.split(',')
    for distribution in distributionList:
         configScriptList += distributionControlGen(distribution)
    
    # Closing
    configScriptClose = indentText(indentLine)+"<Choice value='none' displayValue='None' description='"+oreName[currentOreGen]+" is not generated in the world.'/>\n"
    indentLine -= 1
    configScriptClose += indentText(indentLine)+"</OptionChoice>\n"
    configScriptClose += indentText(indentLine)+"<OptionNumeric name='"+oreConfigName+"Freq' default='1'  min='0' max='5' displayState=':= if(?advOptions,\"shown\",\"hidden\")' displayGroup='group"+modConfigName+"'>\n"
    indentLine += 1
    configScriptClose += indentText(indentLine)+"<Description> Frequency multiplier for "+modName+" "+oreName[currentOreGen]+" distributions </Description>\n"
    configScriptClose += indentText(indentLine)+"<DisplayName>"+modName+" "+oreName[currentOreGen]+" Freq.</DisplayName>\n"
    indentLine -= 1
    configScriptClose += indentText(indentLine)+"</OptionNumeric>\n"
    configScriptClose += indentText(indentLine)+"<OptionNumeric name='"+oreConfigName+"Size' default='1'  min='0' max='5' displayState=':= if(?advOptions,\"shown\",\"hidden\")' displayGroup='group"+modConfigName+"'>\n"
    indentLine += 1
    configScriptClose += indentText(indentLine)+"<Description> Size multiplier for "+modName+" "+oreName[currentOreGen]+" distributions </Description>\n"
    configScriptClose += indentText(indentLine)+"<DisplayName>"+modName+" "+oreName[currentOreGen]+" Size</DisplayName>\n"
    indentLine -= 1
    configScriptClose += indentText(indentLine)+"</OptionNumeric>\n"
          
    return configScriptOpen+configScriptList+configScriptClose

############## DETECT META NUMBER #################################
# If the meta number is anything other than zero, return the number
# Preceded by a colon.

def metaGen(currentMeta):
    if oreMeta[currentMeta] == '0':
        return ""
    else:
        return ":"+oreMeta[currentMeta]


################### ORE CLAMPING #################################
# Set a maximum or minimum level for ore to appear.

def highClamp(clampLevel):
    global errorCondition
    
    if int(clampLevel) == 0:
        return ""
    else:
        return " maxHeight='"+str(clampLevel)+"'"
        
def lowClamp(clampLevel):
    global errorCondition
    
    if int(clampLevel) == 0:
        return ""
    else:
        return " minHeight='"+str(clampLevel)+"'"
        
def clampRange(lowClampLevel, highClampLevel):

    if int(lowClampLevel) == 0 and int(highClampLevel) == 0: # No clamping is needed
        return ""
    elif int(lowClampLevel) > 0 or int(highClampLevel) > 0:
        return lowClamp(lowClampLevel)+highClamp(highClampLevel)
    else:
        print('Error: The \'['+currentOre+']\' Min Height must be a number of 0 or greater.')
        errorCondition = 'T'
        return ""

################## INDIVIDUAL DISTRIBUTIONS ######################
# Each distribution is individually defined.


### Substitution Distribution

def substituteDist(currentOreGen,level):
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
    global indentLine
    
    distText = indentText(indentLine)+"<Substitute name='"+oreConfigName+str(level)+"Substitute' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+">\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description> This is a straight-up replacement of one block with another. </Description>\n"
    distText += replaceList(oreReplaceName)
    indentLine -= 1
    distText += indentText(indentLine)+"</Substitute>\n"
     
    return distText
    
### Standard "Vanilla" Distribution

def vanillaDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreStdHeight[currentOreGen] != "0":
        localHeight = oreStdHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreStdRange[currentOreGen] != "0":
        localRange = oreStdRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseStandard"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetStandardGen"
    
    distText = indentText(indentLine)+"<StandardGen name='"+oreConfigName+str(level)+"Standard' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"This mimics vanilla ore generation.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        
        distText += indentText(indentLine)+"<Setting name='Size' avg=':= "+oreSize[currentOreGen]+" * "+oreStdSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='Height' avg=':= "+localHeight+"' range=':= "+localRange+"' type='uniform'/> \n"
        distText += indentText(indentLine)+"<Setting name='Frequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreStdFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='Frequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName) 
        distText += biomeAvoidList(oreAvoidName)
        
    indentLine -= 1
    distText += indentText(indentLine)+"</StandardGen>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            ##  There is no preferred distribution setup for vanilla distributions.
            # distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Vanilla) Settings -->\n"
            # distText += vanillaDist(currentOreGen, "Prefers")    
            # distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Vanilla) Settings -->\n"
    return distText

### Layered Vein Distribution

def layeredVeinsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetLayeredVeins"
    
    distText = indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Small, fairly rare motherlodes with 2-4 horizontal veins each.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"'/> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Layered Veins) Settings -->\n"
            distText += layeredVeinsDist(currentOreGen, "Prefers")    
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Layered Veins) Settings -->\n"
    return distText

### Vertical Vein Distribution

def verticalVeinsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseParentVeins"
        childInheritLine = oreConfigName+"BaseChildVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetVerticalVeins"
        childInheritLine = "PresetVerticalVeins"
        
    # Parent Distribution
    
    distText = indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"ParentVeins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Single vertical veins that occur with no motherlodes.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"


    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':=  "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"    

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    # Child Distribution
    
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"ChildVeins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+childInheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Single vertical veins that occur with no motherlodes.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"


    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * 3 * _default_'/>\n"    

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
       
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Vertical Veins) Settings -->\n"
            distText += verticalVeinsDist(currentOreGen, "Prefers")    
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Vertical Veins) Settings -->\n"
    return distText

### Small Deposit Distribution

def smallDepositsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetSmallDeposits"
    
    distText = indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Small motherlodes without any branches.\n"
        distText += indentText(indentLine)+"Similar to the deposits produced by StandardGen distributions.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base":
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Small Deposits) Settings -->\n"
            distText += smallDepositsDist(currentOreGen, "Prefers")    
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Small Deposits) Settings -->\n"
    return distText

### Geode Distribution  #########################################################################################################################################

def geodeSimple(currentOreGen,level):

    print "...using simple geode... "
    
    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    
    preferMultiplier = ""
    global indentLine
    
    geodeSeed = oreSeed[currentOreGen]
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetSmallDeposits"
        
    #   Outer Crust
    distText = indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Crust -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Shell' block='"+orePipe[currentOreGen]+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The geode's outer shell, composed of the Pipe material.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 3 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:air'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:water'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:lava'/>\n"
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Crust -->\n"
    distText += indentText(indentLine)+"\n"
            
    # Inner Crystals
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Crystals -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Crystal' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The geode's inner material, usually some form of crystal.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 1.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+orePipe[currentOreGen]+"'/>\n"
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Crystals -->\n"
    distText += indentText(indentLine)+"\n"
        
    #   Central Air Pocket
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Air Pocket -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"AirBubble' block='minecraft:air'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The air pocket within the center of a geode.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+orePipe[currentOreGen]+"'/>\n"
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Air Pocket -->\n"
    distText += indentText(indentLine)+"\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Geode) Settings -->\n"
            distText += geodesDist(currentOreGen, "Prefers") 
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Geode) Settings -->\n"
      
    return distText

def geodeCompound(currentOreGen,level):

    print "	...using compound geodes... "
    
    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    orePreExtraName=oreExtra[currentOreGen]
    
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
    oreExtraName=orePreExtraName.replace(" ", "")
    
    # Generate Extra Block List
    oreExtraBlocks = oreExtraName.split(',')
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    
    preferMultiplier = ""
    global indentLine
    
    geodeSeed = oreSeed[currentOreGen]
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetSmallDeposits"
    
    #   Outer Crust
    distText = indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Crust -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Shell' block='"+orePipe[currentOreGen]+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The geode's outer shell, composed of the Pipe material.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 3 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:air'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:water'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:lava'/>\n"
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Crust -->\n"
    distText += indentText(indentLine)+"\n"
            
    # Inner Crystals
    
    # We don't want the ores fighting for placement, so, we'll divide
    # each density by the number of ores.  To do that, we need to know
    # how many ores we'll be using.  Let's get that out of the way.
    oreTypeCount = len(oreExtraBlocks)+1
    oreCount = 0
    
    # Now, the first run will be for the base "Block" value.
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Crystals -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Crystal' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The geode's inner material, usually some form of crystal.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 1.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+orePipe[currentOreGen]+"'/>\n"
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Crystals -->\n"
    distText += indentText(indentLine)+"\n"
    
    lastBlock = oreBlock[currentOreGen]+metaGen(currentOreGen)
    fractionNumber = oreTypeCount
    
    # Now to add ore distributions for all extra ores.
        
    for extraBlock in oreExtraBlocks:
        oreCount += 1
        fractionNumber -= 1
        distText += indentText(indentLine)+"\n"
        distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Crystals ("+extraBlock+") -->\n"
        distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+str(oreCount)+"Crystal' block='"+extraBlock+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
        indentLine += 1
        distText += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        
        if level == "Base":
            distText += indentText(indentLine)+"The geode's inner material, usually some form of crystal.\n"
        elif level == "Prefers":
            distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
        else:
            distText += indentText(indentLine)+" "
            
        indentLine -= 1
        distText += indentText(indentLine)+"</Description>\n"
        distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
        distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
        
        if level == "Base":
            distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 1.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
            distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
            distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+str(fractionNumber)+"/"+str(oreTypeCount)+" * "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
            distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
            distText += indentText(indentLine)+"<Replaces block='"+lastBlock+"'/>\n"
        
        if level == "Prefers":
            distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
            distText += biomeList(orePreferName)
            distText += biomeAvoidList(oreNoPreferName)
        else:
            distText += biomeList(oreBiomeName)    
            distText += biomeAvoidList(oreAvoidName)
        
        lastBlock = extraBlock
        
        indentLine -= 1
        distText += indentText(indentLine)+"</Veins>\n"
        distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Crystals -->\n"
        distText += indentText(indentLine)+"\n"
            
    #   Central Air Pocket
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Geode Air Pocket -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"AirBubble' block='minecraft:air'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+geodeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"The air pocket within the center of a geode.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "
        
    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'/>\n"
        distText += indentText(indentLine)+"<Replaces block='"+orePipe[currentOreGen]+"'/>\n"
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Geode Air Pocket -->\n"
    distText += indentText(indentLine)+"\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Geode) Settings -->\n"
            distText += geodesDist(currentOreGen, "Prefers") 
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Geode) Settings -->\n"
      
    return distText
        
def geodesDist(currentOreGen,level):
        
    # There will be two functions, one for a simple geode with one
    # ore, or a compound one containing multiple ores.
    
    orePreExtraName=oreExtra[currentOreGen]
    oreExtraName=orePreExtraName.replace(" ", "")
    
    # Generate Extra Block List
    oreExtraBlocks = oreExtraName.split(',')
        
    if oreExtraBlocks[0] == "MISSING":
        return geodeSimple(currentOreGen,level)
    else:
        return geodeCompound(currentOreGen,level)

#########################################################################################################################################

### Huge Vein Distribution

def hugeVeinsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetLayeredVeins"
    
    distText = indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Very large, extremely rare motherlodes.  Each motherlode has many long slender branches - so thin that\n"
        distText += indentText(indentLine)+"parts of the branch won't contain any ore at all.  This, combined with the incredible length of the\n"
        distText += indentText(indentLine)+"branches, makes them more challenging to follow underground.  Once found, however, a motherlode contains\n"
        distText += indentText(indentLine)+"enough ore to keep a player supplied for a very long time.\n"
        distText += indentText(indentLine)+"The rarity of these veins might be too frustrating in a single-player setting.  In SMP, though, teamwork \n"
        distText += indentText(indentLine)+"could make finding them much easier and the motherlodes are big enough to supply several people without\n"
        distText += indentText(indentLine)+"shortage.  This might be a good way to add challenge to multiplayer worlds.\n"
        distText += indentText(indentLine)+"Credit: based on feedback by dyrewulf from the MC forums.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"

    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' /> \n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)

    # "Hint" Veins
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseHintVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetHintVeins"
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Huge Vein Hint Veins -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"HintVeins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Single blocks, generously scattered through all heights (density is about that of vanilla iron ore). \n"
        distText += indentText(indentLine)+"They will replace dirt and sandstone (but not grass or sand), so they can be found nearer  \n"
        distText += indentText(indentLine)+"to the surface than most ores.  Intened to be used as a child distribution for large, rare strategic  \n"
        distText += indentText(indentLine)+"deposits that would otherwise be very difficult to find. \n"

    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    distText += indentText(indentLine)+"<Replaces block='minecraft:dirt'/>\n"
    distText += indentText(indentLine)+"<Replaces block='minecraft:sandstone'/>\n"
    distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Huge Vein Hint Veins -->\n\n"
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Huge Veins) Settings -->\n"
            distText += hugeVeinsDist(currentOreGen, "Prefers")  
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Huge Veins) Settings -->\n"  
    return distText

### Sparse Vein Distribution

def sparseVeinsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetSparseVeins"
    
    distText = indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Large veins filled very lightly with ore.  Because they contain less ore per volume, \n"
        distText += indentText(indentLine)+"these veins are relatively wide and long.  Mining the ore from them is time consuming \n"
        distText += indentText(indentLine)+"compared to solid ore veins.  They are also more difficult to follow, since it is \n"
        distText += indentText(indentLine)+"harder to get an idea of their direction while mining.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' />\n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"    

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Sparse Veins) Settings -->\n"
            distText += sparseVeinsDist(currentOreGen, "Prefers")  
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Sparse Veins) Settings -->\n"  
    return distText

### Pipe Vein Distribution

def pipeVeinsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreVeinHeight[currentOreGen] != "0":
        localHeight = oreVeinHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreVeinRange[currentOreGen] != "0":
        localRange = oreVeinRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    pipeSeed = oreSeed[currentOreGen]
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetPipeVeins"
    
    # Ore
    
    distText = indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Ore Configuration -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"' seed='0x"+pipeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Short sparsely filled veins sloping up from near the bottom of the map.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"' />\n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreVeinFrequency[currentOreGen]+" * "+oreConfigName+"Freq * _default_'/>\n"

        if oreVeinBranchFrequency[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchFrequency' avg=':= "+oreVeinBranchFrequency[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchLengthAvg[currentOreGen] != "1" or oreVeinBranchLengthRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='BranchLength' avg=':= "+oreVeinBranchLengthAvg[currentOreGen]+" * _default_' range=':= "+oreVeinBranchLengthRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinBranchHeight[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchHeightLimit' avg=':= "+oreVeinBranchHeight[currentOreGen]+"'/>\n"
        if oreVeinBranchInclineAvg[currentOreGen] != "0" or oreVeinBranchInclineRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='BranchInclination' avg=':= "+oreVeinBranchInclineAvg[currentOreGen]+"' range=':= "+oreVeinBranchInclineRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentRadiusAvg[currentOreGen] != "1" or oreVeinSegmentRadiusRange[currentOreGen] != "1":
            distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusAvg[currentOreGen]+" * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * "+oreVeinSegmentRadiusRange[currentOreGen]+" * _default_'/>\n"
        if oreVeinSegmentAngleAvg[currentOreGen] != "0" or oreVeinSegmentAngleRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentAngle' avg=':= "+oreVeinSegmentAngleAvg[currentOreGen]+"' range=':= "+oreVeinSegmentAngleRange[currentOreGen]+"'/>\n"
        if oreVeinSegmentPitchAvg[currentOreGen] != "0" or oreVeinSegmentPitchRange[currentOreGen] != "0":
            distText += indentText(indentLine)+"<Setting name='SegmentPitch' avg=':= "+oreVeinSegmentPitchAvg[currentOreGen]+"' range=':= "+oreVeinSegmentPitchRange[currentOreGen]+"'/>\n"
        
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='MotherlodeFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Ore Configuration -->\n"
    distText += indentText(indentLine)+"\n"
    
    # Pipe Material
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Pipe Configuration -->\n"
    distText += indentText(indentLine)+"<Veins name= '"+oreConfigName+str(level)+"Pipe' block='"+orePipe[currentOreGen]+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+oreConfigName+str(level)+"Veins' seed='0x"+pipeSeed+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Fills center of each tube with Pipe material.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    
    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='MotherlodeSize' avg=':= 0.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= 0.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='SegmentRadius' avg=':= 0.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= 0.5 * "+oreSize[currentOreGen]+" * "+oreVeinSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreVeinDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += replaceList(oreReplaceName)
        distText += indentText(indentLine)+"<Replaces block='minecraft:dirt'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:stone'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:gravel'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:netherrack'/>\n"
        distText += indentText(indentLine)+"<Replaces block='minecraft:end_stone'/>\n"
    
    if level == "Prefers":
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Pipe Configuration -->\n"
    distText += indentText(indentLine)+"\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Pipe Veins) Settings -->\n"
            distText += pipeVeinsDist(currentOreGen, "Prefers")    
            distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Pipe Veins) Settings -->\n"
    return distText

### Strategic Cloud Distribution

def strategicCloudsDist(currentOreGen,level):

    # Remove spaces from configured lists.
    orePreConfigName=modPrefix+oreName[currentOreGen]
    orePreBiomeName=oreBiomes[currentOreGen]
    orePreAvoidName=oreAvoid[currentOreGen]
    orePrePreferName=orePreferBiomes[currentOreGen]
    orePreNoPreferName=oreNoPreferBiomes[currentOreGen]
    orePreReplaceName=oreReplace[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    oreBiomeName=orePreBiomeName.replace(" ", "")
    oreAvoidName=orePreAvoidName.replace(" ", "")
    orePreferName=orePrePreferName.replace(" ", "")
    oreNoPreferName=orePreNoPreferName.replace(" ", "")
    oreReplaceName=orePreReplaceName.replace(" ", "")
        
    # Override global height and range with local values.
    if oreCloudHeight[currentOreGen] != "0":
        localHeight = oreCloudHeight[currentOreGen]
    else:
        localHeight = oreHeight[currentOreGen]
    
    if oreCloudRange[currentOreGen] != "0":
        localRange = oreCloudRange[currentOreGen]
    else:
        localRange = oreRange[currentOreGen]
    
    # Misc. variables.
    preferMultiplier = ""
    global indentLine
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseCloud"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetStrategicCloud"
    
    # Main Cloud
    
    distText = indentText(indentLine)+"<Cloud name='"+oreConfigName+str(level)+"Cloud' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Large irregular clouds filled lightly with ore.  These are huge, spanning several \n"
        distText += indentText(indentLine)+"adjacent chunks, and consequently rather rare.  They contain a sizeable amount of \n"
        distText += indentText(indentLine)+"ore, but it takes some time and effort to mine due to low density.\n"
        distText += indentText(indentLine)+"The intent for strategic clouds is that the player will need to actively search for\n"
        distText += indentText(indentLine)+"one and then set up a semi-permanent mining base and spend some time actually mining\n"
        distText += indentText(indentLine)+"the ore.\n"
    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"


    if level == "Base":
        distText += indentText(indentLine)+"<Setting name='CloudRadius' avg=':= "+oreSize[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='CloudThickness' avg=':= "+oreSize[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='CloudHeight' avg=':= "+localHeight+"' range=':= "+localRange+"' type='"+oreDistType[currentOreGen]+"' scaleTo='"+oreScale[currentOreGen]+"'/>\n"
        distText += indentText(indentLine)+"<Setting name='OreDensity' avg=':= "+oreDensity[currentOreGen]+" * "+oreCloudDensity[currentOreGen]+" * _default_' range=':= _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='CloudThickness' avg=':= "+oreSize[currentOreGen]+" * "+oreCloudThickness[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size * _default_' range=':= "+oreSize[currentOreGen]+" * "+oreCloudThickness[currentOreGen]+" * "+oreCloudSize[currentOreGen]+" * "+oreConfigName+"Size  * _default_'/>\n"
        distText += indentText(indentLine)+"<Setting name='DistributionFrequency' avg=':= "+oreFrequency[currentOreGen]+" * "+oreCloudFrequency[currentOreGen]+" * "+oreConfigName+"Freq *_default_'/>\n"
        distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += indentText(indentLine)+"<Setting name='DistributionFrequency' avg=':= "+preferMultiplier+" * _default_'/>\n"
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)

    # "Hint" Veins
    
    if level == "Prefers":
        preferMultiplier = orePreMultiplier[currentOreGen]
        inheritLine = oreConfigName+"BaseHintVeins"
    else:
        preferMultiplier = "1"
        inheritLine = "PresetHintVeins"
    
    distText += indentText(indentLine)+"\n"
    distText += indentText(indentLine)+"<!-- Begin "+oreName[currentOreGen]+" Strategic Cloud Hint Veins -->\n"
    distText += indentText(indentLine)+"<Veins name='"+oreConfigName+str(level)+"HintVeins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'"+clampRange(oreClampLow[currentOreGen],oreClampHigh[currentOreGen])+" inherits='"+inheritLine+"'>\n"
    indentLine += 1
    distText += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    
    if level == "Base":
        distText += indentText(indentLine)+"Single blocks, generously scattered through all heights (density is about that of vanilla iron ore). \n"
        distText += indentText(indentLine)+"They will replace dirt and sandstone (but not grass or sand), so they can be found nearer  \n"
        distText += indentText(indentLine)+"to the surface than most ores.  Intened to be used as a child distribution for large, rare strategic  \n"
        distText += indentText(indentLine)+"deposits that would otherwise be very difficult to find. \n"

    elif level == "Prefers":
        distText += indentText(indentLine)+"Spawns "+preferMultiplier+" more times in preferred biomes.\n"
    else:
        distText += indentText(indentLine)+" "

    indentLine -= 1
    distText += indentText(indentLine)+"</Description>\n"
    distText += indentText(indentLine)+"<DrawWireframe>:=drawWireframes</DrawWireframe>\n"
    distText += indentText(indentLine)+"<WireframeColor>0x60"+oreWireframe[currentOreGen]+"</WireframeColor>\n"
    distText += indentText(indentLine)+"<Replaces block='minecraft:dirt'/>\n"
    distText += indentText(indentLine)+"<Replaces block='minecraft:sandstone'/>\n"
    distText += replaceList(oreReplaceName)
    
    if level == "Prefers":
        distText += biomeList(orePreferName)
        distText += biomeAvoidList(oreNoPreferName)
    else:
        distText += biomeList(oreBiomeName)    
        distText += biomeAvoidList(oreAvoidName)
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Veins>\n"
    distText += indentText(indentLine)+"<!-- End "+oreName[currentOreGen]+" Strategic Cloud Hint Veins -->\n\n"
    
    indentLine -= 1
    distText += indentText(indentLine)+"</Cloud>\n"
        
    if orePreferBiomes[currentOreGen] != "NONE":
        if level == "Base" :
            distText += indentText(indentLine)+"\n"
            ##  There is no preferred distribution setup for vanilla distributions.
            # distText += indentText(indentLine)+"<!-- Begin Preferred Biome Distribution ("+oreName[currentOreGen]+" Strategic Cloud) Settings -->\n"
            # distText += strategicCloudsDist(currentOreGen, "Prefers")    
            # distText += indentText(indentLine)+"<!-- End Preferred Biome Distribution ("+oreName[currentOreGen]+" Strategic Cloud) Settings -->\n"
    return distText

    

################# DISTRIBUTION SETUP #############################
# Sets up the actual ore distribution configuration for each type
# of distribution.

def distributionGen(currentOreGen, currentOrePreDist):
    global indentLine
    distributionText = ""
    orePreConfigName=modPrefix+oreName[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    currentOreDist=currentOrePreDist.replace(" ", "")
    

    distributionText = indentText(indentLine)+"\n"
    distributionText += indentText(indentLine)+"<!-- Begin "+currentOrePreDist+" distribution of "+oreName[currentOreGen]+" -->\n"
        
    if currentOreDist == 'Substitute':
        print "   ..."+oreName[currentOreGen]+": substituting... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"substituteGen\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText += substituteDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"
    elif currentOreDist == 'Vanilla':
        print "   ..."+oreName[currentOreGen]+": simulating vanilla oregen... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"vanillaStdGen\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText += vanillaDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"
        
    elif currentOreDist == 'LayeredVeins':
        print "   ..."+oreName[currentOreGen]+": forming layered veins... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"layeredVeins\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  layeredVeinsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"
        
    elif currentOreDist == 'VerticalVeins':
        print "   ..."+oreName[currentOreGen]+": stacking vertical veins... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"verticalVeins\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  verticalVeinsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'SmallDeposits':
        print "   ..."+oreName[currentOreGen]+": placing small deposits... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"smallDeposits\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  smallDepositsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'Geodes':
        print "   ..."+oreName[currentOreGen]+": growing geodes... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"geodes\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  geodesDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'HugeVeins':
        print "   ..."+oreName[currentOreGen]+": constructing huge veins... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"hugeVeins\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=   hugeVeinsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'SparseVeins':
        print "   ..."+oreName[currentOreGen]+": sprinkling sparse veins... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"sparseVeins\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=   sparseVeinsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'PipeVeins':
        print "   ..."+oreName[currentOreGen]+": rolling and filling pipe veins... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"pipeVeins\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  pipeVeinsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"

#    elif currentOreDist == 'CompoundVeins':
#        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"compoundVeins\"'>\n"
#        distributionText += indentText(indentLine)+"\n"
#        indentLine += 1
#        distributionText += compoundVeinsDist(currentOreGen, "Base")
#        indentLine -= 1
#        distributionText += indentText(indentLine)+"\n"
#        distributionText += indentText(indentLine)+"</IfCondition>\n"

    elif currentOreDist == 'StrategicCloud':
        print "   ..."+oreName[currentOreGen]+": seeding clouds... "
        distributionText += indentText(indentLine)+"<IfCondition condition=':= "+oreConfigName+"Dist = \"strategicCloud\"'>\n"
        distributionText += indentText(indentLine)+"\n"
        indentLine += 1
        distributionText +=  strategicCloudsDist(currentOreGen, "Base")
        indentLine -= 1
        distributionText += indentText(indentLine)+"\n"
        distributionText += indentText(indentLine)+"</IfCondition>\n"
    
    distributionText += indentText(indentLine)+"<!-- End "+currentOrePreDist+" distribution of "+oreName[currentOreGen]+" -->\n"
    distributionText += indentText(indentLine)+"\n"
        
    return distributionText
    

################## DISTRIBUTION SETUP ###############################
# Creates the entire distribution configuration section

def distConfigGen(currentOreGen, world):
    # Start with an empty script
    configScriptList = ""
    
    # The list of ore distributions will determine available options.
    distributionList = oreDistributions[currentOreGen]
    distributionList = distributionList.split(',')
    
    for distribution in distributionList:
        if oreWorld[currentOreGen] == world:
         configScriptList += distributionGen(currentOreGen, distribution)
             
    return configScriptList
    
##################### ORE WORLD CHECK ###############################
# Only returns anything if the ore is configured for the chosen world.

def worldCheck(currentOreGen, world):
    global indentLine    
    if oreWorld[currentOreGen] == world:
        return 1

####################### ORE REPLACEMENT CHECK #######################
# Only returns anything if the ore is configured to replace the
# chosen material.

def replaceCheck(currentOreGen, replace):
    
    orePreReplaceName=oreReplace[currentOreGen]
    oreReplaceName=orePreReplaceName.replace(" ", "")
    
    global indentLine
    if firstReplace(oreReplaceName) == replace:
        return 1

##################### Per-Material Ore Replacement #################
# Lists the vanilla ores to be replaced with the identified material.

def depositRemovalList(world, replacement):
    global indentLine
    outReplacement = ""
    availableOres = []
    replacementBlocks = []
    availableMetas = []
    availableBlocks = []
        
    for oreSelect in range(0, len(oreConfigName)):        
        if replaceCheck(oreSelect, replacement) == 1:
            availableOres.append(oreConfigName[oreSelect])
            availableBlocks.append(oreBlock[oreSelect])
            availableMetas.append(oreMeta[oreSelect])
            replacementBlocks.append(oreReplace[oreSelect])
            
    for availableSelect in range(0, len(availableOres)):
        outReplacement += indentText(indentLine)+"<Replaces block='"+availableBlocks[availableSelect]+":"+availableMetas[availableSelect]+"' />\n"
    
    return outReplacement


############## Remove Existing Ores ###############################
# Substitutes vanilla oregen with appropriate materials.

def depositRemoval(world):
    global indentLine
    replacementBlocks = []
    outConfig = ""
    
    # First, determine if anything needs to be replaced in this
    # world.
    
    for oreSelect in range(0, len(oreConfigName)):
        if oreSubstitution[oreSelect] == "Yes":
            orePreReplaceName=oreReplace[oreSelect]
            oreReplaceName=orePreReplaceName.replace(" ", "")
            
            if worldCheck(oreSelect, world) == 1:
                firstReplacement = firstReplace(oreReplaceName)
                replacementBlocks.append(firstReplacement)
            
    replaceList = list(set(replacementBlocks))
                
    outConfig += indentText(indentLine)+"\n"
    outConfig += indentText(indentLine)+"<!-- Starting Original "+world+" Ore Removal -->\n"
    
    for blockSelect in range (0, len(replaceList)): # list(set(replacementBlocks)) = remove duplicate blocks
        outConfig += indentText(indentLine)+"<Substitute name='"+modPrefix+world+"OreSubstitute"+str(blockSelect)+"' block='"+replaceList[blockSelect]+"'>\n"
        indentLine += 1
        outConfig += indentText(indentLine)+"<Description>\n"
        indentLine += 1
        outConfig += indentText(indentLine)+"Replace vanilla-generated ore clusters.\n"
        indentLine -= 1
        outConfig += indentText(indentLine)+"</Description>\n"
        outConfig += indentText(indentLine)+"<Comment>\n"
        indentLine += 1
        outConfig += indentText(indentLine)+"The global option deferredPopulationRange must be large enough to catch all ore clusters (>= 32).\n"
        indentLine -= 1
        outConfig += indentText(indentLine)+"</Comment>\n"
    
        outConfig += depositRemovalList(world,replaceList[blockSelect])
    
        indentLine -= 1
        outConfig += indentText(indentLine)+"</Substitute>\n"
    
    
    outConfig += indentText(indentLine)+"<!-- Original "+world+" Ore Removal Complete -->\n"
            
        
    return outConfig
    

############################# MOD DETECTION ##########################
# If a mod is not installed, don't run the configuration.

def modDetectLevel():
    global indentLine
    indentLine=1

    if modDetect != "minecraft":
        outConfig = indentText(indentLine)+"<!-- Mod detection -->\n"
        outConfig += indentText(indentLine)+"<IfModInstalled name=\""+modDetect+"\">\n"
        indentLine += 1
        outConfig += indentText(indentLine)+"\n"
        outConfig += indentText(indentLine)+"<!-- Starting Custom Ore Gen Configuration. -->\n"
        outConfig += indentText(indentLine)+"<ConfigSection>\n"
        outConfig += indentText(indentLine)+"\n"
        indentLine += 1
        outConfig += configSetupSection()+"\n"
        outConfig += overworldSetupSection()+"\n"
        outConfig += netherSetupSection()+"\n"
        outConfig += endSetupSection()+"\n"
        indentLine -= 1
        outConfig += indentText(indentLine)+"\n"
        outConfig += indentText(indentLine)+"</ConfigSection>\n"
        outConfig += indentText(indentLine)+"<!-- Custom Ore Gen Configuration Complete! -->\n"
        indentLine -= 1
        outConfig += indentText(indentLine)+"\n"
        outConfig += indentText(indentLine)+"</IfModInstalled> \n "

        return outConfig
    else:
        outConfig = indentText(indentLine)+"\n"
        outConfig += indentText(indentLine)+"<!-- Starting Custom Ore Gen Configuration. -->\n"
        outConfig += indentText(indentLine)+"<ConfigSection>\n "
        indentLine += 1
        outConfig += configSetupSection()+"\n"
        outConfig += overworldSetupSection()+"\n"
        outConfig += netherSetupSection()+"\n"
        outConfig += endSetupSection()+"\n\n"
        indentLine -= 1
        outConfig += indentText(indentLine)+"</ConfigSection>\n"
        outConfig += indentText(indentLine)+"<!-- Custom Ore Gen Configuration Complete! -->\n"
        
        return outConfig

############################# SETUP SCREEN ##########################
# Final configuration screen setup

def configSetupSection():
    global indentLine
    
    print "Setting up configuration UI... "
    
    setupConfig = indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"<!-- Setup Screen Configuration -->\n"
    setupConfig += indentText(indentLine)+"<ConfigSection>\n"
    indentLine += 1
    setupConfig += indentText(indentLine)+"<OptionDisplayGroup name='group"+modConfigName+"' displayName='"+modName+"' displayState='shown'> \n"
    indentLine += 1
    setupConfig += indentText(indentLine)+"<Description>\n"
    indentLine += 1
    setupConfig += indentText(indentLine)+"Distribution options for "+modName+" Ores.\n"
    indentLine -= 1
    setupConfig += indentText(indentLine)+"</Description>\n"
    indentLine -= 1
    setupConfig += indentText(indentLine)+"</OptionDisplayGroup>\n"
    
    for oreSelect in range (0, len(oreName)):
        
        setupConfig += indentText(indentLine)+"\n"
        setupConfig += indentText(indentLine)+"<!-- "+oreName[oreSelect]+" Configuration UI Starting -->\n"
        setupConfig += indentText(indentLine)+"<ConfigSection>\n"
        indentLine += 1
        setupConfig += controlsGen(oreSelect)
        indentLine -= 1
        setupConfig += indentText(indentLine)+"</ConfigSection> \n"
        setupConfig += indentText(indentLine)+"<!-- "+oreName[oreSelect]+" Configuration UI Complete -->\n"
        setupConfig += indentText(indentLine)+"\n"
    
    indentLine -= 1
    setupConfig += indentText(indentLine)+"</ConfigSection>\n"
    setupConfig += indentText(indentLine)+"<!-- Setup Screen Complete -->\n\n"
    
    return setupConfig

################## OVERWORLD CONFIGURATION ##########################
# Final overworld setup (clean vanilla oregen, replace it with COG
# oregen)

def overworldSetupSection():
    global indentLine
    
    print "...adding Overworld ores... "
    
    setupConfig = indentText(indentLine)+"<!-- Setup Overworld -->\n"
    setupConfig += indentText(indentLine)+"<IfCondition condition=':= ?COGActive'>\n"
    indentLine += 1
    setupConfig += depositRemoval("Overworld")
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"<!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        if oreWorld[oreSelect] == "Overworld":
            setupConfig += indentText(indentLine)+"\n"
            setupConfig += indentText(indentLine)+"<!-- Begin "+oreName[oreSelect]+" Generation --> \n"
        
        setupConfig+=distConfigGen(oreSelect, "Overworld")
        
        if oreWorld[oreSelect] == "Overworld":
            setupConfig += indentText(indentLine)+"<!-- End "+oreName[oreSelect]+" Generation --> \n\n"
        
    
    setupConfig += indentText(indentLine)+"<!-- Done adding ores -->\n"
    indentLine -= 1
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"</IfCondition>\n"
    setupConfig += indentText(indentLine)+"<!-- Overworld Setup Complete -->\n\n"
    
    return setupConfig
    
##################### NETHER CONFIGURATION ##########################
# Final nether setup (clean vanilla oregen, replace it with COG
# oregen)

def netherSetupSection():
    global indentLine
    verified = 0
    
    print "...adding Nether ores... "
    
    for oreSelect in range(0, len(oreConfigName)):    
            
        if oreWorld[oreSelect] == "Nether":
            verified = 1
            
    if verified == 0:
        return " "
    
    setupConfig = indentText(indentLine)+"<!-- Setup Nether -->\n"
    setupConfig += indentText(indentLine)+"<IfCondition condition=':= dimension.generator = \"HellRandomLevelSource\"'>\n"
    indentLine += 1
    setupConfig += depositRemoval("Nether")
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"<!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        if oreWorld[oreSelect] == "Nether":
            setupConfig += indentText(indentLine)+"\n"
            setupConfig += indentText(indentLine)+"<!-- Begin "+oreName[oreSelect]+" Generation --> \n"
            
        setupConfig+=distConfigGen(oreSelect, "Nether")
        
        if oreWorld[oreSelect] == "Nether":
            setupConfig += indentText(indentLine)+"<!-- End "+oreName[oreSelect]+" Generation --> \n\n"
    
    setupConfig += indentText(indentLine)+"<!-- Done adding ores -->\n"
    indentLine -= 1
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"</IfCondition>\n"
    setupConfig += indentText(indentLine)+"<!-- Nether Setup Complete -->\n\n"
    
    return setupConfig

####################### END CONFIGURATION ##########################
# Final end setup (clean vanilla oregen, replace it with COG oregen)

def endSetupSection():
    global indentLine
    verified = 0
    
    print "...adding End ores... "
    
    for oreSelect in range(0, len(oreConfigName)):        
        if oreWorld[oreSelect] == "End":
            verified = 1
            
    if verified == 0:
        return " "
    
    setupConfig = indentText(indentLine)+"<!-- Setup End -->\n"
    setupConfig += indentText(indentLine)+"<IfCondition condition=':= dimension.generator = \"EndRandomLevelSource\"'>\n"
    indentLine += 1
    setupConfig += depositRemoval("End")
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"<!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        if oreWorld[oreSelect] == "End":
            setupConfig += indentText(indentLine)+"\n"
            setupConfig += indentText(indentLine)+"<!-- Begin "+oreName[oreSelect]+" Generation --> \n"
            
        setupConfig+=distConfigGen(oreSelect, "End")
        
        if oreWorld[oreSelect] == "End":
            setupConfig += indentText(indentLine)+"<!-- End "+oreName[oreSelect]+" Generation --> \n\n"
    
    setupConfig += indentText(indentLine)+"<!-- Done adding ores -->\n"
    indentLine -= 1
    setupConfig += indentText(indentLine)+"\n"
    setupConfig += indentText(indentLine)+"</IfCondition>\n"
    setupConfig += indentText(indentLine)+"<!-- End Setup Complete -->\n\n"
    
    return setupConfig
    
############# ASSEMBLE CONFIGURATION ################################
# This is where the configuration gets prepared for writing.

def assembleConfig():
    
    configOutput = headerGen()
    configOutput += modDetectLevel()
    
    configOutput += "\n\n\n<!-- This file was made using the Sprocket Configuration Generator. -->"
    
    return configOutput

################ ERROR CHECK ########################################
# If an error was found, we do NOT want to overwrite the config file.

if errorCondition:
    sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": nothing written due to errors")

################# WRITE CONFIG ######################################
# This is actually where the rubber meets the road; the configuration
# is written to an XML file.

xmlConfigFile = open('./'+modConfigName+'.xml', 'w+')
xmlConfigFile.write(assembleConfig())

print "Configuration complete for "+modName+"!"
