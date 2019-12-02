#This program will map out a TXTR file from the Donkey Kong Tropical Freeze Game WiiU Version


import ctypes
import os
import struct

TEXTURE_INFORMATION = [{
    "MODES": {
        "0" : "Uncompressed",
        "1" : "8 Bit Compression",
        "2" : "16 Bit Compression",
        "3" : "32 Bit Compression"
    },
    "TEXTURE_TYPES" : {
        "0" : "1D Texture",
        "1" : "2D Texture",
        "2" : "3D Texture",
        "3" : "Cube Texture",
        "4" : "1D Texture Array",
        "5" : "2D Texture Array",
        "6" : "Multisampled 2D Texture",
        "7" : "Multisampled 2D Texture Array"
    },
    "TEXTURE_FILTERS" : {
        "0" : "GX2_TEX_MIP_FILTER_POINT",
        "1" : "GX2_TEX_MIP_FILTER_LINEAR"
    },
    "TEXTURE_WRAP" : {
        "0" : "GX2_TEX_CLAMP_CLAMP",
        "1" : "GX2_TEX_CLAMP_WRAP",
        "2" : "GX2_TEX_CLAMP_MIRROR",
        "3" : "GX2_TEX_CLAMP_MIRROR_ONCE"
    },
    "TEXTURE_FORMATS": [
        {
        "ID": "0x00",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R8_UNORM"
        },
        {
        "ID": "0x01",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R8_SNORM"
        },
        {
        "ID": "0x02",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R8_UINT"
        },
        {
        "ID": "0x03",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R8_SINT"
        },
        {
        "ID": "0x04",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCD_R16_UNORM"
        },
        {
        "ID": "0x05",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_SNORM"
        },
        {
        "ID": "0x06",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_UINT"
        },
        {
        "ID": "0x07",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_SINT"
        },
        {
        "ID": "0x08",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_FLOAT"
        },
        {
        "ID": "0x09",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R32_UINT"
        },
        {
        "ID": "0x0A",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R32_SINT"
        },
        {
        "ID": "0x0B",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_INVALID"
        },
        {
        "ID": "0x0C",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM"
        },
        {
        "ID": "0x0D",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB"
        },
        {
        "ID": "0x0E",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_G16_B16_A16_FLOAT"
        },
        {
        "ID": "0x0F",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R32_G32_B32_A32_FLOAT"
        },
        {
        "ID": "0x10",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCD_R16_UNORM"
        },
        {
        "ID": "0x11",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCD_R16_UNORM"
        },
        {
        "ID": "0x12",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_D_D24_S8_UNORM"
        },
        {
        "ID": "0x13",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCD_R32_FLOAT"
        },
        {
        "ID": "0x14",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC1_UNORM"
        },
        {
        "ID": "0x15",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC1_SRGB"
        },
        {
        "ID": "0x16",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC2_UNORM"
        },
        {
        "ID": "0x17",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC2_SRGB"
        },
        {
        "ID": "0x18",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC3_UNORM"
        },
        {
        "ID": "0x19",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC3_SRGB"
        },
        {
        "ID": "0x1A",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC4_UNORM"
        },
        {
        "ID": "0x1B",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC4_SNORM"
        },
        {
        "ID": "0x1C",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC5_UNORM"
        },
        {
        "ID": "0x1D",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_T_BC5_SNORM"
        },
        {
        "ID": "0x1E",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R11_G11_B10_FLOAT"
        },
        {
        "ID": "0x1F",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TCD_R32_FLOAT"
        },
        {
        "ID": "0x20",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R16_G16_FLOAT"
        },
        {
        "ID": "0x21",
        "GX2SurfaceFormat": "GX2_SURFACE_FORMAT_TC_R8_G8_UNORM"
        }
    ]
}]


#CLASSES--------------------
class Property:
	def __init__(self, offset, data_type, name, value=None):
		self.offset = offset
		self.name = name
		self.data_type = data_type
		self.byte_size = ctypes.sizeof(data_type)
		self.value = value

