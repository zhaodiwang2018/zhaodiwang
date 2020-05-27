import base64
import time, random
from zhaodi.settings import MEDIA_URL


# from apps.land.models import *
def Parsing(imgbase, suffix):
    img = imgbase.split(',')
    # print(img)
    imgdata = base64.b64decode(img[1])
    timestamp = str(int(time.time())) + str(random.randint(0, 99))
    file_url = MEDIA_URL + '%s.%s' % (timestamp, suffix)
    # print(file_url)
    file = open(file_url, 'wb')
    file.write(imgdata)
    file.close()
    return timestamp + '.' + suffix
