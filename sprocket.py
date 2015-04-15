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


import ConfigParser
import json
import sys
import textwrap
import random
import string

# Initialize variables

configFile = sys.argv[1]
modName = ""        # This is the mod name component for variable names
modNameVis = ""     # This is the mod name displayed in strings.
modPrefix = ""      # This comes before the ore name in variable names
                    #     (tic, mtlg)

# Initialize Ore Options
oreName = []          # The name of this specific Ore
oreWorld = []         # The world the ore spawns in
                      #    (Overworld, Nether, End)
oreBlock = []         # The ore's actual block id
oreMeta = []          # The meta number, if not 0
oreReplace = []       # The block the ore replaces
orePipe = []          # Content of pipe distribution (usually lava)
oreDistributions = [] # Comma-separated list of distribution options.
oreWireframe = []     # Wireframe color (0x60 followed by web code)
oreList = ""

# Open a configuration file for reading.
Config = ConfigParser.SafeConfigParser()
Config.read(configFile)

# Get the mod's name in three forms, one for mod-specific variables,
# one for display in strings, and a prefix to use for ore variables.
modName = Config.get('Mod', 'Code')     # "myMod2"
modNameVis = Config.get('Mod', 'Name')  # "My Mod 2"
modPrefix = Config.get('Mod', 'Prefix') # "mmd2"
modDetect = Config.get('Mod', 'Detect') # "MyMod"

oreName = Config.sections()
oreName.pop(0) # The first section is not an ore, it's the mod's
               # settings.  It needs to go.

oreCount = 0

# Creating a set of lists for the options; memory access is always
# faster than disk access.

for currentOre in oreName:
    
    oreWorld.append(Config.get(currentOre, 'World'))
    oreBlock.append(Config.get(currentOre, 'Block'))
    oreMeta.append(Config.get(currentOre, 'Meta'))
    oreReplace.append(Config.get(currentOre, 'Replace'))
    orePipe.append(Config.get(currentOre, 'Pipe'))
    oreDistributions.append(Config.get(currentOre, 'Distributions'))
    oreWireframe.append(Config.get(currentOre, 'Wireframe'))
    ++oreCount

# All ore data has been imported from the configuration file.  Now we 
# need to generate the actual XML configuration.

# First, we'll set up the variables that will hold the generated text
# until everything is ready to be written to the new file.
headerTemplate = ""
controlsTemplate = []
oreConfigTemplate = []

###################### RANDOM SEED NUMBER ############################
# Generate a random hexadecimal number for a seed value

def generate_random_key(length):
    return ''.join([random.choice('0123456789ABCDEF') for x in range(4)])

########################## MAKE CONFIG HEADING #######################

def headerGen():
    oreList = ", ".join(oreName)
    fmtOreList = "\r\n".join(textwrap.wrap(oreList, 70))
    return "\n\
<!--  \n\
\n\
Custom Ore Generation:   "+modNameVis+" Module\n\n\
Generates: "+fmtOreList+"\n\
\n\
-->"

################## CHOOSE DISTRIBUTION OPTIONS #####################

