from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
CIRCLE_RADIUS = 15
UNIQUE_CIRCLE_RADIUS = 20
SPECIAL_BUBBLE_CHANCE = 0.2  # 20% chance for special bubbles


class GameState:
    def __init__(self):
        self.score = 0
        self.misfires = 0
        self.freeze = False
        self.gameover = 0
        self.bullet = []

game = GameState()
class Bubble:
    def __init__(self, special=False):
        self.x = random.randint(-220, 220)
        self.y = 330
        self.r = random.randint(20, 25)
        self.color = [random.uniform(0.3, 1.0) for _ in range(3)]
        self.special = special
        self.r_delta = 0.5  # Used for radius animation in special bubbles

    def update_radius(self):
        """Expand and shrink the radius if it's a special bubble."""
        if self.special:
            self.r += self.r_delta
            if self.r > 30 or self.r < 15: 
                self.r_delta *= -1    



class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]



# Drawing Algorithms
class DrawingUtils:
    @staticmethod
    def plot_point(x, y):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    @staticmethod
    def convert_to_zone0(x, y, zone):
        conversions = {
            0: (x, y),
            1: (y, x),
            2: (y, -x),
            3: (-x, y),
            4: (-x, -y),
            5: (-y, -x),
            6: (-y, x),
            7: (x, -y)
        }
        return conversions.get(zone, (x, y))

    @staticmethod
    def convert_from_zone0(x, y, zone):
        return DrawingUtils.convert_to_zone0(x, y, zone)

    @staticmethod
    def midpoint_line(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        # Determine zone
        if abs(dx) > abs(dy):
            zone = 0 if dx >= 0 and dy >= 0 else 3 if dx < 0 and dy >= 0 else 4 if dx < 0 and dy < 0 else 7
        else:
            zone = 1 if dx >= 0 and dy >= 0 else 2 if dx < 0 and dy >= 0 else 5 if dx < 0 and dy < 0 else 6

        x1, y1 = DrawingUtils.convert_to_zone0(x1, y1, zone)
        x2, y2 = DrawingUtils.convert_to_zone0(x2, y2, zone)

        dx = x2 - x1
        dy = y2 - y1

        d = 2 * dy - dx
        incrE = 2 * dy
        incrNE = 2 * (dy - dx)

        x, y = x1, y1
        x0, y0 = DrawingUtils.convert_from_zone0(x, y, zone)
        DrawingUtils.plot_point(x0, y0)

        while x < x2:
            if d <= 0:
                d += incrE
                x += 1
            else:
                d += incrNE
                x += 1
                y += 1
            x0, y0 = DrawingUtils.convert_from_zone0(x, y, zone)
            DrawingUtils.plot_point(x0, y0)


# Mid-Point Circle Drawing Algorithm


    @staticmethod
    def midpoint_circle(radius, centerX=0, centerY=0):
        glBegin(GL_POINTS)
        x = 0
        y = radius
        d = 1 - radius
        while y > x:
            glVertex2f(x + centerX, y + centerY)
            glVertex2f(x + centerX, -y + centerY)
            glVertex2f(-x + centerX, y + centerY)
            glVertex2f(-x + centerX, -y + centerY)
            glVertex2f(y + centerX, x + centerY)
            glVertex2f(y + centerX, -x + centerY)
            glVertex2f(-y + centerX, x + centerY)
            glVertex2f(-y + centerX, -x + centerY)
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * x - 2 * y + 5
                y -= 1
            x += 1
        glEnd()



bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()


def draw_bullet():
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in game.bullet:
        DrawingUtils.midpoint_circle(8, i[0], i[1])


def draw_bubble():
    glPointSize(2)

    for i in range(len(bubble)):
        if bubble[i].special:  # Draw special bubble
            bubble[i].update_radius()
            glColor3f(1, 0, 0)  # Red for special bubbles
        else:  # Normal bubbles
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])

        if i == 0 or (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            DrawingUtils.midpoint_circle(bubble[i].r, bubble[i].x, bubble[i].y)

def draw_spaceship(centerX=0, centerY=-365):
    
    
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0)  
    glVertex2f(centerX - 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY - 20) 
    glVertex2f(centerX - 10, centerY - 20)  
    glEnd()
    
    # Rocket nose (triangle)
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 1) 
    glVertex2f(centerX, centerY + 100)  
    glVertex2f(centerX - 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY + 80)  
    glEnd()
    
    # Left fin
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0.5) 
    glVertex2f(centerX - 10, centerY - 20) 
    glVertex2f(centerX - 30, centerY - 40) 
    glVertex2f(centerX - 10, centerY - 40)  
    glEnd()
    
    # Right fin
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0.5) 
    glVertex2f(centerX + 10, centerY - 20) 
    glVertex2f(centerX + 30, centerY - 40) 
    glVertex2f(centerX + 10, centerY - 40)  
    glEnd()
    
    # Rocket thrusters
    for i in range(3):
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 0.5, 0)  
        x_offset = (i - 1) * 10  
        glVertex2f(centerX - 5 + x_offset, centerY - 40)  
        glVertex2f(centerX + 5 + x_offset, centerY - 40)  
        glVertex2f(centerX + 5 + x_offset, centerY - 60)  
        glVertex2f(centerX - 5 + x_offset, centerY - 60) 
        glEnd()



