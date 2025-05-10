import argparse
import pandas
import pylatex

import Graphs


def remover(text):
	'''
	Remove E and M designations from module text
	'''
	targets = ['E','M']
	output = text
	for target in targets:
		output = output.replace(target,'')
	return output


def find_modules(objectives_file):
	'''
	Find all modules referenced in any sheet within the file
	'''
	sheets = pandas.read_excel(objectives_file,sheet_name=None,dtype={'Module':str})
	sheets.pop('Summary',None)
	
	modules = []
	for (name,sheet) in sheets.items():
		duplicated = sheet['Module'].apply(remover).str.split(',').sum()
		modules += duplicated
	modules = sorted(list(set(modules)))
	return modules


def print_modules(modules):
	'''
	Print module list in format suitable for CMake
	'''
	text = ';'.join([f'{module}' for module in modules ])
	print(text,end='')


def find_objectives(objectives_file,module):
	'''
	Find all objectives in module
	'''
	sheets = pandas.read_excel(objectives_file,sheet_name=None,dtype={'Module':str})
	sheets.pop('Summary',None)
	
	objectives = {}
	for (name,sheet) in sheets.items():
		def contains(module_list):
			flag = module in module_list
			return flag
		modules = sheet['Module'].apply(remover).str.split(',')
		mask = modules.apply(contains)
		objectives[name] = sheet[mask]
	
	return objectives


