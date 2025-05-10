import numpy as np


class Function2D:
	def __init__(self):
		defaults = {
			'L':  1.0,
			'G':100.0,
			'N':100.0,
			'τ': -3.0,
			}
		self.set_params(defaults)
	
	def __call__(self,x,y):
		T = self.ϕ(x)+self.ξ(x,y)
		return T
	
	def get_name(self):
		return '2D Heat Conduction'
	
	def get_descriptors(self):
		desc = {
			'L':('Half Length'       ,'L'       ,'m'       , '0.01',  '1.0','0.01'),
			'G':('Generation'        ,'G'       ,'W/K'     , '0.0' ,'500.0','1.0' ),
			'N':('Max Term Count'    ,'N'       ,'\\#'     , '0.0' ,'100.0','1.0' ),
			'τ':('Tolerance Exponent','10^\\tau','\\emdash','-6.0' , '0.0','1.0' ),
			}
		return desc
	
	def set_params(self,params):
		self.L = params['L']
		self.G = params['G']
		self.N = int(params['N'])
		self.τ = params['τ']
	
	def get_params(self):
		params = {
			'L':self.L,
			'G':self.G,
			'N':self.N,
			'τ':self.τ,
			}
		return params
	
	def ϕ(self,x):
		scale = (self.G*self.L**2/2)
		place = 1-(x/self.L)**2
		return scale*place
	
	def ξ(self,x,y):
		scale = -2*self.G*self.L**2
		
		sigma = 0.0
		for n in range(self.N):
			ln = (2*n+1)/(2*self.L)*np.pi
			
			sign = (-1)**n
			num = np.cosh(ln*y)*np.cos(ln*x)
			den = (ln*self.L)**3*np.cosh(ln*self.L)
			
			term = sign*num/den
			sigma += term
			
			if np.abs(term)<10**self.τ:
				break
		
		return scale*sigma
	
	def plot(self,fig,queue,N=75,levels=10):
		x = np.linspace(-self.L,self.L,N)
		y = np.linspace(-self.L,self.L,N+1)
		T = np.empty((x.size,y.size))
		
		queue.put(0)
		for i in range(x.size):
			if i%5==0: queue.put(i/x.size)
			for j in range(y.size):
				T[i,j] = self(x[i],y[j])
		queue.put(1)
		
		fig.clf()
		ax = fig.add_subplot(1,1,1,aspect=1)
		ax.set_xlabel('Position, $x$ [m]')
		ax.set_ylabel('Position, $y$ [m]')
		
		# Plot twice to avoid single pixel gaps in color
		c = ax.contourf(x,y,T.T,levels,zorder=2)
		ax.contour(x,y,T.T,levels,zorder=1)
		
		fig.colorbar(c,ax=ax,label='Temperature, $T$ [C]')
		queue.put('done')
