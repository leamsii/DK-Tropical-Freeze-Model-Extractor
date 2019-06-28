<h4>Credits</h4>
<ul>
<li>Aruki (Unpacker Tool and File Documentation) https://github.com/arukibree</li>
<li>AboodXD (GTX Extractor) https://github.com/aboood40091</li>
<li>Random Talking Bush (Model Extractor) https://twitter.com/randomtbush?lang=en</li>
</ul>

<h4>Tools</h4>
<ol>
<li>GTX Extractor - Converts GTX files to DDS</li>
<li>Model Extractor - Converts CMDL, SMDL, WMDL files to 3d obj models</li>
<li>TXTR Extractor - Converts TXTR files to GTX then to DDS then to PNG</li>
</ol>

<h4>How it Works</h4>
<p>
	This tool takes in a model file from the DK WiiU version and gathers
	the necessary textures of the model by looking in the model folder.
	After finding the textures it calls convert.py to then convert them to PNG
	and renames them according to their owner mesh.
	After that it will call the model_extractor tool to convert the model to an
	obj format along side the textures.
</p>

<h4>Instructions</h4>
<p>
	From command line, call model_export.py target_model_file destination_folder
	Choose a model from a folder where all game textures are, or atleast the current world.
</p>

<h2>Happy Modding!</h2>
<img src = "https://i.postimg.cc/QxX9fndC/unknown.png"/>

