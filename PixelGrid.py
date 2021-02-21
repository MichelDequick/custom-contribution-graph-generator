import cv2
import numpy as np
from win32api import GetSystemMetrics
import sys

class PixelGrid:
    def __init__(self, dimentions, scale):
        self.grid_x, self.grid_y = dimentions
        self.grid = np.zeros((self.grid_y, self.grid_x), int)

        self.window_scale = scale
        self.drawing = 0

        screen_x = GetSystemMetrics(0)
        screen_y = GetSystemMetrics(1)

        if(screen_x / screen_y > self.grid_x / self.grid_y):
            # Scale with height
            self.window_y = int(screen_y * self.window_scale)
            self.window_x = int(self.window_y / self.grid_y * self.grid_x)
        else:
            # Scale with width
            self.window_x = int(screen_x * self.window_scale)
            self.window_y = int(self.window_x / self.grid_x * self.grid_y)

        self.cube_size = int(8 / 10 * (self.window_x) / self.grid_x)
        self.border_size = int(self.cube_size / 8 * 2)
        self.window_x = self.border_size + (self.cube_size + self.border_size) * self.grid_x
        self.window_y = self.border_size + (self.cube_size + self.border_size) * self.grid_y

    def getGrid(self):
        self.img = np.zeros((self.window_y, self.window_x,3), np.uint8)
        self.img[:] = [255, 255, 255]

        ############### Draw grid
        for x in range(0, self.grid_x):
            for y in range(0, self.grid_y):
                self.drawBlock(x, y, (235, 237, 240))

        cv2.namedWindow('Github Contributions Calendar Generator')
        cv2.setMouseCallback('Github Contributions Calendar Generator', self.mouseHandler)
        while(True):
            cv2.imshow('Github Contributions Calendar Generator',self.img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):                   # Press 'c' to clear screen    
                self.clearGrid()
            elif key == ord('\r'):                 # Press 'enter' to confirm
                break
            elif key == ord('x'):
                sys.exit(0)

        cv2.destroyAllWindows()

        np.set_printoptions(linewidth=128)
        print(self.grid)
        return self.grid


    def clearGrid(self):
        self.grid.fill(0)
        self.drawGrid()
        
    def setBlock(self, x, y, value):
        self.grid[y][x] = value
        self.drawGrid()

    def drawGrid(self):
        for x in range(0, self.grid.shape[1]):
            for y in range(0, self.grid.shape[0]):
                if(self.grid[y][x] > 0):
                    self.drawBlock(x, y,(35, 154, 59))
                else:
                    self.drawBlock(x, y,(235, 237, 240))
                    self.grid[y][x] = 0


    def drawBlock(self, x, y, r__g__b):
        x = int(self.border_size + (self.border_size + self.cube_size) * x) - 1
        y = int(self.border_size + (self.border_size + self.cube_size) * y) - 1
        cv2.rectangle(self.img,(x, y),(x + self.cube_size, y + self.cube_size),(r__g__b[0], r__g__b[1], r__g__b[2]), -1)

    def winToGrid(self, x, y):
        x = int((x / self.window_x) * self.grid_x)
        y = int((y / self.window_y) * self.grid_y)
        return (x, y) if x >= 0 and y >= 0 and x < self.grid_x and y < self.grid_y else (-1, -1)

    def gridToWin(self, x, y):
        x = int(self.border_size + (self.border_size + self.cube_size) * x) 
        y = int(self.border_size + (self.border_size + self.cube_size) * y) 
        return (x, y) if x >= 0 and y >= 0 else (-1, -1)

    def mouseHandler(self, event,x,y,flags,param):
        x = self.winToGrid(x, y)[0]
        y = self.winToGrid(x, y)[1]

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = 1
            self.setBlock(x, y, self.drawing)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing != 0:
                self.setBlock(x, y, self.drawing)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = 0
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.drawing = -1
            self.setBlock(x, y, self.drawing)

        elif event == cv2.EVENT_RBUTTONUP:
            self.drawing = 0