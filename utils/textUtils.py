import os
from dotenv import load_dotenv
from pyngrok import ngrok
import http.server
import socketserver
from twilio.rest import Client

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

    print(message.sid)

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


