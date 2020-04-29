import PIL
from PIL import Image


basewidth = 170
baseheight = 300

img = Image.open('dune.jpg')

hpercent = (baseheight / float(img.size[1]))
wsize = int((float(img.size[0]) * float(hpercent)))

wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))

img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
img.save('resized_image.jpg')
