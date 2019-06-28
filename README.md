# NAIN
BP Measuring System

#Packages needed
csv
tkinter

MySQLdb
os
webbrowser

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
