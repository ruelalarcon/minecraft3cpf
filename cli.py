import click
from pathlib import Path
import cpf3d
from itertools import permutations

from minecraft_3cpf_converter import (
	load_block_data,
	create_directories,
	create_metadata,
	create_animation_data,
	write_nbt_data,
	create_functions
)

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(), default='output')
@click.option('--palette', type=click.Path(exists=True), default='palette.json', help='Path to the blocks.json file (default: palette.json)')
@click.option('--offset', nargs=3, type=float, default=(0, 2, 0), help='Offset for the animation (x, y, z) (default: 0 2 0)')
@click.option('--scale', type=float, default=10, help='Scale factor for the animation (default: 10)')
@click.option('--block-scale', type=float, default=0.5, help='Scale factor for individual blocks (default: 0.5)')
@click.option('--rotation', nargs=3, type=float, default=(0, 0, 0), help='Rotation angles in degrees (x, y, z) (default: 0 0 0)')
@click.option('--order', default='xzy', type=click.Choice([''.join(p) for p in permutations('xyz')]), help='Order of rotation (default: xzy)')
def main(input, output, palette, offset, scale, block_scale, rotation, order):
	"""Convert 3CPF animations to Minecraft datapacks."""
	try:
		click.echo(f'Loading block data from {palette}...')
		block_data, color_tree = load_block_data(palette)

		click.echo(f'Loading frame data from {input}...')
		point_frames = cpf3d.load(input, coordinate_order=order)

		# Apply transformations
		rotation_dict = dict(zip('xyz', rotation))
		point_frames.apply_rotation(rotation_dict[order[0]], rotation_dict[order[1]], rotation_dict[order[2]])
		point_frames.apply_scale(scale, scale, scale)
		point_frames.apply_offset(*offset)

		click.echo(f'Creating directories in {output}...')
		create_directories(output)

		data_folder = Path(output) / 'data'
		datapack_folder = Path(output) / 'datapacks' / 'block_animator'
		functions_folder = datapack_folder / 'data' / 'block_animator' / 'functions'

		click.echo('Creating metadata...')
		create_metadata(datapack_folder)

		click.echo('Creating animation data...')
		animation_data = create_animation_data(point_frames)

		click.echo('Writing NBT data...')
		write_nbt_data(data_folder, animation_data)

		click.echo('Creating functions...')
		create_functions(functions_folder, point_frames, block_data, color_tree, block_scale)

		click.echo('* Complete')
	except Exception as e:
		click.echo(f'An error occurred: {str(e)}', err=True)
		raise click.Abort()

if __name__ == '__main__':
	main()