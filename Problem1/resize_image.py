import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor


def resize_image(filename):
    '''
        Summary: Resize the image to 600 width and height 480.
        Args:
            filename str: Image file name.
        
    '''
    with Image.open(filename) as img:
        # Get the original dimensions
        width, height = img.size
        # If the image is already in the target size, do nothing
        if width == 600 and height == 480:
            return
        # Calculate the new dimensions while maintaining aspect ratio
        aspect_ratio = width / height
        if aspect_ratio > 1.25:
            new_width = 600
            new_height = round(600 / aspect_ratio)
        else:
            new_height = 480
            new_width = round(480 * aspect_ratio)
        # Resize the image and save it with the same filename
        img.resize((new_width, new_height)).save(filename)


if __name__ == '__main__':
    # Get a list of all image filenames in the directory
    directory = os.getcwd()
    path = directory.replace(os.sep, '/') 
    image_dir = path + '/images'
    filenames = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith('.jpg')]
    # Use ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(resize_image, filenames)
