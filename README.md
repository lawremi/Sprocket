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
	and skip the configuration.  If the mod's name is "minecraft", then
	detection will not be added to the configuration (in other words,
	this configuration will ALWAYS work)

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
	
	There is no default value; if an ore does not have a block assigned,
	Sprocket will report it, and no configuration file will be written.

    Meta:

	If a block has a meta number, this is the number it uses.
	
	The default is 0, although it's recommended to include the meta
	number to avoid confusion.

    Replace:

	The block name of the block this replaces.  Overworld ores
	usually replace "minecraft:stone", Nether ores usually
	replace "minecraft:netherrack", and End ores usually replace
	"minecraft:end_stone".  Another example would be Tinker's
	Construct's gravel ores, which would replace 
	"minecraft:gravel".
	
	The default is "minecraft:stone".

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
	* CompoundVeins: An ore vein inside another ore vein.  The greater
                         vein will be determined by the ore block, while the
                         smaller vein will use the pipe material.
	* Substitute: This is a simple one-for-one replacement; the block
                      identified by "Replace:" will be replaced by the block
                      identified by "Block:".  The options covering side,
                      frequency, and location are permitted, but are
                      useless.
	
	There is also "none" as a distribution to turn the ores off, but it
	is automatically added at generation.
	
	The default is "Vanilla".  If an invalid distribution is selected,
	Sprocket will report it, and no configuration file will be written.

    Wireframe:

	COG has a feature that will show wireframe outlines of the area
	chosen for motherlodes and veins as they're configured to allow you
	to see if they're working.  If the wireframe goes into a location
	where the ore should be, and you don't see ore intersecting with it,
	something's wrong.
	
	This option specifically is meant to select the color the wireframe
	will be.  The code will be written as "0x60", followed by a 6-digit 
	hexadecimal number (also known as a "hex triplet," or "web color").
	
	The default is randomly generated every time Sprocket is run.

    Pipe:
        
	This identifies the block that is contained in Pipe Veins.  Usually
	set to minecraft:lava (configuration for Diamonds) or 
	minecraft:monster_egg (configuration for Emeralds).  Also used to
	define the "shell" material for geodes.
	
	The default is "minecraft:lava".

    Height:

	This sets the height around which the ore will generate; this is the
	center of the range.  "64" is considered ground level; the actual
	number scales depending on the biome and/or presence of Alternate
	Terrain Generation.
	
	The default is 64.

    Range:

	This sets the range around the above center height that ores will
	generate.  Like the height, this number is scaled based on the biome
	or presence of ATG.
	
	The default is 64.

    Size:

	This is the vein size multiplier.  1 is the default; nothing is
	changed.  Less than 1 (make sure the number is in the form of 0.x)
	make the ore deposits smaller.  More than 1 makes them larger.
	
	The default is 1.

    Frequency:

	Frequency multiplier; works the same way as the size multiplier.
	
	The default is 1.
	
	Biomes:
	
	Biome requirements as a comma-separated list of biome dictionary
	entries.  This means that only those biomes listed will actually
	spawn the ore.  If the biome is not on this list, the ore will not
	spawn there.
	
	The default is "ALL".
	
	Prefers:
	
	Biome preferences as a comma-separated list of biome dictionary
	entries.  This means that the biomes listed in this option will
	have double the ores spawning.  This doubling also includes the
	above multipliers, so be careful to balance the two.
	
	The default value is "NONE".
	
	Scale:
	
	The ScaleTo attribute is there to scale the ore height depending on
	where the "surface" is.  Options includ Base (level 64), SeaLevel,
	CloudLevel, World (averaged over the whole world), Biome (averaged
	over the whole biome), and Position (Either the current ATG level or
	else defaults to Biome).  The default is "Biome," although it will
	change to "Position" when a bug that crashes the game with COG, ATG,
	and Mystcraft is resolved.
	
	Active:

	By default, ores will be distributed based on the first distribution
	choice in "Distributions".  Set this option to "no" for an ore, and
	its default distribution will be set to "none".

In any event, enjoy, and I hope you find this utility useful!
