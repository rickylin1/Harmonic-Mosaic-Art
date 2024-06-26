import ColorCreator, ColorFormats, DISCOVERY, PIL
import pandas as pd
import math
import os
import sys
from PIL import Image
from DISCOVERY import listTileImagesInPath, df_image, getTileImage
from ColorCreator import create_analogous, create_complementary, create_monochrome, create_triadic

def findAverageImageColor(image):
    avg_r = image['r'].mean()
    avg_g = image['g'].mean()
    avg_b = image['b'].mean()
    d = {"avg_r": avg_r, "avg_g": avg_g, "avg_b": avg_b}
    return d

def findImageSubset(image, x, y, width, height):
    imagesubset = image[(image['x'] >= x) & (image['x'] < x + width) & (image['y'] >= y) & (image['y'] < y + height)]
    return imagesubset

def findAverageImageSubsetColor(image, x, y, width, height):
    return findAverageImageColor(findImageSubset(image, x, y, width, height))

def findBestTile(df_tiles, r_avg, g_avg, b_avg):
    df_tiles['distance'] = ((r_avg - df_tiles['r'])**2 + (g_avg - df_tiles['g'])**2 + (b_avg - df_tiles['b'])**2) ** 0.5
    return df_tiles.nsmallest(1, 'distance')

def createTilesDataFrame(path):
    data = []

    for tileImageFileName in listTileImagesInPath(path):
        image = df_image(tileImageFileName)
        averageColor = findAverageImageColor(image)

        d = {"fileName": tileImageFileName, "r": averageColor["avg_r"], "g": averageColor["avg_g"], "b": averageColor["avg_b"]}
        data.append(d)

    df_tiles = pd.DataFrame(data)
    return df_tiles

def createMosaic(targetFile, tileImageFolder='monochrome', maxTileX=200, maxTileY=200):
    print(f"Creating `df_tiles` from tile images in folder `{tileImageFolder}`...")
    df_tiles = createTilesDataFrame(tileImageFolder)
    print(f"...found {len(df_tiles)} tile images!")

    print(f"Loading your base image `{targetFile}`...")
    baseImage = df_image(targetFile)
    
    # Check if baseImage is a DataFrame
    if not isinstance(baseImage, pd.DataFrame):
        raise ValueError("Expected base image to be a DataFrame")
        
    width = baseImage['x'].max()
    height = baseImage['y'].max()

    print(f"Finding best replacement image for each tile...")
    pixelsPerTile = int(math.ceil(width / maxTileX))
    width = int(math.floor(width / pixelsPerTile) * pixelsPerTile)
    height = int(math.floor(height / pixelsPerTile) * pixelsPerTile)
    tilesX = int(width / pixelsPerTile)
    tilesY = int(height / pixelsPerTile)

    mosaic = Image.new('RGB', (int(tilesX * maxTileY), int(tilesY * maxTileY)))
    for x in range(0, width, pixelsPerTile):
        for y in range(0, height, pixelsPerTile):
            avg_color = findAverageImageSubsetColor(baseImage, x, y, pixelsPerTile, pixelsPerTile)
            replacement = findBestTile(df_tiles, avg_color["avg_r"], avg_color["avg_g"], avg_color["avg_b"])

            tile = getTileImage(replacement["fileName"].values[0], maxTileY)
            mosaic.paste(tile, (int(x / pixelsPerTile) * maxTileY, int(y / pixelsPerTile) * maxTileY))

            curRow = int((x / pixelsPerTile) + 1)
            pct = (curRow / tilesX) * 100
            sys.stdout.write(f'\r  ...progress: {curRow * tilesY} / {tilesX * tilesY} ({pct:.2f}%)')

    mosaic.save('mosaic-hd.jpg')
    d = max(width, height)
    factor = d / 4000
    if factor <= 1: factor = 1

    small_w = width / factor
    small_h = height / factor
    baseImage = mosaic.resize((int(small_w), int(small_h)), resample=PIL.Image.LANCZOS)
    baseImage.save('mosaic-web.jpg')

    destination_folder = 'mosaics'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    hd_destination_path = os.path.join(destination_folder, os.path.basename('mosaic-hd.jpg'))
    web_destination_path = os.path.join(destination_folder, os.path.basename('mosaic-web.jpg'))

    os.rename('mosaic-hd.jpg', hd_destination_path)
    os.rename('mosaic-web.jpg', web_destination_path)

    tada = "\N{PARTY POPPER}"
    print("")
    print("")
    print(f"{tada} MOSAIC COMPLETE! {tada}")
    print("- See `mosaic-hd.jpg` to see your HQ mosaic! (The file may be HUGE.)")
    print("- See `mosaic-web.jpg` to see a mosaic best suited for the web (still big, but not HUGE)!")


def get_user_inputs():
    targetFile = os.path.join('targetFiles', input("Enter the target file path: "))
    print("Choose your mosaic color!")
    print('Feel free to reference Color Picker to get an idea of your color')
    color_r = input('Enter red: ')
    color_g = input('Enter green: ')
    color_b = input('Enter blue: ')
    color = (int(color_r), int(color_g), int(color_b))
    tileImageFolder = input("Enter the color group (analogous, complementary, triadic, or default (monochrome)): ") or 'monochrome'
    function_name = f"create_{tileImageFolder}"
    globals()[function_name](color)
    maxTileX = input("Enter the maximum number of tiles in the X direction (default is 200): ")
    maxTileX = int(maxTileX) if maxTileX else 200
    maxTileY = input("Enter the maximum number of tiles in the Y direction (default is 200): ")
    maxTileY = int(maxTileY) if maxTileY else 200

    return targetFile, tileImageFolder, maxTileX, maxTileY

if __name__ == "__main__":
    inputs = get_user_inputs()
    createMosaic(*inputs)