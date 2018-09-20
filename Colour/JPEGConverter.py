import os
import platform
import warnings
import collections
import numpy as np
import webbrowser as wb
from yattag import Doc
from sklearn.cluster import KMeans
from skimage import io, transform, color
from utils import safe_mkdir, get_all_files, animate


class JPEGColourConverter(object):
    def __init__(self, img_path, output_dir, line_height, font_size, h_stretch = 1.5, symbol = '#', max_size = (300,300), web_browser = None, background_colour = None):
        '''
        Purpose: Converts an RGB image given in img_path to a np.array. Performs pooling on the img_array.

        Inputs: img_path [STRING]: path to image file
                max_size [TUPLE]: (max_height/rows, max_width/columns); a tuple containing the max          
                                  height/width (measured in terms of number of pixels/elements in np.array)
                output_dir [STRING]: directory in which all generated HTML files will be saved
                line_height [INT]: height of each line of HTML output (the smaller, the more detailed)
                font_size [INT]: size of HTML text in pixels (the smaller, the more detailed)
                h_stretch [FLOAT]: determines by what factor the image is stretched horizontally
                symbol [STRING]: symbol to be used for the ASCII image
                web_browser [STRING]: the path to the desired web browser application. If this is None (i.e.                                            the default value), then the open_html_file() method will simply use the OS' default                              web_browser
                background_colour [STRING]: sets the background colour of the HTML file. Must be a STRING, so only the basic HTML                             colour values are supported. You cannot input an RGB tuple here. If the default value                             of None is used, then the background_colour will be set to white. 
        '''
        #Original Image Attributes
        self.img_path = img_path
        self.img = io.imread(self.img_path)
        self.img_height_original = self.img.shape[0]
        self.img_width_original = self.img.shape[1]
        self.max_size = max_size

        #Resized Image Attributes
        self.h_stretch = h_stretch
        self.resize_ratio = min(self.max_size[0]/self.img_height_original, self.max_size[1]                                            /self.img_width_original)
        self.resized_height = int(self.resize_ratio*self.img_height_original)
        self.resized_width = int(self.resize_ratio*self.img_width_original*self.h_stretch)
        self.resized_size = (self.resized_height, self.resized_width)
        self.img = transform.resize(self.img, self.resized_size)

        #HTML Output Attributes
        self.symbol = symbol
        self.line_height = line_height
        self.font_size = font_size
        if background_colour:
            self.background_colour = background_colour
        else: self.background_colour = 'white'

        #Miscellaneous Attributes
        self.save_file_name = os.path.splitext(os.path.basename(self.img_path))[0]
        self.output_dir = output_dir
        self.full_save_file_path = os.path.join(self.output_dir, self.save_file_name)+'.html'
        self.web_browser = web_browser

        #Initialisation of yattag module
        self.doc, self.tag, self.text = Doc().tagtext()

    def convert_to_colour_html(self):
        if self.background_colour: 
            with self.tag('body', style='background-color:{}'.format(self.background_colour)):
                for i in range(self.resized_height): #Iterates through the rows
                    rgb_colour_row = []
                    row = self.img[i]
                    for j in range(self.resized_width): #Iterates through the columns
                        rgb_colour_pixel = tuple(map(int, row[j] * 255))
                        rgb_colour_row.append(rgb_colour_pixel)
                    self._write_html_line(rgb_colour_row)

    def _write_html_line(self, rgb_colour_row):
        with self.tag('text', style='white-space:PRE;line-height:{};font-size:{}px'.format(self.line_height, self.font_size)):
            for i in range(len(rgb_colour_row)):
                colour = rgb_colour_row[i]
                with self.tag('span', style='color:rgb{}'.format(colour)):
                    self.text('{}'.format(self.symbol))
        self.doc.stag('br')
    
    def save_html_file(self):
        with open(self.full_save_file_path, 'w') as f:
            f.write(self.doc.getvalue())
    
    def open_html_file(self):
        if self.web_browser:
            wb.get(using=self.web_browser).open('file://'+os.path.realpath(self.full_save_file_path))
        else:
            wb.open('file://'+os.path.realpath(self.full_save_file_path))
    
    @animate
    def convert_save_open(self, open=False):
        self.convert_to_colour_html()
        self.save_html_file()
        if open: 
            self.open_html_file()

class JPEGClusterColourConverter(JPEGColourConverter):
    def __init__(self, img_path, output_dir, line_height, font_size, h_stretch = 1.5, symbol = '#', max_size = (300,300), web_browser=None, background_colour=None, num_clusters=8):
        super().__init__(img_path, output_dir, line_height, font_size, h_stretch, symbol, max_size, web_browser, background_colour)
        self.num_clusters = num_clusters
        self.image_segmentation()

        #Update Parent Class' Miscellaneous Attributes
        self.file_name_suffix = '_n_cluster_{}'.format(num_clusters)
        self.save_file_name = self.save_file_name+self.file_name_suffix
        self.full_save_file_path = os.path.join(self.output_dir, self.save_file_name)+'.html'

    def image_segmentation(self):
        X = self.img.reshape(-1, 3)
        kmeans = KMeans(n_clusters=self.num_clusters).fit(X)
        self.img = kmeans.cluster_centers_[kmeans.labels_].reshape(self.img.shape)
    

        
if __name__ == '__main__':

    #Parameters (JPEG Colour Converter)
    input_dir = './Images'
    output_dir = './GeneratedHTML'
    line_height = 1
    font_size = 5
    h_stretch = 1.5
    symbol = '#'
    max_size = (200, 200)
    background_colour = 'black'

    #Parameters (JPEG Cluster Colour Converter)
    output_dir_cluster = './GeneratedHTML/Clusters'
    num_clusters = [5, 10, 15]

    #Path to Google Chrome Application
    chrome_path_mac = 'open -a /Applications/Google\ Chrome.app %s'
    chrome_path_windows = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    if platform.system() == 'Darwin':
        web_browser_path = chrome_path_mac
    elif platform.system() == 'Windows':
        web_browser_path = chrome_path_windows

    #Running of Main Code Body with Warning Suppression
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        safe_mkdir(output_dir)
        safe_mkdir(output_dir_cluster)

        #JPEG Colour Converter
        print('WITHOUT CLUSTERING: Converting image files to ASCII HTML files now.')
        for file_name in get_all_files(input_dir, file_ext='.jpg'):
            img_obj = JPEGColourConverter(img_path=file_name, output_dir=output_dir, line_height=line_height, font_size=font_size, h_stretch=h_stretch, symbol=symbol, max_size=max_size, web_browser=web_browser_path, background_colour=background_colour)
            img_obj.convert_save_open(open=False, loading_name=img_obj.save_file_name)
        print('Conversion completed.')

        #JPEG Cluster Colour Converter
        print('WITH CLUSTERING: Converting image files to ASCII HTML files now.')
        for num_cluster in num_clusters:
            for file_name in get_all_files(input_dir, file_ext='.jpg'):
                img_obj = JPEGClusterColourConverter(img_path=file_name, output_dir=output_dir_cluster, line_height=line_height, font_size=font_size, h_stretch=h_stretch, symbol=symbol, max_size=max_size, web_browser=web_browser_path, background_colour=background_colour, num_clusters=num_cluster)
                img_obj.convert_save_open(open=False, loading_name=img_obj.save_file_name)
        print('Conversion completed.')

            



