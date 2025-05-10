import argparse
import pandas
import json


def find_students(students_file):
	sheet = pandas.read_excel(students_file,index_col='Username',dtype='string')
	
	output = {}
	for (user,row) in sheet.iterrows():
		first = row['First']
		last = row['Last']
		section = row['Section']
		output[user] = (0,section,f'{first} {last}')
	
	return output


def build_page(students,template_file):
	with open(template_file) as handle:
		template = handle.read()
	
	insertion = {f'{user}':values for (user,values) in students.items()}
	text = json.dumps(insertion)
	
	replacements = {
		'{':'{\n\t\t\t',
		'}':'\n\t\t\t}',
		'], ':'],\n\t\t\t',
		', ':',\t',
		}
	for (token,value) in replacements.items():
		text = text.replace(token,value)
	
	html = template.replace('{FIXME}',text)
	
	return html


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Tool to build student call order page'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('students_file',help='Student list file name')
	parser.add_argument('template_file',help='Student list file name')
	parser.add_argument('output_file',help='Output HTML file')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	students = find_students(args.students_file)
	html = build_page(students,args.template_file)
	
	with open(args.output_file,'w') as handle:
		handle.write(html)


if __name__=='__main__': main()
