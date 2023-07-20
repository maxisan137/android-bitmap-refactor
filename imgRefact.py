from PIL import Image
import os
import sys


PD_KEY_NAME = "NAME"
PD_KEY_SCALING_FACTOR = "SCALING_FACTOR"
PIXEL_DENSITIES = [
    {PD_KEY_NAME: "mdpi", PD_KEY_SCALING_FACTOR: 1},
    {PD_KEY_NAME: "hdpi", PD_KEY_SCALING_FACTOR: 1.5},
    {PD_KEY_NAME: "xhdpi", PD_KEY_SCALING_FACTOR: 2},
    {PD_KEY_NAME: "xxhdpi", PD_KEY_SCALING_FACTOR: 3},
    {PD_KEY_NAME: "xxxhdpi", PD_KEY_SCALING_FACTOR: 4}
]

DEFAULT_ANDROID_FOLDER = "drawable"
DEFAULT_PIXEL_DENSITY = PIXEL_DENSITIES[-1][PD_KEY_NAME]

# Flags to be used with CLI
FLAG_HELP = "-h"
FLAG_INPUT_IMAGE = "-i"
FLAG_OUTPUT_FOLDER = "-o"
FLAG_ANDROID_DIR  = "-a"
FLAG_PIXEL_DENSITY = "-d"

FLAGS = [
    FLAG_INPUT_IMAGE,
    FLAG_OUTPUT_FOLDER,
    FLAG_ANDROID_DIR,
    FLAG_PIXEL_DENSITY
]


def refactorImage(imageName, outputPath="", androidFolderName=DEFAULT_ANDROID_FOLDER, pixelDensity=DEFAULT_PIXEL_DENSITY):

    # Check if input image file exists
    if not os.path.isfile(imageName):
        print(f"Cannot find file named {imageName}")
        return
    
    # Check input pixel density of original image
    if pixelDensity not in [d[PD_KEY_NAME] for d in PIXEL_DENSITIES]:
        print("Please enter correct name of pixel density of the default image. Accepted values: " + ", ".join([d[PD_KEY_NAME] for d in PIXEL_DENSITIES]))
        return

    # Open image wit PIL
    try:
        originalImage = Image.open(imageName)
    except:
        print("Unable to open image file")
        return

    # Create output folder if doesn't exist
    if outputPath is None: outputPath = ""
    if outputPath != "" and not os.path.isdir(outputPath):
        os.mkdir(outputPath)
    
    # Get original image size
    originalResolution = originalImage.size

    # Get scaling factor for the original image, based on selected pixel density
    originalScalingFactor = [d for d in PIXEL_DENSITIES if d[PD_KEY_NAME] == pixelDensity][0][PD_KEY_SCALING_FACTOR]

    for pd in PIXEL_DENSITIES:

        # Compute new resolution for each density
        res = (1, 1)
        if pd[PD_KEY_NAME] == pixelDensity:
            res = originalResolution
        else:
            res = (int(originalResolution[0] / originalScalingFactor * pd[PD_KEY_SCALING_FACTOR]), int(originalResolution[1] / originalScalingFactor * pd[PD_KEY_SCALING_FACTOR]))
        
        # Resize image
        resizedImage = originalImage.resize(res)

        # Create output folder if doesn't exist
        outputDir = os.path.join(outputPath, androidFolderName + "-" + pd[PD_KEY_NAME])
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
        
        # Save output image
        resizedImage.save(os.path.join(outputDir, imageName), originalImage.format)


def printHelpInstructios():

    print("")
    print("Image refactor utility for Android")
    print("")
    print("This utility is used to refactor bitmap images for use in Android app development. It refactors the input image into different pixel density versions: mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi")
    print("")
    print("Usage:")
    print("py imgRefact.py -i <path_to_image>")
    print("")
    print("Example usage:")
    print("py imgRefact.py -i image.png -o output_folder -a mipmaps")
    print("")
    print("Possible flags:")
    print("     " + FLAG_INPUT_IMAGE + " - Required - Path to input image")
    print("     " + FLAG_OUTPUT_FOLDER + " - Optional - Output directory where all the different verions will be saved. By default saves all into current working directory")
    print("     " + FLAG_ANDROID_DIR + " - Optional - Name of directory in Android project. By default will use the name 'drawable'. When refactoring images, separate directories will be created for each pixel density, such as 'drawable-mdpi', 'dawable-hdpi' etc.")
    print("     " + FLAG_PIXEL_DENSITY + " - Optional - Pixel density of the original input image. By default, assumes that the input image is for xxxhdpi density and adjusts the scale of the rest of images accordingly. Only accepts the correct names of supported pixel densities")
    print("     " + FLAG_HELP + " - Print help instructions - used only on it's own")

    quit()


def printIncorrectArgs():
    print("Please enter correct number of arguments. Use -h for help")
    quit()


if __name__ == "__main__":

    args = sys.argv
    params = {
        FLAG_INPUT_IMAGE: None,
        FLAG_OUTPUT_FOLDER: None,
        FLAG_ANDROID_DIR: DEFAULT_ANDROID_FOLDER,
        FLAG_PIXEL_DENSITY: DEFAULT_PIXEL_DENSITY
    }
    
    if len(args) == 1:
        printIncorrectArgs()
    elif len(args) == 2 and args[1] == FLAG_HELP:
        printHelpInstructios()
    elif len(args) > 2 and len(args) % 2 != 1:
        printIncorrectArgs()
    else:
        for i in range(1, len(args), 2):
            if args[i] not in FLAGS:
                printIncorrectArgs()
            else:
                params[args[i]] = args[i + 1]
    
    if params[FLAG_INPUT_IMAGE] is None:
        printIncorrectArgs()
    
    refactorImage(
        imageName=params[FLAG_INPUT_IMAGE],
        outputPath=params[FLAG_OUTPUT_FOLDER],
        androidFolderName=params[FLAG_ANDROID_DIR],
        pixelDensity=params[FLAG_PIXEL_DENSITY]
    )
