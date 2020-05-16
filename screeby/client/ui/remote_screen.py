import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from types import SimpleNamespace
from tkinter import Frame, Tk, Canvas
from threading import Thread
from queue import Queue


class RemoteScreen:
    def __init__(self, window_title, video_source, width, height, play=True):
        if play:
            self.vid = Video(video_source)
        else:
            self.vid = None
        self.window = Tk()
        self.window.title(window_title)
        self.window.wm_minsize(width, height)
        self.frame = Frame(self.window)
        self.frame.pack(fill="both", expand=True)
        self._mouse_move_callback = None
        self._mouse_click_callback = None
        self._mouse_release_callback = None
        self.canvas = Canvas(self.frame, width=width, height=height, cnf={'background': 'gray20'})
        self.canvas.pack()
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind('<ButtonRelease-1>', self.release)
        self.canvas.bind('<Button-3>', self.click)
        self.canvas.bind('<ButtonRelease-3>', self.release)
        self.delay = 15
        if self.vid: self.update()

    def update(self):
        frame = self.vid.get_frame()
        if frame is None: return

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def motion(self, event):
        x, y = event.x, event.y
        ev = SimpleNamespace()
        ev.x = x
        ev.y = y
        if self._mouse_move_callback: self._mouse_move_callback(ev)

    def click(self, event):
        ev = SimpleNamespace()
        ev.name = 'left' if event.num == 1 else 'right'
        ev.press = 'true'
        if self._mouse_click_callback: self._mouse_click_callback(ev)

    def release(self, event):
        ev = SimpleNamespace()
        ev.name = 'left' if event.num == 1 else 'right'
        ev.press = 'false'
        if self._mouse_release_callback: self._mouse_release_callback(ev)

    def on_mouse_move(self, callback):
        self._mouse_move_callback = callback

    def on_mouse_click(self, callback):
        self._mouse_click_callback = callback

    def on_mouse_release(self, callback):
        self._mouse_release_callback = callback

    def wait_until_closed(self):
        self.window.mainloop()


class Video:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.buffer = Queue(maxsize=1024)
        self.stopped = False
        t = Thread(target=self.update_buffer, args=())
        t.daemon = True
        t.start()

    def update_buffer(self):
        if not self.vid.isOpened(): return

        while True:
            if self.stopped:
                return
            if not self.buffer.full():
                (grabbed, frame) = ret, frame = self.vid.read()
                if not grabbed:
                    self.stop()
                    return
                self.buffer.put(frame)

    def stop(self):
        self.stopped = True

    def get_frame(self, scale_factor=None):
        if self.buffer.qsize() == 0: return None

        frame = self.buffer.get()
        if scale_factor: frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
