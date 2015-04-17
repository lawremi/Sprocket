# Sprocket
Configuration Utility for Custom Ore Gen: First Revival mod

	The Custom Ore Generation mod for Minecraft is one of the best
	discoveries I've made to this point.
	
	However, it is apparent that the XML files it requires are a
	particularly tricky thing to deal with; to properly configure COG,
	you need to spend a lot of time writing a large XML file with a lot
	of sections and options, just to get it to work with one or two
	ores.  On the other hand, if you have a mod with a lot of ores, such
	as Metallurgy or Nether Ores, this can turn into a major hassle in a
	hurry... especially when you spend the better part of a week simply
	hunting down a missing angle bracket or misspelled element!
	
	Enter Sprocket.  With Sprocket, you can get a baseline XML file
	built in a short time, just by making an INI file with the key
	information for each ore and the mod.  Then, by running Sprocket on
	the config file, a fully-valid, basic XML file is generated,
	essentially giving you a shortcut to the point where you simply need
	to tweak the file for the needed settings.

The Configuration:
    
	The config file uses a basic INI syntax:
	
        	[Mod]
	        Name: Chisel 2
	        Prefix: chsl
	        Detect: chisel
	
	        [DEFAULT]
	        World: Overworld
	        Replace: minecraft:stone
	        Meta: 0
	        Wireframe: 0x6087930d
	        Pipe: minecraft:lava
	        Distributions: LayeredVeins, StrategicCloud
	        
	        [Andesite]
	        Block: chisel:andesite
	        
	        [Diorite]
	        Block: chisel:diorite
	        
	        .
	        .
	        .
	        
	        
	...and so on.

	The [Mod] section is required in the file; this is what tells 
	Sprocket the mod name, the code name, the prefix code, and the modid
	(detection)	name.
	
	The mod name, identified by "Name", is the name that will appear in
	the setup screen.  This is the actual name of the mod, but be
	careful not to use quotes or apostrophes; this will break the XML
	file.  This isn't the fault of Sprocket, but because XML treats
	those characters in a special way.
	
	The "Prefix" is a shortened version of the name (I prefer keeping it
	to 4 characters) that will be used in the front of ore-configuration
	variables (ticoCopperSize).  The prefix is there to ensure that
	you won't run into a problem with two mods using the same material
	(for example, copper or tin); if they were both set to the same
	name, COG will crash.
	
	The "Detect" name is for the COG mod-detection feature.  COG will
	look for this name in the modid list while running Minecraft.  If
	this name is not found, COG will assume the mod is not installed,
	and skip the configuration.

[DEFAULT] Section
	
	The [DEFAULT] Section is there to reduce the need to repeat the same
	information over, and over.  Any or all of the options can be used
	here, except for section names.  However, odds are good that at
	least one option will need to be set in the individual sections.

Ore-specific Sections

	The remaining sections are each named after the ore they will
	affect (such as [Copper] or [Tin]).  Underneath each of these
	sections is one or more settings that differentiate the ore from
	another (such as its block name or meta number).
	
Options:
	    
    World:
	
	The world that the ore spawns in.  Options are:
	
	* Overworld
	* Nether
	* End
    
    Block:

	The block name, such as "minecraft:iron_ore"

    Meta:

	If a block has a meta number, this is the number it uses.

    Replace:

	The block name of the block this replaces.  Overworld ores
	usually replace "minecraft:stone", Nether ores usually
	replace "minecraft:netherrack", and End ores usually replace
	"minecraft:end_stone".  Another example would be Tinker's
	Construct's gravel ores, which would replace 
	"minecraft:gravel".

    Distributions:

	Custom Ore Generation has several default patterns of
	ore placement.  This option allows you to choose which
	ones the ore in question uses.  The available options
	are:
	
	* Vanilla: Generates in chunks, just like Vanilla.
	* LayeredVeins: Motherlodes with veins branching out.
	* VerticalVeins: Vertical veins without motherlodes.
	* SmallDeposits: Motherlodes without veins.
	* HugeVeins: Very rare, but very huge Layered Veins.
	* Sparse Veins: Large veins, but the ore is spread out within them.
	* PipeVeins: Ore arranged in a pipe, which is filled with another
	             block. The filling blocks are selected by Pipe: below.
	* StrategicCloud: The ore is scattered heavily over multiple chunks.
	                  Once you find a cloud, you'll have a good source
	                  of ore.
	* Geodes: An ore cluster, surrounded by a pipe material, and 
	          surrounding a small air bubble.
	
	There is also "none" as a distribution to turn the ores off, but it
	is automatically added at generation.

    Wireframe:

	COG has a feature that will show wireframe outlines of the area
	chosen for motherlodes and veins as they're configured to allow you
	to see if they're working.  If the wireframe goes into a location
	where the ore should be, and you don't see ore intersecting with it,
	something's wrong.
	
	This option specifically is meant to select the color the wireframe
	will be.  The code will be written as "0x60", followed by a 6-digit 
	hexadecimal number (also known as a "hex triplet," or "web color").

    Pipe:
        
	This identifies the block that is contained in Pipe Veins.  Usually
	set to minecraft:lava (configuration for Diamonds) or 
	minecraft:monster_egg (configuration for Emeralds).  Also used to
	define the "shell" material for geodes.

    Height:

	This sets the height around which the ore will generate.  The number
	for surface level is "64".  The configuration will add "biome"
	scaling	to the number, to account for the biome's average surface
	height.

    Range:

	The ores will be randomly spawned within the range specified here,
	using the above height value as a center.  So, a height of 32 and a
	range of 8 means that ore veins/clouds/clusters will spawn between
	levels 24 and 40.  Similar to the above height value, these are
	scaled based on the average surface height of the current biome.

    Size:

	This is the vein size multiplier.  1 does not multiply the default.
	Less than 1	(make sure the number is in the form of 0.x) makes the
	ore deposit smaller.  More than 1 makes the ore deposit larger.

    Frequency:

	Frequency multiplier; works the same way as the size multiplier.

In any event, enjoy, and I hope you find this utility useful!
