from .minDistance import *
import subprocess

def grep(a):
	try:
		path = 'app/static/papers' #change to whatever path you want!
		output = subprocess.check_output('find {} -name \*.pdf | grep -i -E "{}" | grep -v "syllabus"'.format(path, a.decode()), shell = True)
		if(output == None): 
			raise Exception
		output = output.split('\n'.encode())
		return output
	except:
		output = subprocess.check_output('find app/static/papers -name \*.pdf', shell = True, stderr = subprocess.STDOUT)
		output = output.split('\n'.encode())
		vocab = []
		for i in output:
			j = i.split('/'.encode())
			for k in j:
				vocab.append(k)
		extras = ['nawp', ] #possible keyword that can be spelled incorrect and give output for grep command.
		vocab = vocab + extras
		vocab = list(set(vocab))
		new_word = mindistance(a, vocab)
		return grep(new_word)