#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter
from random import randint
import numpy, blend_modes # For overlay blending
import glob, os, sys

from tools import check_update_needed, openttd_palettise, blend_overlay, blue_over, paste_to

if os.path.isdir("pygen") == False: os.mkdir("pygen")

verbose = True
scale = int(sys.argv[1])
mode = sys.argv[2]
tile_size = scale * 64

if mode == "canal":
  # Remapping of tile positions
  tile_positions = [
    [1, 1, 64, 32],
    [959, 1, 64, 41],
    [241, 1, 64, 24],
    [479, 1, 64, 24],
    [719, 1, 64, 41],
  ]
  rows = 4
  # Infrastructure sprites to use
  infrastructure_list = {
    "canal": "canal",
    "river": "river"
  }
  # Terrain sprites to use
  terrain_list = {
    "arctic_grass": "arctic_groundtiles_32bpp.png",
    "arctic_snow": "arctic_groundtiles_snow_32bpp.png",
    "tropical_grass": "tropical_groundtiles_32bpp.png",
    "tropical_desert": "tropical_groundtiles_desert_32bpp.png",
    "temperate_grass": "temperate_groundtiles_32bpp.png",
    "general_concrete": "general_concretetiles_32bpp.png",
    "toyland_grass": "toyland_groundtiles_32bpp.png",
    "arctic_grass_shores": os.path.join("pygen", "arctic_grass_shoretiles_32bpp.png"),
    "tropical_grass_shores": os.path.join("pygen", "tropical_grass_shoretiles_32bpp.png"),
    "temperate_grass_shores": os.path.join("pygen", "temperate_grass_shoretiles_32bpp.png"),
    "toyland_grass_shores": "toyland_shoretiles_32bpp.png"
  }

# Output image properties
output_width = (scale + (tile_size + scale) * len(tile_positions))
row_height = 0
for i in range(len(tile_positions)):
  if tile_positions[i][3] - 1 > row_height:
    row_height = tile_positions[i][3] - 1
output_height = row_height * rows
output_height += 1
output_height *= scale

print("Running in scale "+str(scale)+" (tile size "+str(tile_size)+") "+mode+" mode")
for terrain_key in terrain_list:
  print(" "+terrain_key)
  # Make image containing arranged terrain backgrounds
  terrain_image_path = os.path.join("..", "..", "terrain", str(tile_size), terrain_list[terrain_key])
  terrain_image = Image.open(terrain_image_path)
  target_image = Image.new("RGBA", (output_width, output_height), (255, 255, 255, 255))
  for i in range(len(tile_positions)):
    target_image = paste_to(terrain_image, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image, i * (tile_size // scale + 1) + 1, 1, scale)
  for i in range(rows):
    target_image = paste_to(target_image, 0, 1, output_width, row_height, target_image, 0, i * row_height + 1, scale)
  # Make a plmask image from terrain background palmask images, if they exists
  terrain_palmask_path = os.path.join("..", "..", "terrain", str(tile_size), terrain_list[terrain_key][:len("_32bpp.png")]+"_palmask.png")
  if os.path.isfile(terrain_palmask_path):
    terrain_image_palmask = openttd_palettise(Image.open())
    for i in range(len(tile_positions)):
      target_image_palmask = paste_to(terrain_image_palmask, tile_positions[i][0], tile_positions[i][1], tile_positions[i][2], tile_positions[i][3], target_image_palmask, i * (tile_size +1) + 1, 1, scale)
    for i in range(rows):
      target_image_palmask = paste_to(target_image_palmask, 0, 0, output_width, row_height, target_image_palmask, 0, i * row_height, scale)
  else:
    target_image_palmask = openttd_palettise(Image.new("RGB", target_image.size, (0, 0, 255)))
  target_image_palmask = target_image_palmask.convert("RGBA")
  for infrastructure_key in infrastructure_list:
    # Overlay each infrastructure set
    print("  "+infrastructure_key)
    # Check files for changes
    infrastructure_alpha_path = infrastructure_list[infrastructure_key]+"_overlayalpha.png"
    infrastructure_normal_path = infrastructure_list[infrastructure_key]+"_overlaynormal.png"
    infrastructure_shading_path = infrastructure_list[infrastructure_key]+"_overlayshading.png"
    output_normal_path = os.path.join("pygen", infrastructure_key+"_"+terrain_key+"_32bpp.png")
    output_palmask_path = os.path.join("pygen", infrastructure_key+"_"+terrain_key+"_palmask.png")
    if check_update_needed([terrain_image_path, infrastructure_alpha_path, infrastructure_normal_path, infrastructure_shading_path], output_normal_path):
      # Open overlay_alpha and make cropped target to its target size
      infrastructure_alpha = Image.open(infrastructure_alpha_path).convert("RGBA")
      overlay_w, overlay_h = infrastructure_alpha.size
      target_image_crop = target_image.crop((0, 0, overlay_w, overlay_h))
      target_image_palmask_crop = target_image_palmask.crop((0, 0, overlay_w, overlay_h))
      # Overlay overlay_alpha
      target_image_crop = Image.alpha_composite(target_image_crop, infrastructure_alpha)
      # Overlay overlaynormal
      infrastructure_normal = Image.open(infrastructure_normal_path).convert("RGBA")
      target_image_crop = Image.alpha_composite(target_image_crop, infrastructure_normal)
      # Overlay overlayshading
      if os.path.isfile(infrastructure_shading_path):
        print(infrastructure_shading_path)
        infrastructure_shading = Image.open(infrastructure_shading_path).convert("RGBA")
        target_image_crop = blend_overlay(target_image_crop, infrastructure_shading, 192/255)
      # Save 32bpp
      target_image_crop.save(output_normal_path)
      # Overlay normal onto palmask image
      target_image_palmask_crop = Image.alpha_composite(target_image_palmask_crop, infrastructure_normal)
      target_image_palmask_crop = openttd_palettise(target_image_palmask_crop)
      target_image_palmask_crop.save(output_palmask_path)