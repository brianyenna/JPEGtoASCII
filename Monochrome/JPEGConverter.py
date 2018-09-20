from PIL import Image, ImageFont, ImageDraw
import numpy as np
import string
import os
import json
from utils import safe_mkdir, get_all_files
from yattag import Doc


class Buckets(object):
    def __init__(self, num_buckets, symbols=None, reverse=False):
        '''
        Purpose: Creates the buckets and sorts the symbol set.
        Inputs: num_buckets [INT]: number of buckets
                symbols [LIST] of [STRINGS]: symbol set
                reverse [BOOLEAN]: if False, inverts the colour scheme. Defaults to False
        '''
        self.num_buckets = num_buckets
        self.min_value = 0
        self.max_value = 255
        self.reverse = reverse

        #Set of symbols to use
        if symbols==None:
            self.symbols = list(string.printable)
            self.symbols = [x for x in self.symbols if x not in ['_', '\t', '\n', '\r', '\f', '\u000b']] 
        else: 
            self.symbols = symbols
        assert self.num_buckets <= len(self.symbols), 'Number of buckets is greater than the number of characters available in the specified symbol set.'

        #Generates sorted symbol set. (new or from .JSON file)
        self.json_file_name = 'dump.JSON'
        self.json_file_path = './data/{}'.format(self.json_file_name)
        if os.path.exists('./data') and os.path.isfile(self.json_file_path):
            print('\n(BUCKET) An existing .JSON file was found. Reading in data now.')
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
            if set(self.symbols).issubset(data['original_symbol_list']):
                print('(BUCKET) Symbol set in .JSON file matches with specified symbol set.\n(BUCKET) Using saved symbol set in .JSON file')
                self.symbols = data['sorted_symbols']
            else: 
                print('(BUCKET) Symbol set in .JSON file does not match with specified symbol set.')
                print('\n(BUCKET) New symbol set being generated...')
                self.symbols = self._sort_symbols()
        else: 
            print('(BUCKET) New symbol set being generated...')
            self.symbols = self._sort_symbols()

        #Generates the starting values of each bucket
        self.buckets = np.linspace(self.min_value, self.max_value, num=self.num_buckets, endpoint=False, dtype=np.int32)
        #Generates the indices of the symbols to be used (in self.symbols)
        self.buckets_symbols_index = np.linspace(1, len(self.symbols), num=self.num_buckets, dtype=np.int32)-1 
        self.used_symbols = [self.symbols[i] for i in self.buckets_symbols_index]

    def _sort_symbols(self):
        '''
        Purpose: Sorts self.symbols in order of increasing intensity (how many pixels each symbol occupies)
                 This function also creates a .JSON file that saves the intensity values of the symbols in self.symbols, as well as the sorted list of symbols. 
        Note:The default font type used is Arial, font size = 100. There is no option to change this font type.
        Returns: sorted [LIST] of symbols
        '''
        helvetica = ImageFont.truetype('Arial.ttf', 100)
        def _draw_symbol(symbol):
            img = Image.new('RGB', (100,100), 'white')
            draw = ImageDraw.Draw(img)
            draw.text((0,0), symbol, font=helvetica, fill='#000000')
            return img
        
        def _count_black_pixels(img):
            pixels = list(img.getdata())
            return len(list(filter(lambda rgb: sum(rgb)==0, pixels)))
        
        #Creates list of sorted symbols
        symbol_store = []
        for symbol in self.symbols:
            symbol_store.append((symbol, _count_black_pixels(_draw_symbol(symbol))))
        sorted_symbols = [s[0] for s in sorted(symbol_store, key=lambda x: x[1], reverse=self.reverse)]

        #Creates and saves .JSON file
        json_dump = {'original_symbol_list': self.symbols, 
                     'intensity_values_unsorted': symbol_store, 
                     'sorted_symbols': sorted_symbols}
        safe_mkdir('./data')
        with open('./data/{}'.format(self.json_file_name), 'w') as f:
            json.dump(json_dump, f)

        return sorted_symbols
    
    def get_bucketed_symbols(self):
        return self.used_symbols
    
    def get_buckets(self):
        return self.buckets
    

