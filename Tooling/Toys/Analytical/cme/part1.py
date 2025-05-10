import numpy as np


class Function1D:
	def __init__(self):
		defaults = {
			'L' :   1.0,
			'k' : 100.0,
			'q' :  20.0, # kW!
			'Tl':   0.0,
			'Tr': 100.0,
			}
		self.set_params(defaults)
	
	def __call__(self,x):
		conduction = (self.Tr-self.Tl)*(x/self.L)
		generation = (self.q/self.k)*(self.L-x)*(x/2)
		T = self.Tl+conduction+generation
		return T
	
	def get_name(self):
		return '1D Heat Conduction'
	
	def get_descriptors(self):
		desc = {
			'L' :('Length'          ,'L'  ,'m'               ,'0.01',  '1.0','0.01'),
			'k' :('Conductivity'    ,'k'  ,'W/{m^2 \\cdot K}','1.0', '300.0','1.0' ),
			'q' :('Generation'      ,'q'  ,'kW'              ,'0.0' ,'100.0','1.0' ),
			'Tl':('BC (left value)' ,'T_l','^\\circ C'       ,'0.0' ,'100.0','1.0' ),
			'Tr':('BC (right value)','T_r','^\\circ C'       ,'0.0' ,'100.0','1.0' ),
			}
		return desc
	
	def set_params(self,params):
		self.L = params['L']
		self.k = params['k']
		self.q = params['q']*1.0E3
		
		self.Tl = params['Tl']
		self.Tr = params['Tr']
	
	def get_params(self):
		params = {
			'L' :self.L,
			'k' :self.k,
			'q' :self.q*1.0E-3,
			'Tl':self.Tl,
			'Tr':self.Tr,
			}
		return params
	
	def plot(self,fig,queue,N=75):
		x = np.linspace(0,self.L,N)
		T = self(x)
		queue.put('done')
		fig.clf()
		ax = fig.add_subplot(1,1,1)
		ax.set_xlabel('Position, $x$ [cm]')
		ax.set_ylabel('Temperature, $T$ [C]')
		ax.plot(x*1.0E2,T)
