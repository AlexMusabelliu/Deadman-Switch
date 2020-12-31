from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
import os, sys, winsound as ws, pyWinhook, win32api, threading
from win32gui import PumpMessages, PostQuitMessage, GetWindowText, GetForegroundWindow
import win32gui, win32con
from PIL import Image, ImageGrab
import autoit
from ctypes import windll, wintypes

GetWindowLong = windll.user32.GetWindowLongW
GetWindowLong.restype = wintypes.ULONG
GetWindowLong.argtpes = (wintypes.HWND, wintypes.INT)
GWL_EXSTYLE = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

def lupdate(label, im):
    data = im.tobytes("raw", "RGBA")

    label.setPixmap(QPixmap(QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)))

def _hook():
    global hm

    hm = pyWinhook.HookManager()
    hm.KeyDown = spooky._hhook
    hm.HookKeyboard()
    PumpMessages()

def hook():
    t = threading.Thread(target=_hook)
    t.start()

class Spook(QMainWindow):
    def __init__(self, parent=None):
        if parent:
            super(Spook, self).__init__(parent=parent, flags=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint | Qt.Tool)
        else:
            super(Spook, self).__init__(flags=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint | Qt.Tool)
        # def _fugg(hwnd, lParam):
        #     if "python" in win32gui.GetWindowText(hwnd).lower():
        #         hwndChild = win32gui.FindWindowEx(hwnd, None, "Qt5151QWindowIcon", None)
        #         print("python", hwnd, win32gui.GetWindowText(hwndChild))
        #         if "DEAD MAN" in win32gui.GetWindowText(hwndChild):
        #             print("dead man", hwndChild)
        #             
        # print(self.winId())
        # def set_no_focus(hwnd):
        # hwnd = win32gui.FindWindowEx(None, None, "DEAD MAN", None) 
        # pr0int(hwnd)
        # win32gui.EnumWindows(_fugg, None)
         # remove toolwindow style
        # style = style | WS_EX_NOACTIVATE | WS_EX_APPWINDOW
        # res = SetWindowLong(hwnd, GWL_EXSTYLE, style)
        # res = SetWindowPos(hwnd, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(sw, sh)
        self.setWindowTitle("DEAD MAN")
        self.enabled = False
        self.move(0, 0)
        self.ran = False
        self.wrap = False
        self.exploded = False
        self.notFading = True
        self.num = [str(x) for x in range(0, 10)]

        self.bg = QLabel()
        self.bg.setFixedSize(sw, sh)
        self.bg.setParent(self)
        # self.bg.hide()

        self.enlabeled = QLabel()
        self.enlabeled.setFixedSize(sw, sh)
        self.enlabeled.setParent(self)
        self.enlabeled.hide()

        # fim = Image.open("images/face.png").resize(sw, sh)
        self.face = QLabel()
        self.face.setFixedSize(sw, sh)
        self.face.setParent(self)
        self.face.hide()

        self.mouth = QLabel()
        self.mouth.setFixedSize(sw, sh)
        self.mouth.setParent(self)
        self.mouth.hide()

        self.password = "2544"
        self.correct = 0
        # lupdate(self.face, fim)

        # self.fancy()

        self.check_msg()
        # hwnd = win32gui.FindWindow(None, "DEAD MAN")
        # self.enable()

    def fancy(self):
        def _show_mouth(right, left, amt):
            amt = round(amt)
            im = Image.new("RGBA", (sw, sh), color=(0, 0, 0, 0))
            im.paste(mous.crop((0, 0, right, sh)), (0, 0))
            im.paste(mous.crop((left, 0, sw, sh)), (left, 0))
            lupdate(self.mouth, im)
            if left > sw // 2:
                QTimer.singleShot(10, lambda: _show_mouth(right + amt, left - amt, amt * 1.2))
            else:
                _show_eyes(im, round(255/607 * sh), 5)

        def _show_eyes(im, top, amt):
            # im = Image.new("RGBA", (sw, sh), color=(0, 0, 0, 0))
            amt = round(amt)
            im.paste(eyes.crop((round(75/835 * sw), top, round(781/835 * sw), round(255/607 * sh))), (round(75/835 * sw), top))
            lupdate(self.mouth, im)
            # print(top)
            if top > 0:
                QTimer.singleShot(10, lambda: _show_eyes(im, top - amt, amt * 1.1))
            else:
                _show_white(im, sh, 20)

        def _show_white(im, top, amt):
            def _flash():
                if amt % 2 == 0:
                    lupdate(self.mouth, whiteface)
                else:
                    lupdate(self.mouth, im)
            # amt = round(amt)
            # im = Image.new("RGBA", (sw, sh), color=(0, 0, 0, 0))
            # im.paste(whiteface.crop((0, top, sw, sh)), (0, top))
            # lupdate(self.mouth, im)
            # if top > 0:
            _flash()
            if top > 0:
                QTimer.singleShot(30, lambda: _show_white(im, top - 50, amt - 1))
            else:
                cont(im)

        def cont(im):
            img = Image.new("RGBA", (sw, sh), color=(255, 0, 0, 255))
            # for _ in range(2):
            lupdate(self.bg, img)
            self.fade(self.mouth, im, 1, 0)
            autoit.win_activate("DEAD MAN")
            # lupdate(self.bg, img)
            
            # QTimer.singleShot(1000, lambda: )

        self.mouth.show()
        ws.PlaySound("audio/laugh.wav", ws.SND_ASYNC)
        mous = Image.open("images/mouth.png").convert("RGBA").resize((sw, sh))
        eyes = Image.open("images/eyesnose.png").convert("RGBA").resize((sw, sh))
        whiteface = Image.open("images/face2.png").convert("RGBA").resize((sw, sh))
        _show_mouth(0, sw, 20)
        
    def end(self):
        im = Image.new("RGBA", (sw, sh), color=(255, 0, 0, 255))
        self.fade(self.bg, im, 1, 0)
        self.enabled = False
        QTimer.singleShot(1000, self.check_msg)

    def explode(self):
        # print("BPOm")
        self.fancy()

    def setBomb(self):
        if GetWindowText(GetForegroundWindow()) != self.activeWindow:
            self.exploded = True
            self.explode()
            # self.enabled = False

        if self.enabled and not self.exploded:
            QTimer.singleShot(100, self.setBomb)

    def check_msg(self):
        if self.ran:
            self.ran = False
            if not self.enabled:   
                self.enable()
            else:
                self.disable()

        if self.wrap:
            self.wrap = False
            self.end()

        QTimer.singleShot(100, self.check_msg)

    def _hhook(self, event):
        # if event.ScanCode == 0x3E and self.ran:
        #     self.end()
        # print(event.Key.lower(), self.password[min(self.correct, len(self.password) - 1)], self.correct)
        if self.correct == len(self.password) - 1:
            self.correct = 0
            self.wrap = True
            return True

        if self.enabled and event.Key.lower() in self.num:
            if event.Key.lower() == self.password[self.correct]:
                self.correct += 1
            else:
                self.correct = 0

        elif self.enabled:
            self.correct = 0
            return False

        if event.ScanCode == 0x3E:
            self.ran = True

        return True

    def fade(self, label, image, start, end, func=lambda: None, speed=1):
        # if self.notFading:
        self.notFading = False
        if type(image) == str:
            im = Image.open(image).convert("RGBA")
        else:
            im = image
        r,g,b,a = im.split()
        rate = 0.1
        d = start + rate * speed * (-1 if start > end else 1)
        # print(self.enabled, self.prev)
        a = a.point(lambda x: x * d)
        nuim = Image.merge("RGBA", (r, g, b, a))
        lupdate(label, nuim)
        if (start < end and d <= end) or (start > end and d >= end):
            # self.notFading = True
            QTimer.singleShot(10, lambda: self.fade(label, image, d, end, func=func, speed=speed))
        else:
            func()

    def enable(self):
        def _end():
            self.notFading = True

        if self.notFading:
            self.enabled = True
            self.enlabeled.show()
            self.fade(self.enlabeled, "images/enabled.png", 0, 1)
            QTimer.singleShot(800, lambda: self.fade(self.enlabeled, "images/enabled.png", 1, 0, func=_end))

            self.activeWindow = GetWindowText(GetForegroundWindow())
            self.setBomb()

    def disable(self):
        def _end():
            self.notFading = True

        if self.notFading:
            self.enabled = False
            self.enlabeled.show()
            self.fade(self.enlabeled, "images/disabled.png", 0, 1)
            QTimer.singleShot(800, lambda: self.fade(self.enlabeled, "images/disabled.png", 1, 0, func=_end))

os.chdir(os.path.abspath(os.path.dirname(__file__)))
app = QApplication()

w = QWidget()

sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
spooky = Spook(parent=w)
spooky.show()
hook()

app.exec_()