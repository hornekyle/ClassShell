import numpy as np
import matplotlib.pyplot as pl
import pandas

def read_data(filename):
	# t,N = np.loadtxt(filename,unpack=True)
	df = pandas.read_csv(filename,sep='\s+',names=['t','N'],comment='#')
	t = df['t'].values
	N = df['N'].values
	return t,N

def plot_data(t,N):
	figure = pl.figure(tight_layout=True)
	axes = figure.add_subplot(1,1,1)
	axes.set_yscale('log')
	axes.set_xlabel('Time, $t$ [yr]')
	axes.set_ylabel('Transistor Count, $N$ [$\\#$]')
	axes.plot(t,N,'C0+')
	return figure

def main():
	t,N = read_data('transistors.dat')
	plot_data(t,N)
	pl.show()

if __name__=='__main__': main()
