import numpy as np
import matplotlib.pyplot as pl


class Function2D:
	def __init__(self,G=100.0,L=1.0,terms_max=100,terms_tol=1.0E-6):
		self.G = G
		self.L = L
		
		self.terms_max = terms_max
		self.terms_tol = terms_tol
	
	def __call__(self,x,y):
		T = self.phi(x)+self.xi(x,y)
		return T
	
	def phi(self,x):
		scale = (self.G*self.L**2/2)
		place = 1-(x/self.L)**2
		return scale*place
	
	def xi(self,x,y):
		scale = -2*self.G*self.L**2
		
		sigma = 0.0
		for n in range(self.terms_max):
			ln = (2*n+1)/(2*self.L)*np.pi
			
			sign = (-1)**n
			num = np.cosh(ln*y)*np.cos(ln*x)
			den = (ln*self.L)**3*np.cosh(ln*self.L)
			
			term = sign*num/den
			sigma += term
			
			if np.abs(term)<self.terms_tol:
				break
		
		return scale*sigma


def plot(N,levels=10):
	f = Function2D()
	x = np.linspace(-f.L,f.L,N)
	y = np.linspace(-f.L,f.L,N+1)
	T = np.empty((x.size,y.size))
	for i in range(x.size):
		for j in range(y.size):
			T[i,j] = f(x[i],y[j])
	
	fig = pl.figure('Function2D',tight_layout=True)
	
	ax = fig.add_subplot(1,1,1,aspect=1)
	ax.set_xlabel('Position, $x$ [m]')
	ax.set_ylabel('Position, $y$ [m]')
	
	# Plot twice to avoid single pixel gaps in color
	c = ax.contourf(x,y,T.T,levels,zorder=2)
	ax.contour(x,y,T.T,levels,zorder=1)
	
	fig.colorbar(c,ax=ax,label='Temperature, $T$ [C]')
	
	return fig


def main():
	plot(51).savefig('Plate.pdf')


if __name__=='__main__': main()

