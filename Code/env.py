import math
import pygame


class buildEnvironment:
    def __init__(self, MapDimensions):
        pygame.init()
        self.pointCloud = []
        self.externalMap = pygame.image.load('Floor Plan.png')
        self.maph, self.mapw = MapDimensions
        self.MapWindowName = 'Point Cloud Test'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.externalMap, (0, 0))
        # Colours
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

    def AD2pos(self, distance, angle, dronePosition):
        x = distance * math.cos(angle) + dronePosition[0]
        y = -distance * math.sin(angle) + dronePosition[1]
        return int(x), int(y)

    def dataStorage(self, data):
        print(len(self.pointCloud))
        for element in data:
            point = self.AD2pos(element[0], element[1], element[2])
            if point not in self.pointCloud:
                self.pointCloud.append(point)

    def show_lidarData(self):
        self.infomap = self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at((int(point[0]), int(point[1])), (255, 0, 0))
