import os, sys
from PIL import Image
from ecosia_images import crawler

size = (256, 256)

def uniform_image(file: str):
    outfile = os.path.splitext(file)[0] + "_thumbnail.jpg"
    if file != outfile:
        try:
            im = Image.open(file)
            im = im.convert('RGB')
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError as ex:
            print("cannot create thumbnail for '%s'" % file)
            print(ex)


try:
    print('Iniciando crawler')
    searcher = crawler()
    print('Buscando')
    searcher.search('chilaquiles')
    print('Descargando')
    files = searcher.download(15)
except Exception as ex:
    print(ex)
    searcher.stop()
    sys.exit(0)
else:
    print('Uniformando')
    for file in files:
        uniform_image(file)
    searcher.stop()
    print('Listo')