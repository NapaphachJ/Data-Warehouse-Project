"""
  การอ่านไฟล์แผนผังคลังสินค้า ตามชื่อไฟล์ที่กำหนด
"""
def read_layout_from_file(file_name): 
  with  open(file_name,'r') as file: 
    content = file.read() 
    content_list = content.split() 
    
    # build list to put element of layout
    layout=[] 
    for i in content_list:
      if i == '*': 
        break
      else:
        map = []
        for j in i:
          map.append(j)
      layout.append(map) 
    
    #build store shelves using dictionary
    dic_store={} 
    for i in range (len(content_list)): 
      if i > content_list.index('*'): 
        each_store = content_list[i].split(':') 
        for j in each_store: 
          num=j.split(',') 
        num = [int(i) for i in num] 
        dic_store[each_store[0]] = num 
 
  return Warehouse(layout,dic_store)



class Warehouse:

  # หากต้องมีข้อมูลอื่นๆที่ต้องใช้ในการสร้าง Warehouse นักศึกษาสามารถเพิ่ม arguments ลงใน __init__ ได้ตามความเหมาะสม
  def __init__(self, layout=None, shelves=None):
    self.layout = layout #แผนผัง
    self.shelves = shelves #ชั้นวาง
    
  
  """
    การหาชั้นวางที่ถูกต้อง ตามหมายเลขที่ระบุไว้บนกล่อง 
    return ตัวอักษรของชั้นวางสินค้าสำหรับกล่องสินค้าที่ระบุ
  """
  def find_shelf (self, label): 
    key_shelve = [i for i in self.shelves] 
    return key_shelve[label % len(self.shelves)]

  
  """
    การหาเส้นทาง (path) ที่จะให้หุ่นยนต์เคลื่อนที่ จากจุดเริ่มต้นที่กำหนดไปยังตำแหน่งของชั้นวางสินค้า 
  	return ลิสของตำแหน่งทั้งหมดที่ต้องใช้ในการเดินทาง
  """
  def find_path (self, start_position, end_position): 
    #using BFS algorithm
    queue = [] 
    queue.append([start_position]) 
    visited = [] 
    solution = [] 

    layout = self.layout 
    rows = len(layout) 
    cols = len(layout[0]) 
    
    #loop จนกระทั่ง checked ครบทุกทางเดิน
    while (len(queue) != 0) :
      path = queue.pop(0) 
      node = path[len(path) - 1] 
      
      if node in visited :
        continue
        
      a = node[0] 
      b = node[1] 

      #The way that robot can walk without obtrucal
      if 0 <= a-1 < rows and 0 <= b < cols and layout[a-1][b] != '#' :
        solution.append((a-1,b)) #up
      if 0 <= a+1 < rows and 0 <= b < cols and layout[a+1][b] != '#' :
        solution.append((a+1,b)) #down
      if 0 <= a < rows and 0 <= b+1 < cols and layout[a][b+1] != '#' :
        solution.append((a,b+1)) #right
      if 0 <= a < rows and 0 <= b-1 < cols and layout[a][b-1] != '#' :
        solution.append((a,b-1)) #left 

        
      for adj in solution: 
        pathway_new = list(path)
        pathway_new.append(adj) 
        queue.append(pathway_new) 
        if adj == end_position : 
          print(pathway_new)
          return pathway_new 
          
      visited.append(node) 
        
    
  """
    การนำกล่องสินค้าเข้ามาในคลังสินค้า 
  	return ชั้นวางสินค้า รายชื่อกล่องสินค้าหลังจากที่ได้วางกล่องสินค้าใหม่ลงไปแล้ว และ 
           path ที่จะให้หุ่นยนต์เคลื่อนที่จากจุดเริ่มต้นไปยังชั้นวางสินค้าดังกล่าว 
  """
  def add_box(self, label, start_position): 
    shelf_name = self.find_shelf(label) #ชื่อชั้นวาง ex.A B..
    shelf_number = self.shelves[shelf_name] 

    #finding end position of path
    for row in range (len(self.layout)): 
      for col in range (len(self.layout[row])):
        if shelf_name == self.layout[row][col]: 
          end_position = (row,col)    

    #If you don't already have this number, add a number of boxes.
    if label not in shelf_number: 
      shelf_number.append(label)
      path = self.find_path(start_position, end_position) 
      return shelf_name,shelf_number,path 

    return None,None,None #กรณีมีหมายเลขนั้นอยู่แล้ว ไม่สามารถใส่เพิ่มได้
  
  """
    การนำกล่องสินค้าออกจากคลังสินค้า 
  	return ชั้นวางสินค้า รายชื่อกล่องสินค้าหลังจากที่ได้นำกล่องสินค้าออกไปแล้ว และ 
           path ที่จะให้หุ่นยนต์เคลื่อนที่จากจุดเริ่มต้นไปยังชั้นสินค้านั้น 
  """
  def remove_box(self, label, start_position): 
    shelf_name = self.find_shelf(label) #ชื่อชั้นวาง ex.A B..
    shelf_number = self.shelves[shelf_name] 

    #finding end position of path
    for row in range (len(self.layout)): 
      for col in range (len(self.layout[row])): 
        if shelf_name == self.layout[row][col]: 
          end_position = (row,col)       

    #If you have this number then remove a number of boxes.
    if label in shelf_number: 
      shelf_number.remove(label)
      path = self.find_path(start_position, end_position)
      return shelf_name,shelf_number,path  

    return None,None,None 

  ''' 
  Bonus Shortest path
  '''
  def find_shortest_path (self,start_position, end_position):
    #เรียกใช้เส้นทางจาก function find path ที่ใช้ bfs algolithm ซึ่งเป็นเส้นทางที่สั้นที่สุด
    return self.find_path(start_position, end_position)
    