class Header:
	def __init__(self, magic_number):
		self.magic_number = magic_number
		self.size = 0
		self.offset = 0
		self.data = None
		self.properties = []

	def setProperties(self, properties):
		for p in properties:
			self.properties.append(p)
		self.updatePropertyValues()

	def updatePropertyValues(self):
		formats = {1 : '>B', 2 : '>H', 4 : '>I', 8 : '>Q'}
		for p in self.properties:
			if (p.value == None):
				p.value = struct.unpack(formats[p.byte_size], self.data[p.offset : p.offset + p.byte_size])[0]

	def viewProperties(self):
		print(self.magic_number)
		for p in self.properties:
			print('{}: {}'.format(p.name, p.value))

#FUNCTIONS----------------------
def collectHeaderData(file_path):
	with open(file_path, 'rb') as txtr_file:
		txtr_file.seek(0x14)
		magic_number = txtr_file.read(4)
		txtr_file.seek(63)
		file_version = txtr_file.read(1)
	
		if magic_number != b'TXTR':
			print("ERROR: This is not a valid TXTR file!")
			exit(-1)

		txtr_file.seek(0)
		data = txtr_file.read()

	#Setup the headers
	RFRM.size = data.find(HEAD.magic_number)
	RFRM.data = data[RFRM.offset : RFRM.size]

	HEAD.offset = RFRM.size
	HEAD.size = data.find(GPU.magic_number)
	HEAD.data = data[HEAD.offset : HEAD.size]

	GPU.offset = HEAD.size
	GPU.size = data.find(b'META')
	GPU.data = data[GPU.offset : GPU.size]

	META.offset = GPU.size
	META.size = (RFRM.size + HEAD.size + GPU.size) - len(data)
	META.data = data[META.offset : META.offset + META.size]

def setMipMapSizes():
	mipmap_property = HEAD.properties[7]
	mipmap_count = mipmap_property.value
	mipmap_offset = mipmap_property.offset-4
	mipmap_sizes = []

	data = HEAD.data
	for i in range(1, mipmap_count+1):
		current_offset = mipmap_offset + (i * 4)
		mipmap_sizes.append(data[current_offset : current_offset+4])

	mipmap_sizes_property = Property(mipmap_offset+4, ctypes.c_void_p, 'Mipmap Sizes')
	mipmap_sizes_property.value = mipmap_sizes
	mipmap_sizes_property.byte_size = mipmap_count * 4

	#Now update the rest of the header properties
	current_offset = current_offset+4
	HEAD.setProperties([
			mipmap_sizes_property,
			Property(current_offset, ctypes.c_uint8, 'Texture Filter'),
			Property(current_offset+1, ctypes.c_uint8, 'Texture Wrap X'),
			Property(current_offset+2, ctypes.c_uint8, 'Texture Wrap Y'),
			Property(current_offset+3, ctypes.c_uint8, 'Texture Wrap Z')
		])

def getBufferData(file_path):
	with open(file_path, 'rb') as target_file:
		data = target_file.read()
		raw_data_start = META.properties[2].value #The start of the GPU data
		raw_data_end = data.find(b'META')#The end of the whole data

		buffer_data = data[raw_data_start : raw_data_end]

	return buffer_data

def viewImageInformation(compressed_data):
	compression_mode = str(compressed_data[0])
	texture_type = str(HEAD.properties[0].value)
	texture_filter = str(HEAD.properties[9].value)
	texture_format = hex(HEAD.properties[1].value).upper()

	for k,v in enumerate(TEXTURE_INFORMATION[0]['TEXTURE_FORMATS']):
		if v['ID'].upper() == texture_format:
			texture_format = v['GX2SurfaceFormat']

	#Replace the format
	HEAD.properties[1].value = texture_format

	#print('\n{:^50}'.format("###Image Details###\n"))
	#RFRM.viewProperties()
	#HEAD.viewProperties()
	#META.viewProperties()

	"""print('\n{:^50}'.format("###Image Information###\n"))
				print('Compression Mode:	{:>1}'.format(compression_mode))
				print('Decompressed Size: 	{:>1}'.format(META.properties[5].value))
				print('Texture Type:		{:>1}'.format(TEXTURE_INFORMATION[0]['TEXTURE_TYPES'][texture_type]))
				print('Texture Format: 	{:>1}'.format(texture_format))
				print('Width: 			{:>1}'.format(HEAD.properties[2].value))
				print('Height:			{:>1}'.format(HEAD.properties[3].value))"""

	print('\n')
	try:
		compression_mode = TEXTURE_INFORMATION[0]['MODES'][compression_mode]
	except:
		print("Warning: Unknown compression mode checking for zlib..")
		compression_mode = -1

	if TEXTURE_INFORMATION[0]['TEXTURE_TYPES'][texture_type] != "2D Texture":
		print("ERROR: This type of texture is not supported by the GTX extractor!")
		exit(-1)
	if HEAD.properties[4].value > 1:
		print("ERROR: This texture has a depth not supported by the GTX extractor!")
		exit(-1)

