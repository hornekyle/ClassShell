import numpy as np
import matplotlib.pyplot as pl

class VectorField:
	def __init__(self,U0,R0):
		self.U0 = U0
		self.R0 = R0
	
	def fu(self,X,Y):
		@np.vectorize
		def fuθ(r):
			if r<=self.R0:
				uθ = r/self.R0*self.U0
			else:
				uθ = self.R0/r*self.U0
			return uθ
		R = np.sqrt(X**2+Y**2)
		Θ = np.arctan2(Y,X)
		Uθ = fuθ(R)
		
		U = -np.sin(Θ)*Uθ
		V =  np.cos(Θ)*Uθ
		return U,V

	def plot(self,X,Y,U,V):
		M = np.sqrt(U**2+V**2)
		
		figure = pl.figure(tight_layout=True)
		axes = figure.add_subplot(1,1,1)
		axes.set_aspect('equal')
		axes.set_xlabel('Coordinate, $x$ [-]')
		axes.set_ylabel('Coordinate, $y$ [-]')
		c = axes.quiver(X,Y,U,V,M)
		figure.colorbar(c,ax=axes,label='Velocity, $|U|$ [-]')
		return figure

def main():
	fieldA = VectorField(1.0,0.5)
	fieldB = VectorField(1.0,1.5)
	
	x = np.linspace(-2,2,19)
	y = np.linspace(-2,2,21)
	X,Y = np.meshgrid(x,y)
	
	U,V = fieldA.fu(X,Y)
	fieldA.plot(X,Y,U,V)
	
	U,V = fieldB.fu(X,Y)
	fieldB.plot(X,Y,U,V)
	
	pl.show()

if __name__=='__main__': main()
