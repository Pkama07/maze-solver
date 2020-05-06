# Pradyun Kamaraju
# Maze generated using DFS
# Maze solved using BFS

from matplotlib import pyplot as plt
from random import shuffle, choice


class Box:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.sides = [True, True, True, True]
		self.visited = False
		self.adjacents = []


	def __repr__(self):
		return str((self.x, self.y))


def generate_maze(node):
	node.visited = True
	x = node.x
	y = node.y
	changes = [(x-1, y, 0), (x, y+1, 1), (x, y-1, 2), (x+1, y, 3)]
	shuffle(changes)
	for change in changes:
		new_x = change[0]
		new_y = change[1]
		if 0 <= new_x < len(maze) and 0 <= new_y < len(maze):
			if not maze[new_y][new_x].visited:
				index = change[2]
				node.sides[index] = False
				maze[new_y][new_x].sides[-index-1] = False
				generate_maze(maze[new_y][new_x])


def draw_maze():
	for row in maze:
		for box in row:
			if box.sides[0]:
				plt.axvline(box.x, (len(maze) - box.y - 1)/len(maze), (len(maze) - box.y)/len(maze))
			if box.sides[3]:
				plt.axvline(box.x+1, (len(maze) - box.y - 1)/len(maze), (len(maze) - box.y)/len(maze))
			if box.sides[2]:
				plt.axhline(len(maze) - box.y, box.x/len(maze), (box.x+1)/len(maze))
			if box.sides[1]:
				plt.axhline(len(maze)-box.y-1, box.x/len(maze), (box.x+1)/len(maze))


def start_end():
	plt.plot([start[0], start[0]+1], [start[1], start[1]+1], color='red')
	plt.plot([start[0], start[0]+1], [start[1]+1, start[1]], color='red')
	if side:
		maze[edge][-1].sides[3] = False
		plt.axvline(maze[edge][-1].x+1, (len(maze) - maze[edge][-1].y - 1)/len(maze), (len(maze) - maze[edge][-1].y)/len(maze), color='green', linewidth='5')
		end = (size[0]-1, edge)
	else:
		maze[0][edge].sides[2] = False
		plt.axhline(len(maze) - maze[0][edge].y, maze[0][edge].x/len(maze), (maze[0][edge].x+1)/len(maze), color='green', linewidth='7')
		end = (edge, 0)
	return end


def make_graph():
	for y in range(size[1]):
		for x in range(size[0]):
			surroundings = [(x-1, y), (x, y+1), (x, y-1), (x+1, y)]
			for node in surroundings:
				if 0 <= node[0] < size[0] and 0 <= node[1] < size[1]:
					index = surroundings.index(node)
					if not maze[y][x].sides[index]:
						maze[y][x].adjacents.append((node[0], node[1]))
			adj_list[(x, y)] = maze[y][x].adjacents


def solve_maze(strt, en):
	converter = [num for num in range(size[0])]
	temp_y = converter[-strt[1]-1]
	new_start = (strt[0], temp_y)
	queue = []
	queue.append(new_start)
	done = False

	visited = [[False for x in range(size[0])] for y in range(size[1])]
	parents = [[None for x in range(size[0])] for y in range(size[1])]

	while queue and not done:
		node = queue.pop(0)
		visited[node[1]][node[0]] = True
		children = maze[node[1]][node[0]].adjacents
		for child in children:
			if not visited[child[1]][child[0]]:
				queue.append(child)
				parents[child[1]][child[0]] = node
			if child == en:
				done = True

	path = []
	parent = en
	while not parent == None:
		path.append(parent)
		parent = parents[parent[1]][parent[0]]

	return path[::-1]


def draw_solution(path):
	converter = [num for num in range(size[0])] + [size[0]]
	for x in range(1, len(path)):
		point = (path[x][0]+.5, converter[-path[x][1]-1]-.5)
		last_point = (path[x-1][0]+.5, converter[-path[x-1][1]-1]-.5)
		
		if last_point[1] == point[1]:
			plt.plot([last_point[0], point[0]], [last_point[1], point[1]], color='green')
		else:
			lower_y, higher_y = min(last_point[1], point[1]), max(last_point[1], point[1])
			plt.vlines(point[0], lower_y, higher_y, colors=['green'])


size = (40, 40)

maze = [[Box(x, y) for x in range(size[0])] for y in range(size[1])]
plt.figure()
plt.ylim([0, size[1]])
plt.xlim([0, size[0]])

start = (1, 1)

generate_maze(maze[-start[1]-1][start[0]])

side = choice([True, False])
edge = choice([x for x in range(size[0])])
end = start_end()

draw_maze()
end = start_end()
plt.show()
# present solution
plt.figure()
plt.ylim([0, size[1]])
plt.xlim([0, size[0]])
draw_maze()
start_end()
adj_list = {}
make_graph()
pathway = solve_maze(start, end)
draw_solution(pathway)
plt.show()