RFRM = Header(b'RFRM')
HEAD = Header(b'HEAD')
GPU = Header(b'GPU')
META = Header(b'META')

def getTXTRData(file_path):
	if os.path.isfile(file_path) == False:
		print("File {} not found!".format(file_path))
		exit(-1)

	collectHeaderData(file_path)

	#Set header properties
	RFRM.setProperties([
			Property(0x4, ctypes.c_uint64, 'Form Size'),
			Property(0x14, ctypes.c_uint32, 'Form ID'),
			Property(0x18, ctypes.c_uint32, 'Form Version'),
			Property(0x1c, ctypes.c_uint32, 'Data Version')
		])

	HEAD.setProperties([
			Property(0x18, ctypes.c_uint32, 'Texture Type'),
			Property(0x1c, ctypes.c_uint32, 'Texture Format'),
			Property(0x20, ctypes.c_uint32, 'Width'),
			Property(0x24, ctypes.c_uint32, 'Height'),
			Property(0x28, ctypes.c_uint32, 'Depth'),
			Property(0x2c, ctypes.c_uint32, 'Tile Mode'),
			Property(0x30, ctypes.c_uint32, 'Swizzle'),
			Property(0x34, ctypes.c_uint32, 'Mipmap Count')
		])

	META.setProperties([
			Property(0x20, ctypes.c_uint32, 'GPU Section Offset'),
			Property(0x24, ctypes.c_uint32, 'Base Alignment'),
			Property(0x28, ctypes.c_uint32, 'GPU Data Start'),
			Property(0x2c, ctypes.c_uint32, 'GPU Section Size'),
			Property(0x30, ctypes.c_uint32, 'Buffer Count'),
			Property(0x34, ctypes.c_uint32, 'Buffer Decompressed Size'),
			Property(0x38, ctypes.c_uint32, 'Buffer Compressed Size'),
			Property(0x3c, ctypes.c_uint32, 'Buffer Offset')

		])

	setMipMapSizes() # Set mipmaps for the texture
	compressed_data = getBufferData(file_path)

	viewImageInformation(compressed_data)
				
	mipmap_offsets = HEAD.properties[8].value
	sums = []
	for mipmap in mipmap_offsets:
		sums.append(struct.unpack('>I', mipmap)[0])

	mipmaps_data_length = sum(sums)
	pitch = round(META.properties[1].value / 2)
	converted = {0 : 0, 1: 500, 2 : 600, 3 : 900, 4 : 1200, 5:1400, 6:1600, 7: 4000}
	swizzle_value = converted[HEAD.properties[6].value]
	header_data = {
		'width': HEAD.properties[2].value,
		'height': HEAD.properties[3].value,
		'depth': HEAD.properties[4].value,
		'mipmap_count': HEAD.properties[7].value,
		'texture_format' : HEAD.properties[1].value,
		'mipmaps_data_length': mipmaps_data_length,
		'tile_mode': HEAD.properties[5].value,
		'texture_type' : HEAD.properties[0].value,
		'swizzle_value':swizzle_value,
		'alignment' : META.properties[1].value,
		'pitch' : pitch,
		'mipmap_offsets': HEAD.properties[8].value,
		'decompressed_size' : META.properties[5].value
	}

	return [compressed_data, header_data]

