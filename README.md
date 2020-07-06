# screeby
A simple screen sharing and control tool for your local network

## Requirements

- `FFmpeg` used to encode and decode remote desktop video stream. See [download instructions](https://ffmpeg.org/download.html)

### System requirements

You need following packages available in your system.
- Tkinter - Writing Tk applications with Python 3.x

For Ubuntu you can install them by running following command:
```
sudo apt install python3-pip ffmpeg python3-tk
```
### pip packages

```
pip install screeninfo pynput opencv-python Pillow
```

### Testing locally

You can test the application in your local machine with a virtual box.
A `Vagrantfile` is provided to get you started.

- First run Vagrant to setup the virtual box.
```
vagrant up
```

- In the GUI, login to vagrant with vagrant as password.

```
cd /screeby
python3 screeby/app.py
```

Now the server should start.

From your how machine you can now connect to the remote machine by connecting to port `5006` because 
in Vagrant setup we are forwarding `5006` port to `5005` of the remote machine where the server is listening to.


