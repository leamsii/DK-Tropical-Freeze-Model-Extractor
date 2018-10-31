#This script converts TXTR files to GTX to be used with the GTX Extractor
#Some TXTR files are not compatible with the GTX extractor

import struct
import os
import sys
from txtr_mapper import getTXTRData
from lzz_decompress import lzssDecompress
from PIL import Image

sys.path.insert(0, '../gtx_extractor/')
from gtx_extract import main

GTX_FORMATS = [{
  "0x00000000": "GX2_SURFACE_FORMAT_INVALID",
  "0x0000001a": "GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM",
  "0x0000041a": "GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB",
  "0x00000019": "GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM",
  "0x00000008": "GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM",
   "0x0000000a": "GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM",
   "0x0000000b": "GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM",
   "0x00000001": "GX2_SURFACE_FORMAT_TC_R8_UNORM",
   "0x00000007": "GX2_SURFACE_FORMAT_TC_R8_G8_UNORM",
   "0x00000002": "GX2_SURFACE_FORMAT_TC_R4_G4_UNORM",
   "0x00000031": "GX2_SURFACE_FORMAT_T_BC1_UNORM",
   "0x00000431": "GX2_SURFACE_FORMAT_T_BC1_SRGB",
   "0x00000032": "GX2_SURFACE_FORMAT_T_BC2_UNORM",
   "0x00000432": "GX2_SURFACE_FORMAT_T_BC2_SRGB",
   "0x00000033": "GX2_SURFACE_FORMAT_T_BC3_UNORM",
   "0x00000433": "GX2_SURFACE_FORMAT_T_BC3_SRGB",
   "0x00000034": "GX2_SURFACE_FORMAT_T_BC4_UNORM",
   "0x00000234": "GX2_SURFACE_FORMAT_T_BC4_SNORM",
   "0x00000035": "GX2_SURFACE_FORMAT_T_BC5_UNORM",
   "0x00000235": "GX2_SURFACE_FORMAT_T_BC5_SNORM"         
}]

def getFormat(_format):
	for k,v in enumerate(GTX_FORMATS[0]):
		gtx_format = GTX_FORMATS[0][v]
		if gtx_format == _format:
			return v
			break
	else:
		print("ERROR: Format not found setting default format!")
		return "0x31"

def getOffsets(offset_arr):
	tmp = b''
	for mipmap in offset_arr:
		tmp += mipmap
	return tmp



def setBlockHeader(major_version, minor_version, block_type, data_size, block_id, incrementing_value, raw_data):
	major_version = struct.pack('>I', major_version)
	minor_version = struct.pack('>I', minor_version)
	block_type = struct.pack('>I', block_type)
	data_size = struct.pack('>I', data_size)
	block_id = struct.pack('>I', block_id)
	incrementing_value = struct.pack('>I', incrementing_value)

	BLK_HEADER = b'\x42\x4c\x4b\x7b\x00\x00\x00\x20%b%b%b%b%b%b%b' % (major_version, minor_version, block_type,
		data_size, block_id, incrementing_value, raw_data)

	return BLK_HEADER

def setGfxHeader(major_version, minor_version, gpu_version, align_mode):
	major_version = struct.pack('>I', major_version)
	minor_version = struct.pack('>I', minor_version)
	gpu_version = struct.pack('>I', gpu_version)
	align_mode = struct.pack('>I', align_mode)

	GFX_HEADER = b'\x47\x66\x78\x32\x00\x00\x00\x20%b%b%b%b%b' % (major_version, minor_version, gpu_version,
		align_mode, bytes(8))

	return GFX_HEADER

