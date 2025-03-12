import pyautogui
import cv2
import numpy as np
import time
import os
import keyboard

tile_template = {}
tile_folder = 'tiles/'

# initial exclude list: list of (row, col) tuples
exclude = []

gridRow = 11
gridCol = 10

cellWidth = 65
cellHeight = 61

# right configuration
# xPos = 430 + (cellWidth * 1)
# yPos = 402 - (cellHeight * 3)

# center configuration
xPos = 445 - (cellWidth * 3)
yPos = 405 - (cellHeight * 3)

def select_exclude_tiles():
    """
    Display a window showing the grid.
    - Clicking on a cell adds it to the exclude list (if not already added).
    - Cells in the exclude list are shown in red.
    - Press 'p' to clear the exclude list.
    - Press 'q' to quit the prompt.
    """
    global exclude

    grid_width = cellWidth * gridCol
    grid_height = cellHeight * gridRow
    screenshot = pyautogui.screenshot(region=(xPos, yPos, grid_width, grid_height))
    base_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    img = base_image.copy()

    def draw_grid(img, exclude):
        """Draw grid lines and cell labels, using red for excluded cells."""
        temp = base_image.copy()
        for row in range(gridRow):
            for col in range(gridCol):
                pt1 = (col * cellWidth, row * cellHeight)
                pt2 = ((col + 1) * cellWidth, (row + 1) * cellHeight)
                cv2.rectangle(temp, pt1, pt2, (0, 255, 0), 1)
                # Set text color: red if in exclude, green otherwise
                color = (0, 0, 255) if (row, col) in exclude else (0, 255, 0)
                cv2.putText(temp, f"{row},{col}", (pt1[0] + 5, pt1[1] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        # Display instructions
        cv2.putText(temp, "Click: add exclude | p: clear | q: quit", (5, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return temp

    # Mouse callback: add cell to exclude list (if not already added)
    def mouse_callback(event, x, y, flags, param):
        nonlocal img
        if event == cv2.EVENT_LBUTTONDOWN:
            col = x // cellWidth
            row = y // cellHeight
            cell = (row, col)
            if cell not in exclude:
                exclude.append(cell)
                print("Added", cell, "to exclude list.")
            else:
                print("Cell", cell, "is already excluded.")
            img = draw_grid(img, exclude)

    cv2.namedWindow("Select Exclude Tiles")
    cv2.setMouseCallback("Select Exclude Tiles", mouse_callback)
    img = draw_grid(img, exclude)

    while True:
        cv2.imshow("Select Exclude Tiles", img)
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            exclude.clear()
            print("Cleared exclude list.")
            img = draw_grid(img, exclude)
    cv2.destroyWindow("Select Exclude Tiles")

def getGrid():
    # Store detected tiles
    tile_grid = []
    screen = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    for row in range(gridRow):
        row_tiles = []
        for col in range(gridCol):
            tile = screen[yPos + cellHeight * row : yPos + cellHeight * (row + 1),
                          xPos + cellWidth * col : xPos + cellWidth * (col + 1)]
            tile_gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
            tile_gray = cv2.GaussianBlur(tile_gray, (3, 3), 0)

            best_match = None
            best_match_score = 0.35  # Adjust threshold as needed

            # cv2.imshow('tilefound', tile_gray)
            # cv2.waitKey(0)

            print(exclude)
            print((row, col), (row, col) in exclude)

            if(row, col) not in exclude:
                for tile_name, template in tile_template.items():
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    result = cv2.matchTemplate(tile_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                    _, score, _, _ = cv2.minMaxLoc(result)
                    if score > best_match_score:
                        best_match = tile_name
                        best_match_score = score

            row_tiles.append(best_match)
        tile_grid.append(row_tiles)

    for row in tile_grid:
        print(row)
    return tile_grid

def getMatch(grid):
    for i in range(gridRow - 1, -1, -1):
        for j in range(gridCol - 1, -1, -1):
            if grid[i][j] is not None:
                if (i > 0 and j > 0) and (i < gridRow - 1 and j < gridCol - 1):
                    if grid[i][j] == grid[i-1][j-1] == grid[i+1][j-1] and grid[i][j-1] is not None:
                        print("h pattern found")
                        return i, j, 'h-left'
                    if grid[i][j] == grid[i-1][j-1] == grid[i-1][j+1] and grid[i-1][j] is not None:
                        print("h pattern found")
                        return i, j, 'v-up'
                    if grid[i][j] == grid[i-1][j+1] == grid[i+1][j+1] and grid[i][j+1] is not None:
                        print("h pattern found")
                        return i, j, 'h-right'
                    if grid[i][j] == grid[i+1][j-1] == grid[i+1][j+1] and grid[i+1][j] is not None:
                        print("h pattern found")
                        return i, j, 'v-down'
                if (i > 1 and j > 1) and (i < gridRow - 2 and j < gridCol - 2):
                    if grid[i][j] == grid[i-1][j-1] == grid[i-2][j-1] and grid[i][j-1] is not None:
                        print("L pattern found1")
                        return i, j, 'h-left'
                    if grid[i][j] == grid[i+1][j-1] == grid[i+2][j-1] and grid[i][j-1] is not None:
                        print("L pattern found2")
                        return i, j, 'h-left'
                    if grid[i][j] == grid[i-1][j+1] == grid[i-2][j+1] and grid[i][j+1] is not None:
                        print("L pattern found1")
                        return i, j, 'h-right'
                    if grid[i][j] == grid[i+1][j+1] == grid[i+2][j+1] and grid[i][j+1] is not None:
                        print("L pattern found2")
                        return i, j, 'h-right'
                    if grid[i][j] == grid[i-1][j-1] == grid[i-1][j-2] and grid[i-1][j] is not None:
                        print("L pattern found1")
                        return i, j, 'v-up'
                    if grid[i][j] == grid[i-1][j+1] == grid[i-1][j+2] and grid[i-1][j] is not None:
                        print("L pattern found2")
                        return i, j, 'v-up'
                    if grid[i][j] == grid[i+1][j-1] == grid[i+1][j-2] and grid[i+1][j] is not None:
                        print("L pattern found1")
                        return i, j, 'v-down'
                    if grid[i][j] == grid[i+1][j+1] == grid[i+1][j+2] and grid[i+1][j] is not None:
                        print("L pattern found2")
                        return i, j, 'v-down'
                if i < (gridRow - 3) and grid[i][j] == grid[i+2][j] == grid[i+3][j] and grid[i+1][j] is not None:
                    return i, j, 'v-down'
                if i > 2 and grid[i][j] == grid[i-2][j] == grid[i-3][j] and grid[i-1][j] is not None:
                    return i, j, 'v-up'
                if j < (gridCol - 3) and grid[i][j] == grid[i][j+2] == grid[i][j+3] and grid[i][j+1] is not None:
                    return i, j, 'h-right'
                if j > 2 and grid[i][j] == grid[i][j-2] == grid[i][j-3] and grid[i][j-1] is not None:
                    return i, j, 'h-left'
    return None

def makeMove(i, j, direction):
    x = xPos + cellWidth * j
    y = yPos + cellHeight * i

    if direction == 'click':
        pyautogui.click(x + 27, y + 27)
    elif direction == 'h-right':
        pyautogui.moveTo(x + 25, y + 27)
        pyautogui.mouseDown(x + 25, y + 27, button='left')
        pyautogui.moveTo(x + 81, y + 27, duration=0.1)
        pyautogui.mouseUp(button='left')
    elif direction == 'h-left':
        pyautogui.moveTo(x + 27, y + 25)
        pyautogui.mouseDown(x + 27, y + 25, button='left')
        pyautogui.moveTo(x - 27, y + 25, duration=0.1)
        pyautogui.mouseUp(button='left')
    elif direction == 'v-down':
        pyautogui.moveTo(x + 27, y + 25)
        pyautogui.mouseDown(x + 27, y + 25, button='left')
        pyautogui.moveTo(x + 27, y + 81, duration=0.1)
        pyautogui.mouseUp(button='left')
    elif direction == 'v-up':
        pyautogui.moveTo(x + 25, y + 27)
        pyautogui.mouseDown(x + 25, y + 27, button='left')
        pyautogui.moveTo(x + 25, y - 27, duration=0.1)
        pyautogui.mouseUp(button='left')

def main():
    # Load tile templates.
    for filename in os.listdir(tile_folder):
        if filename.endswith(".jpg"):
            tile_name = filename.split('.')[0]
            tile_template[tile_name] = cv2.imread(os.path.join(tile_folder, filename), cv2.IMREAD_COLOR)

    print("Press 'e' to add excluded tiles.")
    print("Press 'ctrl' to allow moves to execute.")
    while True:
        if keyboard.is_pressed('e'):
            select_exclude_tiles()
            time.sleep(1)  # Delay to avoid multiple triggers

        if not keyboard.is_pressed('ctrl'):
            grid = getGrid()
            match = getMatch(grid)
            print("Match:", match)
            if match:
                if (match[0], match[1]) not in exclude:
                    makeMove(*match)
                else:
                    print("Matched cell", (match[0], match[1]), "is excluded.")
            print("Executed!")
        time.sleep(0.1)  # Prevent high CPU usage

if __name__ == '__main__':
    main()

# cv2.destroyAllWindows()
