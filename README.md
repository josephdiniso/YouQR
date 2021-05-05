# QR Based Embedded YouTube URL
#### By *Walter Newsome* and *Joseph DiNiso* <br>
### How to Install: <br>
`pip3 install -r requirements.txt`

### How to create a label: <br>
To create a label, call 
`python3 create_label.py EMBEDDED_URL` <br> <br>
Where `EMBEDDED_URL` is an embedded YouTube URL code. For example, calling <br>
`python3 create_label.py 8AHCfZTRGiI` <br>
will create a QR code URL for the song 'Hurt'.

To find the code for an embedded YouTube URL, click the **SHARE** button as seen here, and then <br>
copy all characters after **youtu.be/** <br>
![](./images/share_button.png) <br>
### How to detect a label: <br>
To detect a label, call `python3 detect_label.py` and a webcam view should open up, hold a <br>
generated QR image to the webcam. The webcam will automatically detect the code and try to <br>
parse the stored data in the code. When correctly parsed, the program will automatically <br>
open the video in your default browser.

