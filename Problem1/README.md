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