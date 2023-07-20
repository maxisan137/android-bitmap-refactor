# Image refactor utility for Android App Development

This utility is used to refactor bitmap images for use in Android app development. It refactors the input image into different pixel density versions: mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi

## How to use

Usage:

    py imgRefact.py -i <path_to_image>

Example usage:

    py imgRefact.py -i image.png -o output_folder -a mipmaps

Possible flags:

 - **-i** - Required - Path to input image;
 - **-o** - Optional - Output directory where all the different verions will be saved. By default saves all into current working directory;
 - **-a** - Optional - Name of directory in Android project. By default will use the name 'drawable'. When refactoring images, separate directories will be created for each pixel density, such as 'drawable-mdpi', 'dawable-hdpi' etc.;
 - **-d** - Optional - Pixel density of the original input image. By default, assumes that the input image is for xxxhdpi density and adjusts the scale of the rest of images accordingly. Only accepts the correct names of supported pixel densities;
 - **-h** - Print help instructions - used only on it's own.