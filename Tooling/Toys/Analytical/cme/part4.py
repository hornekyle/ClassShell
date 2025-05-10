import numpy as np

import importlib.resources
import io


class Transistors:
	def __init__(self):
		text_data = importlib.resources.read_text(__package__,'transistors.txt')
		buf = io.StringIO(text_data)
		t,N = np.loadtxt(buf,unpack=True)
		buf.close()
		
		N *= 1.0E3
		self.t = t
		self.N = N
		
		defaults = {
			'tl':int(t.min()-1.0),
			'th':int(t.max()+1.0),
			}
		self.set_params(defaults)
	
	def __call__(self,t):
		A,τ2,t0,mask = self.fit()
		
		scale = A
		place = np.log(2)*(t-t0)/τ2
		N = scale*np.exp(place)
		return N
	
	def get_name(self):
		return 'Regression Fit'
	
	def get_descriptors(self):
		tl = int(self.t.min()-1.0)
		th = int(self.t.max()+1.0)
		desc = {
			'tl':('Start Time','t_l','yr',tl,th-1.0,'1.0'),
			'th':('End Time'  ,'t_h','yr',tl+1.0,th,'1.0'),
			}
		return desc
	
	def set_params(self,params):
		self.tl = params['tl']
		self.th = params['th']
	
	def get_params(self):
		params = {
			'tl':self.tl,
			'th':self.th,
			}
		return params
	
	def fit(self):
		t0 = self.t.min()
		mask = np.logical_and(self.t>self.tl,self.t<self.th)
		
		X = self.t[mask]-t0
		Y = np.log(self.N[mask])
		
		# N = A*exp(r*t)
		m,b = np.polyfit(X,Y,1)
		
		A = np.exp(b)
		τ2 = np.log(2)/m
		
		
		return A,τ2,t0,mask
	
	def plot(self,fig,queue,N=75):
		
		A,τ2,t0,mask = self.fit()
		t = np.linspace(self.t.min(),self.t.max(),N)
		N = self(t)
		lbl = f'Fit\n| $A = {A:.2f}$\n| $\\tau_2 = {τ2:.2f} yr$\n| $t_0 = {t0:.2f} yr$'
		
		fig.clf()
		
		ax = fig.add_subplot(1,1,1)
		ax.set_xlabel('Time, $t$ [yr]')
		ax.set_ylabel('Transistors, $N$ [$\\#$]')
		ax.set_yscale('log')
		ax.plot(self.t[mask],self.N[mask],'C0+',label='Included Data')
		ax.plot(self.t[~mask],self.N[~mask],'C1x',label='Excluded Data')
		ax.plot([],[],linestyle='none',marker='none',label=' ')
		ax.plot(t,N,'C2-',label=lbl)
		ax.axvline(self.tl,linestyle='--',color='C7')
		ax.axvline(self.th,linestyle='--',color='C7')
		
		ax.set_ylim(0.9*self.N.min(),1.1*self.N.max())
		ax2 = ax.secondary_xaxis('top')
		ax2.set_xticks([self.tl,self.th])
		ax2.set_xticklabels(['$t_l$','$t_h$'])

		formula = '$N\\left(t;A,\\tau_2,t_0\\right) = A \\cdot 2^\\frac{t-t_0}{\\tau_2}$\n'
		ax.legend(loc='upper left',bbox_to_anchor=(1,1),title=formula)
		queue.put('done')