def distributionControlGen(currentOreDistBase):
    currentOreDist = currentOreDistBase.replace(" ", "")
    if currentOreDist == 'Vanilla': # uses StandardGen
        return "\n\
               <Choice value='vanillaStdGen' displayValue='Vanilla'>\n\
                   <Description>\n\
                       Vanilla-style clusters. \n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'LayeredVeins': # uses Veins
        return "\n\
               <Choice value='layeredVeins' displayValue='Layered Veins'>\n\
                   <Description>\n\
                       Layered Veins. \n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'VerticalVeins': # uses Veins
        return "\n\
               <Choice value='verticalVeins' displayValue='Vertical Veins'>\n\
                   <Description>\n\
                       Vertical Veins. \n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'SmallDeposits': # uses Veins
        return "\n\
               <Choice value='smallDeposits' displayValue='Small Deposits'>\n\
                   <Description>\n\
                       Small Deposits. \n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'Geodes': # uses Veins
        return "\n\
               <Choice value='geodes' displayValue='Geodes'>\n\
                   <Description>\n\
                       Geodes. \n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'HugeVeins': # uses Veins
        return "\n\
               <Choice value='hugeVeins' displayValue='Huge Veins'>\n\
                   <Description>\n\
                       Huge Veins\n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'SparseVeins': # uses Veins
        return "\n\
               <Choice value='sparseVeins' displayValue='Sparse Veins'>\n\
                   <Description>\n\
                       Sparse Veins\n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'PipeVeins': # uses Veins
        return "\n\
               <Choice value='pipeVeins' displayValue='Pipe Veins'>\n\
                   <Description>\n\
                       Pipe Veins\n\
                   </Description>\n\
               </Choice>\n"
    elif currentOreDist == 'StrategicCloud': # uses Cloud
        return "\n\
               <Choice value='strategicCloud' displayValue='Clouds'>\n\
                   <Description>\n\
                       Strategic Clouds \n\
                   </Description>\n\
               </Choice>\n"
    else:
        return "\n\
<!-- "+currentOreDist +": Invalid Distribution Type  -->\n"

################### CONFIGURATION SETUP ##############################
# Assembles the configuration section for in-game setup.

def controlsGen(currentOreGen):
    # Start with an empty script
    configScriptList = ""
    
    # The list of ore distributions will determine available options.
    distributionList = oreDistributions[currentOreGen]
    distributionList = distributionList.split(',')
    for distribution in distributionList:
         configScriptList += distributionControlGen(distribution)
    
    oreConfigName=modPrefix+oreName[currentOreGen]
    oreConfigName=oreConfigName.replace(" ", "")
    
    configScriptOpen = "\n\
            <!-- "+oreName[currentOreGen]+" Configuration UI -->\n\
\n\
            <OptionChoice name='"+oreConfigName+"Dist' displayState='shown' displayGroup='group"+modName+"'> \n\
                <Description> Controls how "+oreName[currentOreGen]+" is generated </Description> \n\
                <DisplayName>"+modNameVis+" "+oreName[currentOreGen]+" Type</DisplayName>\n"
    
    configScriptClose = "\
                <Choice value='none' displayValue='None' description='"+oreName[currentOreGen]+" is not generated in the world.'/>\n\
            </OptionChoice>\n\
    \n\
            <OptionNumeric name='"+oreConfigName+"Freq' default='1'  min='0' max='5' displayState='hidden' displayGroup='group"+modName+"'>\n\
                <Description> Frequency multiplier for "+modNameVis+" "+oreName[currentOreGen]+" distributions </Description>\n\
                <DisplayName>"+modNameVis+" "+oreName[currentOreGen]+" Freq.</DisplayName>\n\
            </OptionNumeric>\n\
\n\
            <OptionNumeric name='"+oreConfigName+"Size' default='1'  min='0' max='5' displayState='hidden' displayGroup='group"+modName+"'>\n\
                <Description> Size multiplier for "+modNameVis+" "+oreName[currentOreGen]+" distributions </Description>\n\
                <DisplayName>"+modNameVis+" "+oreName[currentOreGen]+" Size</DisplayName>\n\
            </OptionNumeric>\n"
          
    return configScriptOpen+configScriptList+configScriptClose

############## DETECT META NUMBER #################################
# If the meta number is anything other than zero, return the number
# Preceded by a colon.

def metaGen(currentMeta):
    if oreMeta[currentMeta] == '0':
        return ""
    else:
        return ":"+oreMeta[currentMeta]

################# DISTRIBUTION SETUP #############################
# Sets up the actual ore distribution configuration for each type
# of distribution.

