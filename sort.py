# c = number of colors / number of containers that are initially full
# n = number of containers initially empty
# capacity for each tube = 4

from copy import deepcopy

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
  i = 0
  new_lst = []
  for x in lst: 
    if lst[i][1] != "empty": 
      new_lst.append(lst[i])
    i = i + 1
  return new_lst

def choose(map):
  map_copy = deepcopy(map)
  lst_raw = list(map_copy.values())
  lst = remove_empty(lst_raw)

  for x in lst:
    temp = lst.copy()
    temp.remove(x)
    for y in temp:
      if x[1] == y[1]:
        x[0] = x[0] + y[0]
        lst.remove(y)
  return lst

def find_max(lst):
  i = 0
  j = 1
  for x in lst:
    if (j < len(lst)):
      if lst[i][0] > lst[j][0]:
        max_color = lst[i][1]
        occurence = lst[i][0]
      else:
        max_color = lst[j][1]
        occurence = lst[j][0]
    i = i + 1
    j = j + 1
  return max_color, occurence

def find_destination(num_tubes, size_of_tube, color, unit, state):
  for i in range(num_tubes):
    if state[i][0] == color:
      if (size_of_tube - len(state[i]) >= unit):
        return i
  return state.index(["empty"])

def only_color(color, lst):
  for i in lst:
    if i != color:
      return False
  return True

def remove_color(color, lst):
  i = 0
  for _ in lst:
    if lst[i][1] == color:
      lst.remove(lst[i])
    i = i + 1
  return lst

def find_color(num_tubes, color, map, state):
  for i in range(num_tubes):
    if map[i][1] == color:
      num = map[i][0]

      if only_color(color, state[i]):
        color, num = find_max(remove_color(color, choose(map)))
        return color, num
  return color, num

def modify_state(num_tubes, color, dest, map, state):
  color, num = find_color(num_tubes, color, map, state)
  
  for i in range(num_tubes):
    if map[i][1] == color:
      try:
        while True:
          state[i].remove(color)
      except ValueError:
        if not state[i]:
          state[i].append("empty")
        else:
          pass

      if state[dest] == ['empty']:
        state[dest].remove('empty')

  for x in range(num):
    state[dest].append(color)
      
  return state

def main():
  state = [["pb" , "sr" , "kr" , "pb"] , ["sr" , "ys" , "ys" , "kr"] , ["mv", "mv", "mv"] , [ "kr", "ys" , "kr" , "pb"] , ["sr", "ys", "mv" , "mv"] , ["empty"] , ["empty"]]
  size_of_tube = 4
  map = create_map(state)
  color, unit = find_max(choose(map))
  dest = find_destination(len(state), size_of_tube, color, unit, state)
  result = modify_state(len(state), color, dest, map, state)
  print(result)

if __name__ == "__main__":
    main()
