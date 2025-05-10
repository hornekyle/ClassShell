import numpy as np
import matplotlib.pyplot as pl


def fT(X,Y,G,L):
	T = fϕ(X,G,L)+fξ(X,Y,G,L)
	return T


def fϕ(X,G,L):
	ϕ = G*L**2/2*(1-(X/L)**2)
	return ϕ


def fξ(X,Y,G,L,Nmax=30):
	'''
	Take in X and Y as rank-2 arrays.
	Compute ξ(X,Y) as defined in handout.
	Use sub-functions for both λn and terms in summation.
	'''
	def fλ(n):
		λ = (2*n+1)/(2*L)*np.pi
		return λ
	
	def fterm(n):
		λ = fλ(n)
		A = (-1)**n/(λ*L)**3
		B = np.cosh(λ*Y)/np.cosh(λ*L)
		C = np.cos(λ*X)
		return A*B*C
	
	S = fterm(0)
	for k in range(1,Nmax):
		S += fterm(k)
	
	ξ = -2*G*L**2*S
	return ξ


def plot(X,Y,T):
	figure = pl.figure(tight_layout=True)
	axes = figure.add_subplot(1,1,1)
	axes.set_aspect('equal')
	axes.set_xlabel('Coordinate, $x$ [-]')
	axes.set_ylabel('Coordinate, $y$ [-]')
	c = axes.contourf(X,Y,T,15)
	figure.colorbar(c,ax=axes,label='Temperature, $T$ [-]')
	return figure


def main():
	L = 1.0
	x = np.linspace(-L,L,49)
	y = np.linspace(-L,L,51)
	
	X,Y = np.meshgrid(x,y)
	T = fT(X,Y,100,1)
	plot(X,Y,T)
	pl.show()


if __name__=='__main__': main()
