import wget
import re
import pytesseract as tess
from PIL import Image as img

def check_if_tweet_is_ok (tweet):
    pattern = '(.*coin\s*of\s*the\s*week[:;,\s](.*))'
    p = re.compile(pattern, re.IGNORECASE)
    m = p.match(tweet)
    if m:
        return m.group(2)
    return None

def get_media_url(json_obj):
    if 'entities' in json_obj:
        entity = json_obj["entities"]
        if 'media' in entity:
            media_obj = entity['media'][0];
            if 'media_url_https' in media_obj:
                return media_obj['media_url_https']
    return None

def download_media(url):
    file = wget.download(url, out='./img/')
    return img.open(file)

def make_ocr(file):
    print(str(file))
    text = tess.image_to_string(file)
    return text

def get_symbol(content):
    pattern = '(.*[(+]([A-Z]*))'
    p = re.compile(pattern)
    m = p.match(content)
    if m:
        return m.group(2)
    return None
