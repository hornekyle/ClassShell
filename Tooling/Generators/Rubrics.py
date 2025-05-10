import argparse
import pandas
import pylatex


def find_rubrics(rubrics_file):
	'''
	Find all rubrics (sheets) in file
	'''
	sheets = pandas.read_excel(rubrics_file,sheet_name=None)
	
	rubrics = sorted(list(sheets.keys()))
	return rubrics


def print_rubrics(rubrics):
	'''
	Print rubrics list in format suitable for CMake
	'''
	text = ';'.join([f'{rubric}' for rubric in rubrics])
	print(text,end='')


def find_criteria(rubrics_file,rubric):
	'''
	Extract rubric data from sheet
	'''
	comment = pandas.read_excel(rubrics_file,sheet_name=rubric,nrows=1,header=None).values.flatten()[0]
	print(comment)
	
	sheet = pandas.read_excel(rubrics_file,sheet_name=rubric,dtype={'Points':'Int64'},skiprows=1).ffill()
	
	criteria = {}
	for criterion in sheet['Criterion'].unique():
		mask = sheet['Criterion']==criterion
		data = sheet[mask]
		description = data['Description'].dropna().values[0]
		proficiencies = data[['Points','Justification']].dropna().set_index('Points').squeeze().to_dict()
		proficiencies = {int(key):val for (key,val) in proficiencies.items()}
		proficiencies = {key:proficiencies[key] for key in reversed(sorted(proficiencies.keys()))}
		
		criteria[(criterion,description)] = proficiencies
	return criteria,comment


def build_rubric(criteria,comment,tex_file):
	'''
	Build TeX file including all criteria in rubric
	'''
	
	class CMERubricCriterion(pylatex.base_classes.Environment):
		_latex_name = 'CMERubricCriterion'
		packages = [pylatex.Package('tcolorbox')]
		escape = False
		content_separator = '\n'
	
	class CustomItemize(pylatex.Description):
		_latex_name = 'itemize'
	
	class tcblower(pylatex.base_classes.CommandBase):
		packages = [pylatex.Package('tcolorbox')]
	
	class CriterionPoints(pylatex.base_classes.CommandBase):
		_latex_name = 'CriterionPoints'
		packages = [pylatex.Package('tcolorbox')]
	
	with open(tex_file,'w') as fh:
		pylatex.Section('Rubric').dump(fh)
		fh.write(f'{comment}\n')
		for ((criterion,description),proficiencies) in criteria.items():
			box = CMERubricCriterion(options=criterion)
			box.append(description)
			box.append(tcblower())
			with box.create(CustomItemize()) as listing:
				for (points,justification) in proficiencies.items():
					listing.add_item(CriterionPoints(points),justification)
			box.dump(fh)


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to manage rubrics'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('rubrics_file',help='Rubrics file name')
	
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--rubrics',action='store_true',help='List all rubrics in file')
	group.add_argument('--build',nargs=2,metavar=('RUBRIC', 'FILE'),help='Build rubric for RUBRIC and save as TeX FILE')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	rubrics_file = args.rubrics_file
	
	if args.rubrics:
		rubrics = find_rubrics(rubrics_file)
		print_rubrics(rubrics)
	elif args.build:
		rubric,tex_file = args.build
		criteria,comment = find_criteria(rubrics_file,rubric)
		build_rubric(criteria,comment,tex_file)


if __name__=='__main__': main()
