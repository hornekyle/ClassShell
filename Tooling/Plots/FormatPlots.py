import matplotlib.pyplot as pl

preamble = r"""
\usepackage{amssymb}
\usepackage{units}

\usepackage[light]{plex-serif}
\usepackage[light]{plex-sans}
\usepackage[light]{plex-mono}

% \usepackage{sourceserifpro}
% \usepackage{sourcesanspro}
% \usepackage{sourcecodepro}

% \usepackage{beraserif}
% \usepackage{berasans}
% \usepackage{beramono}

\usepackage{eulervm}
"""

# Default MPL sequence
MPL_sequence = [
	'#1F77B4','#FF7F0E','#2CA02C','#D62728','#9467BD',
	'#8C564B','#E377C2','#7F7F7F','#BCBD22','#17BECF',
	]

# Modified Tol sequence
Tol_sequence = [
	'#332288','#EE7733','#117733','#882255','#AA4499',
	'#DDCC77','#CC6677','#AAAAAA','#999933','#88CCEE',
	]

KEEN_sequence = [
	'#245270','#f3b000','#3eb0a5','#ef733b','#783d81',
	'#a0522d','#dda0dd','#bfcdd3','#563432','#63a2bf',
	]

settings = {
	'backend':'agg',
	
	'font.family':'serif',
	'font.size':10,
	
	'font.serif':'IBM Plex Serif',
	'font.sans-serif':'IBM Plex Sans',
	'font.monospace':'IBM Plex Mono',
	
	'mathtext.fontset':'custom',
	'mathtext.bf':   'Euler Math:bold',
	'mathtext.bfit': 'Euler Math:italic:bold',
	'mathtext.cal':  'cursive',
	'mathtext.it':   'Euler Math:italic',
	'mathtext.rm':   'IBM Plex Serif',
	'mathtext.sf':   'IBM Plex Sans',
	'mathtext.tt':   'IBM Plex Mono',
	
	'axes.unicode_minus':False,
	'figure.figsize':(5.5,2.75),
	'figure.dpi':1200,
	'figure.max_open_warning':False,
	'pgf.texsystem':'pdflatex',
	'pgf.preamble':preamble,
	'savefig.facecolor':(1.0,1.0,1.0,0.0),
	'axes.prop_cycle':pl.cycler('color',MPL_sequence),
	# 'axes.spines.right': False,
	# 'axes.spines.top': False,
	'axes.formatter.use_mathtext': False,
	
	'figure.max_open_warning': 0,
}

pl.rcParams.update(settings)
