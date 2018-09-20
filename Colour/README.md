# JPEG to Colour ASCII converter
Converts any JPEG image to coloured ASCII

<img src=markdown_images/mountain.jpg width="40%">
<img src=markdown_images/mountain_ascii.JPG width="30%">

Using a k-means clustering algorithm (with 5 and 10 clusters respectively):

<img src=markdown_images/mountain_ascii_cluster_5.JPG width="35%">
<img src=markdown_images/mountain_ascii_cluster_10.JPG width="35%">

## Basic Information: 
3 main steps are involved in the `JPEGColourConverter` class:
1. Given an image, a numpy array is generated (height * width * num_channels). The image is resized to fit the `max_size` tuple (max_height, max_width). Simply put, the resized image will have dimensions smaller than or equal to the dimensions specified in the `max_size` tuple. The resize ratio is set to min(original_height/max_height, original_width/max_width). 
2. The colour channels are extracted for each pixel in the resized_image. Then, the script iterates through each row in the resized_image array and generates HTML syntax, associating each pixel with its colour. This is achieved through the `yattag` module. 
3. The HTML syntax is then saved to a HTML file. The `open_html_file()` function can also be invoked to automatically open the saved HTML file. This uses the `webbrowser` module. In the script, the preferred web browser is Google Chrome. 

2 main steps is involved in the `JPEGClusterColourConverter` class:
1. Perform KMeans Clustering on the given image with `num_clusters` clusters. 
2. The __init__() method calls on the newly-defined `image_segmentation()` method, so the API for the `JPEGClusterColourConverter` class is the same as `JPEGColourConverter` (i.e. `convert_to_colour_html()`, `save_html_file()`, `open_html_file()`)

## Instructions for Use:
1. Create a directory containing all the images you wish to convert to ASCII. Set the parameter `input_dir` to this directory. 
    - The script may work on image files that are not JPEG files as well. This feature has yet to be fully tested.
2. Set `output_dir` to the directory you wish to save all generated HTML files. Set `output_dir_cluster` to the directory you wish to save all generated HTML files that have clustering enabled.
3. Set the parameters:
    - `line_height` (Height occupied by each row of HTML text)
    - `font_size` (factor by which image will be stretched horizontally. This is necessary because ASCII characters are taller than they are wide, causing the generated ASCII art to be elongated vertically. `h_stretch` compensates for this. However, it must be noted that these numbers must be changed when different symbols are used.)
    - `symbol` (The ASCII character that will be used when displaying the HTML file)
    - `max_size` (maximum size of the image. This is a tuple (max_width, max_height). Any image will be resized to fit this constraint. Increasing this is a good way to ensure density and contrast in the ASCII art.)
    - `web_browser` (The web browser application that will be used to open the saved HTML file upon invoking the `open_html_file()` function. If set to None, which is the default value, the default web browser of the user's computer will be used. Otherwise, a path to desired web browser application must be provided. See the default script to examine an instance of the web browser being set to Google Chrome.)
    - `background_colour` (Background colour of the HTML page. Set this to 'black' for the best colour contrast.)
4. NOTE: After creating an instance of the JPEGColourConverter class, first call `convert_to_colour_html()` before calling `save_html_file()` to save a HTML file. You can also call `open_html_file()` to automatically open the saved HTML file in your web browser. Finally, there is also a convenience function `convert_save_open()` that takes a parameter `open`. The parameter `open` is set to False by default, and if set to True, will open each saved HTML file in a web browser. The convenience function `convert_save_open()` is wrapped with the `animate()` decorator found in utils.py. It will show a loading animation as the file is processed. 

