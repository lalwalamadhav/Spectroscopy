from astropy.io import fits as fit
import numpy as np
from scipy.optimize import curve_fit as cfit
import scipy.constants as s
import matplotlib.pyplot as plt
from scipy.signal import find_peaks as fp
import re
from matplotlib.widgets import Slider, Button
k = input("Enter the name of file:\n")
k = k+".fits"
dat = fit.open(k)
dat = dat[0].data
wvl=np.arange(1150,25001,5)
l=wvl*10**-10
def B(l,T,n):
	t=(n*2*s.h*s.c**2)/((l**5)*(np.exp((s.h*s.c)/(l*s.k*T))-1))
	return t
plt.plot(wvl,dat)
plt.show()
inp = input("Where to cut:\n")
if inp=='max':
	cut = np.argmax(dat)
else:
	cut=wvl.tolist().index(int(inp))

cut=int(cut)
spec=wvl.tolist().index(3500)
val, var = cfit(B,l[cut:],dat[cut:],p0=[1000,1])
print(val[1])


peaks,_=fp((B(l,val[0],val[1])-dat),prominence=0.05)

wvlpk = (peaks*5+1150)
fig = plt.figure()
black_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
slider1_ax = plt.axes([0.1, 0.05, 0.5, 0.01])
slider2_ax = plt.axes([0.1, 0.03, 0.5, 0.01])
plt.axes(black_ax)
black_plot, = plt.plot(wvl,B(l,val[0],val[1]))
n_slider = Slider(slider1_ax,'unit',0,10*val[1],valinit=val[1])
T_slider = Slider(slider2_ax,'Temperature',1000,50000,valinit=val[0])
def update(val):
	n = n_slider.val
	T = T_slider.val
	black_plot.set_ydata(B(l,T,n))
	fig.canvas.draw_idle()
n_slider.on_changed(update)
T_slider.on_changed(update)

print(wvlpk)
line = 1
while line !="":
	line = input("Enter wavelength with name:\n")
	if line=="":
		pass
	else:
		c = re.split(" ",line)
		plt.axvline(x=float(c[0]),ls = '--',color = 'black')
		plt.text(float(c[0]),np.max(dat)*(0.5),c[1],rotation=90)

plt.plot((peaks*5+1150),dat[peaks],"x")

plt.plot(wvl,dat)
plt.title(val[0])

plt.ylim(0,np.max(dat)*(1.1))
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    n_slider.reset()
    T_slider.reset()
button.on_clicked(reset)
plt.show()
