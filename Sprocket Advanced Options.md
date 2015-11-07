# Sprocket INI Options

## Option Types:

* *List*: A comma-separated list of items.  Can also use regular expressions.
* *Value*: a single value only
* *Boolean*: A simple "yes" or "no" will suffice.
* *Statistical Variation*: This option consists of four values.
    * The statistical average.
    * The statistical deviation, also called the range.
    * Preference, consisting of _one_of_the_following_:
        * "normal" (prefers to stay closer to the average)
        * "inverse" (prefers to stay closer to the deviation)
        * "uniform" (no preference, completely random)
    * Scaling option (see COG's documentation for more details), usually defaults to "base".

## Distribution Meta Options

### Seed (Value)
     Default: MISSING

### Active (Boolean)
     Default: yes

### Size (Statistical Variation)
     Default: _default_, _default_, normal, base

### Frequency (Statistical Variation)
     Default: _default_, _default_, normal, base

### Height (Statistical Variation)
     Default: _default_, _default_, normal, base

### Density (Statistical Variation)
     Default: _default_, _default_, normal, base

### Parent Range Limit (Statistical Variation)
     Default: _default_, _default_, normal, base

### Main Block Cleanup (Boolean)
     Default: yes

### Alternate Block Cleanup (Boolean)
     Default: no

### Distribution Presets (List)
     Default: Vanilla
     
## Block Lists

### Blocks (List)
     Default: MISSING

### Alternate Blocks (List)
     Default: minecraft:stone

### Replaces (List)
     Default: minecraft:stone

### Block Weights (List)
     Default: MISSING

### Alternate Block Weights (List)
     Default: MISSING

### Replacement Weights (List)
     Default: MISSING

## Location Options

### Dimensions (List)
     Default: 0

### Need Biomes (List)
     Default: .*

### Need Biome Types (List)
     Default: MISSING

### Avoid Biomes (List)
     Default: MISSING

### Avoid Biome Types (List)
     Default: MISSING

### Prefer Biomes (List)
     Default: MISSING

### Prefer Biome Types (List)
     Default: MISSING

### Biome Rainfall Range (List)
     Default: MISSING

### Biome Temperature Range (List)
     Default: MISSING

### Place Below (List)
     Default: MISSING

### Place Beside (List)
     Default: MISSING

### Place Above (List)
     Default: MISSING
     
# Substitution Distribution Options

### Height Clamp Range (List)
     Default: MISSING

### Substitution Height Clamp Range (List)
     Default: MISSING

## Standard Distribution Options

### Standard Size (Statistical Variation)
     Default: MISSING

### Standard Frequency (Statistical Variation)
     Default: MISSING

### Standard Height (Statistical Variation)
     Default: MISSING

### Standard Parent Range Limit (Statistical Variation)
     Default: MISSING

### Standard Height Clamp Range (List)
     Default: MISSING
     
## Cloud Distribution Options

### Cloud Frequency (Statistical Variation)
     Default: MISSING

### Cloud Parent Range Limit (Statistical Variation)
     Default: MISSING

### Cloud Radius (Statistical Variation)
     Default: MISSING

### Cloud Thickness (Statistical Variation)
     Default: MISSING

### Cloud Noise (Statistical Variation)
     Default: _default_, _default_, normal, base

### Cloud Height (Statistical Variation)
     Default: MISSING

### Cloud Inclination (Statistical Variation)
     Default: _default_, _default_, normal, base

### Cloud Density (Statistical Variation)
     Default: MISSING

### Cloud Noise Cutoff (Statistical Variation)
     Default: _default_, _default_, normal, base

### Cloud Radius Multiplier (Statistical Variation)
     Default: _default_, _default_, normal, base

### Cloud Height Clamp Range (List)
     Default: MISSING
     
## Vein Distribution Options

### Vein Motherlode Frequency (Statistical Variation)
     Default: MISSING

### Vein Motherlode Range Limit (Statistical Variation)
     Default: MISSING

### Vein Motherlode Size (Statistical Variation)
     Default: MISSING

### Vein Motherlode Height (Statistical Variation)
     Default: MISSING

### Vein Branch Frequency (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Branch Inclination (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Branch Length (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Branch Height Limit (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Segment Fork Frequency (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Segment Fork Length Multiplier (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Segment Length (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Segment Angle (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Segment Radius (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Ore Density (Statistical Variation)
     Default: MISSING

### Vein Ore Radius Multiplier (Statistical Variation)
     Default: _default_, _default_, normal, base

### Vein Height Clamp Range (List)
     Default: MISSING

## Debugging Options

### Wireframe (Boolean)
     Default: yes

### Bounding Box (Boolean)
     Default: no

### Wireframe Color (Value)
     Default: MISSING

### Bounding Box Color (Value)
     Default: MISSING
