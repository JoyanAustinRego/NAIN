import nidaqmx
#from drawnow import *
from matplotlib.widgets import Button
import matplotlib.animation as animation
import daqplot
import random
import peakdetect
import matplotlib.pyplot as plt
from math import *
import os
from numpy import *
from tkMessageBox import *


samples = 60
samplesPerSecond = 60
voltage0 = []
voltage1 = []
voltage2 = []
timeval = []
volt0=[]
volt1=[]
time=[]
capv1=[]
capv2=[]
captime1=[]
captime2=[]
value = True
anim = []
count = 0
bpval = []
fig, ax1, readbutton = [], [], []



def randomgen():
    vol00,vol11,vol22 = [], [], []
    for i in range(samples):
        vol00.append(sin(2*pi*500*i/8000.0)*cos(4*pi*600*i/8000.0))
        vol11.append(2*sin(2*pi*400*i/8000.0)*cos(2*pi*800*i/8000.0))
        vol22.append(2 * sin(2 * pi * 400 * i / 8000.0) * 3 * random.randint(0,10))
    return [vol00,vol11,vol22]


def readChannel(channel):
    try:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(channel)
            task.timing.cfg_samp_clk_timing(rate=samplesPerSecond, samps_per_chan=samples)
            return task.read(number_of_samples_per_channel=samples, timeout=25.0)
    except:
        return randomgen()



def timegenerate():
    global count, timeval
    times = []
    if count == 0 or count == 1:
        t = 0
    else:
        t = timeval[len(timeval) - 1]
    for i in range(samples):
        times.append(t)
        t += 1.0/samples
    return times


def makefig(i):
    global count

    result = readChannel('Dev1/ai0:2')
    vol0, vol1, vo22 = result[0], result[1], result[2]
    tim = timegenerate()
    if count > 0:
        for x in range(samples):
            voltage0.append(vol0[x])
            voltage1.append(vol1[x])
            voltage2.append(vo22[x])
            timeval.append(tim[x])

        plotgraph()
        plt.pause(0.000001)
        for i in range(samples-20):
            voltage0.pop(0)
            voltage1.pop(0)
            timeval.pop(0)
    count += 1

def capturevalue():
    global volt0, volt1, time, capv1, capmin1, capmin2, capv2, captime1, captime2
    capmin1 = volt0.index(min(volt0))
    capmin2 = volt1.index(min(volt1))
    while capmin1 != (len(volt0)-1):
        capv1.append(volt1[capmin1])
        captime1.append(time[capmin1])
        capmin1 += 1
    while capmin2 != (len(volt1)-1):
        capv2.append(volt1[capmin2])
        capmin2 += 1
        captime2.append(time[capmin2])
    print(capv1)
    print(volt0)


def returnvalue(event):
    global volt0, volt1, time, bpval
    _pause()
    bpval = daqplot.process(volt0, volt1, time)
    capturevalue()


def plotgraph():
        global ax1, readbutton,volt0, volt1, time
        ax1.clear()
        time = timeval[-(samples+20):]
        volt0 = voltage0[-(samples+20):]
        volt1= voltage1[-(samples+20):]
        plt.subplot(2, 1, 1)
        plt.plot(time, volt0, 'r-', label='voltage0')
        plt.legend(loc='upper right')
        plt.subplot(2, 1, 2)
        plt.plot(time, volt1, 'b-', label='voltage1')
        plt.legend(loc='upper right')
        readaxis = fig.add_axes((0.5, 0.005, 0.1, 0.05))
        readbutton = Button(readaxis, 'Read', hovercolor='1.0')
        readbutton.on_clicked(returnvalue)


def _pause():
    global anim
    anim.event_source.stop()


def main():
    global anim, fig, ax1

    fig = plt.figure()
    ax1 = fig
    anim = animation.FuncAnimation(fig, makefig, interval=1) # interval is the delay in ms after which makefig has to be called
    # show plot

    try:
        plt.show()
    except :
        pass
    finally:
         plt.close()


def sendval():
    global bpval
    return bpval


def filelog(tab,text,no,mode):
    flog = open('timelog.csv', mode)
    flog.write('%s%d,%s\n'%('Waveform', no, 'Values'))
    flog.write('%s,%s\n' % ('Time', text))
    for i in range(len(tab)):
        flog.write('%f,%f\n'%(tab[i][0],tab[i][1]))
    flog.close()


def peak():
    global capv1, capv2, captime1, captime2
    maxtab0, mintab0 = peakdetect.peakdet(capv1, 0.1, captime1) # change 2nd argument to fine tune peak detection
    maxtab1, mintab1 = peakdetect.peakdet(capv2, 0.1, captime2) # change 2nd argument to fine tune peak detection
    filelog(maxtab0,'Maximum',1,'w')
    filelog(mintab0, 'Minimum', 1, 'a')
    filelog(maxtab1, 'Maximum', 2, 'a')
    filelog(mintab1, 'Minimum', 2, 'a')
    plt.subplot(2,1,1)
    plt.plot(captime1,capv1)
    plt.scatter(array(maxtab0)[:, 0], array(maxtab0)[:, 1], color='blue')
    plt.scatter(array(mintab0)[:, 0], array(mintab0)[:, 1], color='red')
    plt.subplot(2,1,2)
    plt.plot(captime2, capv2)
    plt.scatter(array(maxtab1)[:, 0], array(maxtab1)[:, 1], color='blue')
    plt.scatter(array(mintab1)[:, 0], array(mintab1)[:, 1], color='red')
    os.startfile('timelog.csv')
    plt.show()
