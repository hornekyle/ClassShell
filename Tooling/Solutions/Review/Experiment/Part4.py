import numpy as np
import matplotlib.pyplot as pl


class Transistors:
	def __init__(self,file_name):
		t,N = np.loadtxt(file_name,unpack=True)
		N *= 1.0E3
		
		A,tau2,t0 = self.fit(t,N,t.min())
		
		self.t = t
		self.N = N
		self.A = A
		self.t0 = t0
		self.tau2 = tau2
	
	def __call__(self,t):
		scale = self.A
		place = np.log(2)*(t-self.t0)/self.tau2
		N = scale*np.exp(place)
		return N
		
	@staticmethod
	def fit(t,N,t0):
		X = t-t0
		Y = np.log(N)
		
		# N = A*exp(r*t)
		m,b = np.polyfit(X,Y,1)
		
		A = np.exp(b)
		tau2 = np.log(2)/m
		
		return A,tau2,t0


def plot(N):
	f = Transistors('Transistors.txt')
	t = np.linspace(f.t.min(),f.t.max(),N)
	N = f(t)
	lbl = f'Fit\n| $A = {f.A:.2f}$\n| $\\tau_2 = {f.tau2:.2f} yr$'
	
	fig = pl.figure('Transistors',tight_layout=True)
	
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('Time, $t$ [yr]')
	ax.set_ylabel('Transistors, $N$ [$\\#$]')
	ax.set_yscale('log')
	ax.plot(f.t,f.N,'C0+',label='Data')
	ax.plot(t,N,'C1:',label=lbl)
	ax.legend()
	
	return fig


def main():
	plot(100).savefig('Transistors.pdf')


if __name__=='__main__': main()