def distributionGen(currentOreGen, currentOrePreDist):

    orePreConfigName=modPrefix+oreName[currentOreGen]
    oreConfigName=orePreConfigName.replace(" ", "")
    currentOreDist=currentOrePreDist.replace(" ", "")

    if currentOreDist == 'Vanilla':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"vanillaStdGen\"'>\n\
                    <StandardGen name='"+oreConfigName+"Standard' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetStandardGen'>\n\
                        <Description> This mimics vanilla ore generation. </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='Size' avg=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='Frequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </StandardGen>\n\
                </IfCondition>\n"
    elif currentOreDist == 'LayeredVeins':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"layeredVeins\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetLayeredVeins'>\n\
                        <Description> \n\
                            Small, fairly rare motherlodes with 2-4 horizontal veins each.\n\
                        </Description> \n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor> \n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'VerticalVeins':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"verticalVeins\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetVerticalVeins'>\n\
                        <Description>\n\
                            Single vertical veins that occur with no motherlodes.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= 1.3 * "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'SmallDeposits':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"smallDeposits\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetSmallDeposits'>\n\
                        <Description>\n\
                            Small motherlodes without any branches.\n\
                            Similar to the deposits produced by StandardGen distributions.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'Geodes':
        geodeSeed = "'0x"+generate_random_key(3)+"'"
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"geodes\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+orePipe[currentOreGen]+"' inherits='PresetSmallDeposits' seed="+geodeSeed+">\n\
                        <Description>\n\
                            The geode's outer shell, composed of the Pipe material.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= 3 * "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='minecraft:air'/>\n\
                        <Replaces block='minecraft:water'/>\n\
                        <Replaces block='minecraft:lava'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetSmallDeposits' seed="+geodeSeed+">\n\
                        <Description>\n\
                            The geode's inner material, usually some form of crystal.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= 1.5 * "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+orePipe[currentOreGen]+"'/>\n\
                    </Veins>\n\
                    <Veins name='"+oreConfigName+"Veins' block='minecraft:air' inherits='PresetSmallDeposits' seed="+geodeSeed+">\n\
                        <Description>\n\
                            The air pocket within the center of a geode.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'HugeVeins':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"hugeVeins\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetLayeredVeins'>\n\
                        <Description> \n\
                            Very large, extremely rare motherlodes.  Each motherlode has many long slender branches - so thin that\n\
                            parts of the branch won't contain any ore at all.  This, combined with the incredible length of the\n\
                            branches, makes them more challenging to follow underground.  Once found, however, a motherlode contains\n\
                            enough ore to keep a player supplied for a very long time.\n\
                            The rarity of these veins might be too frustrating in a single-player setting.  In SMP, though, teamwork \n\
                            could make finding them much easier and the motherlodes are big enough to supply several people without\n\
                            shortage.  This might be a good way to add challenge to multiplayer worlds.\n\
                            Credit: based on feedback by dyrewulf from the MC forums.\n\
                        </Description> \n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor> \n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'SparseVeins':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"sparseVeins\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetSparseVeins'>    \n\
                        <Description>\n\
                            Large veins filled very lightly with ore.  Because they contain less ore per volume, \n\
                            these veins are relatively wide and long.  Mining the ore from them is time consuming \n\
                            compared to solid ore veins.  They are also more difficult to follow, since it is \n\
                            harder to get an idea of their direction while mining.\n\
                        </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'PipeVeins':
        pipeSeed = "'0x"+generate_random_key(3)+"'"
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"pipeVeins\"'>\n\
                    <Veins name='"+oreConfigName+"Veins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetPipeVeins' seed="+pipeSeed+">\n\
                        <Description> Short sparsely filled veins sloping up from near the bottom of the map. </Description>\n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor>\n\
                        <Setting name='MotherlodeFrequency' avg=':= "+oreConfigName+"Freq * _default_'/>\n\
                        <Setting name='MotherlodeSize' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                    </Veins>\n\
                    <Veins name= "+oreConfigName+"Pipe block='"+orePipe[currentOreGen]+"' inherits='PresetPipeVeins' seed="+pipeSeed+">\n\
                        <Description> Fills center of each tube with Pipe material. </Description>\n\
                        <Setting name='MotherlodeSize' avg=':= 0.5 * _default_'/>\n\
                        <Setting name='SegmentRadius' avg=':= 0.5 * _default_'/>\n\
                        <Setting name='OreDensity' avg='1' range='0'/>\n\
                        <ReplacesOre block='stone'/>\n\
                        <Replaces block='minecraft:dirt'/>\n\
                        <Replaces block='minecraft:gravel'/>\n\
                        <Replaces block='minecraft:netherrack'/>\n\
                        <Replaces block='minecraft:end_stone'/>\n\
                        <Replaces block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'/>\n\
                    </Veins>\n\
                </IfCondition>\n"
    elif currentOreDist == 'StrategicCloud':
        return "\n\
                <IfCondition condition=':= "+oreConfigName+"Dist = \"strategicCloud\"'>\n\
                    <Cloud name='"+oreConfigName+"Cloud' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetStrategicCloud'>\n\
                        <Description>  \n\
                            Large irregular clouds filled lightly with ore.  These are huge, spanning several \n\
                            adjacent chunks, and consequently rather rare.  They contain a sizeable amount of \n\
                            ore, but it takes some time and effort to mine due to low density.\n\
                            The intent for strategic clouds is that the player will need to actively search for\n\
                            one and then set up a semi-permanent mining base and spend some time actually mining\n\
                            the ore.\n\
                        </Description> \n\
                        <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                        <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor> \n\
                        <Setting name='DistributionFrequency' avg=':= "+oreConfigName+"Freq *_default_'/>\n\
                        <Setting name='CloudRadius' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Setting name='CloudThickness' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        <Replaces block='"+oreReplace[currentOreGen]+"'/>\n\
                        <Veins name='"+oreConfigName+"HintVeins' block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"' inherits='PresetHintVeins'>\n\
                            <DrawWireframe>:=drawWireframes</DrawWireframe>\n\
                            <WireframeColor>"+oreWireframe[currentOreGen]+"</WireframeColor> \n\
                            <Setting name='MotherlodeFrequency' avg=':= 1.2 * _default_' range=':= _default_'/> \n\
                            <Setting name='MotherlodeRangeLimit' avg=':= "+oreConfigName+"Size * _default_' range=':= "+oreConfigName+"Size * _default_'/>\n\
                        </Veins>\n\
                    </Cloud>\n\
                </IfCondition>\n"
    else:
        return "<!-- "+currentOreDist +": Invalid Distribution Type  -->\n "
    

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
# Prevents nether, overworld, and end ores from showing up in the wrong
# worlds.  Also removes invalid <Substitute> entries from a world's
# generation.

