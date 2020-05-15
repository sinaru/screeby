import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from types import SimpleNamespace


class RemoteScreen:
    def __init__(self, window_title, video_source):
        self.window = tkinter.Tk()
        self.window.title(window_title)
        self.vid = Video(video_source)
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self._onMouseMove = None
        self._onMouseClick = None
        self._onMouseRelease = None
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind('<Button-3>', self.click)
        self.canvas.bind('<ButtonRelease-3>', self.release)
        self.delay = 15
        self.update()

    def update(self):
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def motion(self, event):
        x, y = event.x, event.y
        ev = SimpleNamespace()
        ev.x = x
        ev.y = y
        if self._onMouseMove: self._onMouseMove(ev)

    def click(self, event):
        ev = SimpleNamespace()
        ev.name = 'left' if event.num == 1 else 'right'
        ev.press = 'true'
        if self._onMouseClick: self._onMouseClick(ev)

    def release(self, event):
        ev = SimpleNamespace()
        ev.name = 'left' if event.num == 1 else 'right'
        ev.press = 'false'
        if self._onMouseRelease: self._onMouseRelease(ev)

    def onMouseMove(self, callback):
        self._onMouseMove = callback

    def onMouseClick(self, callback):
        self._onMouseClick = callback

    def onMouseRelease(self, callback):
        self._onMouseRelease = callback

    def wait_until_closed(self):
        self.window.mainloop()


class Video:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
