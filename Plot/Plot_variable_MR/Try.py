__author__ = 'yueli'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#!/usr/bin/env python
#-* coding:UTF-8 -*

from tkinter import *
root = Tk()

class Flash:
  def __init__(self, root):
    self.root = root
    self.cnt = 0
    canvas = Canvas(self.root, width = 400, height = 300, bg = 'green')
    self.canvas = canvas
    self.photo = PhotoImage(file = 'tt.gif')
    self.item = canvas.create_image(100, 200, image = self.photo)

    canvas.pack()