#######################################################################
### สำหรับทดสอบโปรแกรมเท่านั้น ห้ามแก้ไขโค้ดด้านล่างนี้ แต่สามารถแก้ไข main ฟังก์ชันได้ เพื่อทดสอบโปรแกรมด้วยตนเอง ###
### DO NOT MODIFIED THE FOLLOWING CODE ###
#######################################################################
      
"""
  ฟังก์ชันนี้ใช้สำหรับการทดสอบว่า path ที่ระบุถูกต้องหรือไม่ เท่านั้น 
  ห้ามปรับเปลี่ยนโค้ดในฟังก์ชันนี้
"""
def is_valid_path(path, obstacle):
  for pos in obstacle:
    if pos in path:
      print("เส้นทางต้องไม่มีตำแหน่งของสิ่งกีดขวาง")
      return False
      
  for i in range(0, len(path) - 1):
    row, col = path[i]
    next_row, next_col = path[i+1]

    if row == next_row and col + 1 == next_col:    # right
      continue
    elif row == next_row and col - 1 == next_col:  # left
      continue
    elif row - 1 == next_row and col == next_col:  # up
      continue
    elif row + 1 == next_row and col == next_col:  # down
      continue
    else:
      print("หุ่นยนต์ต้องเดินทางใน 4 ทิศ คือเดินหน้า ถอยหลัง ซ้าย และขวา เท่านั้น ไม่สามารถเดินทางในแนวทะแยง หรือข้ามไปตำแหน่งที่ไม่อยู่ติดกันได้")
      return False
  return True


"""
  ทดสอบฟังก์ชัน read_layout_from_file(...)
"""
def test_read_layout(layout_file):
  warehouse = read_layout_from_file(layout_file)
  assert warehouse is not None, f"Warehouse is created, but got None" 
  return warehouse


"""
  ทดสอบฟังก์ชัน find_shelf(...)
"""
def test_find_shelf(warehouse, labels, expected_shelves):  
  print('-'*40)
  for i in range(0, len(labels)):
    shelf = warehouse.find_shelf(labels[i])
    print('Box', labels[i], 'should be on shelf', shelf)
    assert shelf == expected_shelves[i], f"expected shelf {expected_shelves[i]}, got shelf {shelf}"


"""
  ทดสอบฟังก์ชัน find_path(...)
"""
def test_find_path(warehouse, starts, ends, obstacles):
  print('-'*40)
  for i in range(0, len(starts)):
    path = warehouse.find_path (starts[i], ends[i])
    print('Path from', starts[i], 'to', ends[i], 'can be found.')
    assert starts[i] == path[0] and ends[i] == path[-1], f"Path must start with {starts[i]} and end with {ends[i]}"
    assert is_valid_path(path, obstacles) == True, f"Path is invalid, please check the project description"