def build_legend():
	class CMELegend(pylatex.base_classes.Environment):
		_latex_name = 'CMELegend'
		packages = [pylatex.Package('tcolorbox')]
		escape = False
		content_separator = '\n'
	
	class tcbsubtitle(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	categories = [{
		'Recall':('skill1','Retain and recall information'),
		'Understand':('skill2','Explain ideas and concepts'),
		'Apply':('skill3','Apply knowledge to technical problems'),
		'Design':('design','Design and evaluate solutions'),
		'Math':('math','Math concepts and skills'),
		},{
		'Attitude':('basic','Participate in learning activities'),
		'Curiosity':('curiosity','Demonstrate curiosity in a variety of topics'),
		'Connections':('connections','Explore connections between groups and ideas'),
		'Value Creation':('createvalue','Create value for people using skills'),
		},{
		'Principle':('principle','Principles and guide-lines'),
		}]
	
	legend = CMELegend(arguments='Icons Key')
	for (k,group) in enumerate(categories):
		if k!=0:
			subtitle = tcbsubtitle(options='CMELegendSubtitleStyle',arguments='')
			legend.append(subtitle)
		with legend.create(pylatex.Description()) as listing:
			for (category,(icon,description)) in group.items():
				graphics = f'\\includegraphics[height=1.2em]{{../../Tooling/Icons/{icon}}}'
				title = category
				label = pylatex.NoEscape(f'{{{graphics} {title}}}')
				listing.add_item(label,description)
	return legend


def build_objectives(objectives,tex_file):
	'''
	Build TeX file including all objectives in module
	'''
	introduction = [
		'Learning objectives help maintain consistency of instruction, study, and grading.',
		'Splitting objectives in to skill-set (cognitive) and mindset (affective) helps keep things straight.',
		'The following sections list the various objectives for this module.',
		'Icons provide visual clues to the type of each objective; icon meanings are detailed in the "Icons Key".',
		]
	reasons = {
		'Skill-set':[
			'Drawing from the cognitive domain (thinking), these objectives describe technical skills or knowledge.',
			'Mastery of these objectives forms the bulk of all work needed to succeed in this course.',
			'The complexity of these skills ranges from simple (recall) to complex (design and analysis).',
			'All skill-set objectives are important to success.',
			],
		'Mindset':[
			'Engineering practice draws upon many skills, but perspectives, attitudes, and culture also matter.',
			'Mindset objectives describe skills in the affective domain (feeling), and are frequently missed in classes.',
			'Careful consideration should be applied to the professional mindset but it takes time.',
			'Thus, mindset objectives are repeated during the semester to help students come around to new ideas.',
			],
		'Principles':[
			'Some general principles apply to many different circumstances.',
			'These are listed here, and may be taken as general guild lines.',
			'Exceptions can (and should) be found; patterns do not need absolute compliance to be useful.',
			],
		}
	with open(tex_file,'w') as fh:
		pylatex.Section('Objectives').dump(fh)
		for line in introduction:
			fh.write(f'{line}\n')
		legend = build_legend()
		legend.dump(fh)
		
		for (name,sheet) in objectives.items():
			pylatex.Subsection(name).dump(fh)
			for line in reasons[name]:
				fh.write(f'{line}\n')
			items = pylatex.Description()
			for (k,row) in sheet.iterrows():
				icon = 'design'
				if 'Group' not in row:
					icon = 'principle'
				elif row['Group'] in ['Curiosity','Connections','CreateValue','Basic']:
					icon = row['Group'].lower()
				elif row['Module'].startswith('M'):
					icon = 'math'
				elif row['Level'] in [1,2,3]:
					level = row['Level']
					icon = f'skill{level}'
				
				graphics = f'\\includegraphics[height=1.2em]{{../../Tooling/Icons/{icon}}}'
				title = row['Title']
				label = pylatex.NoEscape(f'{{{graphics} {title}}}')
				text = row['Description']
				items.add_item(label,pylatex.NoEscape(text))
			items.dump(fh)


def build_describe(objectives,tex_file):
	'''
	Build TeX file for describe sheets
	'''
	
	class CMEDescribeNote(pylatex.base_classes.Environment):
		_latex_name = 'CMEDescribeNote'
		packages = [pylatex.Package('tcolorbox')]
		escape = False
		content_separator = '\n'
	
	class tcblower(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	class tcbsubtitle(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	class Multicols(pylatex.base_classes.Environment):
		_latex_name = 'multicols'
		packages = [pylatex.Package('multicols')]
		escape = False
		content_separator = '\n'
	
	class Minipage(pylatex.base_classes.Environment):
		_latex_name = 'minipage'
		escape = False
		content_separator = '\n'
	
	with open(tex_file,'w') as fh:
		for (name,sheet) in objectives.items():
			pylatex.Section(name).dump(fh)
			for (k,row) in sheet.iterrows():
				icon = 'design'
				if 'Group' not in row:
					icon = 'principle'
				elif row['Group'] in ['Curiosity','Connections','CreateValue','Basic']:
					icon = row['Group'].lower()
				elif row['Module'].startswith('M'):
					icon = 'math'
				elif row['Level'] in [1,2,3]:
					level = row['Level']
					icon = f'skill{level}'
				
				graphics = f'\\includegraphics[height=1.2em]{{../../Tooling/Icons/{icon}}}'
				title = row['Title']
				label = pylatex.NoEscape(f'{{{graphics}\\hspace{{1ex}}{title}}}\\vphantom{{Ap}}')
				description = row['Description']
				
				note = CMEDescribeNote(arguments=[label])
				
				page = Minipage(arguments=pylatex.NoEscape('1\\columnwidth'),options=[pylatex.NoEscape('t][0.5in')])
				cols = Multicols(arguments=[2])
				items = pylatex.Description()
				items.add_item('Type',name)
				if 'Level' in row:
					items.add_item('Level',row['Level'])
				cols.append(items)
				page.append(cols)
				note.append(page)
				
				page = Minipage(arguments=pylatex.NoEscape('1\\columnwidth'),options=[pylatex.NoEscape('t][0.5in')])
				items = pylatex.Description()
				items.add_item('Objective',description)
				page.append(items)
				note.append(page)
				
				note.append(tcbsubtitle(arguments=['Description and Application']))
				note.append(tcblower())
				note.append(tcbsubtitle(arguments=['Significance and Connections']))
				
				note.dump(fh)
				pylatex.basic.NewPage().dump(fh)


def find_tree(objectives_file,module):
	# Read sheet and set index to Title
	sheet = pandas.read_excel(objectives_file,sheet_name='Skill-set',dtype={'Level':str}).set_index('Title')
	sheet['Requires'] = sheet['Requires'].fillna('')
	
	# Find all groups
	groups = sorted(list(sheet['Group'].unique()))
	
	# Find current module titles: tree trunk
	trunk_mask = sheet['Module'].astype(str).str.replace('E','')==module
	trunk_titles = sorted(map(str.strip,sheet[trunk_mask].index))
	# print(trunk_titles)
	
	# Find titles required by current module: tree roots
	root_titles = sheet.loc[trunk_titles]['Requires'].str.split(',').sum()
	root_titles = sorted(list(set(map(str.strip,root_titles))))
	root_titles = [title for title in root_titles if not (title in trunk_titles)]
	root_titles = [title for title in root_titles if not (title=='')]
	# print(root_titles)
	
	# Find titles which require current module: tree leaves
	in_trunk = lambda titles: any([title in map(str.strip,titles) for title in trunk_titles])
	leaf_mask = sheet['Requires'].str.split(',').apply(in_trunk)
	leaf_titles = sorted([title for title in map(str.strip,sheet[leaf_mask].index)])
	leaf_titles = sorted([title for title in leaf_titles if not (title in trunk_titles)])
	leaf_titles = sorted([title for title in leaf_titles if not (title in root_titles)])
	leaf_titles = sorted([title for title in leaf_titles if not (title=='')])
	# print(leaf_titles)
	
	# Package node lists
	nodes = {
		'root':sheet.loc[root_titles],
		'trunk':sheet.loc[trunk_titles],
		'leaf':sheet.loc[leaf_titles],
		}
	
	# Edges from root to trunk
	trunk_edges = {
		trunk:[
			title for title in map(str.strip,sheet.loc[trunk]['Requires'].split(','))
			if not (title=='')
			]
		for trunk in trunk_titles
		}
	# print(trunk_edges)
	
	leaf_edges = {
		leaf:[
			title for title in map(str.strip,sheet.loc[leaf]['Requires'].split(','))
			if (title in trunk_titles) and not (title=='')
			]
		for leaf in leaf_titles
		}
	# print(leaf_edges)
	edges = trunk_edges | leaf_edges
	return nodes,edges,groups


def build_tree(nodes,edges,groups,dot_file):
	graph = Graphs.build_objectives(nodes,edges,groups)
	graph.save(dot_file)


def build_notes(objectives,tex_file):
	'''
	Build TeX file for all objectives board notes
	'''
	
	class CMEBoardNote(pylatex.base_classes.Environment):
		_latex_name = 'CMEBoardNote'
		packages = [pylatex.Package('tcolorbox')]
		escape = False
		content_separator = '\n'
	
	class tcblower(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	class tcbsubtitle(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	class Multicols(pylatex.base_classes.Environment):
		_latex_name = 'multicols'
		packages = [pylatex.Package('multicols')]
		escape = False
		content_separator = '\n'
	
	class Minipage(pylatex.base_classes.Environment):
		_latex_name = 'minipage'
		escape = False
		content_separator = '\n'
	
	with open(tex_file,'w') as fh:
		for (name,sheet) in objectives.items():
			pylatex.Section(name).dump(fh)
			for (k,row) in sheet.iterrows():
				icon = 'design'
				if 'Group' not in row:
					icon = 'principle'
				elif row['Group'] in ['Curiosity','Connections','CreateValue','Basic']:
					icon = row['Group'].lower()
				elif row['Module'].startswith('M'):
					icon = 'math'
				elif row['Level'] in [1,2,3]:
					level = row['Level']
					icon = f'skill{level}'
				
				graphics = f'\\includegraphics[height=1.2em]{{../../Tooling/Icons/{icon}}}'
				title = row['Title']
				label = pylatex.NoEscape(f'{{{graphics}\\hspace{{1ex}}{title}}}\\vphantom{{Ap}}')
				description = row['Description']
				
				note = CMEBoardNote(arguments=[label])
				
				page = Minipage(arguments=pylatex.NoEscape('1\\columnwidth'),options=[pylatex.NoEscape('t][0.5in')])
				cols = Multicols(arguments=[2])
				items = pylatex.Description()
				items.add_item('Type',name)
				if 'Level' in row:
					items.add_item('Level',row['Level'])
				page.append(cols)
				note.append(page)
				
				page = Minipage(arguments=pylatex.NoEscape('1\\columnwidth'),options=[pylatex.NoEscape('t][0.5in')])
				items = pylatex.Description()
				items.add_item('Description',description)
				page.append(items)
				note.append(page)
				
				note.append(tcbsubtitle(arguments=['Activity Plan']))
				note.append(tcblower())
				note.append(tcbsubtitle(arguments=['Board Plan']))
				
				note.dump(fh)
				pylatex.basic.NewPage().dump(fh)
		legend = build_legend()
		legend.dump(fh)


def build_invoice(objectives,tex_file):
	'''
	Build TeX file for module invoice
	'''
	
	with open(tex_file,'w') as fh:
		fh.write('\\newcommand{\\LearningObjective}[1]{%\n')
		fh.write('\\ChoiceMenu[combo,maxlen=37,name=combo-#1,height=1.5em,bordercolor=C0]{}{%\n')
		fh.write(37*'\\_'+'=0\n')
		for (name,sheet) in objectives.items():
			if 'skill' not in name.lower():
				continue
			for row in sheet.itertuples():
				points = 2**int(row.Level)
				fh.write(f'{points}| {row.Title}={row.Index+1},\n')
		fh.write('}}\n')


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to manage objectives'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('objectives_file',help='Objectives file name')
	
	group = parser.add_mutually_exclusive_group()
	
	hlp = 'List all modules in file'
	group.add_argument('--modules',action='store_true',help=hlp)
	
	hlp = 'Build objectives list for MODULE and save as TeX FILE'
	group.add_argument('--objectives',nargs=2,metavar=('MODULE', 'FILE'),help=hlp)
	
	hlp = 'Build board notes for MODULE and save as TeX FILE'
	group.add_argument('--notes',nargs=2,metavar=('MODULE', 'FILE'),help=hlp)
	
	hlp = 'Build invoice for MODULE and save as TeX FILE'
	group.add_argument('--invoice',nargs=2,metavar=('MODULE', 'FILE'),help=hlp)
	
	hlp = 'Build describe sheets for MODULE and save as TeX FILE'
	group.add_argument('--describe',nargs=2,metavar=('MODULE', 'FILE'),help=hlp)
	
	hlp = 'Build objectives graph for MODULE and save as dot FILE'
	group.add_argument('--tree',nargs=2,metavar=('MODULE', 'FILE'),help=hlp)
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	objectives_file = args.objectives_file
	
	if args.modules:
		modules = find_modules(objectives_file)
		print_modules(modules)
	elif args.objectives:
		module,tex_file = args.objectives
		objectives = find_objectives(objectives_file,module)
		build_objectives(objectives,tex_file)
	elif args.notes:
		module,tex_file = args.notes
		objectives = find_objectives(objectives_file,module)
		build_notes(objectives,tex_file)
	elif args.invoice:
		module,tex_file = args.invoice
		objectives = find_objectives(objectives_file,module)
		build_invoice(objectives,tex_file)
	elif args.describe:
		module,tex_file = args.describe
		objectives = find_objectives(objectives_file,module)
		build_describe(objectives,tex_file)
	elif args.tree:
		module,dot_file = args.tree
		nodes,edges,groups = find_tree(objectives_file,module)
		build_tree(nodes,edges,groups,dot_file)


if __name__=='__main__': main()
