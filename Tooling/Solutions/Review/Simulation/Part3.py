import numpy as np
import matplotlib.pyplot as pl


class FunctionVector:
	def __init__(self,R=1.0,U=1.0):
		self.R = R
		self.U = U
	
	def __call__(self,x,y):
		th = np.arctan2(y,x)+np.pi/2
		eh = np.array((np.cos(th),np.sin(th)))
		r = np.sqrt(x**2+y**2)
		return self.uth(r)*eh
		
	def uth(self,r):
		rstar = r/self.R
		scale = self.U
		place = rstar if rstar<=1 else 1/rstar
		return scale*place


def plot(N):
	f = FunctionVector()
	x = np.linspace(-2*f.R,2*f.R,N)
	y = np.linspace(-2*f.R,2*f.R,N+1)
	U = np.empty((x.size,y.size))
	V = np.empty((x.size,y.size))
	for i in range(x.size):
		for j in range(y.size):
			U[i,j],V[i,j] = f(x[i],y[j])
	Umag = np.sqrt(U**2+V**2)
	
	fig = pl.figure('FunctionVector',tight_layout=True)
	
	ax = fig.add_subplot(1,1,1,aspect=1)
	ax.set_xlabel('Position, $x$ [m]')
	ax.set_ylabel('Position, $y$ [m]')
	
	c = ax.quiver(x,y,U.T,V.T,Umag.T)
	
	fig.colorbar(c,ax=ax,label='Velocity, $|\\vec{u}|$ [m/s]')
	
	return fig


def main():
	plot(21).savefig('Vortex.pdf')


if __name__=='__main__': main()

