import binascii
import os
import sys
from shutil import copyfile
import string

print("#This tool was made with Python version 3.0, any older version will cause problems.")

def get_name(data, index):
	name = ''
	while True:
		letter = data[index]
		if letter != 0:
			letter = chr(letter)
			if (string.digits + string.ascii_letters + '_' + ':').find(letter) >= 0:
				name += letter
		else:
			break
		index-=1
	return name[::-1]


def create_materials(names, model):
	data = b''
	#newmtl metalRail_01 0A map_Kd barrel\\metalRail1.png 0A
	material_name = names[0].encode('utf-8') + b'.mtl'
	for name in names:
		path = os.path.basename(folder_path) + '\\' + name + '.png'
		path = path.replace(':', '_')
		path = path.encode('utf-8')
		data += b'\x0A' + b'newmtl ' + name.encode() + b'\x0A' + b'map_Kd ' + path + b'\x0A'

	with open(folder_path + '\\' + material_name.decode().replace(':', '_'), 'wb') as file:
		file.write(data)

	data = b''
	with open(model + '.obj', 'rb') as file:
		data = b'mtllib ' + material_name.decode().replace(':', '_').encode() + b'\x0A' + file.read()

	os.system('del ' + model + '.obj')

	with open(os.path.dirname(model) + '\\' + names[0].replace(':', '_') + '.obj', 'wb') as file:
		file.write(data)

#Validate
args = sys.argv
if len(args) <= 1:
	print("Error: Please specify a model file, ie: main.py file folder")
	sys.exit(-1)
elif len(args) <= 2:
	print("Error: Please specify a destination folder, ie: main.py file folder")
	sys.exit(-1)

file_path = args[1].strip().replace('"', '')
folder_path = args[2].strip().replace('"', '')

if os.path.isfile(file_path) == False:
	print("Error: File not found! ", file_path)
	sys.exit(-1)
elif os.path.isdir(folder_path) == False:
	print("Error: Folder not found! ", folder_path)
	sys.exit(-1)


with open(file_path, 'rb') as file:
	index = file.read().find(b'MTRL')
	if index < 0:
		print("Error: This is not a valid model file!")
		sys.exit(-1)

	file.seek(index)
	data = file.read()

	#Convert model file
	print("Log: Converting model file...")
	copyfile(file_path, folder_path + '\\' + os.path.basename(file_path))
	os.chdir('./model_extractor')
	os.system('DKTZModelExporter.exe ' + folder_path + '\\' + os.path.basename(file_path))

	texture_count = data.count(b'DIFT')
	if texture_count <= 0:
		print("Log: No texture refrences were found.")
		print("Log: Program finished.")
		sys.exit(-1)

	textures = {}

	print("Log: Found {} required textures...".format(texture_count))
	for i in range(texture_count):

		index = data.find(b'DIFT')
		name = get_name(data, index - 0x1e)
		index += 8
		asset_id = binascii.hexlify(data[index : index + 0x10])
		data = data[index+1:]

		textures[name]={'name' : name, 'id' : asset_id}

	print("Log: Looking for the textures in the directory of the model file...")
	texture_names = []
	for k,v in enumerate(textures):
		name = v
		texture_names.append(name)
		_id = textures[v]['id'].decode() + '.TXTR'
		directory = os.path.dirname(file_path)

		if os.path.isfile(directory + '\\' + _id):
			print("Log: Copying {} to destination folder...".format(name))
	
			#Copy the texture to the dest folder
			copyfile(directory + '\\' + _id, folder_path + '\\' + name.replace(':', '_') + '.TXTR')

		else:
			print("Warning: Could not find {} Skipping...".format(_id))

	create_materials(texture_names, folder_path + '\\' + os.path.basename(file_path))

os.chdir('../txtr_extractor')
os.system('mass_convert.py ' + folder_path)
os.system('del ' + folder_path + '\\' + os.path.basename(file_path))

print("Log: Program finished.")