def worldCheck(currentOreGen, world):
    # Start with an empty script
    configScriptList = ""
    
    # The list of ore distributions will determine available options.
    distributionList = oreDistributions[currentOreGen]
    distributionList = distributionList.split(',')
    
    for distribution in distributionList:
        if oreWorld[currentOreGen] == world:
         configScriptList += "\
            <Replaces block='"+oreBlock[currentOreGen]+metaGen(currentOreGen)+"'/>\n"
             
    return configScriptList


############## Remove Existing Ores ###############################
# Substitutes vanilla oregen with appropriate materials.

def depositRemoval(world):
    outConfig = ""
    availableOres = []
    replacementBlocks = []
    validOre = 0
        
    for oreSelect in range(0, len(oreName)):

        if worldCheck(oreSelect, world):
            availableOres.append(oreName[oreSelect])
            validOre += 1
    
    for oreSelect in range(0, len(availableOres)):
        replacementBlocks.append(oreReplace[oreSelect])

    outConfig += "\n\
                <!-- **********   Vanilla Deposit Removal   ************* -->\n"
    
    for blockSelect in range (0, len(list(set(replacementBlocks)))):
    
        outConfig += "\n\
                    <Substitute name='"+modName+"StandardOreSubstitute"+str(blockSelect)+"' block='"+list(set(replacementBlocks))[blockSelect]+"'>\n\
                        <Description> \n\
                            Replace vanilla-generated ore clusters.   \n\
                        </Description>\n\
                        <Comment>  \n\
                            The global option deferredPopulationRange must be large enough to catch all ore clusters (>= 32).\n\
                        </Comment>\n "
                
        for oreSelect in range(0, len(oreName)):
            if oreReplace[oreSelect] == list(set(replacementBlocks))[blockSelect]:
                outConfig += "\
                        <Replaces block='"+oreBlock[oreSelect]+metaGen(oreSelect)+"' />\n"

        outConfig += "\n\
                </Substitute>\n"
            
        
    return outConfig
    
    

