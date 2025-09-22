import oom_markdown
import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import copy

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    file_input = kwargs.get('file_input', '')
    directory_output = kwargs.get('directory_output', 'image_tiled')
    directory_single = kwargs.get('directory_single', '')
    directory_iterate = kwargs.get('directory_iterate', 'parts')
    width = kwargs.get('width', 600)
    height = kwargs.get('height', 400)
    width_tile = kwargs.get('width_tile', 100)
    height_tile = kwargs.get('height_tile', 150)
    load_working_yaml = kwargs.get('load_working_yaml', False)
    
    jobs = []

    job_default = {}
    job_default['width'] = width
    job_default['height'] = height
    job_default['width_tile'] = width_tile
    job_default['height_tile'] = height_tile

    if file_input != '':        
        file_image_source = file_input
        job = copy.deepcopy(job_default)
        job['file_image_source'] = file_image_source        
        #is directory_of image plus directory_output
        directory_image = os.path.dirname(file_image_source)
        directory_output_local = f"{directory_image}/{directory_output}"
        job["directory_output"] = directory_output_local
        jobs.append(job)
    elif directory_single != '':
        file_image_source = f'{directory_single}/image.jpg'
        job = copy.deepcopy(job_default)
        job['file_image_source'] = file_image_source
        #is directory_single plus directory_output
        directory_image = os.path.dirname(file_image_source)
        directory_output_local = f"{directory_image}/{directory_output}"
        job["directory_output"] = directory_output_local
        if load_working_yaml:
            yaml_file = f'{directory_single}/working.yaml'
            if os.path.exists(yaml_file):
                import yaml
                with open(yaml_file, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                #add directory for some keys
                keys = ["file_input", "file_image_source"]
                for key in keys:
                    if key in yaml_data:
                        yaml_data[key] = f'{directory_iterate}/{directory}/{yaml_data[key]}'
                job.update(yaml_data)
        jobs.append(job)
    elif directory_iterate != '':
        directories = os.listdir(directory_iterate)
        for directory in directories:
            if os.path.isdir(f'{directory_iterate}/{directory}'):
                file_image_source = f'{directory_iterate}/{directory}/image.jpg'
                job = copy.deepcopy(job_default)
                job['file_image_source'] = file_image_source
                job["directory_output"] = f'{directory_iterate}/{directory}/{directory_output}'
                if load_working_yaml:
                    yaml_file = f'{directory_iterate}/{directory}/working.yaml'
                    if os.path.exists(yaml_file):
                        import yaml
                        with open(yaml_file, 'r') as f:
                            yaml_data = yaml.safe_load(f)
                        #add directory for some keys
                        keys = ["file_input", "file_image_source"]
                        for key in keys:
                            if key in yaml_data:
                                yaml_data[key] = f'{directory_iterate}/{directory}/{yaml_data[key]}'
                        job.update(yaml_data)
                jobs.append(job)
    #project_name is the name of the input file no directory or extension, and the one previous directory
    
    for job in jobs:
        deets = {}
        deets.update(job)
        run_job(**deets)

    project_name = file_image_source.replace("source_files/","").replace('/', '_').replace('\\', '_').replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('.bmp', '')
    
    



def run_job(**kwargs):
    output_directory = kwargs.get('directory_output', 'image_tiled')
    width = kwargs.get('width', 600)
    height = kwargs.get('height', 400)

    file_image_source = kwargs.get('file_image_source', '')
    
    #1200 dpi
    #pixels_per_inches = 1200
    pixels_per_inches = 1800
    #pixels_per_inches = 72
    pixels_per_mm = pixels_per_inches / 25.4
    #pixels_per_mm = 1
    width_pixel = int(width * pixels_per_mm)
    height_pixel = int(height * pixels_per_mm)
    ratio = width/height

    width_tile = kwargs.get('width_tile', 100)
    height_tile = kwargs.get('height_tile', 150)
    width_tile_pixel = int(width_tile * pixels_per_mm)
    height_tile_pixel = int(height_tile * pixels_per_mm)
    #overlap_target = 0.1
    overlap_target = 0.05

    
    
    width_calc = width_pixel
    width_number_of_tiles = (width_calc // (width_tile_pixel * (1-overlap_target))) + 1
    height_calc = height_pixel
    height_number_of_tiles = (height_calc // (height_tile_pixel * (1-overlap_target))) + 1    
    print(f'width_number_of_tiles_target: {width_number_of_tiles}')
    print(f'height_number_of_tiles_target: {height_number_of_tiles}')
    print(f"total number of tiles_target: {width_number_of_tiles * height_number_of_tiles}")

    
    #calculating for width
    width_minimum_tiles = (width_pixel * 1+overlap_target) // width_tile_pixel + 1
    width_pixels_available = width_minimum_tiles * width_tile_pixel
    width_pixels_needed = width_pixel    
    width_extra_pixels = width_pixels_available - width_pixels_needed
    if width_minimum_tiles <= 1:
        width_extra_pixels_per_tile = 0
    else:
        width_extra_pixels_per_tile = width_extra_pixels / (width_minimum_tiles-1)
    width_extra_ratio = width_extra_pixels_per_tile / width_tile_pixel
    overlap_width = width_extra_ratio
    
    #calculating for height
    height_minimum_tiles = (height_pixel * 1+overlap_target) // height_tile_pixel + 1
    height_pixels_available = height_minimum_tiles * height_tile_pixel
    height_pixels_needed = height_pixel
    height_extra_pixels = height_pixels_available - height_pixels_needed
    if height_minimum_tiles <= 1:
        height_extra_pixels_per_tile = 0
    else:
        height_extra_pixels_per_tile = height_extra_pixels / (height_minimum_tiles-1)
    height_extra_ratio = height_extra_pixels_per_tile / height_tile_pixel
    overlap_height = height_extra_ratio
    

    width_number_of_tiles = width_minimum_tiles
    height_number_of_tiles = height_minimum_tiles
    print(f'width_number_of_tiles: {width_number_of_tiles}')
    print(f'height_number_of_tiles: {height_number_of_tiles}')
    print(f"total number of tiles: {width_number_of_tiles * height_number_of_tiles}")
    print(f'overlap_width: {overlap_width}')
    print(f'overlap_height: {overlap_height}')
    pass

    

    pass

    #load in the image    
    #check if image file exists
    
    #load image
    img = ""
    if True:
        print(f'loading image: {file_image_source}')
        img = Image.open(file_image_source)
        ratio_image = img.width / img.height

    #clip image to right ratio
    if True:
        if ratio_image > ratio:
            img = img.crop((0, 0, img.height * ratio, img.height))
        else:
            img = img.crop((0, 0, img.width, img.width / ratio))
        ratio_image = img.width / img.height
    
    #reratio image
    if True:
        #resize use width pixel
        if ratio_image > ratio:
            img = img.resize((width_pixel, int(width_pixel / ratio_image)))
        else:
            img = img.resize((int(height_pixel * ratio_image), height_pixel))
        #save the source image
        file_output_name = f'{output_directory}/source.png'
        file_source_name = file_output_name
        print(f'saving source image: {file_output_name}')
        #if directory does not exist create it
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)        
        try:
            img.save(file_output_name)
        except:
            print(f'error saving source image: {file_output_name}')
        print(f'ratio_image: {ratio_image}')

    #create the tiles remember the overlap, offset every other row by half a width
    tiles = []
    
    for row in range(int(height_number_of_tiles)):
        for col in range(int(width_number_of_tiles)):
            x = col * width_tile_pixel * (1 - overlap_width)
            y = row * height_tile_pixel * (1 - overlap_height)
            if row % 2 == 1 and width_number_of_tiles > 1:
                x += -width_tile_pixel / 2
            tile = {}
            tile['x_pixel'] = x
            tile['y_pixel'] = y
            tile['column']= col + 1
            tile['row']= row + 1            
            tiles.append(tile)
            #add extra tile for the even rows            
            if width_number_of_tiles > 1:
                if row % 2 == 1 and col == width_number_of_tiles - 1:
                    x = (col + 1) * width_tile_pixel * (1 - overlap_width)
                    y = row * height_tile_pixel * (1 - overlap_height)
                    tile = {}
                    tile['x_pixel'] = x - width_tile_pixel / 2
                    tile['y_pixel'] = y
                    tile['column']= col + 1 + 1
                    tile['row']= row + 1
                    #if row is odd and column doesn't qual 1 then add the tile                
                    tiles.append(tile)
                
                


    #create the tiles in output directory
    if True:
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        for tile in tiles:
            #tile = tiles[tile_id]
            #if tile is a dict
            if not isinstance(tile, dict):
                x = tile[0]
                y = tile[1]
                row = tile[2]
                column = tile[3]
                img_tile_1 = img.crop((x, y, x + width_tile_pixel, y + height_tile_pixel))
            else:
                x = tile['x_pixel']
                y = tile['y_pixel']
                row = tile['row']
                column = tile['column']            
                img_tile = img.crop((x, y, x + width_tile_pixel, y + height_tile_pixel))
            file_output_name = f'{output_directory}/tile_row_{row}_column_{column}.png'
            print(f'saving tile: {file_output_name}')
            #add notes to the image
            if True:
                if row != 1:
                    draw = ImageDraw.Draw(img_tile)
                    font_size = height_tile_pixel // 50
                    #make it bold
                    font = ImageFont.truetype("arialbd.ttf", font_size)
                    shift_corner  = 750
                    draw.text((shift_corner, shift_corner), f'{row},{column}', fill='white', font=font)
                    draw.text((shift_corner, shift_corner-150), f'{row},{column}', fill='black', font=font)

                    #add a line 10 pixels above the divide line
                    height = height_tile_pixel * overlap_height
                    height = height - 400
                    height_line = height
                    draw.line((0, height, width_tile_pixel, height), fill='white', width=20)

                    #add a vertical line from the top to height one 500 in one in the middle and one 500 from the far side
                    overlap_width_pixel = width_tile_pixel * overlap_width
                    x_coors = []
                    #add middle
                    x_coors.append(width_tile_pixel / 2)
                    #add 500 from the left
                    x_coors.append(500)                    
                    x_coors.append(width_tile_pixel - 500)
                    #add overlap pixels
                    x_coors.append(overlap_width_pixel)
                    x_coors.append(width_tile_pixel - overlap_width_pixel)
                    #add overlap pixels inside 200
                    shift = 500
                    x_coors.append(overlap_width_pixel - shift)
                    x_coors.append(width_tile_pixel - overlap_width_pixel + shift)
                    for x_coor in x_coors:
                        draw.line((x_coor, 0, x_coor, height_line), fill='white', width=20)
                    

            

            img_tile.save(file_output_name)

    #create overlay on the image
    

    # create overlay on the image
    if True:
        print(f'creating overlay')
        # load source image
        Image.MAX_IMAGE_PIXELS = None
        img = Image.open(file_source_name)
        #resize to 1200 pixels wide maintaining aspect ratio use seevral lines
        
        draw = ImageDraw.Draw(img)
        # create overlay
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'brown']
        count = 0
        for tile in tiles:
            
            x = tile['x_pixel']
            y = tile['y_pixel']
            row = tile['row']
            column = tile['column']
            # draw rectangle
            color = colors[count % len(colors)]
            draw.rectangle([x, y, x + width_tile_pixel, y + height_tile_pixel], outline=color, width=100)
            # draw text 100 pixels tall     
            font = ImageFont.truetype("arial.ttf", 500)       
            
            shift_corner  = 300
            draw.text((x+shift_corner, y+shift_corner), f'row: {row} column: {column}', fill=color, font=font)
            count += 1
        # save the image
        img = img.resize((1200, int(1200 / ratio_image)))                
        file_output_name = f'{output_directory}/overlay.png'
        img.save(file_output_name)

if __name__ == '__main__':
    # parse arguments
    argparser = argparse.ArgumentParser(description='project description')
    #--file_input -fi
    argparser.add_argument('--file_source', '-fs', type=str, default='', help='file_source')   
    ##directory output -do
    argparser.add_argument('--directory_output', '-do', type=str, default='image_tiled', help='directory_output')
    #directory_single -ds
    argparser.add_argument('--directory_single', '-ds', type=str, default='', help='directory_single')
    #directory_iterate -di
    argparser.add_argument('--directory_iterate', '-di', type=str, default='parts', help='directory_iterate')
    #--width -w
    argparser.add_argument('--width', '-wid', type=int, default=600, help='width in mm')
    #--height -ht
    argparser.add_argument('--height', '-hei', type=int, default=400, help='height in mm')
    #--width_tile -wt 100
    argparser.add_argument('--width_tile', '-wt', type=int, default=100, help='width_tile in mm')
    #--height_tile -ht 150
    argparser.add_argument('--height_tile', '-ht', type=int, default=150, help='height_tile in mm')
    # loading_working_yaml -lwy boolean
    argparser.add_argument('--loading_working_yaml', '-lwy', type=bool, default=False, help='loading_working_yaml')

    args = argparser.parse_args()
    kwargs = {}
    # update kwargs with args
    kwargs.update(vars(args))

    
    
    
    
    main(**kwargs)