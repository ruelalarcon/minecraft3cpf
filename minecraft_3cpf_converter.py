import json
from pathlib import Path
import numpy as np
from scipy.spatial import KDTree

from nbtlib import Compound, File, Float, Int, List

def load_block_data(block_colors_path):
	with open(block_colors_path, 'r') as f:
		block_data = json.load(f)

	# Create a KDTree for efficient color matching
	colors = np.array([block['rgb'] for block in block_data])
	color_tree = KDTree(colors)

	return block_data, color_tree

def find_closest_block(color, block_data, color_tree):
	_, index = color_tree.query(color)
	return block_data[index]['id']

def create_directories(output_folder):
	(Path(output_folder) / 'data').mkdir(parents=True, exist_ok=True)
	(Path(output_folder) / 'datapacks' / 'block_animator' / 'data' / 'block_animator' / 'functions').mkdir(parents=True, exist_ok=True)

def create_metadata(datapack_folder):
	meta = {
		'pack': {
			'pack_format': 6,
			'description': 'Functions for running block animations.',
		}
	}
	with open(Path(datapack_folder) / 'pack.mcmeta', 'w') as f:
		json.dump(meta, f, indent=4)

def create_animation_data(point_frames):
	frames = []
	for frame_index in range(len(point_frames.frames)):
		position_data = {}
		for point_index in range(len(point_frames.points)):
			position = point_frames.get_position(point_index, frame_index)
			position_data.update({
				f'{point_index}x': Float(position[0]),
				f'{point_index}y': Float(position[1]),
				f'{point_index}z': Float(position[2])
			})
		frames.append(Compound(position_data))

	return Compound({
		'DataVersion': Int(3700),
		'contents': Compound({
			'data': Compound({'frames': List(frames)})
		})
	})

def write_nbt_data(data_folder, animation_data):
	nbt_file = File({'data': animation_data}, gzipped=True)
	nbt_file.save(Path(data_folder) / 'command_storage_animator_storage.dat')

def create_functions(functions_folder, point_frames, block_data, color_tree, block_scale):
	functions = {
		'create': '$summon minecraft:block_display ~ ~2 ~ {Tags:["$(v)","animation"],block_state:{Name:"minecraft:$(id)"}}\n$execute as @e[type=minecraft:block_display,tag=$(v)] run data merge entity @s {transformation:{translation:[0.0f,0.0f,0.0f],scale:[$(s)f,$(s)f,$(s)f]}}',
		'initialize': 'kill @e[type=minecraft:block_display]\n' + '\n'.join(f'function block_animator:create {{v:"{i}",id:"{find_closest_block(point.color, block_data, color_tree)}",s:{block_scale}f}}' for i, point in enumerate(point_frames.points)),
		'move': '$execute as @e[tag=$(v)] run data merge entity @s {transformation:{translation:[$(x),$(y),$(z)]},interpolation_duration:2,start_interpolation:0}',
		'render': '\n'.join(f'$function block_animator:move {{v:"{i}",x:$({i}x)f,y:$({i}y)f,z:$({i}z)f}}' for i in range(len(point_frames.points))),
		'render_frame': '\n'.join(f'execute if score @p Frame matches {i} run function block_animator:render with storage animator_storage:data frames[{i}]' for i in range(len(point_frames.frames)))
	}

	for name, content in functions.items():
		with open(Path(functions_folder) / f'{name}.mcfunction', 'w') as f:
			f.write(content)