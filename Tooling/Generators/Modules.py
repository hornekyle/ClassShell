import argparse
import pandas
import pathlib


def read_modules(modules_file):
	df = pandas.read_excel(modules_file,index_col='Module')
	
	output = {}
	for (module,row) in df.iterrows():
		output[f'{module:02d}'] = (row['Title'],row['Topic'])
	
	return output


def read_templates(templates_path):
	
	output = {}
	for file_path in templates_path.glob('*.lyx'):
		with open(file_path,'r') as handle:
			output[file_path.stem] = handle.read()
	
	return output


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to build course module files from templates'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('modules_file',help='Modules list file name')
	parser.add_argument('templates_path',help='TEMPLATE files path')
	parser.add_argument('outputs_path',help='OUTPUT files path')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	output_path = pathlib.Path(args.outputs_path)
	
	modules = read_modules(pathlib.Path(args.modules_file))
	templates = read_templates(pathlib.Path(args.templates_path))
	
	for (name,contents) in templates.items():
		for (module,(title,topic)) in modules.items():
			replacements = {
				'FIXME_MODULE':module,
				'FIXME_TITLE':title,
				'FIXME_TOPIC':topic,
				}
			
			file_title = title.replace('&','and')
			output_file = output_path.joinpath(f'{module}={file_title} -- {name}.lyx')
			output_contents = contents
			for (pattern,value) in replacements.items():
				output_contents = output_contents.replace(pattern,value)
			
			with open(output_file,'w') as handle:
				handle.write(output_contents)


if __name__=='__main__': main()
