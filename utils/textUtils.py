import os
import http.server
import socketserver
from dotenv import load_dotenv
from pyngrok import ngrok
from PIL import Image
from twilio.rest import Client

def make_image_square(image_path):
    """Make the image square starting from the top left corner."""
    load_dotenv()
    screenshot_file_path = os.getenv('SCREENSHOTFILEPATH')
    with Image.open(image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        square_image_path = image_path.replace(screenshot_file_path, "square_")
        new_image_path = f"{screenshot_file_path}{square_image_path}"
        width, height = img.size
        pixels = img.load() 
        map_color_range = {
            "min": (68, 138, 173),  # Minimum RGB values
            "max": (88, 158, 193)   # Maximum RGB values
        }
        start_y = height // 2
        map_start_y = height
        
        for y in range(start_y, height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]
                if map_color_range["min"][0] <= r <= map_color_range["max"][0] and map_color_range["min"][1] <= g <= map_color_range["max"][1] and map_color_range["min"][2] <= b <= map_color_range["max"][2]:
                    map_start_y = y - 200
                    print(f"Found Google Map color at ({x}, {y})")
                    break
            if map_start_y != height:
                break

        crop_height = map_start_y if map_start_y != height else height
        cropped_img = img.crop((0, 0, width, crop_height))

        square_size = max(width, crop_height)
        square_img = Image.new('RGB', (square_size, square_size), (255, 255, 255))

        x_offset = (square_size - width) // 2
        square_img.paste(cropped_img, (x_offset, 0))
        square_img.save(new_image_path)
        print(f"Image cropped and made square: {new_image_path}")
        return new_image_path

def send_twilio_with_image(title, url):
    load_dotenv()
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone = os.getenv('PHONE')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=title,
                        from_='+13602275539',
                        media_url=url,
                        to=phone
                    )

    print(f'Message {message.sid} sent to {phone} with image {url}')

def ngrok_server():
    port = 3000
    directory = os.getenv('SCREENSHOTFILEPATH')
    token = os.getenv('NGROK_TOKEN')
    subdomain = os.getenv('SUBDOMAIN')
    ngrok.set_auth_token(token)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    public_url = ngrok.connect(port, subdomain=subdomain).public_url
    print(f"ngrok tunnel {public_url} -> http://127.0.0.1:{port}")

    with socketserver.TCPServer(('127.0.0.1', port), Handler) as httpd:
        try:
            print("serving at port", port)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(" Shutting down server.")
            httpd.socket.close()

if __name__ == "__main__":
    make_image_square("/Users/donotdestroy/documents/dev/free-as-in-freedom-refactor/screenshots/Exercisebikeforparaplegics.png")
