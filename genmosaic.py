"""
program name: generate mosaic images
created by	: gamesbrewer.com
file name	: genmosaic.py
file version: 1.0
created on	: 14/02/2022
Requirements: scipy, numpy
description	: generate tiled mosaic images, and rudimentary knowledge of kd-tree. check it out here https://www.wikiwand.com/en/K-d_tree
"""

import glob
from PIL import Image
from scipy import spatial
import numpy as np
import sys

#our data definition
tile_paths = []
tiles = []
colors = []
main_photo = None
resized_photo = None

# Get all tiles
def build_tile_path_list():
    for file in glob.glob(tile_photos_path):
        tile_paths.append(file)

# Import and resize all tiles
def build_tiles(tile_size):
    for path in tile_paths:
        tile = Image.open(path)
        tile = tile.resize(tile_size) #resize it, this need to modify to generate multiple sized tils in the output
        tiles.append(tile)

# Calculate dominant color
def build_colors():
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

# Pixelate main photo
def pixelate_images():
    main_photo = Image.open(main_photo_path)
    width = int(np.round(main_photo.size[0] / tile_size[0]))
    height = int(np.round(main_photo.size[1] / tile_size[1]))
    resized_photo = main_photo.resize((width, height))

    # Find closest tile photo for every pixel
    tree = spatial.KDTree(colors)
    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for i in range(width):
        for j in range(height):
            closest = tree.query(resized_photo.getpixel((i, j)))
            closest_tiles[i, j] = closest[1]

    # Create an output image
    output = Image.new('RGB', main_photo.size)

    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*tile_size[0], j*tile_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            output.paste(tiles[index], (x, y))

    # Save output
    output.save(output_path)

# Sources and settings
if __name__ == "__main__":
    main_photo_path = sys.argv[1]
    tile_photos_path = "tiles\\*"
    tile_size_small = (8, 8)
    tile_size_medium = (16, 16)
    tile_size_large = (32, 32)
    tile_size_xtra_large = (64, 64)
    tile_size_gigantic = (128, 128)
    tile_size_titanic = (256, 256)
    selected_tile = tile_size_large
    tile_size = selected_tile
    output_path = "output\\output.png"

    build_tile_path_list()
    build_tiles(selected_tile)
    build_colors()
    pixelate_images()