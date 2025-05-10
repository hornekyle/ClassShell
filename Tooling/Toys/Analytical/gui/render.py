from io import BytesIO
import matplotlib
import matplotlib.pyplot as pl

matplotlib.use('Agg')


def render_latex(formula,fontsize=10,dpi=96):
	fig = pl.figure()
	text = fig.text(0,0,f'${formula}$',fontsize=fontsize)
	bbox = text.get_window_extent()
	
	width,height = bbox.size/dpi+0.05
	dy = -bbox.ymin/dpi/height
	
	fig.set_size_inches((width,height))
	text.set_position((0,dy))
	
	buf = BytesIO()
	fig.savefig(buf,dpi=dpi,transparent=True,format='png')
	pl.close(fig)
	
	return buf.getvalue()