"""
  ทดสอบฟังก์ชัน add_box(...)
"""
def test_add_box(warehouse, labels, expected_shelves, starts, obstacles):
  print('-'*40)
  for i in range(0, len(labels)):
    shelf, boxes_on_shelf, path = warehouse.add_box(labels[i], starts[i])
    if expected_shelves[i] is not None:
      # robot can add a new box
      print('The robot can add new box', labels[i])
      assert shelf == expected_shelves[i], f"expected shelf {expected_shelves[i]}, got {shelf}"
      assert labels[i] in boxes_on_shelf, f"expected box {labels[i]} on shelf {expected_shelves[i]}, got no box on shelf"
      assert is_valid_path(path, obstacles) == True, f"Path is invalid, please check the project description"
    else:
      # the box already exists in the warehouse
      print('The box', labels[i],  ' already exists, so it cannot be added')
      assert shelf is None, f"Box {labels[i]} already exists in the warehouse, expected: shelf is None"
      assert boxes_on_shelf is None, f"Box {labels[i]} already exists in the warehouse, expected: boxes on shelf is None"
      assert path is None, f"Box {labels[i]} already exists in the warehouse, expected: path is None"


"""
  ทดสอบฟังก์ชัน remove_box(...)
"""
def test_remove_box(warehouse, labels, expected_shelves, starts, obstacles):
  print('-'*40)
  for i in range(0, len(labels)):
    shelf, boxes_on_shelf, path = warehouse.remove_box(labels[i], starts[i])
    if expected_shelves[i] is not None:
      # The robot can remove the box 
      print('The robot can remove box', labels[i])
      assert shelf == expected_shelves[i], f"expected shelf {expected_shelves[i]}, got {shelf}"
      assert labels[i] not in boxes_on_shelf, f"Box {labels[i]} must be removed from shelf {expected_shelves[i]}, got the box is still on shelf"
      assert is_valid_path(path, obstacles) == True, f"Path is invalid, please check the project description"
    else:
      # The box does not exist, so it cannot be removed
      print('The box', labels[i], 'does not exist, so it cannot be removed')
      assert shelf is None, f"Box {labels[i]} does not exist in the warehouse, expected: shelf is None"
      assert boxes_on_shelf is None, f"Box {labels[i]} does not exist in the warehouse, expected: boxes on shelf is None"
      assert path is None, f"Box {labels[i]} does not exist in the warehouse, expected: path is None"


"""
  Bonus :
  ทดสอบฟังก์ชัน find shortest path
"""
def test_find_shortest_path(warehouse, starts, ends, obstacles):
  print('-'*40)
  for i in range(0, len(starts)):
    print('Find Shortest Path from', starts[i], 'to', ends[i], ' :')
    path = warehouse.find_shortest_path (starts[i], ends[i])
    assert starts[i] == path[0] and ends[i] == path[-1], f"Path must start with {starts[i]} and end with {ends[i]}"
    assert is_valid_path(path, obstacles) == True, f"Path is invalid, please check the project description"
    
      
#######################################################################
### นักศึกษาสามารถแก้ไข main ฟังก์ชันได้ เพื่อทดสอบโปรแกรมด้วยตนเอง           ###
#######################################################################
if __name__ == "__main__":
  """
    ทดสอบแผนผังแบบที่ 1 (1_mini_3x3.txt)
  """
  layout_file = "layout/1_mini_3x3.txt"
  warehouse = test_read_layout(layout_file)
  
  labels =  [0,    1,   2,   3,   10,  11,  12, 20]
  shelves = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'A']
  test_find_shelf(warehouse, labels, shelves)  
  
  starts = [(0,0), (1,0), (0,1), (2,1)]
  ends = [(1,2), (2,2), (2,2), (0,0)]
  obstacles = [(1,1)]
  test_find_path(warehouse, starts, ends, obstacles)

  labels = [22, 25, 1, 2]
  starts = [(0,0), (1,0), (0,0), (1,0)]
  shelves = ['A', 'B', None, None]
  test_add_box(warehouse, labels, shelves, starts, obstacles)

  labels = [22, 25, 28, 29]
  starts = [(0,0), (1,0), (0,0), (1,0)]
  shelves = ['A', 'B', None, None]
  test_remove_box(warehouse, labels, shelves, starts, obstacles)


  #comment ด้านบนและเปิด print test นี้เพื่อเข้าถึง output find shortest path 
"""
  '''
  Print test Bonus :
  '''
  layout_file = "layout/2_small_5x4.txt"
  warehouse = test_read_layout(layout_file)
  starts = [(0,1)]
  ends = [(4,1)]
  obstacles = [(0,0), (2,1), (0,3), (2,2),(4,0),(4,3)]
  print("Challenge Bonus-Shortest path : ")
  test_find_shortest_path(warehouse, starts, ends, obstacles)

"""
