import argparse
import pandas
import pylatex


def find_modules(definitions_file):
	'''
	Find all modules referenced in any sheet within the file
	'''
	sheets = pandas.read_excel(definitions_file,sheet_name=None,dtype={'Module':str})
	
	modules = []
	for (name,sheet) in sheets.items():
		duplicated = list(sheet['Module'].unique())
		modules += duplicated
	modules = sorted(list(set(modules)))
	return modules


def print_modules(modules):
	'''
	Print module list in format suitable for CMake
	'''
	text = ';'.join([f'{module}' for module in modules ])
	print(text,end='')


def find_definitions(definitions_file,module):
	'''
	Find all definitions in module
	'''
	sheets = pandas.read_excel(definitions_file,sheet_name=None,dtype={'Module':str})
	
	definitions = {}
	for (name,sheet) in sheets.items():
		mask = sheet['Module']==module
		definitions[name] = sheet[mask]
	
	return definitions


def build_definitions(definitions,tex_file):
	'''
	Build TeX file including all definitions in module
	'''
	introduction = [
		'Function and term definitions play an important role in computer programming.',
		'Interpreting messages from the Python interpreter require knowledge of both.',
		'Make sure to review this section of each module to keep up with language needs.',
		]
	reasons = {
		'Vocabulary':[
			'Students have reported difficulty keeping track of the various terms used in this course.',
			'To reduce this difficulty and support student success, this vocabulary section has been added.',
			'Look here for unfamiliar terms, or terms used in a novel sense.',
			'Recommendations for additions to this list are welcome!',
			],
		'Functions':[
			'Python provides many standard functions which are always available for use.',
			'Additionally, various packages provide yet more functions which see frequent use.',
			'Consider each function listed here and the various potential uses they might have.',
			],
		}
	with open(tex_file,'w') as fh:
		pylatex.Section('Definitions').dump(fh)
		for line in introduction:
			fh.write(f'{line}\n')
		for (name,sheet) in definitions.items():
			if sheet.shape[0]==0:
				continue
			pylatex.Subsection(name).dump(fh)
			for line in reasons[name]:
				fh.write(f'{line}\n')
			items = pylatex.Description()
			for (k,row) in sheet.iterrows():
				label = row[row.index[0]]
				text = row[row.index[2]]
				items.add_item(label,pylatex.NoEscape(text))
			items.dump(fh)


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to manage definitions'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('definitions_file',help='Definitions file name')
	
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--modules',action='store_true',help='List all modules in file')
	group.add_argument('--build',nargs=2,metavar=('MODULE', 'FILE'),help='Build definitions for MODULE and save as TeX FILE')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	definitions_file = args.definitions_file
	
	if args.modules:
		modules = find_modules(definitions_file)
		print_modules(modules)
	elif args.build:
		module,tex_file = args.build
		definitions = find_definitions(definitions_file,module)
		build_definitions(definitions,tex_file)


if __name__=='__main__': main()
