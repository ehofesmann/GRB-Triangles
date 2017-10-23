import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


burstnum = 143

filename = "./cat64ms." + str(burstnum).zfill(5)

file = open(filename, "r") 
file.readline()
channel = []
nlasc = file.readline() #number of 1000ms 
nlasc = eval(nlasc.split('  ')[3])
for line in file:
    ch1 = eval(line.split('  ')[1])
    ch2 = eval(line.split('  ')[2])
    ch3 = eval(line.split('  ')[3])
    ch4 = eval(line.split('  ')[4])
    channel.append(ch1+ch2+ch3+ch4)

    
#generate triangle (I forgot I already made the method)
#chnew = []
#for i in range(len(channel)):
#    if(i <= nlasc):
#        chnew.append(100)
#    elif(i <= nlasc+100):
#        chnew.append(100+i-nlasc)
#    elif(i <= nlasc+200):
#        chnew.append(300+nlasc-i)
#    else:
#        chnew.append(100)
#channel=chnew
    


t = np.arange(-nlasc*0.064, (len(channel)-nlasc)*0.064, 0.064)


def fit_pulse(ts, A, t1, t2, bkg):
    lam = np.exp(2*np.sqrt(t1/t2))
    inten = A*lam*np.exp(-t1/(t-ts)-(t-ts)/t2)+bkg
    for i in range(len(t)):
        if t[i] <= ts:
            inten[i] = bkg
    return inten

def fit_pulse_t(ts, A, t1, t2,t0):
    lam = np.exp(2*np.sqrt(t1/t2))
    inten = A*lam*np.exp(-t1/(t0-ts)-(t0-ts)/t2)
    return inten


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.4, top = 0.99)


a0 = 59.0
ts0 = -7.1
t10 = 5.0
t20 = 10.0
bkg0 = 100.0

s = fit_pulse(ts0,a0,t10,t20,bkg0)

l, = plt.plot(t, s)
plt.plot(t,channel)


ax = plt.gca()
ax.set_xlim([-400,400])

axts = plt.axes([0.25, 0.1, 0.65, 0.03])
axA = plt.axes([0.25, 0.15, 0.65, 0.03])
axt1 = plt.axes([0.25, 0.05, 0.65, 0.03])
axt2 = plt.axes([0.25, 0.01, 0.65, 0.03])
axbkg = plt.axes([0.25,0.2,0.65,0.03])
axwin1 = plt.axes([0.25,0.25,0.65,0.03])
axwin2 = plt.axes([0.25,0.28,0.65,0.03])

def generate_triangle(inten_array):
        #take a flat line (array of all zeros) and make a triangle in the middle of it
        for i in range(len(inten_array)):
                if 200 >= i >= 100:
                        inten_array[i] = i-100
                elif 300 >= i > 200:
                        inten_array[i] = 300 - i
        return inten_array
    
    
sts = Slider(axts, 'Start Time', -100.0, 100.0, valinit=ts0)
sA = Slider(axA, 'Amp', 1.0, max(channel), valinit=a0)
st1 = Slider(axt1, "Tau 1", 0.01, 500.0, valinit=t10)
st2 = Slider(axt2, "Tau 2", 0.01, 100.000, valinit=t20)
sbkg = Slider(axbkg, "Background", 0.0, 5000.000, valinit=bkg0)
swin1 = Slider(axwin1, "window min", -400.0, 400.000, valinit=-400.0)
swin2 = Slider(axwin2, "window max", -400.0, 400.000, valinit=400.0)

def update(val):
    tempA = sA.val
    tempts = sts.val
    tempt1 = st1.val
    tempt2 = st2.val
    tempbkg = sbkg.val
    tempwin1 = swin1.val
    tempwin2 = swin2.val
    snew = fit_pulse(tempts,tempA,tempt1,tempt2,tempbkg)
    l.set_ydata(snew)
    ax.set_xlim([tempwin1, tempwin2])
    fig.canvas.draw_idle()
    
    resdiff = channel-snew
    res.set_ydata(resdiff)
    ax3.set_xlim([tempwin1, tempwin2])
    ax3.set_ylim([min(resdiff),max(resdiff)])
    fig2.canvas.draw_idle()
    
sts.on_changed(update)
sA.on_changed(update)
st1.on_changed(update)
st2.on_changed(update)
sbkg.on_changed(update)
swin1.on_changed(update)
swin2.on_changed(update)


fig2, ax2 = plt.subplots()
res, = plt.plot(t, channel-s)
ax3 = plt.gca()
ax3.set_xlim([-400,400])
ax3.set_ylim([-1000,1000])

plt.show()

