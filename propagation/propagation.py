import math
import random
import pygame

class Point:
	def __init__(self, x, y, label = None):
		self.x = x
		self.y = y
		self.label = label

	@staticmethod
	def random(xmin, xmax, ymin, ymax):
		self.x = random.random() * (xmax - xmin) + xmin
		self.y = random.random() * (ymax - ymin) + ymin
		self.label = None

	def distSquared(self, other):
		x = self.x - other.x
		y = self.y - other.y
		return x * x + y * y


class Rect:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def isPointInside(self, point):
		return point.x >= self.x and point.x < self.x + self.w and point.y >= self.y and point.y < self.y + self.h

	def intersects(self, rect):
		return not (self.x + self.w < rect.x or rect.x + rect.w < self.x or self.y + self.h < rect.y or rect.y + rect.h < self.y)


class QuadTree:
	def __init__(self, rect, capacity = 4):
		self.rect = rect
		self.capacity = capacity
		self.points = [None] * capacity
		self.size = 0
		self.ne = None
		self.se = None
		self.sw = None
		self.nw = None

	def add(self, point):
		if not self.rect.isPointInside(point):
			return False

		if self.size < self.capacity:
			self.points[self.size] = point
			self.size += 1
			return True

		if self.ne is None:
			rect = Rect(self.rect.x + self.rect.w / 2, self.rect.y, self.rect.w / 2, self.rect.h / 2)
			self.ne = QuadTree(rect, self.capacity)
			rect = Rect(self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2, self.rect.w / 2, self.rect.h / 2)
			self.se = QuadTree(rect, self.capacity)
			rect = Rect(self.rect.x, self.rect.y + self.rect.h / 2, self.rect.w / 2, self.rect.h / 2)
			self.sw = QuadTree(rect, self.capacity)
			rect = Rect(self.rect.x, self.rect.y, self.rect.w / 2, self.rect.h / 2)
			self.nw = QuadTree(rect, self.capacity)

		if self.ne.add(point):
			return True
		if self.se.add(point):
			return True
		if self.sw.add(point):
			return True
		if self.nw.add(point):
			return True

		return False

	def getPointsInside(self, rect, liste):
		if not rect.intersects(self.rect):
			return

		for i in range(self.size):
			if rect.isPointInside(self.points[i]):
				liste.append(self.points[i])

		if self.ne is not None:
			self.ne.getPointsInside(rect, liste)
			self.se.getPointsInside(rect, liste)
			self.sw.getPointsInside(rect, liste)
			self.nw.getPointsInside(rect, liste)

	def draw(self, screen, drawPoint = True):
		pRect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
		pygame.draw.rect(screen, (128, 128, 128), pRect, width=1)

		if drawPoint:
			for i in range(self.size):
				color = self.points[i].label

				if color is None:
				    color = (0, 0, 0)

				pygame.draw.circle(screen, color, (self.points[i].x, self.points[i].y), 4)

		if self.ne is not None:
			self.ne.draw(screen, drawPoint)
			self.se.draw(screen, drawPoint)
			self.sw.draw(screen, drawPoint)
			self.nw.draw(screen, drawPoint)

class Cloud:
	def __init__(self, rect):
		self.rect = rect
		self.points = []
		self.size = 0
		self.sizeLabeled = 0

		# TODO retirer les lignes suivante qui ne servent qu'a l'affichage
		self.quadTree = QuadTree(self.rect)
		self.propagation_en_cours = False

	def add(self, point):
		self.points.append(point)
		self.size += 1

		if point.label is not None:
			self.sizeLabeled += 1

		# TODO retirer la ligne suivante qui ne sert qu'a l'affichage
		self.quadTree.add(point)

	def extract(self, rect):
		extracted = []
		liste = []
		self.quadTree.getPointsInside(rect, liste)

		for point in liste:
			if point.label is None:
				extracted.append(point)

		return extracted

	def propagate_setup(self):
		if self.sizeLabeled == 0:
			return
		
		closests = []

		for p1 in self.points:
			closest = float('inf')

			for p2 in self.points:
				if p1 != p2:
					dist = p1.distSquared(p2)

					if dist < closest:
						closest = dist

			closests.append(closest)

		self.rangeIncrement = 4 * sum(closests) / len(closests)

		self.propagation_en_cours = True
		self.labeled = [p for p in self.points if p.label is not None]
		self.labeledRange = [0 for p in self.labeled]
		self.resetQuadTree = True

	def propagate_update(self):
		if not self.propagation_en_cours:
			return False

		if len(self.labeled) >= self.size:
			self.propagation_en_cours = False
			return False

		processed = []

		if self.resetQuadTree:
			self.quadTree = QuadTree(self.rect)

			for p in self.points:
				if p.label is None:
					self.quadTree.add(p)

			self.resetQuadTree = False

		for i, pointA in enumerate(self.labeled):
			self.labeledRange[i] += self.rangeIncrement

			rect = Rect(
				pointA.x - self.labeledRange[i],
				pointA.y - self.labeledRange[i],
				2 * self.labeledRange[i],
				2 * self.labeledRange[i]
			)

			insideSquareRange = self.extract(rect)
			
			for pointB in insideSquareRange:
				if pointA.distSquared(pointB) < self.labeledRange[i]:
					pointB.label = pointA.label
					processed.append(pointB)
					self.labeledRange.append(0)

		self.labeled = self.labeled + processed

		if len(processed) > 0:
			self.resetQuadTree = True

		return True

	def draw(self, screen):
		for point in self.points:
			color = point.label

			if color is None:
				color = (0, 0, 0)

			pygame.draw.circle(screen, color, (point.x, point.y), 4)

		if self.propagation_en_cours:
			self.quadTree.draw(screen, False)

			for i, point in enumerate(self.labeled):
				a = math.sqrt(self.labeledRange[i])
				pygame.draw.circle(screen, (128, 128, 128), (point.x, point.y), a, width=1)