class JPEGtoASCII(object):
    def __init__(self, image_path, num_buckets, save_file_name, h_stretch=1.5, save_file_path_html='.', save_file_path_txt = '.', html_line_height = 0.05, html_font_size = 1, max_size=(100, 300), symbols=None, reverse=False):
        '''
        Purpose: Converts a JPEG file provided at image_path into an ASCII text object

        Inputs: image_path [STRING]: path to JPEG file
                num_buckets [INT]: number of buckets to bin colour values of pixels in JPEG image
                save_file_path_txt [STRING]: path to directory containing the generated ASCII text files
                                         (defaults to the current directory)
                save_file_path_html [STRING]: path to directory containing the generated ASCII html files (defaults to the current directory)
                save_file_name [STRING]: name of ASCII .txt file generated
                h_stretch [FLOAT]: determines by what factor the image is stretched horizontally
                max_size [TUPLE]: (max_width, max_height) to ensure that the generated ASCII text files
                                  can fit inside the screen 
                symbols [LIST] of [STRINGS]: list containing all character symbols (symbol set)
                html_line_height [FLOAT]: sets the line_height for the html files (the smaller, the more detail)
                html_font_size [INT]: sets the font_size for the html files (the smaller, the more detail)
                reverse [BOOLEAN]: if False, inverts the colour scheme. Defaults to False.
        '''
        #Bucket Attribtues
        self.bucket_obj = Buckets(num_buckets, symbols, reverse)
        self.used_symbols = self.bucket_obj.get_bucketed_symbols()
        self.buckets = self.bucket_obj.get_buckets()

        #Image Attributes
        self.image_path = image_path
        self.img = Image.open(image_path).convert('L') #convert image to Black and White
        self.img_height = self.img.height
        self.img_width = self.img.width
        self.max_size = max_size

        #Miscellaneous Attribtues
        self.save_file_path_txt = save_file_path_txt
        self.save_file_path_html = save_file_path_html
        self.save_file_name = save_file_name
        self.html_line_height = html_line_height
        self.html_font_size = html_font_size
        self.h_stretch = h_stretch
        self.resize_ratio = min(self.max_size[0]/self.img_width, self.max_size[1]/self.img_height)
        self.resized_width = int(self.resize_ratio*self.img_width*self.h_stretch)
        self.resized_height = int(self.resize_ratio*self.img_height)
        self.resized_size = (self.resized_width, self.resized_height)
        
    def convert_to_ascii(self):
        #Converts image to appropriate size
        self.img = self.img.resize(self.resized_size, Image.BICUBIC)

        self.ascii_img = [[] for row in range(self.resized_height)] #index into ascii_img[row][column]
        pixels = list(self.img.getdata())
        # self.ascii_img = [pixels[(i*self.img_width):((i+1)*self.img_width)] for i in range(self.img_height)] #index into ascii_img[row][column]

        for index, pixel in enumerate(pixels):
            row = int(index/self.resized_width)
            bucket_index = np.digitize(pixel, self.buckets) - 1
            symbol_to_append = self.used_symbols[bucket_index]
            self.ascii_img[row].append(symbol_to_append)
    
    def print_img_to_console(self):
        for row in self.ascii_img:
            for pixel in row:
                print(pixel, end = '')
            print('\n')
    
    def save_to_file(self):
        ascii_img_str = []
        for row in self.ascii_img:
            ascii_img_str.append(''.join(row)+'\n')
        with open(os.path.join(self.save_file_path_txt, self.save_file_name+'.txt'), 'w') as f:
            for row_str in ascii_img_str:
                f.write(row_str)
    
    def save_as_html(self):
        #Initialisation of yattag module
        doc, tag, text = Doc().tagtext()

        #Parsing symbols
        for row in self.ascii_img:
            with tag('pre', color = "#000000", style='white-space:PRE;line-height:{};font-size:{}px'.format(self.html_line_height, self.html_font_size)):
                text(''.join(row))
        with open(os.path.join(self.save_file_path_html, self.save_file_name+'.html'), 'w') as f:
            f.write(doc.getvalue())
        


    

################################
########EXECUTE THE CODE########
################################
if __name__ == '__main__':

    #Set parameters
    num_buckets = 80
    h_stretch = 1.5
    max_size = (300,600)
    reverse = True
    symbols = None
    html_line_height = 0.2
    html_font_size = 5

    #Set directories
    save_file_path = './GeneratedASCII'
    save_file_path_txt = './GeneratedASCII/txt'
    save_file_path_html = './GeneratedASCII/html'
    image_src_dir = './Images'
    
    #Get ASCII text files
    safe_mkdir(save_file_path)
    safe_mkdir(save_file_path_txt)
    safe_mkdir(save_file_path_html)
    for image_path in get_all_files(image_src_dir, file_ext='.jpg'):
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        image = JPEGtoASCII(image_path=image_path, 
                            num_buckets=num_buckets, 
                            save_file_name=file_name, 
                            h_stretch=h_stretch, 
                            save_file_path_html=save_file_path_html,
                            save_file_path_txt=save_file_path_txt, 
                            html_font_size=html_font_size,
                            html_line_height=html_line_height,
                            max_size=max_size, 
                            symbols=symbols, 
                            reverse=reverse)
        image.convert_to_ascii()
        image.save_to_file()
        image.save_as_html()


    #Unicode symbols
    # whitespace_int = [9, 10, 11, 12, 13, 32, 33, 160, 5760, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201, 8202, 8232, 8233, 8239, 8287, 12288]
    # symbols = [chr(i) for i in range(500) if i not in whitespace_int]

        
    