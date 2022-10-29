import pygame, sys
from pygame import Vector2

WIDTH = 600
HEIGHT = 600
FPS = 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 10)


def lerp(p0, p1, t):
    return p0 + t * (p1 - p0)

def line(st_pos, end_pos, color = 'white'):
    pygame.draw.line(screen, color, st_pos, end_pos, 2)

def dot(center, color = 'white'):
    pygame.draw.circle(screen, color, center, 5)

def rect(rct, color = 'white'):
    pygame.draw.rect(screen, color, rct)

def create_dot_rect_surface(center, size = 5):
    return pygame.Rect(center.x-(size/2), center.y-(size/2), size, size)

class Curve():
    def __init__(self):
        self.p0 = Vector2(0, HEIGHT/2)
        self.p1 = Vector2(WIDTH, HEIGHT/2)
        self.t = 0
        self.bezier = list()

    def quadratic(self, p0, p1, p2, draw = True):
        line(p0, p1)
        line(p1, p2)

        x1 = lerp(p0.x, p1.x, self.t)
        y1 = lerp(p0.y, p1.y, self.t)
        x2 = lerp(p1.x, p2.x, self.t)
        y2 = lerp(p1.y, p2.y, self.t)
        line((x1, y1), (x2, y2), 'red')

        x = lerp(x1, x2, self.t)
        y = lerp(y1, y2, self.t)
        dot((x, y), 'red')
        dot((x1, y1), 'red')
        dot((x2, y2), 'red')

        if draw:
            self.bezier.append(Vector2(x, y))

        return Vector2(x, y)

    def cubic(self, start_p, c_p0, c_p1, end_p, draw = True):
        q_p0 = self.quadratic(start_p, c_p0, c_p1, False)
        q_p1 = self.quadratic(c_p0, c_p1, end_p, False)

        line(q_p0, q_p1, 'green')

        x = lerp(q_p0.x, q_p1.x, self.t)
        y = lerp(q_p0.y, q_p1.y, self.t)

        dot((x, y), 'green')

        if draw:
            self.bezier.append(Vector2(x, y))

        return Vector2(x, y)

    def quartic(self, start_p, c_p0, c_p1, c_p2, end_p, draw = True):
        cubic_p0 = self.cubic(start_p, c_p0, c_p1, c_p2, False)
        cubic_p1 = self.cubic(c_p0, c_p1, c_p2, end_p, False)

        line(cubic_p0, cubic_p1, 'blue')

        x = lerp(cubic_p0.x, cubic_p1.x, self.t)
        y = lerp(cubic_p0.y, cubic_p1.y, self.t)

        dot((x, y), 'blue')

        if draw:
            self.bezier.append(Vector2(x, y))


    def render_bezier(self):
        prev_point = self.p0
        for point in self.bezier[1:]:
            line(prev_point, point, 'yellow')
            prev_point = point


points_rect = list()

curve = Curve()

start_point = curve.p0
points_rect.append([start_point, create_dot_rect_surface(start_point), False])

curving_point = Vector2(100, 400)
points_rect.append([curving_point, create_dot_rect_surface(curving_point), False])

curving_point2 = Vector2(200, 50)
points_rect.append([curving_point2, create_dot_rect_surface(curving_point2), False])

curving_point3 = Vector2(500, 150)
points_rect.append([curving_point3, create_dot_rect_surface(curving_point3), False])

end_point = curve.p1
points_rect.append([end_point, create_dot_rect_surface(end_point), False])

print(points_rect)

render = False
moving = False

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE:
            if render:
                if curve.t < 1:
                    curve.t += 0.001

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                render = True

        if event.type == pygame.MOUSEBUTTONUP:
            moving = False

            for p_r in points_rect:
                p_r[2] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
            for p_r in points_rect:

                if p_r[1].collidepoint(event.pos):
                    p_r[2] = True
                    break
                else:
                    p_r[2] = False

        

    screen.fill((25, 25, 25))

    mouse_pos = pygame.mouse.get_pos()

    for p_r in points_rect:
        if p_r[2] and moving:
            p_r[0] = Vector2(mouse_pos)
            p_r[1] = create_dot_rect_surface(p_r[0])

        rect(p_r[1])

    if render:
        curve.quartic(points_rect[0][0], points_rect[1][0], points_rect[2][0], points_rect[3][0], points_rect[4][0])
        curve.render_bezier()


    pygame.display.flip()
    clock.tick(FPS)