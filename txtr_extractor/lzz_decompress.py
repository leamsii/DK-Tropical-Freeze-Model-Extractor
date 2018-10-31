#LZZ Decompression for DonkeyKong Tropical Wii U
#Credit to Aruki for documenting the DK files and providing decompression code.

import zlib, struct

def decompress(file, decompressed_size):
	compression_mode = int.from_bytes(file.read(1), 'little')
	file.seek(4)

	if compression_mode == 0:
		print("Log: The buffer is already decompressed..")
		return file.read()

	if compression_mode != 3:
		zlib_magic = file.read(1)
		if zlib_magic == b'\x78':
			print("Log: Zlib compression found! Decompressing.. Unpredictable!")
			file.seek(4)
			try:
				data = zlib.decompress(file.read())
				if len(data) < decompressed_size:
					print("Invalid decompression size! Adding padding..")
					data += bytes(decompressed_size - len(data))
				return data
				
			except:
				print("ERROR: Zlib decompression failed!")
				exit(-1)

		print("ERROR: This type of compression is not supported! Compression Mode: ", compression_mode)
		exit(-1)

	print("Log: 32 Bit compression mode found, starting decompression...")
	data = b''
	while len(data) < decompressed_size:
		byte_header = file.read(1)
		if byte_header == b'':
			print("Warning: Reached end of file, adding padding....")
			data += bytes(decompressed_size - len(data))
			break

		byte_header = ord(byte_header)
		for _ in range(8):
			if byte_header & 0x80:
				try:
					byte1 = ord(file.read(1))
					byte2 = ord(file.read(1))
				except:
					return data

				count = (byte1 >> 4) + 1
				length = (((byte1 & 0xF) << 0x8) | byte2) << 2
				seek = len(data) - length
		
				if seek < 0 or seek > len(data):
					print("Oh oh.", seek, len(data))

				for c in range(count):
					data += data[seek : seek + 4]
					seek+=4
			else:
				data += file.read(4)

			byte_header = byte_header << 1
		
		if decompressed_size < len(data):
			break
	
	return data


def lzssDecompress(file_path, decompressed_size):
	with open(file_path, 'rb') as file:
		decompressed_data = decompress(file, decompressed_size)
		
	return decompressed_data


