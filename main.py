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
font = pygame.font.SysFont('arial', 30)


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

    def reset(self):
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


    def render_bezier(self, str_p):
        prev_point = str_p
        for point in self.bezier[1:]:
            line(prev_point, point, 'yellow')
            prev_point = point

class Button():
    def __init__(self, center_pos, txt, w = 150, h = 50, bg = 'black', antialias = True, txt_color = 'white'):
        self.pos = center_pos
        self.w = w
        self.h = h
        self.txt = txt
        self.antialias = antialias
        self.txt_color = txt_color
        self.bg = bg
    
    def render(self):
        self.bg_rect = pygame.Rect((self.pos[0]-(self.w/2)), (self.pos[1]-(self.h/2)), self.w, self.h)
        self.text = font.render(self.txt, self.antialias, self.txt_color)
        self.rect = self.text.get_rect(center = self.pos)
        pygame.draw.rect(screen, self.bg, self.bg_rect)
        screen.blit(self.text, self.rect)

    def pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        self.min_x = self.pos[0]-(self.w/2)
        self.max_x = self.pos[0]+(self.w/2)
        self.min_y = self.pos[1]-(self.h/2)
        self.max_y = self.pos[1]+(self.h/2)
        return self.min_x < mouse_pos[0] < self.max_x and self.min_y < mouse_pos[1] < self.max_y

class Text():
    def __init__(self, center_pos, txt, size, color = 'white', bg_color = 'black', antialias = True, font = 'arial'):
        self.txt = txt
        self.color = color
        self.bg_color = bg_color
        self.antialias = antialias
        self.center_pos = center_pos
        self.font = pygame.font.SysFont(font, size)
        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)

    def render(self):
        screen.blit(self.rendered_txt, self.rect)

    def update(self, new_txt = None, new_center = None, new_color = None, new_bg_color = None):
        if new_txt == None:
            new_txt = self.txt
        else:
            self.txt = new_txt

        if new_center == None:
            new_center = self.center_pos
        else:
            self.center_pos = new_center

        if new_color == None:
            new_color = self.color
        else:
            self.color = new_color

        if new_bg_color == None:
            new_bg_color = self.bg_color
        else:
            self.bg_color = new_bg_color

        self.rendered_txt = self.font.render(self.txt, self.antialias, self.color, self.bg_color)
        self.rect = self.rendered_txt.get_rect(center = self.center_pos)

    


points_rect = list()
all_p = list()
quadratic_points = list()
cubic_points = list()
quartic_points = list()

curve = Curve()

text_offsett = Vector2(-10, -10)

start_point = curve.p0
text_pos = start_point+text_offsett
all_p.append([start_point, create_dot_rect_surface(start_point), False, Text((text_pos.x, text_pos.y), 'P', 10)])

curving_point = Vector2(100, 400)
text_pos = curving_point+text_offsett
all_p.append([curving_point, create_dot_rect_surface(curving_point), False, Text((text_pos.x, text_pos.y), 'P', 10)])

curving_point2 = Vector2(200, 50)
text_pos = curving_point2+text_offsett
all_p.append([curving_point2, create_dot_rect_surface(curving_point2), False, Text((text_pos.x, text_pos.y), 'P', 10)])

curving_point3 = Vector2(500, 150)
text_pos = curving_point3+text_offsett
all_p.append([curving_point3, create_dot_rect_surface(curving_point3), False, Text((text_pos.x, text_pos.y), 'P', 10)])

end_point = curve.p1
text_pos = end_point+text_offsett
all_p.append([end_point, create_dot_rect_surface(end_point), False, Text((text_pos.x, text_pos.y), 'P', 10)])

for idx, point in enumerate(all_p[:2].copy()):
    point[3].update(new_txt = (f'P{idx}'))
    quadratic_points.append(point)
last_p = all_p[-1].copy()
last_p[3].update(new_txt = f'P{len(quadratic_points)}')
quadratic_points.append(last_p)

for p in quadratic_points:
    print(p[3].txt)

for idx, point in enumerate(all_p[:3].copy()):
    point[3].update(new_txt = (f'P{idx}'))
    cubic_points.append(point)
last_p = all_p[-1].copy()
last_p[3].update(new_txt = f'P{len(cubic_points)}')
cubic_points.append(last_p)

for idx, point in enumerate(all_p[:4].copy()):
    point[3].update(new_txt = (f'P{idx}'))
    quartic_points.append(point)
last_p = all_p[-1].copy()
last_p[3].update(new_txt = f'P{len(quartic_points)}')
quartic_points.append(last_p)

render = False
moving = False
mouse_pressed = False

menu = True
quadratic = False
quartic = False
cubic = False

quad_btn = Button((100, 250), 'Quadratic', 160, 50)
cub_btn = Button((300, 250), 'Cubic', 160, 50)
quar_btn = Button((500, 250), 'Quartic', 160, 50)

title = Text((WIDTH/2, 75), 'Bezier Curve', 50, bg_color = None)
description_l1 = Text((WIDTH/2, 470), "Choose the curve that you'd like to see", 24, bg_color=None)
description_l2 = Text((WIDTH/2, 500), "once you saw it press ESC to come back here", 24, bg_color=None)

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
            if event.key == pygame.K_RETURN and not moving:
                render = True
            elif event.key == pygame.K_ESCAPE:
                quadratic = False
                cubic = False
                quartic = False
                render = False
                menu = True

                points_rect = list()

                curve.reset()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            moving = False
            for p_r in points_rect:
                p_r[2] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
            if not render:
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
            new_txt_pos = p_r[0] + text_offsett
            p_r[1] = create_dot_rect_surface(p_r[0])
            p_r[3].update(new_center = (new_txt_pos.x, new_txt_pos.y))

        rect(p_r[1])
        p_r[3].render()

    if quadratic:
        if render:
            curve.quadratic(points_rect[0][0], points_rect[1][0], points_rect[2][0])
            curve.render_bezier((points_rect[0][0].x, points_rect[0][0].y))


    elif cubic:
        if render:
            curve.cubic(points_rect[0][0], points_rect[1][0], points_rect[2][0], points_rect[3][0])
            curve.render_bezier((points_rect[0][0].x, points_rect[0][0].y))

    elif quartic:
        if render:
            curve.quartic(points_rect[0][0], points_rect[1][0], points_rect[2][0], points_rect[3][0], points_rect[4][0])
            curve.render_bezier((points_rect[0][0].x, points_rect[0][0].y))

    elif menu:

        title.render()
        description_l1.render()
        description_l2.render()

        quad_btn.render()
        cub_btn.render()
        quar_btn.render()

        if mouse_pressed:

            if quad_btn.pressed():
                menu = False
                quadratic = True
                points_rect = quadratic_points.copy()
                for p in points_rect:
                    print(p[3].txt)

            elif cub_btn.pressed():
                menu = False
                cubic = True
                points_rect = cubic_points.copy()
                for p in points_rect:
                    print(p[3].txt)

            elif quar_btn.pressed():
                menu = False
                quartic = True
                points_rect = quartic_points.copy()
                for p in points_rect:
                    print(p[3].txt)


    pygame.display.flip()
    clock.tick(FPS)
