import argparse
import pylatex
import pathlib
import tempfile
import os
import pickle

import Tracer
import Graphs


def find_solutions(root_path):
	'''
	Find all solution folders in this path
	'''
	solutions = sorted([
		f'{child.relative_to(root_path)}'
		for child in root_path.iterdir()
		])
	
	return solutions


def print_solutions(solutions):
	'''
	Print solution list in format suitable for CMake
	'''
	text = ';'.join([f'{solution}' for solution in solutions])
	print(text,end='')


def dump_data(file_path):
	with open(file_path,'rb') as handle:
		data = handle.read()
	return data


def create_trace(root_path):
	original_path = root_path.cwd()
	trace = {}
	
	for assignment_path in sorted(root_path.iterdir()):
		results = {}
		initial_files = {}
		
		with tempfile.TemporaryDirectory() as tmp:
			tmp_path = pathlib.Path(tmp)
			
			for file_path in assignment_path.iterdir():
				initial_files[file_path.name] = dump_data(file_path)
				
				sym_path = tmp_path.joinpath(file_path.relative_to(assignment_path))
				sym_path.symlink_to(file_path.absolute())
			
			os.chdir(tmp_path)
			for file_path in sorted(pathlib.Path('.').iterdir()):
				if not Tracer.is_script(file_path):
					continue
				
				results[file_path.name] = Tracer.process_file(file_path)
			
			generated_files = {
				file_path.name:dump_data(file_path)
				for file_path in tmp_path.iterdir()
				if file_path.name not in initial_files
				}
			
		os.chdir(original_path)
		
		trace[assignment_path.name] = {
			'initial':initial_files,
			'generated':generated_files,
			'results':results,
			}
	
	return trace


def build_latex(source_files,outputs,tex_handle):
	handlers = {
		'.py':python_handler,
		'.tex':tex_handler,
		'.pgf':tex_handler,
		'.pdf':pdf_handler,
		'.png':png_handler,
		}
	
	for (file_name,file_contents) in source_files.items():
		ext = pathlib.Path(file_name).suffix
		
		if ext in handlers:
			handlers[ext](file_name,file_contents,outputs,tex_handle)


class CMESolutionListing(pylatex.base_classes.Environment):
	_latex_name = 'CMESolutionListing'
	packages = [pylatex.Package('tcolorbox')]
	escape = False
	content_separator = '\n'


class minted(pylatex.base_classes.Environment):
	packages = [pylatex.Package('minted')]
	escape = False
	content_separator = '\n'


def python_handler(file_name,file_contents,outputs,tex_handle):
	block = CMESolutionListing(arguments=file_name)
	opts = [
		pylatex.NoEscape('fontsize=\\footnotesize'),
		'showtabs=true',pylatex.NoEscape('tab=\\rightarrowfill'),'tabsize=2','tabcolor=gray',
		'showspaces=true',pylatex.NoEscape('space=\\textbullet'),'spacecolor=gray',
		]
	code = minted(arguments='python',options=opts)
	code.append(file_contents.decode('utf8'))
	block.append(code)
	
	if file_name in outputs:
		output = outputs[file_name]
		block.append(pylatex.Command('tcblower'))
		opts = [
			pylatex.NoEscape('fontsize=\\footnotesize'),
			'showtabs=true',pylatex.NoEscape('tab=\\rightarrowfill'),'tabsize=2','tabcolor=gray',
			'showspaces=true',pylatex.NoEscape('space=\\textbullet'),'spacecolor=gray',
			]
		code = minted(arguments='text',options=opts)
		code.append('\n'.join(output))
		block.append(code)
	
	# pylatex.basic.NewPage().dump(tex_handle)
	block.dump(tex_handle)
	tex_handle.write('\n\n')


def tex_handler(file_name,file_contents,outputs,tex_handle):
	block = CMESolutionListing(arguments=file_name)
	block.append(file_contents.decode('utf8'))
	block.dump(tex_handle)
	tex_handle.write('\n\n')


def pdf_handler(file_name,file_contents,outputs,tex_handle):
	block = CMESolutionListing(arguments=file_name)
	destination = pathlib.Path(tex_handle.name).parent.joinpath(file_name)
	target = pathlib.Path(tex_handle.name).parent.name
	with open(destination,'wb') as fh:
		fh.write(file_contents)
	block.append(pylatex.figure.StandAloneGraphic(f'../../Build/Solutions/{target}/{file_name}'))
	block.dump(tex_handle)
	tex_handle.write('\n\n')


def png_handler(file_name,file_contents,outputs,tex_handle):
	block = CMESolutionListing(arguments=file_name)
	destination = pathlib.Path(tex_handle.name).parent.joinpath(file_name)
	target = pathlib.Path(tex_handle.name).parent.name
	with open(destination,'wb') as fh:
		fh.write(file_contents)
	block.append(pylatex.figure.StandAloneGraphic(f'../../Build/Solutions/{target}/{file_name}'))
	block.dump(tex_handle)
	tex_handle.write('\n\n')


def parse_arguments():
	'''
	Parse program arguments
	'''
	
	desc = 'Tool to manage solutions'
	parser = argparse.ArgumentParser(description=desc)
	
	group = parser.add_mutually_exclusive_group()
	
	hlp = 'Root path to search'
	group.add_argument('--solutions',nargs=1,metavar=('PATH'),help=hlp)
	
	hlp = 'Solution PATH for trace OUTPUT'
	group.add_argument('--trace',nargs=2,metavar=('PATH','OUTPUT'),help=hlp)
	
	hlp = 'Solution TRACE for callgraphs saved at PATH'
	group.add_argument('--callgraphs',nargs=2,metavar=('TRACE','PATH'),help=hlp)
	
	hlp = 'PATH for LaTeX files generated from TRACE'
	group.add_argument('--latex',nargs=2,metavar=('TRACE','PATH'),help=hlp)
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	
	if args.solutions:
		root_path = pathlib.Path(args.solutions[0])
		solutions = find_solutions(root_path)
		print_solutions(solutions)
	elif args.trace:
		path,output = [pathlib.Path(text) for text in args.trace]
		trace = create_trace(path)
		with open(output,'wb') as handle:
			pickle.dump(trace,handle)
	elif args.callgraphs:
		trace_path,output_path = [pathlib.Path(text) for text in args.callgraphs]
		
		with open(trace_path,'rb') as handle:
			trace = pickle.load(handle)
		
		for (name,assignment) in trace.items():
			functions = {}
			calls = {}
			
			for (file_name,results) in assignment['results'].items():
				functions |= results['functions']
				calls |= results['calls']
				
			graph = Graphs.build_callgraph(functions,calls)
			with open(output_path.joinpath(f'{name}.dot'),'w') as handle:
				handle.write(f'{graph}')
	elif args.latex:
		trace_path,latex_path = [pathlib.Path(text) for text in args.latex]
		
		with open(trace_path,'rb') as handle:
			trace = pickle.load(handle)
		
		for (name,assignment) in trace.items():
			
			with open(latex_path.joinpath(f'{name}.tex'),'w') as handle:
				pylatex.Section(f'Assignment: {name}').dump(handle)
				
				files = dict(sorted(assignment['initial'].items()))
				outputs = {file_name:result['stdout'] for (file_name,result) in assignment['results'].items()}
				if len(files)>0:
					# pylatex.Subsection('Source Files').dump(handle)
					build_latex(files,outputs,handle)
				
				files = dict(sorted(assignment['generated'].items()))
				if len(files)>0:
					# pylatex.Subsection('Generated Files').dump(handle)
					build_latex(files,outputs,handle)


if __name__=='__main__': main()
