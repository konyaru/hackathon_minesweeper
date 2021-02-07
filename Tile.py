class Tile:
  def __init__(self, gridX, gridY, bomb_count=0, isBomb=False, hasFlag=False, opened=False):
    self.gridX = gridX
    self.gridY = gridY
    self.bomb_count = bomb_count # 0~8
    self.isBomb = isBomb # 
    self.hasFlag = hasFlag # ToDo #旗が置かれている時、右クリックしか受け付けない
    self.opened = opened
    