import argparse
import pandas
import pylatex


def find_modules(questions_file):
	'''
	Find all modules referenced in any sheet within the file
	'''
	sheets = pandas.read_excel(questions_file,sheet_name=None,dtype={'Module':str})
	
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


def find_questions(questions_file,module):
	'''
	Find all questions in module
	'''
	
	questions = {}
	sheets = pandas.read_excel(questions_file,sheet_name=None,dtype={'Module':str})
	for (name,sheet) in sheets.items():
		mask = sheet['Module']==module
		questions[name] = sheet[mask]
	
	return questions


def build_questions(questions,tex_file):
	'''
	Build TeX file including all questions in module
	'''
	
	class ICMQuestion(pylatex.base_classes.Environment):
		_latex_name = 'ICMQuestion'
		packages = [pylatex.Package('tcolorbox')]
		escape = False
		content_separator = '\n'
	
	class tcblower(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	with open(tex_file,'w') as fh:
		for (sheet,data) in questions.items():
			for (idx,row) in data.iterrows():
				text = row['Question']
				responses = row['Responses']
				
				args = [responses,'0.5in',sheet]
				question = ICMQuestion(arguments=args)
				question.append(text)
				question.append(tcblower())
				question.dump(fh)
		


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to manage questions'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('questions_file',help='Definitions file name')
	
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--modules',action='store_true',help='List all modules in file')
	group.add_argument('--build',nargs=2,metavar=('MODULE', 'FILE'),help='Build questions for MODULE and save as TeX FILE')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	questions_file = args.questions_file
	
	if args.modules:
		modules = find_modules(questions_file)
		print_modules(modules)
	elif args.build:
		module,tex_file = args.build
		questions = find_questions(questions_file,module)
		build_questions(questions,tex_file)


if __name__=='__main__': main()
