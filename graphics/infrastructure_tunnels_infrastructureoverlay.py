#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, blend_overlay, paste_to, alpha_to, blue_to, colour_to, blue_to_alpha

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
mode = sys.argv[2]
tile_size = scale * 64

if mode == "rail":
  # Infrastructure sprites to use
  infrastructure_list = {
    "rail": "rail",
    "monorail": "monorail",
    "maglev": "maglev"
  }
elif mode == "road":
  # Infrastructure sprites to use
  infrastructure_list = {
    "road": "road"
  }
# Terrain sprites to use
terrain_tile_positions = [
  [719, 1, 64, 39],
  [959, 1, 64, 39],
  [479, 1, 64, 24],
  [241, 1, 64, 24]
]
# Terrain extra offset
terrain_tile_voffs = [0, 0, -7, -7]
# Terrain list to process
terrain_list = {
  "arctic_grass": "arctic_groundtiles_32bpp.png",
  "arctic_snow": "arctic_groundtiles_snow_32bpp.png",
  "tropical_grass": "tropical_groundtiles_32bpp.png",
  "tropical_desert": "tropical_groundtiles_desert_32bpp.png",
  "temperate_grass": "temperate_groundtiles_32bpp.png",
  "toyland_grass": "toyland_groundtiles_32bpp.png",
}
# Infrastructure sprites to use
infrastructure_tile_positions = [
  [1, 1, 64, 31],
  [66, 1, 64, 31],
  [1, 1, 64, 31],
  [66, 1, 64, 31]
]
col_width = 64
row_height = 64

# Output image properties
output_width = ((col_width + 1) * 2 + 1) * scale
output_height = ((row_height + 1) * len(infrastructure_tile_positions) + 1) * scale 

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  for infrastructure_key in infrastructure_list:
    terrain_image_path = os.path.join("..", "..", "..", "terrain", str(tile_size), terrain_list[terrain_key])
    infrastructure_image_path = os.path.join("..", "..", "..", "infrastructure", str(tile_size), infrastructure_list[infrastructure_key]+"_overlayalpha.png")
    name_overlay = os.path.join("pygen", infrastructure_list[infrastructure_key]+"tunnels_regions_32bpp.png")
    name_overlayshading = infrastructure_list[infrastructure_key]+"tunnels_overlayshading.png"
    output_normal_path = os.path.join("pygen", "tunnels_"+infrastructure_list[infrastructure_key]+"_"+terrain_key+"_32bpp.png")
    # Check if update needed
    if check_update_needed([terrain_image_path, infrastructure_image_path, name_overlay, name_overlayshading], output_normal_path):
      # Make image containing arranged infrastructure on and slope backgrounds
      terrain_image = Image.open(terrain_image_path)
      infrastructure_image = blue_to_alpha(Image.open(infrastructure_image_path))
      target_image = Image.new("RGBA", (output_width, output_height), (255, 255, 255, 255))
      for i in range(len(infrastructure_tile_positions)):
        target_image = paste_to(terrain_image, terrain_tile_positions[i][0], terrain_tile_positions[i][1], terrain_tile_positions[i][2], terrain_tile_positions[i][3], target_image, 0 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - terrain_tile_positions[i][3] + terrain_tile_voffs[i] + 1) * scale, scale)
        target_image = paste_to(terrain_image, terrain_tile_positions[i][0], terrain_tile_positions[i][1], terrain_tile_positions[i][2], terrain_tile_positions[i][3], target_image, 1 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - terrain_tile_positions[i][3] + terrain_tile_voffs[i] + 1) * scale, scale)
        #target_image = alpha_to(infrastructure_image, infrastructure_tile_positions[i][0], infrastructure_tile_positions[i][1], infrastructure_tile_positions[i][2], infrastructure_tile_positions[i][3], target_image, 0 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - infrastructure_tile_positions[i][3] + 1) * scale, scale)
        target_image = alpha_to(infrastructure_image, infrastructure_tile_positions[i][0], infrastructure_tile_positions[i][1], infrastructure_tile_positions[i][2], infrastructure_tile_positions[i][3], target_image, 1 * (tile_size // scale + 1) + 1, i * (tile_size // scale + 1) + (tile_size - infrastructure_tile_positions[i][3] + 1) * scale, scale)
        # Overlay each infrastructure set
        print("  "+infrastructure_key)
        # Overlay overlay_alpha
        print(name_overlay)
        overlay_image = Image.open(name_overlay).convert("RGBA")
        target_image = colour_to(overlay_image, 0, 0, output_width, output_height, target_image, 0, 0, scale, 252, 0, 255) # Warning magenta (255, 0, 255) gets change to 252, 0, 255 by building_shapeproc
        # Overlay overlayshading, if it exists
        if os.path.isfile(name_overlayshading):
          print(name_overlayshading)
          infrastructure_image = Image.open(name_overlayshading).convert("RGBA")
          target_image = blend_overlay(target_image, infrastructure_image, 192/255)
        # Save 32bpp image
        target_image.save(output_normal_path)
