# Problem 1

## Description

There are 1,00,000 images. We need to find the width and height of each image. Depending on the dimensions we would need to resize it down to 600 x 480. We have a machine which has 4gb Ram and 2 core vcpu. What is the fastest way to go through the 1L images?

## Solution 

To process 100,000 images and resize them to 600 x 480 dimensions, the most efficient approach would be to use a parallel processing technique to utilize the available CPU cores to process images in parallel. Here's one way to do it in Python:

## Requirements

```
pip install -r requirements.txt
```

## Usage

```
python resize_image.py
```

## Breif explaination about solution

In this code, we define a function resize_image that takes a filename as input, opens the image with PIL, calculates the new dimensions while maintaining aspect ratio, resizes the image, and saves it back to the same file. Then we use os.listdir to get a list of all filenames in the directory, filter it to only include JPEG files, and construct a list of full pathnames. Finally, we use ThreadPoolExecutor to process the resize_image function in parallel using the available CPU cores.

The max_workers argument of ThreadPoolExecutor is set to 2, which means that up to 2 threads can run in parallel. You can adjust this value based on the available CPU resources and the performance you observe.

## Estimation

The time required to resize 100,000 images using the above approach will depend on several factors, such as the size of the images, the available CPU resources, and the number of threads used for parallel processing.

Assuming that the images are not too large (let's say around 1-2 MB each), and the available CPU resources are as specified (4GB RAM and 2 vCPUs), and the code is executed on a machine that is not under heavy load, we can estimate the time required as follows:

On average, it may take around 1-2 seconds to resize one image. With two CPU cores available, we can run two threads in parallel, which means we can process two images at a time. Therefore, it will take around 50,000-100,000 seconds to resize all 100,000 images. So, the total time required can be estimated to be around 13.8-27.7 hours, assuming that there are no other bottlenecks and the CPU resources are fully utilized. However, this is just an estimate, and the actual time required may vary depending on several factors.