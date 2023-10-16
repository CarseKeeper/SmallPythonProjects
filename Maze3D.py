import copy, sys, os

WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'
BLOCK = chr(9617) #Character 9617 is the '░'
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'

def wallStrToWallDict(wallStr):
    wallDict: dict[tuple[int,int]] = {}
    height:int = 0
    width:int = 0
    for y, line in enumerate(wallStr.splitlines()):
        if y > height:
            height = y
        for x, character in enumerate(line):
            if x > width:
                width = x
            wallDict[(x,y)] = character
    wallDict['height'] = height + 1
    wallDict['width'] = width + 1
    return wallDict

EXIT_DICT = {(0,0): 'E', (1,0): 'X', (2,0): 'I', (3,0): 'T', 'height': 1, 'width': 4}

ALL_OPEN = wallStrToWallDict(r'''
.................
____.........____
...|\......./|...
...||.......||...
...||__...__||...
...||.|\./|.||...
...||.|.X.|.||...
...||.|/.\|.||...
...||_/...\_||...
...||.......||...
___|/.......\|___
.................
.................'''.strip())

CLOSED = {}
CLOSED['A'] = wallStrToWallDict(r'''
_____
.....
.....
.....
_____'''.strip())

CLOSED['B'] = wallStrToWallDict(r'''
.\.
..\
...
...
...
../
./.'''.strip())

CLOSED['C'] = wallStrToWallDict(r'''
___________
...........
...........
...........
...........
...........
...........
...........
...........
___________'''.strip())

CLOSED['D'] = wallStrToWallDict(r'''
./.
/..
...
...
...
\..
.\.'''.strip())

CLOSED['E'] = wallStrToWallDict(r'''
..\..
...\.
....|
....|
....|
....|
....|
....|
....|
....|
....|
.../.
../..'''.strip())

CLOSED['F'] = wallStrToWallDict(r'''
../..
./...
|....
|....
|....
|....
|....
|....
|....
|....
|....
.\...
..\..'''.strip())

def displayWallDict(wallDict):
    print(BLOCK * (wallDict['width'] + 2))
    for y in range(wallDict['height']):
        print(BLOCK, end='')
        for x in range(wallDict['width']):
            wall = wallDict[(x,y)]
            if wall == '.':
                wall = ' '
            print(wall, end='')
        print(BLOCK)
    print(BLOCK * (wallDict['width'] + 2))
    
def pasteWallDict(srcWallDict, distWallDict, left, top):
    distWallDict = copy.copy(distWallDict)
    for x in range(srcWallDict['width']):
        for y in range(srcWallDict['height']):
            distWallDict[(x + left,y + top)] = srcWallDict[(x,y)]
    return distWallDict

def makeWallDict(maze, playerx, playery, playerDirection, exitx, exity):
    if playerDirection == NORTH:
        offsets = (('A', 0, -2), ('B', -1, -1), ('C', 0, -1), 
                   ('D', 1, -1), ('E', -1, 0), ('F', 1, 0))
    if playerDirection == SOUTH:
        offsets = (('A', 0, 2), ('B', 1, 1), ('C', 0, 1), 
                   ('D', -1, 1), ('E', 1, 0), ('F', -1, 0))
    if playerDirection == EAST:
        offsets = (('A', 2, 0), ('B', 1, -1), ('C', 1, 0),
                   ('D', 1, 1), ('E', 0, -1), ('F', 0, 1))
    if playerDirection == WEST:
        offsets = (('A', -2, 0), ('B', -1, 1), ('C', -1, 0),
                   ('D', -1, -1), ('E', 0, 1), ('F', 0, -1))
    
    section = {}
    for sec, xOff, yOff in offsets:
        section[sec] = maze.get((playerx + xOff, playery + yOff), WALL)
        if (playerx + xOff, playery + yOff) == (exitx, exity):
            section[sec] = EXIT
    
    wallDict = copy.copy(ALL_OPEN)
    PASTE_CLOSED_TO = {'A': (6,4), 'B': (4,3), 'C': (3,1),
                       'D': (10,3), 'E': (0,0), 'F': (12,0)}
    
    for sec in 'ABDCEF':
        if section[sec] == WALL:
            wallDict = pasteWallDict(CLOSED[sec], wallDict,
                                     PASTE_CLOSED_TO[sec][0], PASTE_CLOSED_TO[sec][1])
            
    if section['C'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 7, 9)
    if section['E'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 0, 11)
    if section['F'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 13, 11)

    return wallDict

while True:
    filename = input("Input filename, LIST for maze files, or QUIT\n>")
    if filename.upper() == 'LIST':
        print('MAZE FILES IN ', os.getcwd())
        for file in os.listdir():
            if(file.startswith('maze') and file.endswith('.txt')):
                print('\t', file)
        continue
    
    if filename.upper() == 'QUIT':
        sys.exit()
    
    if os.path.exists(filename):
        break
    print('Couldn\'t find file named ', filename)
    

print('Maze Runner 3D!!!')

mazeFile = open(filename)
maze = {}
lines = mazeFile.readlines()
px = None
py = None
exitx = None
exity = None
y = 0
for line in lines:
    WIDTH = len(line.rstrip())
    for x, character in enumerate(line.rstrip()):
        assert character in (WALL, EMPTY, START, EXIT), 'Invalid character at column {1}, line {2}'.format(x+1, y+1)
        if character in (WALL, EMPTY):
            maze[(x,y)] = character
        elif character == START:
            px, py = x, y
            maze[(x,y)] = EMPTY
        elif character == EXIT:
            exitx, exity = x, y
            maze[(x,y)] = EMPTY
    y += 1
HEIGHT = y
    
assert px != None and py != None, 'No START point in maze. :('
assert exitx != None and exity != None, 'No EXIT point in maze. :('
pDir = NORTH

while True:
    displayWallDict(makeWallDict(maze, px, py, pDir, exitx, exity))
    
    while True:
        print('Location ({},{}) Direction: {}'.format(px,py,pDir))
        print('                    (W)')
        print('Enter direction: (A)   (D) or QUIT.')
        move = input('> ').upper()
        
        if move == 'QUIT':
            print('Thanks for playing.')
            sys.exit()
        
        if (move not in ['F', 'L', 'R', 'W', 'A', 'D'] and not move.startswith('T')):
            print('Please enter one of F, L, or R (or W, A, D).')
            continue
        
        if move == 'F' or move == 'W':
            if pDir == NORTH and maze[(px,py - 1)] == EMPTY:
                py -= 1
                break
            if pDir == SOUTH and maze[(px,py + 1)] == EMPTY:
                py += 1
                break
            if pDir == EAST and maze[(px + 1,py)] == EMPTY:
                px += 1
                break
            if pDir == WEST and maze[(px - 1,py)] == EMPTY:
                px -= 1
                break
        elif move == 'L' or move == 'A':
            pDir = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}[pDir]
            break
        elif move == 'R' or move == 'D':
            pDir = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[pDir]
            break
        elif move.startswith('T'):
            px, py = move.split()[1].split(',')
            px = int(px)
            py = int(py)
            break
        else:
            print('You can\'t move there.')
            
    if (px,py) == (exitx,exity):
        print('You solved the maze! :)\n Thanks for Playing!')
        sys.exit()