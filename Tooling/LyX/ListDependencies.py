'''
Program to find and list all dependencies for a LyX file.
Output format is intended for consumption by CMake as a list of files.
'''

import argparse
import pathlib


def find_filenames(filepath,document_root,excludes=[]):
	'''
	Find all the paths a LyX file depends on
	'''
	
	def keep_line(line):
		'''
		Decide if line contains an included file path
		'''
		keep = False
		keep |= line.startswith('filename')
		keep |= line.startswith('\\input{')
		keep |= line.startswith('\\include{')
		return keep
	
	def find_path(line):
		'''
		Extract path from line with filename
		'''
		banned = '\'\"{}'
		text = ''.join([c if c not in banned else ' ' for c in line])
		name = pathlib.Path(text.split()[-1])
		path = filepath.parent.joinpath(name).resolve().relative_to(document_root)
		
		if ('\\include' in text) or ('\\input' in text) and path.suffix=='':
			path = path.with_suffix('.tex')
		
		return path
	
	# Open LyX file and read contents
	with open(filepath) as handle:
		lines = [line.strip() for line in handle.readlines()]
	
	# Extract the relevant paths
	refpaths = [find_path(line) for line in lines if keep_line(line)]
	
	# If needed, recursively search included files for more includes
	for path in refpaths:
		if path in excludes or path.suffix != '.lyx': continue
		refpaths += find_filenames(path,document_root,refpaths)
	
	return refpaths


def print_paths(paths):
	'''
	Print list of paths in semicolon separated list without newline
	'''
	text = ';'.join(f'{path}' for path in paths)
	print(text,end='')


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Process a LyX file into a dependency list for cmake'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('filename',help='LyX document to process')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	filepath = pathlib.Path(args.filename)
	# Get document root directory
	document_root = pathlib.Path(__file__).parent.parent.parent
	
	paths = find_filenames(filepath,document_root)
	unique_paths = sorted(list(set(paths)))
	print_paths(unique_paths)


if __name__=='__main__': main()
