# =====================================================================================================================================
# AUTHOR:   Mitch Alves (idp7116)
# DATE:     2021-03-12
# DESC:     IMG TO ASCII
# =====================================================================================================================================


import PIL.Image


ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
print(ASCII_CHARS)
ASCII_CHARS = ASCII_CHARS[::-1]
print(ASCII_CHARS)


def resize(image, width=100):
    img_width, img_height = image.size
    ratio = img_height / img_width
    height = int(width * ratio)
    resized_image = image.resize((width, height))
    return resized_image

def main():
    path = 'hca.png'
    try:
        image = PIL.Image.open(path)
    except:
        print(path, ' , image not found.')

main()