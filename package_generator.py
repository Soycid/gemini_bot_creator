import os
import shutil
import tempfile
import sys

def get_qr_from_config():
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        destination = shutil.copytree(os.getcwd(),os.path.join(tmpdirname,"dog"))
        print(destination)
        uploader = os.path.join(destination,"uploader.py")
        exec(open(uploader).read())
        qr = os.path.join(destination,"qr.png")
        shutil.copyfile(qr,"./qr.png")

