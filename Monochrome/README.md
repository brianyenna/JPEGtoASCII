# JPEG to ASCII Converter
Converts any JPEG image file to ASCII Art!
<img src=markdown_images/tiger.jpg width="46%">.
<img src=markdown_images/ascii_tiger.JPG width="40%">.

## Basic Information:
3 main steps are involved in the JPEGtoASCII converter:
1. Given a symbol set (i.e. a LIST of STRINGS, each of which is a 'symbol'), sort them in increasing order of intensity (the number of pixels the symbol covers on the screen)
2. Given num_buckets, generate the buckets/bins/intervals into which each B/W pixel value of the image will be placed into. Match each bucket to a symbol in the symbol set (higher-valued buckets correspond with darker/more intense symbols)
3. Given an image, convert it into a black and white image (i.e. remove the RGB channels). For each pixel, map it to a bucket and its associated symbol. Generate an array of symbols for the pixels. (array[img_height][img_width])

## Instructions for Use:
1. Create a directory containing all the images you wish to convert to ASCII. Set the parameter `image_src_dir` to this directory. 
    - The script may work on image files that are not JPEG files as well. This feature has yet to be fully tested.
2. Set `save_file_path_txt` to the directory you wish to save all generated ASCII art files (for .txt format). Likewise for `save_file_path_html`. These directories will be automatically created by the script.
3. Set the parameters:
    - `num_buckets` (number of buckets)
    - `h_stretch` (factor by which image will be stretched horizontally. This is necessary because ASCII characters are taller than they are wide, causing the generated ASCII art to be elongated vertically.   `h_stretch` compensates for this.)
    - `max_size` (maximum size of the image. This is a tuple (max_width, max_height). Any image will be resized to fit this constraint. Increasing this is a good way to ensure density and contrast in the ASCII art.)
    - `reverse` (set this to False to keep dark values dark. If this is set to False, lighter values will be inverted to become darker values. This curious toggle exists because 255 is mapped to white, but the sorted() function usually sorts the values in increasing order (intensity/darkness))
    - `symbols` (symbol set. The number of symbols available in the symbol set must be less than the number of buckets, or else an error will be raised.)
4. NOTE: After creating an instance of the JPEGtoASCII class, first call `convert_to_ascii()` before calling `save_to_file()` to create a .txt file, or call `save_as_html` to save as a .html file to display in a web browser.

## Structure of `dump.JSON` file
{<br/>
    <pre>`'original_symbol_list'`: [LIST] of [STRINGS, symbols] (corresponds to self.symbols) </pre> <br/>
    <pre>`'intensity_values_unsorted'`: [LIST] of [TUPLES, (symbol, intensity_val)] (output of _count_black_pixels()) </pre> <br/>
    <pre>`'sorted_symbols': [LIST] of` [STRINGS, symbols] (this is what self.symbols is set to) </pre> <br/>
}

## Resources Used:
I got the bit of code used to determine the number of pixels covered by each symbol in the symbol set from this site: http://alexmic.net/letter-pixel-count/. 
