import numpy as np
import matplotlib.pyplot as pl


class Function1D:
	def __init__(self,L=1.0,Tl=0.0,Tr=50.0,k=1.0,q=300.0):
		self.L = L
		self.k = k
		self.q = q
		
		self.Tl = Tl
		self.Tr = Tr
	
	def __call__(self,x):
		conduction = (self.Tr-self.Tl)*(x/self.L)
		generation = (self.q/self.k)*(self.L-x)*(x/2)
		T = self.Tl+conduction+generation
		return T


def plot(N):
	f = Function1D()
	x = np.linspace(0,f.L,N)
	T = f(x)
	
	fig = pl.figure('Function1D',tight_layout=True)
	
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('Position, $x$ [m]')
	ax.set_ylabel('Temperature, $T$ [C]')
	ax.plot(x,T)
	
	return fig


def main():
	plot(100).savefig('Wall.pdf')


if __name__=='__main__': main()
