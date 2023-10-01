import pygame
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import sys
import random
import time 
from functools import wraps

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def timer(f):

	@wraps(f)
	def wrapper(*args, **kwargs):
		t0 = time.perf_counter()
		f(*args, **kwargs)
		t1 = time.perf_counter()
		print (f"Elapsed time {t1-t0:0.2f} seconds")
	return wrapper


@dataclass
class Box:
	pos_x: int
	pos_y: int 
	width: int
	height: int
	color: Tuple[int] = field(default_factory = tuple)

	def __post_init__(self):
		self.r = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height) 
	


@dataclass
class SortingVis:

	pygame.font.init()
	font = pygame.font.SysFont('Comic Sans MS', 32)
	arr: List[Any] = field(default_factory = list)
	val_range: int = 500
	block_width: int = 1
	bottom_line: int = 700
	width: int = 1280
	height: int = 720
	gap: int = 0
	is_sorted = False

	def __post_init__(self):

		self.n = len(self.arr)
		if self.n:
			self.block_width = self.set_block_width()
		self.screen = pygame.display.set_mode((self.width, self.height))

	def set_block_width(self):
		return max(self.block_width, (self.width - self.n * self.gap) // self.n)

	def generate_random(self, n):
		
		self.n = n
		self.block_width = self.set_block_width()
		for i in range(self.n):
			rand = random.randint(1, self.val_range)
			self.arr.append(rand)

	def draw_sorted(self):
		# self.screen.fill(BLACK)
		self.is_sorted = True
		for i in range(self.n):
			x = self.arr[i]
			pygame.draw.rect(self.screen, GREEN, pygame.Rect(i * (self.block_width + self.gap), self.bottom_line - x, self.block_width, x))
			time.sleep(0.005)
			pygame.display.flip()

	def draw(self, a = -1, b = -1, t = 0, slowdown = 0):
		
		time.sleep(slowdown)
		self.screen.fill(BLACK)
		if t:
			self.draw_time(t)
		for i in range(self.n):
			x = self.arr[i]
			if i in [a-i for i in range(1, 2)]:
				clr = RED
			elif i in [b-i for i in range(1, 2)]:
				clr = RED
			else:
				clr = WHITE
			pygame.draw.rect(self.screen, clr, pygame.Rect(i * (self.block_width + self.gap), self.bottom_line - x, self.block_width, x))
		pygame.display.flip()

	def draw_time(self, t):
		
		text = self.font.render(f"Elapsed time {t:0.2f} seconds", False, GREEN)
		text_rect = text.get_rect()
		text_rect.center = (self.width // 2, 100)
		self.screen.blit(text, text_rect)

	
	def bubble_sort(self):
		t0 = time.perf_counter()
		for i in range(self.n - 1):
			for j in range(self.n - 1 - i):
				if self.arr[j] > self.arr[j + 1]:

					self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]

				t1 = time.perf_counter() 
				
				self.draw(j, j + 1, t1 - t0)

		self.draw_sorted()

	def insertion_sort(self):
		t0 = time.perf_counter()

		for i in range(self.n):
			curr = self.arr[i]
			j = i - 1
			
			while j >= 0 and curr < self.arr[j]:
				self.arr[j + 1] = self.arr[j]
				j -= 1
				self.draw(j + 1, t = time.perf_counter() - t0, slowdown = 0)

			self.arr[j + 1] = curr
			self.draw(t = time.perf_counter() - t0, slowdown = 0)

		self.draw_sorted()

	def merge(self, l, mid, r, t0):
		
		L = self.arr[l:mid]
		R = self.arr[mid:r]
		a, b = l, mid
		k = l 
		while L and R:
			if L[0] <= R[0]:
				a += 1
				self.arr[k] = L.pop(0)
			else:
				b += 1
				self.arr[k] = R.pop(0)
			k += 1
			self.draw(a, b, t = time.perf_counter() - t0, slowdown = 0)
		
		while L:

			self.arr[k] = L.pop(0)
			a += 1
			k += 1
			self.draw(a, k, t = time.perf_counter() - t0, slowdown = 0)
		while R:
			self.arr[k] = R.pop(0)
			self.draw(a, k, t = time.perf_counter() - t0, slowdown = 0)
			b += 1
			k += 1

		self.draw(t = time.perf_counter() - t0, slowdown = 0)

	def merge_sort(self, l, r, t0):
		
		if l < r - 1:
			
			mid = (l + r) // 2
			
			self.merge_sort(l, mid, t0)
			self.draw(time.perf_counter() - t0, slowdown = 0)
			self.merge_sort(mid, r, t0)
			self.draw(time.perf_counter() - t0, slowdown = 0)
			self.merge(l, mid, r, t0)


	def quick_sort(self, l, r, t0):

		if len(self.arr[l:r+1]) == 1:
			return

		if l < r:
			pivot = self.partition(l, r, t0)
			self.quick_sort(l, pivot - 1, t0)
			self.quick_sort(pivot + 1, r, t0)
			self.draw(slowdown = 0)

		
	def partition(self, l, r, t0):
		i = l - 1
		pivot = self.arr[r]
		
		for j in range(l, r):
			if self.arr[j] <= pivot:

				i += 1
				self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

			# self.draw(j, slowdown = 0.01)
			self.draw(i, j, time.perf_counter() - t0, slowdown = 0)
		self.arr[i + 1], self.arr[r] = self.arr[r], self.arr[i + 1]
		return i + 1

	def unsort(self):
		self.screen.fill(BLACK)
		self.is_sorted = False
		random.shuffle(self.arr)

pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.arrow)


lst = SortingVis()
lst.generate_random(100)
clock = pygame.time.Clock()
clock.tick(144)
lst.draw()
while True:
	
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_b:
				lst.bubble_sort()
			if event.key == pygame.K_i:
				lst.insertion_sort()

			if event.key == pygame.K_r:
				lst.unsort()

			if event.key == pygame.K_q:
				t0 = time.perf_counter()
				lst.quick_sort(0, lst.n - 1, t0)
				lst.draw_sorted()
			if event.key == pygame.K_m:
				t0 = time.perf_counter()
				lst.merge_sort(0, lst.n, t0)
				lst.draw_sorted()
				
	
	if not lst.is_sorted:
		lst.draw()
	
		
	
	# lst.draw()






