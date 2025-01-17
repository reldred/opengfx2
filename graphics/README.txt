This is an 8-bit (8bpp) image set.

Many images are automatically generated. All 8-bit images are generated from RGB or RGBA (32bpp) png images.
The 32bpp png images may themselves have a source, and may be manually derived from Paint.NET (pdn), GIMP (xcf) or Blender (blend) files.

All "*_8bpp.png" images are automatically generated from the file called "*_32bpp.png".
Do not directly modify any file named "*_8bpp.png", your changes will be overwritten!

Files within a directory named "pygen" are automatically generated from images in the parent directory.
This includes files named "*_32bpp.png", do not modify them as your changes will be overwritten!

NB. The "*_32bpp.png" images may not actually be RGB or RGBA, but their name indicates they should be handled as 32bpp source images.

Typically, sprites are generated by:
Either, for buildings:
	Taking an object shape from a file named "*_shape.png" and recolouring and texturing it based on specialised pixels on row 1 of the image.
Or, for terrain and infrastructure tiles:
	Taking a base texture from a reference "*_32bpp.png" file, eg. standard ground grass
Overlaying various additional layers to add detail:
	"*_overlayalpha.png": A 32bpp image overlaid in alpha blending mode.
	"*_overlayshading.png": A 32bpp image overlaid in overlay blending mode.
	"*_overlaynormal.png": A pseudo-8bpp image overlaid in alpha blending mode.
Converting to 8bpp:
	Conversion uses a custom, standardised, dither script.
	If "*_palmask.png" exists, restricting dither to within the colour series/groups within this set.
	"*_palmask.png" is usually generated from unshaded recoloured "*_shape.png" images, overlaid with "*_overlaynormal.png"
	Animated palette indices are not used in normal dithering, unless in the "*_palmask.png" image, in which case they are protected and preserved.

Further sprite specific processing may then be done, including:
	Overlaying/merging building sprites with ground tiles
	Cutting up a multi-tile sprite into individual sprites
