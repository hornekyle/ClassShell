import numpy as np


def graphviz(root,filename):
	
	def node(widget,h,s,v):
		name = ('root'+str(widget)).replace('!','').replace('.','_')
		basename = name.split('_')[-1]
		basename += '' if len(basename)>0 else '<ROOT>'
		try:
			txt = widget.cget('text')
		except Exception:
			txt = ''
		try:
			get = widget.get()
		except Exception:
			get = ''
		
		# print(widget,txt,get)
		lines = [basename,txt,get]
		label = '\n'.join([line for line in lines if (not line.startswith('PY')) and (len(line)>0)])
		
		key = ''.join(filter(lambda x: x.isalpha(),basename))
		shapes = {
			'frame'       :'folder',
			'labelframe'  :'tab',
			'menu'        :'house',
			'entry'       :'component',
			'label'       :'cds',
			'progressbar' :'parallelogram',
			'button'      :'octagon',
			'combobox'    :'component',
			'listbox'     :'component',
			'canvas'      :'note',
			'notebook':'tab',
			'panedwindow':'folder',
			'problempage':'folder',
			'spinbox':'component',
			'separator':'assembly',
			}
		if key in shapes:
			shape = shapes[key]
		else:
			shape = 'diamond'
		color = f'{h:.3f} {s:.3f} {v:.3f}'
		code = f'{name} [label="{label}",shape={shape},height="0.75",width="2",color="black",fillcolor="{color}"];'
		return name,code
	
	def hunt(parent,fh,depth=0,hl=0,hh=1,w=0.7,r=0.6):
		pname,pcode = node(parent,0.0,0.0,1.0)
		if depth==0:
			fh.write(pcode+'\n')
		
		children = parent.winfo_children()
		if len(children)>0:
			hb = np.linspace(hl,hh,len(children)+1)
			hm = (hb[1:]+hb[:-1])/2
			hδ = (hb[1]-hb[0])/2
		else:
			hm = np.array([hl+hh])/2
			hδ = (hh-hl)/2
		
		for (k,child) in enumerate(children):
			name,code = node(child,hm[k],r**depth,1.0)
			fh.write(code+'\n')
			fh.write(f'{pname} -> {name};')
			hunt(child,fh,depth+1,hm[k]-w*hδ,hm[k]+w*hδ)
	
	with open(filename,'w') as fh:
		fh.write('digraph {\n')
		fh.write('rankdir=LR;\n')
		fh.write('splines=ortho;\n')
		fh.write('ranksep=1.5;\n')
		hunt(root,fh)
		fh.write('}\n')
