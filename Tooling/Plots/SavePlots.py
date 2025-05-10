'''
Program to run a plotting script and save its output to a target directory.
'''

import argparse
import zipimport
from pathlib import Path
import os

import FormatPlots


def build_figures(script_file):
	'''
	Manually import script and run parts to get plot names and figures.
	'''
	
	# Import script and build interface object
	filepath = Path(script_file)
	importer = zipimport.zipimporter(str(filepath))
	module_name = filepath.stem
	module = importer.load_module(module_name)
	interface = module.Interface()
	
	# Create figures
	figures = {
		k:v for (k,v) in
		zip(interface.get_names(),interface.get_figures(FormatPlots.pl))
		}
	return figures


def save_figures(output_root,script_file,figures):
	'''
	Save figures in appropriate location within plots root
	'''
	
	output_path = Path(output_root).joinpath(Path(script_file).with_suffix(''))
	for (name,figure) in figures.items():
		save_name = output_path.joinpath(Path(name))
		save_name.parent.mkdir(parents=True,exist_ok=True)
		figure.savefig(save_name.with_suffix('.svg'))
		figure.savefig(save_name.with_suffix('.pgf'))


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to build plots'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('script_file',help='Script file name')
	parser.add_argument('output_root',help='Root path for plot outputs')
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	figures = build_figures(args.script_file)
	save_figures(args.output_root,args.script_file,figures)



if __name__=='__main__': main()
