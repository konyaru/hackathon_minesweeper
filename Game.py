import tkinter as tk
import math
import random
from Tile import Tile

class Game:

  def __init__(self):
    self.SQUARE_LENGTH = 30
    self.RADIUS = self.SQUARE_LENGTH / 2 - 5
    self.POSITION = {"x": 8, "y": 8}
    self.BORDER_WIDTH = 2
    self.TILES_PER_ROW = 20
    self.BOMB_NUM = self.TILES_PER_ROW * 2
    self.LENGTH = self.SQUARE_LENGTH * self.TILES_PER_ROW + self.BORDER_WIDTH * self.TILES_PER_ROW
    self.tiles = []
    self.root, self.canvas = self._create_canvas()
    self.canvas.focus_set()

  def _create_game(self):
    root, canvas = self._create_canvas()
    return root, canvas

  def _create_canvas(self):
    root = tk.Tk()
    root.geometry(f"""{self.LENGTH + self.POSITION["x"] * 2}x{self.LENGTH + self.POSITION["y"] * 2}""")
    root.title("マインスイーパー")
    canvas = tk.Canvas(root, width=(self.LENGTH + self.POSITION["x"]), height=(self.LENGTH + self.POSITION["y"]))
    canvas.place(x=0, y=0)
  
    return root, canvas

  def _create_tiles(self):
    self.tiles = []
    for i in range(self.TILES_PER_ROW**2):
      gridX, gridY = self._to_2D(i)
      tile = Tile(gridX, gridY)
      self.tiles.append(tile)

  def _create_bombs(self):
    tmp_tiles = random.sample(self.tiles, self.BOMB_NUM)
    for bomb_tile in tmp_tiles:
      bomb_tile.isBomb = True
 
  def _set_field(self):
    self.canvas.create_rectangle(self.POSITION["x"], self.POSITION["y"], self.LENGTH + self.POSITION["x"], self.LENGTH + self.POSITION["y"], fill='#aaa', width=self.BORDER_WIDTH)
  
    for i in range(self.TILES_PER_ROW - 1):
      x = self.POSITION["x"] + self.SQUARE_LENGTH * (i + 1) + self.BORDER_WIDTH * i + self.BORDER_WIDTH
      y = self.POSITION["y"] + self.SQUARE_LENGTH * (i + 1) + self.BORDER_WIDTH * i + self.BORDER_WIDTH
      self.canvas.create_line(x, self.POSITION["y"], x, self.LENGTH + self.POSITION["y"], width=self.BORDER_WIDTH)
      self.canvas.create_line(self.POSITION["x"], y, self.LENGTH + self.POSITION["x"], y, width=self.BORDER_WIDTH)
  
  def _set_item(self, tile, game_starting=False, game_clear=False):
    x = tile.gridX
    y = tile.gridY
    center_x = self.POSITION["x"] + self.BORDER_WIDTH * x + self.BORDER_WIDTH / 2 + self.SQUARE_LENGTH * x + self.SQUARE_LENGTH / 2
    center_y = self.POSITION["y"] + self.BORDER_WIDTH * y + self.BORDER_WIDTH / 2 + self.SQUARE_LENGTH * y + self.SQUARE_LENGTH / 2
  
    self.canvas.create_rectangle(center_x - self.SQUARE_LENGTH / 2, center_y - self.SQUARE_LENGTH / 2, center_x + self.SQUARE_LENGTH / 2, center_y + self.SQUARE_LENGTH / 2, fill="#fff", width=0)

    if game_clear:
      self.canvas.create_rectangle(center_x - self.SQUARE_LENGTH / 2, center_y - self.SQUARE_LENGTH / 2, center_x + self.SQUARE_LENGTH / 2, center_y + self.SQUARE_LENGTH / 2, fill="#ffff00", width=0)
      self.canvas.create_text(center_x, center_y, text='C', justify="center", font=("", 25), tag="count_text")
      return

    if not game_starting:
      tile.opened = True
      self.canvas.create_rectangle(center_x - self.SQUARE_LENGTH / 2, center_y - self.SQUARE_LENGTH / 2, center_x + self.SQUARE_LENGTH / 2, center_y + self.SQUARE_LENGTH / 2, fill="#aaa", width=0)
      if tile.isBomb:
        self.canvas.create_oval(center_x - self.RADIUS, center_y - self.RADIUS, center_x + self.RADIUS, center_y + self.RADIUS, fill="#f00", width=0)
      elif tile.bomb_count != 0:
        self.canvas.create_text(center_x, center_y, text=str(tile.bomb_count), justify="center", font=("", 25), tag="count_text")

  def _set_flag(self, tile):
    x = tile.gridX
    y = tile.gridY
    center_x = self.POSITION["x"] + self.BORDER_WIDTH * x + self.BORDER_WIDTH / 2 + self.SQUARE_LENGTH * x + self.SQUARE_LENGTH / 2
    center_y = self.POSITION["y"] + self.BORDER_WIDTH * y + self.BORDER_WIDTH / 2 + self.SQUARE_LENGTH * y + self.SQUARE_LENGTH / 2
    if not tile.opened:
      if tile.hasFlag:
        self.canvas.create_rectangle(center_x - self.SQUARE_LENGTH / 2, center_y - self.SQUARE_LENGTH / 2, center_x + self.SQUARE_LENGTH / 2, center_y + self.SQUARE_LENGTH / 2, fill="#87cefa", width=0)
        self.canvas.create_text(center_x, center_y, text='F', justify="center", font=("", 25), tag="count_text")
      else:
        self.canvas.create_rectangle(center_x - self.SQUARE_LENGTH / 2, center_y - self.SQUARE_LENGTH / 2, center_x + self.SQUARE_LENGTH / 2, center_y + self.SQUARE_LENGTH / 2, fill="#fff", width=0)

  def _set_tiles(self):
    for tile in self.tiles:
      self._set_item(tile, game_starting=True)

  def _point_to_grid_coord(self, event_x, event_y):
      x = math.floor((event_x - self.POSITION["x"]) / (self.SQUARE_LENGTH + self.BORDER_WIDTH))
      y = math.floor((event_y - self.POSITION["y"]) / (self.SQUARE_LENGTH + self.BORDER_WIDTH))
      return x, y
  
  def _to_2D(self, index_num):
    gridY, gridX = divmod(index_num, self.TILES_PER_ROW)
    return gridX, gridY

  def _to_1D(self, x, y):
    if x < 0 or self.TILES_PER_ROW <= x \
      or y < 0 or self.TILES_PER_ROW <= y:
      return None
    return x + y * self.TILES_PER_ROW

  def _calc_bomb_count(self):
    for tile in self.tiles:
      if tile.isBomb:
        tile.bomb_count = None
      else:
        for delta in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)): # check_surrounding_tilesの中でやるべき処理。ここでやるなら分けなくていい 
          if self._check_surrounding_tiles_isBomb(tile, delta):
            tile.bomb_count += 1

  def _check_surrounding_tiles_isBomb(self, tile, delta):
    index = self._to_1D(tile.gridX + delta[0], tile.gridY + delta[1])
    if index is not None:
      neighbor = self.tiles[index]
      if neighbor.isBomb:
        return True
    return False

  def _open_surrounding_tiles(self, tile, just_started=True):
    if tile.opened:
      return
    self._set_item(tile)

    neighbor_list = []
    for delta in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)):
      neighbor = None
      index = self._to_1D(tile.gridX + delta[0], tile.gridY + delta[1])
      if index is not None:
        neighbor = self.tiles[index]
        neighbor_list.append(neighbor)

    for neighbor in neighbor_list:
      if tile.bomb_count == 0 or (just_started and neighbor.bomb_count == 0):
        self._open_surrounding_tiles(neighbor, False)

  def _game_over(self):
    for tile in self.tiles:
      self._set_item(tile)

  def _game_clear(self):
    bomb_list = list(filter(lambda n: n.isBomb == True, self.tiles))
    for tile in bomb_list:
        self._set_item(tile, game_clear=True)

  def _check_clear(self):
    opened_tiles = list(filter(lambda n: n.opened==True, self.tiles))
    remained_tiles_num = self.TILES_PER_ROW**2 - len(opened_tiles)
    if remained_tiles_num == self.BOMB_NUM:
      return True

  def _click(self, event):
    x, y = self._point_to_grid_coord(event.x, event.y)
    index = self._to_1D(x, y) 
    if index is not None:
      tile = self.tiles[index]
      if not tile.hasFlag:
        if tile.isBomb:
          self._game_over()
        else:
          self._open_surrounding_tiles(tile)
    if self._check_clear():
      self._game_clear()

  def _right_click(self, event):
    x, y = self._point_to_grid_coord(event.x, event.y)
    index = self._to_1D(x, y) 
    if index is not None:
      tile = self.tiles[index]
      tile.hasFlag = not tile.hasFlag
      self._set_flag(tile)

  def _start_game(self):
    self._set_field() 
    self._create_tiles()
    self._create_bombs()
    self._calc_bomb_count()
    self._set_tiles()
  
  def _reset(self):
    self._game_over()
    for tile in self.tiles:
      tile.opened = False
    self.play()

  def _process(self):
    self.canvas.bind("<Button-1>", lambda event: self._click(event))
    self.canvas.bind("<Control-Button-1>", lambda event: self._right_click(event))
    self.canvas.bind("<Control-Return>", lambda event: self._reset())
    self.root.mainloop() 

  def play(self):
    self._start_game()
    self._process()
