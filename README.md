# Sprocket
Configuration Utility for Custom Ore Gen: First Revival mod
(http://tinyurl.com/qdpekog)

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

## Using the Program:

Sprocket is a command-line program.  It requires that you have Python 2.7
installed on your system.  You can pick up Python 2.7 from www.python.org

To run the program, you have one of two options:
        
        `sprocket.py name-of-file.ini`

or 

        `python sprocket.py name-of-file.ini`

If Sprocket works correctly, you should either see it start a long chain
of progress messages, starting with the ore's name, or else an error
message stating (in English) what you need to do to correct the INI file.

It will always create the XML file in the folder you are currently in, and
it will name the configuration based on the mod name in the configuration file.

## The Configuration:
    
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
    (detection)    name.
    
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

### [DEFAULT] Section
    
    The [DEFAULT] Section is there to reduce the need to repeat the same
    information over, and over.  Any or all of the options can be used
    here, except for section names.  However, odds are good that at
    least one option will need to be set in the individual sections.

### Ore-specific Sections

    The remaining sections are each named after the ore they will
    affect (such as [Copper] or [Tin]).  Underneath each of these
    sections is one or more settings that differentiate the ore from
    another (such as its block name or meta number).
    
### Options:
        
    World:
    
        The world that the ore spawns in.  Options are:
    
        * Overworld
        * Nether
        * End
    
    Block:

        The block name, such as "minecraft:iron_ore"
        
        There is no default value; if an ore does not have a block assigned,
        Sprocket will report it, and no configuration file will be written.
    
    Extra:
        
        Some ore distributions handle multiple types of ore at the same time.
        This option is a comma-separated list of blockid:meta values to use
        as the "extra" ore blocks to use in a distribution.  Currently only
        used in the "geode" distribution.
        
        There is no default value; if left empty, the extra field is just
        not used.

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
        "minecraft:gravel".  Multiple blocks can be selected 
        (comma-separated list), but only the first one will count
        to replace vanilla-distributed ore.
    
        The default is "minecraft:stone".

    Distributions:

        Custom Ore Generation has several default patterns of
        ore placement.  This option allows you to choose which
        ones the ore in question uses.  The available options
        are:
        
        * Vanilla: Generates in chunks, just like Vanilla.  In the
                   configuration options, this is also called "Standard."
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
                  surrounding a small air bubble.  Can be either simple
                      (containing only one ore type) or compound (mixing
                      different ore blocks together)
        * Substitute: This is a simple one-for-one replacement; the block
                      identified by "Replace:" will be replaced by the
                      block identified by "Block:".  The options
                      covering side, frequency, and location are
                      permitted, but are useless.
        
        There is also "none" as a distribution to turn the ores off, but it
        is automatically added at generation.
    
        The default is "Vanilla".  If an invalid distribution is selected,
        Sprocket will report it, and no configuration file will be written.
    
    Distribution Type:
    
        Determines the randomness of the distribution placement.
        * normal: prefers placing ores closer to the center of the range.
        * uniform: prefers perfectly random placement.
        * inverse: prefers placing ores further from the center of the range.
        * inverseAbs: prefers placing ores in one direction from center only.
    
        The default is 'normal'.

    Substitute: 

        Custom Ore Generation's first action in every chunk loaded is to
        wipe it clean of all previously-generated ores.  The process of
        looking for and removing ores can take a small amount of time,
        which can add up with each additional configuration.

        Many mods include configuration options that allow you to turn off
        their in-built oregens for just a tool such as this one.

        The Substitution option allows the modpack designer to disable
        COG's "wipe it clean first" feature for the mods they disabled
        oregen in.  This will improve chunk-loading performance by doing
        away with the cleanup-before-orespawn step.

        By default, this value is set to "Yes" (do the substitution
        "wipe-it-clean" step for this ore/mod).  Changing an ore, or the
        [DEFAULT] to "no" will skip the step for this ore or mod,
        respectively.

    Wireframe:

        COG has a feature that will show wireframe outlines of the area
        chosen for motherlodes and veins as they're configured to allow you
        to see if they're working.  If the wireframe goes into a location
        where the ore should be, and you don't see ore intersecting with it,
        something's wrong.
        
        This option specifically is meant to select the color the wireframe
        will be.  This is simply the 6-digit hexadecimal number known as a
        "hex triplet" (or "web color").  Do not use the hash ("#") mark,
        however.  For example, "68fa2b" works, but "#68fa2b" doesn't.
        
        The default is randomly generated every time Sprocket is run, and
        is the same for all ores in a configuration file.

    Seed:
        
        Some distributions, such as the Pipe and Geode distributions, depend
        on the multiple configurations being identically-located, so they can
        interact as desired.  This means that they have to share a random number
        seed.  If you want to use a specific value, or you just don't want it
        changing every time you re-run Sprocket, you can set the seed number
        with this command.

        The default is randomly generated each time Sprocket is run.

    Pipe:
        
        This identifies the block that is contained in Pipe Veins.  Usually
        set to minecraft:lava (configuration for Diamonds) or 
        minecraft:monster_egg (configuration for Emeralds).  Also used to
        define the "shell" material for geodes.
        
        The default is "minecraft:lava".

    Height:

        This sets the height around which the ore will generate; this is the
        center of the range.  "64" is considered sea level; the actual
        number scales depending on the Scale setting.
        
        There are also height commands for each distribution type:
        
        * Standard Height
        * Vein Height
        * Cloud Height
        
        The default is 64.

    Min Height:

        A function of height clamping; this will limit the lower end of ore
        generation to a    minimum level.  If this is set to '0', then there is
        no limit.
        
        The default is 0.

    Max Height:

        A function of height clamping; this will limit the upper end of ore
        generation to a maximum level.  If this is set to '0', then there is
        no limit.
        
        The default is 0.

    Range:

        This sets the range around the above center height that ores will
        generate.  Like the height, this number is scaled based on the 
        Scale setting.
        
        There are also range commands for each distribution type:
        
        * Standard Range
        * Vein Range
        * Cloud Range
    
        The default is 64.

    Size:
    
        This is the vein size multiplier.  1 is the default; nothing is
        changed.  Less than 1 (make sure the number is in the form of 0.x)
        make the ore deposits smaller.  More than 1 makes them larger.
        
        Additionally, the following can be used to further multiply the
        specific distributions (they combine with the Size multiplier)
    
        * Standard Size
        * Vein Size
        * Cloud Size
    
        The default is 1.

    Frequency:

        Frequency multiplier; works the same way as the size multiplier.
        
        Additionally, the following can be used to further multiply the
        specific distributions (they combine with the Frequency multiplier)
        
        * Standard Frequency
        * Vein Frequency
        * Cloud Frequency
        
        The default is 1.
    
    Density:
    
        Sometimes, you don't want a vein or cloud to be too full of ore.
        Density will reduce the ore in a vein or cloud, causing space to be
        generated between the various blocks.  The lower the density, the
        fewer ore blocks are in an area.  This setting is a multiplier of
        the default density.
        
        Additionally, the following can be used to further multiply the
        specific distributions (they combine with the Density multiplier)
    
        Standard Density
        Vein Density
        Cloud Density
        
        The default is 1.
                
    Vein Settings:
    
        A lot of other commands have been added in order to allow close
        duplication of the original Minecraft vein configuration.  It is
        not likely you will need these commands, but in case you do, here
        they are:
        
        * Vein Branch Settings:
            * Vein Branch Frequency
            * Vein Branch Height Limit
            * Vein Branch Inclination Average
            * Vein Branch Length Average
            * Vein Branch Length Range
        * Vein Segment Settings:
            * Vein Segment Angle Average
            * Vein Segment Angle Range
            * Vein Segment Pitch Average
            * Vein Segment Pitch Range
            * Vein Segment Radius Average
            * Vein Segment Radius Range
    
    Biomes: (And "Avoids:")
    
        Biome requirements as a comma-separated list of biome dictionary
        entries.  This means that only those biomes listed will actually
        spawn the ore.  If the biome is not on this list, the ore will not
        spawn there.  If you want to prevent the ore from spawning in a
        specific biome (for example, frozen, but not frozen ocean), the
        Avoid list can select those biome tags the ore will not spawn in.
    
        The default is "ALL". (There is no "NONE")
    
    Prefers: (And "Prefers Not:")
    
        Biome preferences as a comma-separated list of biome dictionary
        entries.  This means that the biomes listed in this option will
        have additional ores spawning in those biomes. The additional
        frequency will be 1 additional spawn, but this can be altered
        using the "Prefers Multiplier" option.  Additionally, if you
        want a specific biome to avoid being "preferred," you can add
        the "Prefer Not" option to prevent that biome from being used
        (for example, if you want "frozen", but not "frozen ocean").
    
        The default value is "NONE". (There is no "ALL")
    
    Prefers Multiplier:
    
        Sometimes, you want the preferred biome to do more than double the
        ore.  This option will multiply the preferred biome frequency (for
        example, using "2" will double the distributions in the preferred
        biome... in addition to the single distribution generated from the
        non-preferred set... for a total multiplier of "3" in a preferred
        biome.
    
        The default is 1.
    
    Adjacent (Above/Below/Beside):
    
        This option allows you to select multiple blocks (separated by
        commas) which the current block must be adjacent to.  The block
        will then only spawn when the adjacency conditions are met.
        
        The commands are...
            Adjacent Above:  
            Adjacent Below:  
            Adjacent Beside:  
        
        ...followed with one or more block names, separated by commas,
        such as...
            minecraft:dirt, minecraft:netherrack, minecraft:sand
        
        By default, adjacency is unused.
    
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
