from datetime import datetime
import base64, io

def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")
def get_b64_img(post):
    bytes_im = io.BytesIO(post.image.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image