def getSurfaceHeader(header_information):

	first_slice_id = 0
	first_mipmap_id = 0
	aa_mode = 0
	usage = 1
	component_selector = b'\x00\x01\x02\x03' #Colors
	registers = bytes(20)

	dimension = header_information['texture_type']
	width = header_information['width']
	height = header_information['height']
	depth = header_information['depth']
	mipmap_count = header_information['mipmap_count']
	data_length = header_information['decompressed_size']
	mipmaps_data_length = header_information['mipmaps_data_length']
	tile_mode = header_information['tile_mode']
	swizzle_value = header_information['swizzle_value']
	alignment = header_information['alignment']
	pitch = header_information['pitch']
	mipmap_offsets = header_information['mipmap_offsets']
	texture_format = header_information['texture_format']
	texture_format = getFormat(texture_format)
	texture_format = int(str(texture_format), 16)
	number_of_true_mipmaps = (mipmap_count - first_mipmap_id)
	number_of_true_slices = (depth - first_slice_id)
	mipmap_extra = bytes((13 - mipmap_count) * 4)

	dimension = struct.pack('>I', dimension)
	width = struct.pack('>I', width)
	height = struct.pack('>I', height)
	depth = struct.pack('>I', depth)
	mipmap_count = struct.pack('>I', 1)
	texture_format = struct.pack('>I', texture_format)
	aa_mode = struct.pack('>I', aa_mode)
	usage = struct.pack('>I', usage)
	data_length = struct.pack('>I', data_length)
	data_pointer = bytes(4)
	mipmaps_data_length = struct.pack('>I', mipmaps_data_length)
	mipmaps_pointer = bytes(4)
	tile_mode = struct.pack('>I', tile_mode)
	swizzle_value = struct.pack('>I', swizzle_value)
	alignment = struct.pack('>I', alignment)
	pitch = struct.pack('>I', pitch)
	first_mipmap_id = struct.pack('>I', first_mipmap_id)
	number_of_true_mipmaps = struct.pack('>I', number_of_true_mipmaps)
	first_slice_id = struct.pack('>I', first_slice_id)
	number_of_true_slices = struct.pack('>I', number_of_true_slices)

	mipmap_offsets = getOffsets(mipmap_offsets) + mipmap_extra

	surface_header = dimension + width + height + depth + mipmap_count + texture_format + aa_mode + usage + data_length + data_pointer +\
	mipmaps_data_length + mipmaps_pointer + tile_mode + swizzle_value + alignment + pitch + mipmap_offsets + first_mipmap_id +\
	number_of_true_mipmaps + first_slice_id + number_of_true_slices + component_selector + registers

	return surface_header

def flip_image(image_path, dest):
	img_obj = Image.open(image_path)
	rotated_img = img_obj.transpose(Image.FLIP_LEFT_RIGHT)
	rotated_img = rotated_img.rotate(180)
	rotated_img.save(dest)
	
if len(sys.argv) <= 1:
	print("ERROR: Please enter a source ie: converter.py target.txtr")
	exit(-1)

file_path = sys.argv[1]

if os.path.isfile(file_path) == False:
	print("ERROR: File not found!", file_path)
	exit(-1)

#------------------------------
major_version = 7
minor_version = 1
gpu_version = 2

TXTR_DATA = getTXTRData(file_path) #Returns the raw image data and the header information
raw_image_data = TXTR_DATA[0]
header_information = TXTR_DATA[1]

#Decompress the image
with open('raw_image_data.bin', 'wb') as file:
	file.write(raw_image_data)

print("Log: Decompressing", os.path.basename(file_path))

raw_image_data = lzssDecompress('raw_image_data.bin', header_information['decompressed_size'])
gfx_header = setGfxHeader(major_version, minor_version, gpu_version, 0)
surface_header = getSurfaceHeader(header_information)
surface_header_block = setBlockHeader(0, 1, 11, len(surface_header), 0, 0, surface_header)
raw_image_block = setBlockHeader(1, 0, 12, header_information['decompressed_size'], 0, 0, raw_image_data)
padding_block = setBlockHeader(1, 0, 1, 0, 0, 0, b'')

with open('{}.gtx'.format(file_path[:file_path.find('.')]), 'wb') as file:
	file.write(gfx_header)
	file.write(surface_header_block)
	file.write(raw_image_block)
	file.write(padding_block)
	file.write(padding_block)



print("Log: Converting {} to PNG".format(os.path.basename(file_path)))
gtx_file = file_path[:file_path.find('.')] + '.gtx'
main(gtx_file)
try:
	flip_image(gtx_file[:gtx_file.find('.')] + '.dds', gtx_file[:gtx_file.find('.')] + '.png' )
	os.system("del {}".format(file_path[:file_path.find('.')] + '.dds'))
except:
	print("Error: Could not convert {} to png!".format(gtx_file))


os.system("del raw_image_data.bin")
os.system("del {}".format(file_path[:file_path.find('.')] + '.gtx'))
os.system("del {}".format(file_path[:file_path.find('.')] + '.TXTR'))
