#encoding=utf-8

from os import system, getcwd, path, mkdir;
import webbrowser;

if not path.exists(getcwd()+"\\log"):
	mkdir('log');
system('python -V >log\\py_log');
f = open(getcwd() + '\\log\\py_log', 'r', encoding='utf-8');
lst = f.readlines();
content = str(lst);
if 'python 3' in content or 'Python 3' in content:
    # print('pass');
    if path.exists('trans.exe'):
	    while True:
	        system(getcwd() + '\\trans.exe');
    elif path.exists('trans.py'):
    	while True:
    		system('python trans.py');
else:
    print('Python\'s not installed! ');
    webbrowser.open("https://www.python.org/downloads");