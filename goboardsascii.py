import sys
import os


# class Setting:
#     """Main settings class for game."""

#     def __init__(self, board: Board):
#         """Initialization for settings."""

#         board.size = 13


class Board:
    def __init__(self):
        self.size = 13
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]  # '.' = empty
        self.style = {
            'stone': {'black': '█', 'white': '▒'},
            'star': {'dot': '•', 'cross': '┼', 'cross2': '╬'},
            'grid': {
                'thin': {
                    'top_left': '┌',
                    'horizontal_line': '─',
                    'top': '┬',
                    'top_right': '┐',
                    'left': '├',
                    'center': '┼',
                    'right': '┤',
                    'bottom_left': '└',
                    'bottom': '┴',
                    'bottom_right': '┘',
                },
                'thick': {
                    'top_left': '╔',
                    'horizontal_line': '═',
                    'top': '╦',
                    'top_right': '╗',
                    'left': '╠',
                    'center': '╬',
                    'right': '╣',
                    'bottom_left': '╚',
                    'bottom': '╩',
                    'bottom_right': '╝',
                },
            }
        }
        self.star_points = {(4, 4), (4, 10), (10, 4), (10, 10), (7, 7)}  # Traditional 9x9 star points
        # TODO: add ko detection

    def render(self):
        """Draws the goboard grid with correct stone placements."""
        style = self.style['grid']['thick']
        rows = ' '.join(str(i) for i in range(1, 10))
        if self.size > 9:
            rows += ''.join(str(i) for i in range(10, self.size + 1))
        rows = [rows]

        grid_pattern = []

        # Build board's top row: 123232324, 1 & 4 = corners, 2 = spaces, 3 = lines
        # Look for captures around the border, since not implemented
        grid_pattern.append([1] + [2, 3] * (self.size - 2) + [2, 4])

        # Build board's middle row: 52
        for i in range(2, self.size):
            row_pattern = [5, 2]  # Left edge
            for j in range(2, self.size):
                if self.grid[i][j] == 'B':
                    row_pattern.append(self.style['stone']['black'])
                elif self.grid[i][j] == 'W':
                    row_pattern.append(self.style['stone']['white'])
                elif (i, j) in self.star_points:
                    row_pattern.append(self.style['star']['dot'])
                else:
                    row_pattern.append(6)  # Center
                if j < self.size:
                    row_pattern.append(2)  # Horizontal line
            row_pattern.append(7)  # Right edge
            grid_pattern.append(row_pattern)

        # Bottom line
        grid_pattern.append([8] + [2, 9] * (self.size - 2) + [2, 10])

        # Render the pattern
        output = []
        for row in grid_pattern:
            line = ""
            for num in row:
                if isinstance(num, str):  # Stone or star
                    line += num
                elif num == 1:
                    line += style['top_left']
                elif num == 2:
                    line += style['horizontal_line']
                elif num == 3:
                    line += style['top']
                elif num == 4:
                    line += style['top_right']
                elif num == 5:
                    line += style['left']
                elif num == 6:
                    line += style['center']
                elif num == 7:
                    line += style['right']
                elif num == 8:
                    line += style['bottom_left']
                elif num == 9:
                    line += style['bottom']
                elif num == 10:
                    line += style['bottom_right']
            output.append(line)
        return "\n".join(rows + output)

    def place_stone(self, x, y, player):
        if self.is_valid_move(x, y):
            self.grid[x][y] = player.color[0]  # 'B' or 'W'
            self.check_captures(x, y, player)

    def is_valid_move(self, x, y):
        return (0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == '.')

    def check_captures(self, x, y, player):
        opponent = 'W' if player.color == "B" else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == opponent:
                if not self.has_liberties(nx, ny, opponent):
                    self.remove_group(nx, ny, opponent, player)

    def has_liberties(self, x, y, color, visited=None):
        if visited is None:
            visited = set()
        if (x, y) in visited or not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if self.grid[x][y] == '.':
            return True
        if self.grid[x][y] != color:
            return False
        visited.add((x, y))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return any(self.has_liberties(x + dx, y + dy, color, visited) for dx, dy in directions)

    def remove_group(self, x, y, color, player, visited=None):
        if visited is None:
            visited = set()
        if (x, y) in visited or not (0 <= x < self.size and 0 <= y < self.size) or self.grid[x][y] != color:
            return
        visited.add((x, y))
        self.grid[x][y] = '.'
        player.captured += 1
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            self.remove_group(x + dx, y + dy, color, player, visited)


class Player():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.captured = 0

    def __str__(self):
        return self.name


def clear_console():
    """Clear all text in the terminal to prepare for the next drawing function."""
    os.system('cls' if os.name == 'nt' else 'clear')

def call_help(name):
    if name == 'render':
        return print(help(Board.render))
    elif name == 'clear_console':
        return print(help(clear_console))
    else:
        return print("Definition for function not defined, or mispelled.")

if __name__ == '__main__':
    # settings = Setting()
    goban = Board()
    brian = Player('brian', 'B')
    ben = Player('ben', 'W')
    black = True
    White = True

    running = True
    print("\033[30;47m")  # 30 = black text, 47 = White background
    try:
        while running:
            clear_console()
            print('broken program, please fix me', '\n')
            print(goban.render())
            if black:
                user_input = input(f"● {brian}'s turn, enter x,y: ")
                if user_input == '':
                    running = False
                    break
                elif user_input == 'help':
                    user_input = input('What definition do you want help with?')
                    call_help(user_input)
                x, y = map(int, user_input.split(","))
                if goban.is_valid_move(x, y):
                    goban.place_stone(x, y, brian)
                    goban.check_captures(x, y, brian)
                    black = False
                    White = True
                else:
                    print("Not Valid Move")
            elif White:
                user_input = input(f"○ {ben}'s turn, enter x,y: ")
                if user_input == '':
                    running = False
                    break
                x, y = map(int, user_input.split(","))
                if goban.is_valid_move(x, y):
                    goban.place_stone(x, y, ben)
                    goban.check_captures(x, y, ben)
                    White = False
                    black = True
                else:
                    print("Not Valid Move")
    finally:
        print("\033[0m\033c")  # Ensure color reset on exit
