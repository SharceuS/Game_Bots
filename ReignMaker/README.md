# ReignMaker Bot

This is a bot for the ReignMaker game that automates tile matching and movement.

## Project Structure

```
ReignMaker/
    bot.py
    tiles/
        air.1.jpg
        air.2.jpg
        air.png
        earth.1.jpg
        earth.2.jpg
        earth.3.jpg
        earth.4.jpg
        earth.png
        fire.1.jpg
        fire.2.jpg
        fire.3.jpg
        fire.4.jpg
        fire.5.jpg
        fire.png
        health.png
        point.png
        void.1.jpg
        void.2.jpg
        void.png
        water.1.jpg
        water.2.jpg
        water.png
```

## Requirements

- Python 3.x
- `pyautogui`
- `opencv-python`
- `numpy`
- `keyboard`

You can install the required packages using pip:

```sh
pip install pyautogui opencv-python numpy keyboard
```

## Usage

1. Place the tile images in the `tiles/` directory.
2. Run the bot script:

```sh
python bot.py
```

3. Press `e` to add excluded tiles.
4. Press `ctrl` to allow moves to execute.

## Functions

### `select_exclude_tiles()`

Displays a window showing the grid. Clicking on a cell adds it to the exclude list. Press `p` to clear the exclude list and `q` to quit the prompt.

### `getGrid()`

Captures a screenshot of the game grid and detects tiles.

### `getMatch(grid)`

Finds matching patterns in the grid.

### `makeMove(i, j, direction)`

Performs a move based on the detected pattern.

### `main()`

Main function that loads tile templates and runs the bot.