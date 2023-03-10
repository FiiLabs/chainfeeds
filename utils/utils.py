import base64

def base64_encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def base64_decode(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')

def remove_prefix(text, prefix):
    if text.find(prefix) > 0:
        return text[:text.index(prefix)]
    return text  # or whatever