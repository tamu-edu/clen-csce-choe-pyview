#!/usr/bin/env python
##############################################################################
# Copyright (c) 2012 Hajime Nakagami<nakagami@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# A image viewer. Require Pillow ( https://pypi.python.org/pypi/Pillow/ ).
#
# Modified by Yoonsuck Choe
# - takes list of files through command line argument
# - navigate via key binding, not buttons
##############################################################################
import PIL.Image
import sys
import glob

try:
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog
import PIL.ImageTk

class App(Frame):
    def chg_image(self,img):

        scr_w = self.master.winfo_screenwidth()
        scr_h = self.master.winfo_screenheight()
        img_w, img_h = img.size
        scale_w = scr_w/img_w
        scale_h = scr_h/img_h
        scale = min(scale_w,scale_h)
        img = img.resize((int(scale*img_w), int(scale*img_h)))

        if img.mode == "1": # bitmap image
            self.img = PIL.ImageTk.BitmapImage(img, foreground="white")
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(img)

        self.la.config(image=self.img, bg="#000000",
            width=self.img.width(), height=self.img.height())

    def show_image(self,idx):
         image_path = self.flist[idx]
         #print("Displaying {}".format(image_path), flush=True)
         self.master.title("pyview.py [{}/{}]: {}".format(self.num_page,self.flist_size,image_path))
         pil_image = PIL.Image.open(image_path)
         self.chg_image(pil_image)
         self.master.update()
         self.master.update_idletasks()

    def open(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.im = PIL.Image.open(filename)
        self.chg_image()
        self.num_page=0
        self.num_page_tv.set(str(self.num_page+1))

    def toggle_fullscreen(self, event=None):
        if self.fullscreen_flag == False:
          self.fullscreen_flag = True
          self.master.attributes('-fullscreen',True)
        else:
          self.fullscreen_flag = False
          self.master.attributes('-fullscreen',False)

    def seek_prev(self, event=None):
        self.num_page=(self.num_page-1)%self.flist_size
        self.show_image(self.num_page)
        #self.num_page_tv.set(str(self.num_page+1))

    def seek_next(self, event=None):
        self.num_page=(self.num_page+1)%self.flist_size
        self.show_image(self.num_page)
        #self.num_page_tv.set(str(self.num_page+1))

    def __init__(self, argv, master=None):
        Frame.__init__(self, master)
        self.master.title('Image Viewer')

        self.num_page=0
        self.num_page_tv = StringVar()

        self.fullscreen_flag = False

        # yschoe: get filelist
        self.flist = glob.glob(argv[1],recursive=True)
        self.flist_size = len(self.flist)
        print('pyview.py: Displaying {}: {} files'.format(argv[1],self.flist_size),flush=True)

        fram = Frame(self)
        # yschoe: use keybinding for navigation
        self.master.bind('<Escape>',quit)
        self.master.bind('<Left>',self.seek_prev)
        self.master.bind('<Right>',self.seek_next)
        self.master.bind('<f>',self.toggle_fullscreen)
        Label(fram, textvariable=self.num_page_tv).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        # this is the canvas
        self.la = Label(self)
        self.la.pack()

        self.pack()
        self.show_image(0)

if __name__ == "__main__":
    app = App(argv=sys.argv); app.mainloop()
