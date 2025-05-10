import argparse
import dataclasses
import pathlib
from shutil import copyfile


@dataclasses.dataclass(frozen=True)
class RecentFile:
	file_name: str
	
	def __str__(self):
		return f'{self.file_name}'


@dataclasses.dataclass(frozen=True)
class LastOpenedFile:
	order: str
	file_name: str
	
	def __str__(self):
		terms = [self.order,self.file_name]
		text = ', '.join(str(txt) for txt in terms)
		return text


@dataclasses.dataclass(frozen=True)
class CursorPositionFile:
	pos_1: str
	pos_2: str
	file_name: str
	
	def __str__(self):
		terms = [self.pos_1,self.pos_2,self.file_name]
		text = ', '.join(str(txt) for txt in terms)
		return text


@dataclasses.dataclass(frozen=True)
class BookmarkFile:
	pos_1: str
	pos_2: str
	pos_3: str
	file_name: str
	
	def __str__(self):
		terms = [self.pos_1,self.pos_2,self.pos_3,self.file_name]
		text = ', '.join(str(txt) for txt in terms)
		return text


@dataclasses.dataclass(frozen=True)
class ShellEscapeFile:
	file_name: str
	set_flag: str
	
	def __str__(self):
		terms = [self.file_name,self.set_flag]
		text = ','.join(str(txt) for txt in terms)
		return text


class SessionFile:
	def __init__(self,file_name):
		fh = open(file_name,'r')
		lines = fh.readlines()
		lines.append('\n')
		fh.close()
		
		self.recent_files = self.extract(lines,'[recent files]',RecentFile)
		self.last_open_files = self.extract(lines,'[last opened files]',LastOpenedFile)
		self.cursor_position_files = self.extract(lines,'[cursor positions]',CursorPositionFile)
		self.bookmark_files = self.extract(lines,'[bookmarks]',BookmarkFile)
		self.shell_escape_files = self.extract(lines,'[shell escape files]',ShellEscapeFile)
	
	@staticmethod
	def extract(lines,header,init):
		field_count = len(init.__dataclass_fields__)
		output = []
		lk = lines.index(header+'\n')+1
		while lines[lk] != '\n':
			token_list = lines[lk].strip().split(',')
			args_list = [ token_list[tk].strip() for tk in range(field_count-1) ]
			args_list.append( (','.join(token_list[field_count-1:])).strip() )
			output.append(init(*args_list))
			lk += 1
		return output
	
	def write_file(self,file_name):
		lines = [
			'## Automatically generated lyx session file ',
			'## Editing this file manually may cause lyx to crash.',
			'',
			]
		
		heading_list = [
			'recent files',
			'last opened files',
			'cursor positions',
			'last commands',
			'bookmarks',
			'auth files',
			'shell escape files'
			]
		contents_list = [
			self.recent_files,
			self.last_open_files,
			self.cursor_position_files,
			[],
			self.bookmark_files,
			[],
			self.shell_escape_files
			]
		
		for (heading,contents) in zip(heading_list,contents_list):
			lines += ['[%s]'%heading]
			for entry in contents:
				lines += [str(entry)]
			lines += ['']
		
		for k in range(len(lines)):
			lines[k] += '\n'
		lines.pop()
		
		fh = open(file_name,'w')
		fh.writelines(lines)
		fh.close()
	
	def add_shell_file(self,file_name):
		new_file_on  = ShellEscapeFile(file_name,'1')
		new_file_off = ShellEscapeFile(file_name,'0')
		
		if new_file_off in self.shell_escape_files:
			self.shell_escape_files.remove(new_file_off)
		if new_file_on not in self.shell_escape_files:
			self.shell_escape_files.append(new_file_on)


def authorize_file(target_file,session_file='~/.lyx/session'):
	session_path = pathlib.Path(session_file).expanduser().resolve()
	copyfile(session_path,pathlib.Path(f'{session_path}'+'_backup'))
	session = SessionFile(session_path)
	session.add_shell_file(target_file)
	session.write_file(session_path)


def parse_arguments():
	'''
	Parse program arguments
	'''
	desc = 'Authorize a LyX file for shell escape'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('filename',help='LyX document to process')
	
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	authorize_file(pathlib.Path(args.filename).resolve())


if __name__=='__main__': main()
