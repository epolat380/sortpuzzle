from copy import deepcopy

TUBE_SIZE = 4

def count_first(cont):
  i = 0
  first = cont[0]
  for color in cont:
    if (color == first):
      i = i + 1
    else:
      return [i, first]
  return [i, first]

def create_map(state):
  map = {}
  i=0
  for cont in state:
    if cont != []:
      map[i] = count_first(cont)
    else: 
      map[i] = "empty"
    i = i + 1
  return map

def remove_empty(lst):
  new_lst = []
  for i in range(len(lst)): 
    if lst[i][1] != "empty": 
      new_lst.append(lst[i])
  return new_lst

def compress_map(lst):
  for x in lst:
    temp = lst.copy()
    temp.remove(x)
    for y in temp:
      if x[1] == y[1]:
        x[0] = x[0] + y[0]
        lst.remove(y)
  return lst

def choose(map):
  map_copy = deepcopy(map)
  lst_raw = list(map_copy.values())
  lst = remove_empty(lst_raw)
  return compress_map(lst)

def find_max(lst):
  max_color = ""
  occurence = 0
  j = 1
  for i in range(len(lst)):
    if (j < len(lst)):
      if (lst[i][0] >= lst[j][0]) & (lst[i][0] >= occurence):
        max_color = lst[i][1]
        occurence = lst[i][0]
      elif (lst[j][0] >= lst[i][0]) & (lst[j][0] >= occurence):
        max_color = lst[j][1]
        occurence = lst[j][0]
      else:
        continue
      j = j + 1
    elif (len(lst) == 1): 
      max_color = lst[0][1]
      occurence = lst[0][0]
  return max_color, occurence

def other_possible_paths(num, size_of_tube, color, unit, state):
  for i in range(num):
    if state[i][0] == color:
      n = 0
      for x in state[i]:
        if x == color:
          n = n - 1
    
      if ((size_of_tube - len(state[i])) != 0) & ((size_of_tube - len(state[i])) >= (unit + n)):
        return True
      else:
        return False
    
def find_destination(num_tubes, size_of_tube, color, unit, state):
  for i in range(num_tubes):
    if state[i][0] == color:
      n = 0
      for x in state[i]:
        if x == color:
          n = n - 1
      
      if other_possible_paths(len(state[i+1:]), size_of_tube, color, unit, state[i+1:]):
        find_destination(len(state[i+1:]), size_of_tube, color, unit, state[i+1:])
      elif ((size_of_tube - len(state[i])) != 0) & ((size_of_tube - len(state[i])) >= (unit + n)):
        if (unit != (-n)): #efficient çözüm değil!!
          return i
        else:
          return state.index(["empty"])
      else:
        continue
  return state.index(["empty"])

def only_color(color, state):
  length = []
  b = []
  counter = 0
  for x in state:
    if x[0] == color:
      counter = counter + 1
      length.append(len(x))
      print(x)
      for y in x:
        if y != color:
          b.append(False)
          break
  return b, length, counter

def remove_color(color, lst):
  i = 0
  for _ in lst:
    if lst[i][1] == color:
      lst.remove(lst[i])
    i = i + 1
  return lst

def not_unique_color(state, color, unit):
  sum = 0
  for i in range(len(state)):
    if state[i][0] == color:
      sum = sum + len(state[i])
  print(sum > unit)
  return sum > unit

def find_color(map, state):
  new_map = deepcopy(map)
  i = 0
  for _ in map:
    print(map[i][1])
    print(map[i][0])
    b, length, counter = only_color(map[i][1], state)
    if ((not b) & (len(length)) == 1) or ((not b) & (min(length) == TUBE_SIZE)):
      print("hey")
      new_map = remove_color(map[i][1], compress_map(new_map))
    elif ((len(b) >= counter) & not_unique_color(state, map[i][1], TUBE_SIZE)):
      print("yey")
      try:
        state.index(["empty"])
      except ValueError:
        new_map = remove_color(map[i][1], compress_map(new_map))
    else:
      print("ney")
      pass
    i = i + 1
  return find_max(new_map)

def modify_state(num_tubes, map, state, size_of_tube):
  new_color, num = find_color(choose(map), state)
  dest = find_destination(len(state), size_of_tube, new_color, num, state)

  print(new_color)
  print(dest)

  for i in range(num_tubes):
    if map[i][1] == new_color:
      j = 0
      while (j < (len(state[i]))):
        if (state[i][j] == new_color):
          state[i].remove(new_color)
        else: 
          break
      
      if not state[i]:
        state[i].append("empty")

      if state[dest] == ['empty']:
        state[dest].remove('empty')
  
  for x in range(num):
    state[dest].insert(0, new_color)
  
  return state

def main():
  state = [['sr', 'sr', 'sr', 'sr'], ['empty'], ['kr', 'kr', 'kr', 'kr'], ['pb', 'pb', 'pb', 'pb'], ['yş'], ['mv', 'mv', 'mv', 'mv'], ['yş', 'yş', 'yş']]
  map = create_map(state)
  result = modify_state(len(state), map, state, TUBE_SIZE)
  print(result)

if __name__ == "__main__":
    main()