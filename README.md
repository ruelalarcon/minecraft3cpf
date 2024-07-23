# Minecraft3cpf

> A Python-based CLI tool for converting [3cpf](https://github.com/ruelalarcon/3cpf) files into Minecraft datapacks for block animations.

## Installation

To use Minecraft3cpf, you need to have Python 3 (Tested on 3.8+) installed on your system. Clone this repository and install the required dependencies:

```bash
git clone https://github.com/ruelalarcon/minecraft3cpf.git
cd minecraft3cpf
pip install -r requirements.txt
```

## Usage

The basic usage of Minecraft3cpf is as follows:

```bash
python cli.py <input> [output]
```

- `<input>`: Path to the input .3cpf file.
- `[output]`: Optional path to the output directory. Defaults to 'output'.

### Optional Arguments

You can customize the conversion using the following optional arguments:

```bash
--palette <path>           Path to the palette.json file (default: palette.json)
--offset <float> <float> <float>
                           Offset for the animation (x, y, z) (default: 0 2 0)
--scale <float>            Scale factor for the animation (default: 10)
--block-scale <float>      Scale factor for individual blocks (default: 0.5)
--rotation <float> <float> <float>
                           Rotation angles in degrees (x, y, z) (default: 0 0 0)
--order <string>           Order of coordinates (choices: xyz, xzy, yxz, yzx, zxy, zyx) (default: xzy)
```

> Note: The transformations are applied in order of rotation, scale, then offset. The `--offset` and `--rotation` arguments follow the coordinate order specified by `--order`. The default coordinate order is xzy, rather than xyz as minecraft is compatible with xzy ordering.

### Usage Examples

Create a basic datapack with default settings:

```bash
python cli.py input.3cpf
```

Create a datapack with custom output directory and palette:

```bash
python cli.py input.3cpf custom_output --palette custom_palette.json
```

Apply transformations to the animation:

```bash
python cli.py input.3cpf --offset 1 2 3 --rotation 45 0 90 --scale 15 --order yzx
```

### Input/Output Examples

The input for this converter is a .3cpf file, which contains 3D colored point frame data. The output is a Minecraft datapack that can be used to create block animations in-game.

Input example:
```
input.3cpf (Any valid 3cpf file)
```

Output example:
```
output/
├── data/
│   └── command_storage_animator_storage.dat
└── datapacks/
    └── block_animator/
        ├── data/
        │   └── block_animator/
        │       └── functions/
        │           ├── create.mcfunction
        │           ├── initialize.mcfunction
        │           ├── move.mcfunction
        │           ├── render.mcfunction
        │           └── render_frame.mcfunction
        └── pack.mcmeta
```

## How to Use the Generated Datapack

To use the generated datapack and create animations in Minecraft:

1. Place the `output` folder contents in your Minecraft world save folder (drag `data` and `datapack` into your save).
   - On Windows: `%appdata%\.minecraft\saves\<world_name>`
   - On macOS: `~/Library/Application Support/minecraft/saves/<world_name>`
   - On Linux: `~/.minecraft/saves/<world_name>`

2. Launch Minecraft and load the world.

3. In-game, run `/reload` to load the new datapack.

4. Use the provided functions to control the animation:
   - `/function block_animator:initialize` to set up the initial state
   - `/function block_animator:render_frame` to display a specific frame

You can also use the provided save file:

### Using the Provided Save File

For a more streamlined experience, you can use the provided save file:

1. Download the `3cpfAnimator.zip` file from the repository.

2. Extract the contents to your Minecraft saves folder.

3. Launch Minecraft and load the "3cpfAnimator" world.

4. In this world, you'll find command blocks set up to initialize the environment and control the animation.

5. To use your own converted 3CPF animation:
   - Replace the `data` and `datapacks` folder in your world save with the output from the converter.
   - Run `/reload` in-game to load your new animation data.

6. You can now use the command blocks to control your custom animation.

Remember that the animation's scale, offset, and other parameters are determined by the converter settings you used. You may need to adjust your viewing position in-game to see the full animation.

## Credits

- This program uses the [cpf3d](https://github.com/ruelalarcon/cpf3d) package to process 3cpf files.
- The concept is inspired by various Minecraft animation tools and techniques.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
