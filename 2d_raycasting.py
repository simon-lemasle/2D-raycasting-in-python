import pygame
import math
import numpy as np

pygame.init()

# Screen
WIDTH , HEIGHT = 1200 , 800
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('2d raycating')



# line class --------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Line:
    def __init__(self, Ax, Ay, Bx, By, color = (255, 255, 255)):
        self.Ax = Ax
        self.Ay = Ay
        self.Bx = Bx
        self.By = By
        self.color = color

        self.dx = Bx - Ax
        self.dy = By - Ay
    

    def intercept(self, ray):
        matB = np.array([self.Ax - ray.Ax, self.Ay - ray.Ay])
        matA = np.array([[ray.dx,ray.dy],
                         [-self.dx,-self.dy]])
        detMatA = np.linalg.det(matA)
        if detMatA != 0:
            S = np.matmul(matB,np.linalg.inv(matA))
            if S[0] > 0 and 0 <= S[1] <= 1:
                x = self.Ax + S[1] * self.dx
                y = self.Ay + S[1] * self.dy
                return x , y
        return ray.Ax + WIDTH * ray.dx, ray.Ay + WIDTH * ray.dy





    def draw(self):
        pygame.draw.line(SCREEN,self.color, (self.Ax,self.Ay), (self.Bx,self.By), 2)
        

# ray class --------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Ray:
    def __init__(self, Px, Py, theta, color = (241, 250, 140)):
        self.Ax = Px
        self.Ay = Py
        self.theta = theta
        self.color = color

        self.dx = math.cos(theta)
        self.dy = math.sin(theta)

        self.intercept = []

    def draw(self):
        if self.intercept == []:
            return
        pygame.draw.line(SCREEN,self.color, (self.Ax,self.Ay), self.intercept, 1)


# draw function --------------------------------------------------------------------------------------------------------------------------------------------------------------------



# main function --------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    clock = pygame.time.Clock()

    lines = [

    # --- Outer Room (rectangle) ---  ##### pasted from chatGPT
    Line(100,100,1100,100),
    Line(1100,100,1100,700),
    Line(1100,700,100,700),
    Line(100,700,100,100),

    # --- Central Box ---
    Line(450,300,750,300),
    Line(750,300,750,500),
    Line(750,500,450,500),
    Line(450,500,450,300),

    # --- Triangle ---
    Line(200,500,350,650),
    Line(350,650,100,650),
    Line(100,650,200,500),

    # --- Diagonal Structure ---
    Line(800,150,1050,300),
    Line(1050,300,900,450),

    # --- Broken Wall ---
    Line(300,150,500,200),
    Line(550,220,700,260)
]
    rays = []

    running = True
    while running:
        clock.tick(60)
        SCREEN.fill((0,0,0))

        point = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for i in range(360):
            rays.append(Ray(point[0],point[1],i*3.14159265/(180)))
        for ray in rays:
            for line in lines:
                inter = line.intercept(ray)
                if inter != None:
                    distanceFromInterceptSquared = (point[0]-inter[0]) ** 2 + (point[1]-inter[1]) ** 2
                    if len(ray.intercept) == 0:
                        ray.intercept = inter
                    elif distanceFromInterceptSquared < ((point[0]-ray.intercept[0]) ** 2 + (point[1]-ray.intercept[1]) ** 2):
                        ray.intercept = inter
            ray.draw()
        for line in lines:
            line.draw()
        pygame.draw.circle(SCREEN,(255,255,255),point,10)
        rays = []

        pygame.display.update()
    pygame.quit()

main()
