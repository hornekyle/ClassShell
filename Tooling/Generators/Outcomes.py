#!/usr/bin/env python

import os
import argparse
import pandas


def buildOutcomes(module,objectivesFile,modulesFile,outputFile):
	objectives = pandas.read_excel(objectivesFile,dtype='str',sheet_name='Skill-set')
	topics = pandas.read_excel(modulesFile,dtype='str',sheet_name='Map',index_col=[0])
	
	topic = topics['Topic'][int(module)]
	
	mask = objectives['Module']==f'E{module}'
	columns = ['Title','Description']
	selection = objectives[mask][columns]
	
	title = list(selection['Title'].values)
	description = list(selection['Description'].values)
	N = len(title)
	
	code = 'XXX-20XXX'
	data = {
		'vendor_guid':[f'{code}-Module-{module}']+[f'{code}-{txt}' for txt in title],
		'object_type':['group']+N*['outcome'],
		'course_id':(N+1)*[''],
		'title':[f'Module-{module}']+title,
		'description':[topic]+description,
		'friendly_description':(N+1)*[''],
		'display_name':(N+1)*[''],
		'calculation_method':['']+N*['highest'],
		'calculation_int':(N+1)*[''],
		'parent_guids':['']+N*[f'{code}-Module-{module}'],
		'workflow_state':(N+1)*['active'],
		'mastery_points':['']+N*['2'],
		}
	header = [key for key in data.keys()]+['ratings']+(1+4*2)*['']
	for (k,letter) in enumerate('ABCDF'):
		data['ratings'+k*'_'] = ['']+N*[f'{4-k}']
		data['values'+k*'_'] = ['']+N*[f'{letter}']
	output = pandas.DataFrame.from_dict(data)
	output.to_csv(outputFile,index=False,header=header)


def parseArguments():
	desc = 'Tool build outcome spreadsheets'
	parser = argparse.ArgumentParser(description=desc)
	
	parser.add_argument('objectivesFile',help='Spreadsheet containing objectives')
	parser.add_argument('modulesFile',help='Spreadsheet containing modules map')
	parser.add_argument('outputFile',help='Path for root of output',default=None)
	
	return parser.parse_args()


def main():
	args = parseArguments()
	
	outputDir,fileName = os.path.split(args.outputFile)
	buildDir,module = os.path.split(outputDir)
	buildOutcomes(module,args.objectivesFile,args.modulesFile,args.outputFile)


if __name__=='__main__': main()
