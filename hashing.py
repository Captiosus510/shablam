from PIL import Image
import imagehash

path1 = "C:/Users/preme/OneDrive/Documents/vscode/hacked/cat.jpg"
path2 = "C:/Users/preme/OneDrive/Documents/vscode/hacked/cat2.jpg"
path1copy = "C:/Users/preme/OneDrive/Documents/vscode/hacked/cat - Copy.jpg"
smallcat = "C:/Users/preme/OneDrive/Documents/vscode/hacked/smallcat.png"
spunchbob = "C:/Users/preme/OneDrive/Documents/vscode/hacked/spunchbob.jpg"

standard_size = (1440, 1920)

def crop_to_aspect(image, aspect_ratio=(1, 1)):
    width, height = image.size
    target_width = height * aspect_ratio[0] / aspect_ratio[1]
    if width > target_width:
        offset = (width - target_width) / 2
        image = image.crop((offset, 0, width - offset, height))
    else:
        target_height = width * aspect_ratio[1] / aspect_ratio[0]
        offset = (height - target_height) / 2
        image = image.crop((0, offset, width, height - offset))
    return image

image1 = Image.open(path1)
image2 = Image.open(path2)
image3 = Image.open(path1copy)
image4 = Image.open(smallcat)
image5 = Image.open(spunchbob)
image1resize = crop_to_aspect(image1)
image2resize = crop_to_aspect(image2)
image3resize = crop_to_aspect(image3)
image4resize = crop_to_aspect(image4)
image5resize = crop_to_aspect(image5)

hash1 = imagehash.whash(image1resize)
hash2 = imagehash.whash(image2resize)
hash1copy = imagehash.whash(image3resize)
smallhash = imagehash.whash(image4resize)
spongehash = imagehash.whash(image5resize)

hamm1_2 = hash1 - hash2
hamm1_copy = hash1 - hash1copy
hamm1_small = hash1 - smallhash
hamm1_sponge = hash1 - spongehash

print(hash1)
print(hash2)
print(hash1copy)
print(smallhash)    
print(spongehash)
print("hamm1_2:", hamm1_2)
print("hamm1_copy:", hamm1_copy)
print("hamm1_small:", hamm1_small)
print("hamm1_sponge", hamm1_sponge)

