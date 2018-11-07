<p>Credit to Aruki for developing the unpacker tools and file documentation</p>
<p>Credit to AboodXD for the GTX Texture Converter</p>
<p>Credit to Random Talking Bush for the model extractor</p>

<h4>Tools</h4>
<ol>
  GTX Extractor - Converts GTX images to DDS
	Model Extractor - Converts CMDL, SMDL, WMDL files to 3d obj models.
	TXTR Extractor - Converts TXTR files to GTX then to DDS then to PNG
 </ol>
	

	--How it Works---
	This tool takes in a model file from the DK WiiU version and gathers
	the necessary textures of the model by looking in the model folder.
	After finding the textures it calls convert.py to then convert them to PNG
	and renames them according to their owner mesh.
	After that it will call the model_extractor tool to convert the model to an
	obj format along side the textures.

	--Instructions---
	From command line, call model_export.py target_model_file destination_folder
	Choose a model from a folder where all game textures are, or atleast the current world.
	
	--Warning--
	The tool will overwright whatever is in the destination folder.
Make sure all your file paths are correct.
