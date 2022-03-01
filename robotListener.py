import tkinter as tk
class KeyControl:

    def arrow(self, key):
        print(key.keycode)

    def waist(self, key):
        print(key.keycode)

    def head(self, key):
        print(key.keycode)
    

win = tk.Tk()
keys = KeyControl()

win.bind('<Up>', keys.arrow)
win.bind('<Down>', keys.arrow)
win.bind('<Left>', keys.arrow)
win.bind('<Right>', keys.arrow)
win.bind('<a>', keys.waist)
win.bind('<d>', keys.waist)
win.bind('<i>', keys.head)
win.bind('<k>', keys.head)
win.bind('<j>', keys.head)
win.bind('<l>', keys.head)
win.mainloop()
 



