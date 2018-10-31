import os
import sys
import glob

args = sys.argv
if len(args) <= 1:
	print("Error: Please specify a souce folder, ie: main.py folder")
	exit(-1)
path = args[1].strip().lower().replace('"', '')
if os.path.isdir(path) == False:
	print("Error: Folder not found! ", path)
	exit(-1)

files = glob.glob(path + '\\*.TXTR')
if len(files) <= 0:
	print("Error: No TXTR files were found!")
	exit(-1)

for f in files:
	os.system('"convert.py" ' + f)