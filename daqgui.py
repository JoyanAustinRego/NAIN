from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkSimpleDialog import *
from tkMessageBox import *
import daqdb
import datetime
import threading
import daqread
from PIL import Image, ImageTk
import matplotlib
import matplotlib.pyplot as plt
from createtable import *
matplotlib.use("TkAgg")


def homeCallback():
    window1.withdraw()
    top.deiconify()


def profileCallback():
    global name, age, cdate, ctime
    #ledblinkkkkkkkkkkk.red()
    name = askstring('BP monitoring system', 'Enter name:')
    age = askinteger('BP monitoring system', 'Enter age:')
    currentDT = datetime.datetime.now()
    cdate = currentDT.strftime("%d-%m-%Y")
    ctime = currentDT.strftime("%H:%M:%S")


def startCallback():
    threading.Thread(target=daqread.main())



def tabulateCallback():
    """global bpval
    daqread._pause()
    bpval = daqread.returnvalue()"""
    top.withdraw()
    window1.deiconify()
    list1 = window1.grid_slaves()
    for l in list1:
        l.destroy()
    home = Button(window1, text='Home', fg='blue', bg='red', command=homeCallback)
    # canvas1.create_window(235, 200, window=home)
    home.grid(row=0, column=1)
    view = Button(window1, text='View', fg='red', bg='blue', command=viewcallback)
    view.grid(row=0, column=2)


def saveCallback():
    daqdb.fwrite(cdate, ctime, name, age, bpval)
    daqdb.dbinit()
    daqdb.createTable()
    daqdb.entries(cdate, ctime, name, age, bpval)


def displayVal():
    global bpval
    bpval = daqread.sendval()
    showinfo('BP monitoring system', 'BP value in mmHg:%f' % (bpval))
    daqread.peak()


def exitCallback():
    #ledblinkkkkkkkkkkk.offyellow()
    #ledblinkkkkkkkkkkk.offred()
    #stopCallback()
    plt.close()
    top.destroy()


def viewcallback():
    f = open('timelog.csv')
    newtable = createstandardtable(f, window1)
    newtable.grid()
    f.close()

top = Tk()
window1 = Toplevel(top)
window1.minsize(50, 50)
window1.withdraw()

top.title('Blood Pressure Monitoring System')
top.minsize(360, 240)
top.maxsize(360, 240)

canvas1 = Canvas(top, width=360, height=240)    # create the canvas (Tkinter module)
canvas1.pack()
try:
    image1 = ImageTk.PhotoImage(file ='pulse.jpg')
except:
    image1 = ImageTk.PhotoImage(file ='C:\\python\\pulse.jpg')
finally:
    canvas1.create_image(180,120,image = image1)

profile = Button(top, text='Profile', command=profileCallback, bg='blue', fg='red')
canvas1.create_window(50, 35, window=profile)

start = Button(top, text='Start', bg='blue', fg='red', command=startCallback)
canvas1.create_window(90, 35, window=start)

tabulate = Button(top, text='Tabulate', command=tabulateCallback, bg='blue', fg='red')
canvas1.create_window(175, 220, window=tabulate)

display = Button(top, text='Display', bg='blue', fg='red', command=displayVal)
canvas1.create_window(132, 35, window=display)

save = Button(top, text='Save', command=saveCallback, bg='blue', fg='red')
canvas1.create_window(173, 35, window=save)

viewxl = Button(top, text='ViewXL' ,command=daqdb.viewxl, bg='blue', fg='red')
canvas1.create_window(215, 35, window=viewxl)

viewdb = Button(top,text='ViewDB', command=daqdb.viewdb, bg='blue', fg='red')
canvas1.create_window(265, 35, window=viewdb)

bexit = Button(top, text='Exit', command=exitCallback, bg='red', fg='blue')
canvas1.create_window(305, 35, window=bexit)


top.mainloop()
