import numpy as np


class FunctionVector:
	def __init__(self):
		defaults = {
			'R':1.0,
			'L':2.0,
			'U':0.5,
			}
		self.set_params(defaults)
	
	def __call__(self,x,y):
		θ = np.arctan2(y,x)+np.pi/2
		eh = np.array((np.cos(θ),np.sin(θ)))
		r = np.sqrt(x**2+y**2)
		return self.uθ(r)*eh
	
	def get_name(self):
		return '2D Vector Field'
	
	def get_descriptors(self):
		desc = {
			'R':('Vortex Radius'     ,'R','m'  , '0.05','3.0','0.05'),
			'L':('Domain Half Length','L','m'  , '1.0' ,'2.0','0.05'),
			'U':('Max Velocity'      ,'U','m/s', '0.0' ,'1.0','0.1' ),
			}
		return desc
	
	def set_params(self,params):
		self.R = params['R']
		self.L = params['L']
		self.U = params['U']
	
	def get_params(self):
		params = {
			'R':self.R,
			'L':self.L,
			'U':self.U,
			}
		return params
	
	def uθ(self,r):
		ρ = r/self.R
		scale = self.U
		place = ρ if ρ<=1 else 1/ρ
		return scale*place
	
	def plot(self,fig,queue,N=75):
		x = np.linspace(-self.L,self.L,N)
		y = np.linspace(-self.L,self.L,N+1)
		U = np.empty((x.size,y.size))
		V = np.empty((x.size,y.size))
		
		queue.put(0)
		for i in range(x.size):
			if i%5==0: queue.put(i/x.size)
			for j in range(y.size):
				U[i,j],V[i,j] = self(x[i],y[j])
		Umag = np.sqrt(U**2+V**2)
		queue.put(1)
		
		fig.clf()
		ax = fig.add_subplot(1,1,1,aspect=1)
		ax.set_xlabel('Position, $x$ [m]')
		ax.set_ylabel('Position, $y$ [m]')
		
		c = ax.streamplot(x,y,U.T,V.T,1.25,color=Umag.T,cmap='viridis')
		fig.colorbar(c.lines,ax=ax,label='Velocity, $|\\vec{u}|$ [m/s]')
		queue.put('done')
