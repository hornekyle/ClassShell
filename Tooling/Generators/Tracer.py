import importlib.util
import sys
import pathlib
import trace
import graphviz
from io import StringIO
import os


class Capturing(list):
	def __enter__(self):
		self._stdout = sys.stdout
		sys.stdout = self._stringio = StringIO()
		return self
	
	def __exit__(self, *args):
		self.extend(self._stringio.getvalue().splitlines())
		del self._stringio # free up some memory
		sys.stdout = self._stdout


def is_script(path):
	if path.suffix!='.py':
		return False
	
	def test(line):
		text = line.replace('\'','"')
		mangled = ''.join(text.split())
		flag = mangled.startswith('if__name__=="__main__"')
		return flag
	
	with open(path) as handle:
		flags = [test(line) for line in handle.readlines()]
	
	flag = any(flags)
	return flag


def collect_paths(script_file):
	script_path = pathlib.Path(script_file).absolute()
	
	other_paths = [
		path for path in script_path.parent.glob('*.py')
		if (path!=script_path) and not is_script(path)
		]
	
	return script_path,other_paths


def import_file(file_path):
	module_name = file_path.stem
	spec = importlib.util.spec_from_file_location(module_name,file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module
	spec.loader.exec_module(module)
	return module


def expand_excludedirs(excludedirs):
	paths = []
	for directory in excludedirs:
		for packed in os.walk(directory):
			dirpath = pathlib.Path(packed[0])
			paths.append(dirpath)
	return paths


def run_trace(function):
	tracer = trace.Trace(count=False,trace=False,countcallers=True)
	
	with Capturing() as redirect:
		tracer.runfunc(function,)
	
	stdout = [line for line in redirect]
	results = tracer.results()
	return results,stdout


def parse_trace(trace,excludedirs):
	order = []
	functions = {}
	calls = {}
	
	for (key,val) in trace.callers.items():
		(cpath,cmodule,cfunction),(path,module,function) = key
		tests = [
			cmodule=='trace', # skip self
			pathlib.Path(path).parent in excludedirs, # skip internals
			pathlib.Path(cpath).parent in excludedirs, # skip internals
			not path.startswith('/tmp'),
			not cpath.startswith('/tmp'),
			f'{pathlib.Path(path)}'.startswith('<'), # skip internal packages
			]
		if any(tests): continue
		
		context = (cmodule,cfunction)
		target = (module,function)
		
		call = (context,target)
		order.append(call)
		
		if target not in functions:
			functions[target] = 0
		
		if context not in functions:
			functions[context] = 1
		
		if context not in calls:
			calls[context] = {}
		
		if target not in calls[context]:
			calls[context][target] = 0
		
		functions[target] += val
		calls[context][target] += val
	
	return functions,calls,order


def process_file(script_file):
	excludedirs = expand_excludedirs(sys.path[1:])
	
	sys.dont_write_bytecode = True
	script_path,other_paths = collect_paths(script_file)
	
	other_modules = []
	while len(other_modules)<len(other_paths):
		for path in other_paths:
			try:
				other_modules.append(import_file(path))
				print(f'Loaded module in path: {path}')
			except:
				print(f'Failed to load module in path {path}')
	main_module = import_file(script_path)
	
	function = getattr(main_module,'main')
	trace,stdout = run_trace(function)
	functions,calls,order = parse_trace(trace,excludedirs)
	
	output = {
		'functions':functions,
		'calls':calls,
		'order':order,
		'stdout':stdout,
		}
	
	return output