def draw_ui():
    # shooter
    draw_spaceship(centerX=catcher.x, centerY=-365)

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    DrawingUtils.midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    DrawingUtils.midpoint_line(-210, 350, -190, 370)
    DrawingUtils.midpoint_line(-210, 350, -190, 330)

    # Right Cross Button
    glPointSize(4)
    glColor3f(0.9, 0, 0)
    DrawingUtils.midpoint_line(210, 365, 180, 335)
    DrawingUtils.midpoint_line(210, 335, 180, 365)

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if game.freeze:
        DrawingUtils.midpoint_line(-15, 370, -15, 330)
        DrawingUtils.midpoint_line(-15, 370, 15, 350)
        DrawingUtils.midpoint_line(-15, 330, 15, 350)
    else:
        DrawingUtils.midpoint_line(-10, 370, -10, 330)
        DrawingUtils.midpoint_line(10, 370, 10, 330)


def convert_coordinate(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


def keyboard_listener(key, x, y):
    if key == b' ':
        if not game.freeze and game.gameover < 3:
            game.bullet.append([catcher.x, -365])
    elif key == b'a':
        if catcher.x > -230 and not game.freeze:
            catcher.x -= 10
    elif key == b'd':
        if catcher.x < 230 and not game.freeze:
            catcher.x += 10
    glutPostRedisplay()





def mouse_listener(button, state, x, y):
    global bubble
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            game.freeze = False
            print('Starting Over')
            bubble = [Bubble() for _ in range(5)]
            bubble.sort(key=lambda b: b.x)
            game.score = 0
            game.gameover = 0
            game.misfires = 0
            game.bullet = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', game.score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            game.freeze = not game.freeze

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullet()
    draw_bubble()
    glutSwapBuffers()

import time
def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global bubble
    if not game.freeze and game.gameover < 3 and game.misfires < 3:
        delidx = []
        for i in range(len(game.bullet)):
            if game.bullet[i][1] < 400:
                game.bullet[i][1] += 10
            else:
                delidx.append(i)
                game.misfires += 1
        try:
            for j in sorted(delidx, reverse=True):
                del game.bullet[j]
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + game.score * 5) * delta_time
                else:
                    game.gameover += 1
                    del bubble[i]
                    bubble.append(Bubble(special=random.random() < SPECIAL_BUBBLE_CHANCE))
                    bubble.sort(key=lambda b: b.y)
                    break
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + game.score * 5) * delta_time
                else:
                    game.gameover += 1
                    del bubble[i]
                    bubble.append(Bubble(special=random.random() < SPECIAL_BUBBLE_CHANCE))
                    bubble.sort(key=lambda b: b.y)
                    break
        try:
           
            to_remove_bubble = []
            to_remove_bullet = []
            
            for i in range(len(bubble)):
               
                if abs(bubble[i].y - -345) < bubble[i].r and abs(bubble[i].x - catcher.x) < (bubble[i].r + 20):
                    game.gameover += 3  # game over
                    break
                    
                # Collision with bullets
                for j in range(len(game.bullet)):
                    if abs(bubble[i].y - game.bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - game.bullet[j][0]) < (bubble[i].r + 20):
                        game.score += 5 if bubble[i].special else 1
                        print("Score:", game.score)
                        to_remove_bubble.append(i)
                        to_remove_bullet.append(j)
                        break

            # Remove collided objects
            for i in sorted(to_remove_bubble, reverse=True):
                del bubble[i]
                bubble.append(Bubble(special=random.random() < SPECIAL_BUBBLE_CHANCE))
            for j in sorted(to_remove_bullet, reverse=True):
                del game.bullet[j]

        except Exception as e:
            print(f"Error in collision detection: {e}")

    # Game over condition
    if (game.gameover >= 3 or game.misfires >= 3) and not game.freeze:
        print("Game Over! Score:", game.score)
        game.freeze = True
        bubble = []  # Clear bubbles

    time.sleep(1 / 1000)
    glutPostRedisplay()



def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)

def main():
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

    glutCreateWindow(b"Shoot The Circles!")
    init()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()