############################# MOD DETECTION ##########################
# If a mod is not installed, don't run the configuration.

def modDetectLevel():
    
    outConfig="\n\
<IfModInstalled name=\""+modDetect+"\"> \n\n\
    <ConfigSection>\n "
    
    outConfig += configSetupSection()+"\n"
    outConfig += overworldSetupSection()+"\n"
    outConfig += netherSetupSection()+"\n"
    outConfig += endSetupSection()+"\n"
    
    outConfig +="\n\n\
    </ConfigSection>\n\
</IfModInstalled> \n "

    return outConfig

############################# SETUP SCREEN ##########################
# Final configuration screen setup

def configSetupSection():
    
    setupConfig="\n\
        <!-- Setup Screen Configuration -->\n\
\n\
            <ConfigSection> \n\
                <OptionDisplayGroup name='group"+modName+"' displayName='"+modNameVis+" Ores' displayState='shown'> \n\
                    <Description> \n\
                        Distribution options for "+modNameVis+" Ores.\n\
                    </Description>\n\
                </OptionDisplayGroup>\n\
    \n "
    
    for oreSelect in range (0, len(oreName)):
        setupConfig += "\
                <ConfigSection>\n"
        setupConfig += controlsGen(oreSelect)
        setupConfig += "\
                </ConfigSection> \n"
    
    setupConfig += "\
            </ConfigSection> \n"
    
    return setupConfig

################## OVERWORLD CONFIGURATION ##########################
# Final overworld setup (clean vanilla oregen, replace it with COG
# oregen)

def overworldSetupSection():
    
    setupConfig="\n\
            <!-- Setup Overworld -->\n\
\n\
            <IfCondition condition=':= ?COGActive'>\n\
\n"
    
    setupConfig+=depositRemoval("Overworld")
    
    setupConfig+="\n\
        <!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        setupConfig+=distConfigGen(oreSelect, "Overworld")
    
    setupConfig+="\n\
            </IfCondition>\n"
    
    return setupConfig
    
##################### NETHER CONFIGURATION ##########################
# Final nether setup (clean vanilla oregen, replace it with COG
# oregen)

def netherSetupSection():
    
    setupConfig="\n\
            <!-- Setup Nether -->\n\
\n\
            <IfCondition condition=':= dimension.generator = \"HellRandomLevelSource\"'>\n\
\n"
    
    setupConfig+=depositRemoval("Nether")
    
    setupConfig+="\n\
        <!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        setupConfig+=distConfigGen(oreSelect, "Nether")
    
    setupConfig+="\n\
            </IfCondition>\n"
    
    return setupConfig

####################### END CONFIGURATION ##########################
# Final end setup (clean vanilla oregen, replace it with COG oregen)

def endSetupSection():
    
    setupConfig="\n\
            <!-- Setup End -->\n\
\n\
            <IfCondition condition=':= dimension.generator = \"EndRandomLevelSource\"'>\n\
\n"
    
    setupConfig+=depositRemoval("End")
    
    setupConfig+="\n\
        <!-- Adding ores --> \n"
               
    for oreSelect in range(0,len(oreName)):
        setupConfig+=distConfigGen(oreSelect, "End")
    
    setupConfig+="\n\
            </IfCondition>\n"
    
    return setupConfig
    
############# ASSEMBLE CONFIGURATION ################################
# This is where the configuration setup begins and ends.

def assembleConfig():
    configOutput = modDetectLevel()
    
    return configOutput
    
################# WRITE CONFIG ######################################
# This is actually where the rubber meets the road; the configuration
# is assembled and written to an XML file.

xmlConfigFile = open('./'+modName+'.xml', 'w+')
xmlConfigFile.write(assembleConfig())
