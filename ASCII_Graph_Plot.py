import sys
from time import sleep

'''
Limiting values:

max_functions- number of user functions you can enter to graph

max_range- sets the size of the graph that is displayed

'''
max_functions = 3
max_range = 61

#Graph ascii characters:
fill, end_str = 'X', ''

#Text color reference library
color_dict = {
  0:'\033[1;30;50m',
  1:'\033[1;31;50m',
  2:'\033[1;32;50m',
  3:'\033[1;33;50m',
  4:'\033[1;34;50m',
  5:'\033[1;35;50m',
  6:'\033[1;36;50m',
  7:'\033[1;37;50m'
}

def input_numfunctions(max_functions):
  ''' Retrieves user input value for number of functions to graph '''
  print(f'Graphing Calculator:')
  while True:
    try:
      num_functions = int(input(f'How many functions would you like to graph? (up to {max_functions}) '))
      if num_functions >= 1 and num_functions <= max_functions:
        return num_functions
      else:
        raise Exception
    except:
      print('Please give a correct value ')
  
def input_colorfunctions(num_functions,color_dict=[]):
  ''' Retrieves user input values for function colors and outputs as list'''
  def appendInt(num):
    ''' Converts numerals to ordinals '''
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return 'st'
    elif (lastDigit == 2):
        return 'nd'
    elif (lastDigit == 3):
        return 'rd'
    else:
        return 'th'

  user_colors = []
  print(f'Options:\n',
        f'{color_dict[0]} Dark Gray(0)\n', 
        f'{color_dict[1]} Bright Red(1)\n',     
        f'{color_dict[2]} Bright Green(2)\n',   
        f'{color_dict[3]} Yellow(3)\n',        
        f'{color_dict[4]} Bright Blue(4)\n',   
        f'{color_dict[5]} Bright Magenta(5)\n',
        f'{color_dict[6]} Bright Cyan(6)\n',    
        f'{color_dict[7]} White(7)'
        ) 

  for count in range(1,num_functions+1):
    while True:
      try:
        user_input = int(round(float(input(f'What color for {count}{appendInt(count)} graph? '))))
        if user_input >= 0 and user_input <= 7:
          #Color value is offshifted here by 1 to not interfere with null plot points in matrix
          user_colors.append(user_input+1)
          break
        else:
          raise Exception
      except:
        print('Please enter a valid value')
  return user_colors

def input_userfunctions(num_functions):
  ''' Retrieves user functions and outputs as list '''
  user_functions = []
  for count in range(num_functions):
    user_input = str(input("y = ")) 
    user_functions.append(user_input)
  return user_functions

def generate_matrix(max_range):
  ''' Generates a 2d list based on maximum range '''
  matrix = [[0 for _ in range(max_range)] for _ in range(max_range)]
  return matrix

def eval_userfunctions(num_functions,midpoint,matrix=[],user_colors=[],user_functions=[]):
  ''' Evaluates user functions within range of matrix and assigns relevant x and y values '''
  a_range = midpoint * (-1)
  b_range = midpoint - 1
  
  for _ in range(num_functions):
    for count in range(a_range, b_range):
      try:
        #Evaluates value of Y for value of X of user's function, taking complex numbers into account
        x = count
        #Takes care of any pesky uppercase issues:
        function_formatted = str(user_functions[_]).lower()
        y = eval(function_formatted)
        if isinstance(y, complex):
          y = round(round(y.real),round(y.imag))
        else:
          y = round(y)
      except:
        #Exits program with user message if functions are not evaluable
        print(f'Your function: {user_functions[_]}? Yeah.... that\'s not going to work, we\'re going to need to try that again')
        sleep(1000)
        sys.exit()
      #Stores the x and y plot points in the matrix to correspond to cartesian system when 'printed', 'X' is stored as it's relevant color value
      if y >= a_range and y <= b_range:
        matrix[-1*(y+midpoint)][x+midpoint-1] = user_colors[_]
  return matrix

def print_graph(fill,end_str,midpoint,matrix=[],color_dict=[]):
  ''' Prints the matrix '''
  print(f'\n'*3)
  counter_row, counter_pixel = 0, 0

  for row in matrix:
    counter_row += 1
    counter_pixel = 0

    for pixel in row:
      counter_pixel += 1
      
      if pixel:
        #Displays fill value (ie. function plot points) in color determined by stored value in matrix 
        if counter_row == midpoint:
          print(f'{color_dict[(pixel-1)]}.{fill}', end = end_str)
        else:
          print(f'{color_dict[(pixel-1)]} {fill}', end = end_str)

      #Draws the Y axis lines
      elif counter_pixel == midpoint:
        if counter_row == midpoint:
          print(f'{color_dict[7]}.|', end = end_str)
        else:
          print(f'{color_dict[7]} |', end = end_str)
      #Draws the X axis, leftmost point has a space to keep everything looking even
      elif counter_row == midpoint:
        if counter_pixel == 1:
          print(f'{color_dict[7]} .', end = end_str)  
        else:
          print(f'{color_dict[7]}..', end = end_str)
      #Draws the remaining empty space on the graph
      else:
        print(f'{color_dict[7]} .', end = end_str) 

    print()

midpoint = int((max_range + 1)/2)

num_functions = input_numfunctions(max_functions)
user_colors = input_colorfunctions(num_functions,color_dict)
user_functions = input_userfunctions(num_functions)
matrix = generate_matrix(max_range)
 
eval_userfunctions(num_functions,midpoint,matrix,user_colors,user_functions)
print_graph(fill,end_str,midpoint,matrix,color_dict)
