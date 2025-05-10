'''
Program to find and list plots in sub directories from location of this file.
Output format is intended for consumption by CMake as a dictionary of lists of files.
'''

import argparse
import zipimport
import pathlib
import os


def find_scripts(basedir):
	'''
	Find all script files in local directories
	'''
	
	scripts = {}
	for packed in os.walk(basedir):
		path = pathlib.Path(packed[0])
		filenames = [pathlib.Path(p) for p in packed[-1]]
		# Skip root of directory tree; we don't want these scripts
		if basedir==path:
			continue
		
		# Add each file's name and output list to the return value
		for filename in filenames:
			filepath = path.relative_to(basedir).joinpath(pathlib.Path(filename))
			if filepath.suffix!='.pyz':
				continue
			
			# Manually import the script and run 'get_names'
			importer = zipimport.zipimporter(str(filepath))
			module_name = filepath.stem
			module = importer.load_module(module_name)
			interface = module.Interface()
			names = interface.get_names()
			
			scripts[filepath] = names
	
	return scripts


def print_scipts(scripts):
	'''
	Print dictionary of scripts.
	Key-value pairs as separated by a semicolon.
	List values are separated by a comma.
	'''
	codes = [
		f'{path}|'+','.join(names)
		for (path,names) in scripts.items()
		]
	text = ';'.join(codes)
	print(text,end='')


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to list plots'
	parser = argparse.ArgumentParser(description=desc)
	args = parser.parse_args()
	return args


def main():
	agrs = parse_arguments()
	basedir = pathlib.Path(__file__).parent
	scripts = find_scripts(basedir)
	print_scipts(scripts)


if __name__=='__main__': main()
