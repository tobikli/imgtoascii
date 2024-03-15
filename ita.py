#!/usr/bin/env python3

import os               #For filepath parsing
import argparse         #For argument parsing
from PIL import Image   #For image reading

def get_char(number):
    dict = {
        (0, 15): ".",
        (15, 30): ",",
        (30, 50): "=",
        (50, 80): "°",
        (70, 80): "+",
        (80, 100): "*",
        (100, 110): "\"",
        (110, 120): "=",
        (120, 150): "%",
        (150, 180): "§",
        (180, 210): "$",
        (210, 230): "&",
        (230, 255): "#",
    }

    for (start, end), char in dict.items():
        if start <= number <= end:
            return char
    return "."


def get_full(imgPath, scale):

    try:
        img = Image.open(imgPath)
    except:
        print("Error while reading image", imgPath)
        exit(-1)

    img_gray = img.convert('L')

    width, height = img_gray.size

    if scale != None:
        width, height = int (width / scale), int(height / scale)
        img_gray.thumbnail((width, height))

    pxls = img_gray.load()

    outString = ""

    for i in range(0, height):
        for j in range(0, width):
            currPxl = pxls[j, i]
            outString += get_char(currPxl)
        outString += '\n'

    return outString




def main():
    parser = argparse.ArgumentParser(prog='ITA', description='Image to ASCII parser', epilog='https://github.com/tobikli/imgtoascii')

    parser.add_argument('filename')
    parser.add_argument('-o', help="Specify the output file", dest="output")
    parser.add_argument('-s', type=int, choices=[1,2,4,8], help="Scale down Output by given factor, else full Size")

    args = parser.parse_args()

    imgPath = args.filename
    scale = args.s

    outFull = get_full(imgPath, scale)

    filename = os.path.basename(imgPath)
    if "." in filename:
       filename = filename.split('.')[0]

    filename += "_ascii"

    if args.output != None:
        filename = args.output

    if scale != None:
        filename += "_" + str(scale) + "x"

    try:
        f = open(filename, "w")
    except:
        print("Error while writing to file", filename)
        exit(-1)

    f.write(outFull)
    print("Finished writing to", filename+"!")

    exit()

if __name__ == '__main__':
    main()
