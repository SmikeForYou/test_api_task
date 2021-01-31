import random
import socket
import time
import os

from django.conf import settings

if __name__ == "__main__":
    postgres = settings.DATABASES["default"]
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(((os.getenv("POSTGRES_HOST")), int(os.getenv("POSTGRES_PORT"))))
                print("Successfully started postgres")
                break
        except socket.error:
            print("Waiting for postgres")
            time.sleep(0.5 + (random.randint(0, 100) / 1000))
