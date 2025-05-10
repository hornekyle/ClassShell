import graphviz


node_style = {
	'shape':'note',
	'style':'filled',
	'color':'black',
	'fontname':'Helvetica',
	'fontsize':'16',
	'width':'2.5',
	'height':'0.5',
	'penwidth':'2',
	'style':'filled',
	}

edge_style = {
	'penwidth':'2',
	'headport':'w',
	'tailport':'e'
	}


def build_objectives(nodes,edges,groups):
	shapes = ['folder','note','cds','rectangle','tab','box','hexagon','rectangle','component',
		'rectangle','folder','tab','invhouse']
	styles = {group:shapes[k] for (k,group) in enumerate(groups)}
	
	colorscheme = {'colorscheme':'set14','fontcolor':'white'}
	graph = graphviz.Digraph(node_attr=node_style | colorscheme,edge_attr=edge_style)
	graph.attr(rankdir='LR',ranksep='2',nodesep='0.25')
	
	with graph.subgraph(name='cluster_roots') as subgraph:
		subgraph.attr(label='Earlier Modules')
		subgraph.attr(style='filled',color='lightskyblue')
		subgraph.attr(rank='same',newrank='True')
		for title in nodes['root'].index:
			color_idx = int(nodes['root'].loc[title]['Level'][:1])
			group = nodes['root'].loc[title]['Group']
			subgraph.node(title,title,fillcolor=f'{color_idx}',shape=styles[group])
	
	with graph.subgraph(name='cluster_module') as subgraph:
		subgraph.attr(label='Current Module')
		subgraph.attr(style='filled',color='lightgray')
		subgraph.attr(newrank='True')
		for title in nodes['trunk'].index:
			color_idx = int(nodes['trunk'].loc[title]['Level'][:1])
			group = nodes['trunk'].loc[title]['Group']
			subgraph.node(title,title,fillcolor=f'{color_idx}',shape=styles[group])
	
	with graph.subgraph(name='cluster_leaves') as subgraph:
		subgraph.attr(label='Later Modules')
		subgraph.attr(style='filled',color='gold')
		subgraph.attr(rank='same',newrank='True')
		for title in nodes['leaf'].index:
			color_idx = int(nodes['leaf'].loc[title]['Level'][:1])
			group = nodes['leaf'].loc[title]['Group']
			subgraph.node(title,title,fillcolor=f'{color_idx}',shape=styles[group])
	
	for (destination,sources) in edges.items():
		for source in sources:
			graph.edge(source,destination)
	
	return graph


def build_callgraph(functions,calls):
	label = lambda pair: f'{pair[0]}'+'|'+f'{pair[1]}'
	modules = sorted(list(set([target[0] for target in functions.keys()])))
	
	print(functions)
	print(calls)
	
	node_idx = 0
	cluster_idx = 0
	node_color_count = 12
	cluster_color_count = 9
	
	colorscheme = {'colorscheme':'set312','fontcolor':'black'}
	graph = graphviz.Digraph(node_attr=node_style | colorscheme,edge_attr=edge_style)
	graph.attr(rankdir='LR',ranksep='2',nodesep='0.25')
	for module in modules:
		with graph.subgraph(name=f'cluster_{module}') as subgraph:
			color_idx = cluster_idx%cluster_color_count+1
			cluster_idx += 1
			subgraph.attr(label=module,style='filled',colorscheme='pastel19',color=f'{color_idx}')
			placed = 0
			for (target,count) in functions.items():
				if target[0]!=module: continue
				color_idx = node_idx%node_color_count+1
				node_idx += 1
				subgraph.node(label(target),f'{target[1]}',fillcolor=f'{color_idx}')
				placed += 1
	
	for (context,targets) in calls.items():
		for (target,count) in targets.items():
			graph.edge(label(context),label(target))
	
	return graph
