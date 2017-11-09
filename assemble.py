import os, random
from PIL import Image

def assemble(size=640, dimensions=(6,6), folder="./img", seed=None):
    if seed:
        random.seed(seed)
    poster = Image.new("RGB", (dimensions[0]*size, dimensions[1]*size))
    contents = os.listdir(folder)
    random.shuffle(contents) # not a fan of how shuffle works
    for i, filename in enumerate(contents):
        img = Image.open(folder + "/" + filename)
        poster.paste(img, (i % dimensions[1] * size, i // dimensions[0] * size))
    poster.save("poster.jpg")


def resize_all(folder="./img", size=640):
    for filename in os.listdir(folder):
        img = Image.open(folder + "/" + filename)
        img = img.resize((size,size))
        img.save(folder + "/" + filename)

def calculate_size(folder="./img", size=640):
    image_count = 0
    for filename in os.listdir(folder):
        image_count += 1
    return dim(image_count)

def dim(n):
    m = n ** 0.5
    if int(m) == m:
        return (int(m), int(m))
    return (round(m), int(m)+1)
