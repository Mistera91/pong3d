# Game classes definition
class Paddle:
    def __init__(self, position, controls):
        self.controls = controls

        self.paddleHeight = 20
        self.paddleWidth = 100

        if position == "LEFT":
            self.paddleX = width/4 - self.paddleWidth/2
            self.xmin = 0
            self.xmax = width/2 - self.paddleWidth
        elif position == "RIGHT":
            self.paddleX = width/4*3 - self.paddleWidth/2
            self.xmin = width/2
            self.xmax = width-self.paddleWidth

        self.paddleY = height-100-self.paddleHeight

        self.speed = 12

        self.color = "#FFFFFF"

    def render(self):
        if application.keys.state[self.controls['left']]:
            self.paddleX -= self.speed
        elif application.keys.state[self.controls['right']]:
            self.paddleX += self.speed

        self.paddleX = constrain(self.paddleX, self.xmin, self.xmax)

        noStroke()
        fill(self.color)
        rect(self.paddleX, self.paddleY, self.paddleWidth, self.paddleHeight)


class Ball:
    def __init__(self):
        self.radius = 20
        self.a = float(0.5)

        self.color = 255

        self.velocityAfterPaddleCollition = -20
        self.velocityFactorAfterWallCollition = 20

        # Velocity
        self.vx = 8
        self.vy = 0

        # Friction
        self.fx = 0.99
        self.vxMin = 8

        # Position
        self.x = width/2
        self.y = 100

    def isUnderground(self):
        return self.y+self.vy+self.radius+height-application.stage.paddles[0].paddleY >= height

    def isOverPaddles(self):
        onPlatform1 = self.x+self.radius > application.stage.paddles[0].paddleX and self.x - \
            self.radius < application.stage.paddles[0].paddleX+application.stage.paddles[0].paddleWidth
        onPlatform2 = self.x+self.radius > application.stage.paddles[1].paddleX and self.x - \
            self.radius < application.stage.paddles[1].paddleX+application.stage.paddles[1].paddleWidth
        return onPlatform1 or onPlatform2

    def isCollidingWithWalls(self):
        onWall1 = self.x-self.radius <= 0
        onWall2 = self.x+self.radius >= width
        return onWall1 or onWall2

    def render(self):
        # if self.y+self.vy+self.radius+height-application.stage.paddles[1].paddleY >= height:
        if self.isUnderground():
            if self.isOverPaddles():
                self.vy = self.velocityAfterPaddleCollition
            else:
                application.__init__()

        if self.isCollidingWithWalls():
            self.vx = -1 * self.velocityFactorAfterWallCollition * (self.vx / abs(self.vx))

        # self.vx = max(self.vx*self.fx, self.vxMin)
        self.vx *= self.fx
        self.vx = max(abs(self.vx), abs(self.vxMin))*(self.vx / abs(self.vx))

        self.x += self.vx
        print(self.y, self.vy)
        self.y += self.vy
        print(self.y, self.vy)
        self.vy += self.a
        print(self.y, self.vy, self.a)
        noStroke()
        fill(self.color)
        circle(self.x, self.y, self.radius*2)


class Stage:
    def __init__(self):
        self.background = color(16, 16, 16, 0.2)
        self.paddles = [Paddle('LEFT', {'up': 90, 'left': 81, 'bottom': 83, 'right': 68}),
                        Paddle('RIGHT', {'up': 80, 'left': 76, 'bottom': 77, 'right': 0})]

    def render(self):
        background(self.background)
        self.paddles[0].render()
        self.paddles[1].render()


class Keys:
    def __init__(self):
        self.state = [None for i in range(600)]

    def keyPressed(self, e):
        if e.getKeyCode() >= 599:
            print(e.getKeyCode())
        if e.getKeyCode() == 10:
            application.__init__()
        self.state[e.getKeyCode()] = True

    def keyReleased(self, e):
        self.state[e.getKeyCode()] = False


class Main:
    def __init__(self):
        self.stage = Stage()
        self.keys = Keys()
        self.ball = Ball()

    def renderFrame(self):
        self.stage.render()
        self.ball.render()

        stroke(255)
        line(width/4, 0, width/4, height)
        line(width/4*2, 0, width/4*2, height)
        line(width/4*3, 0, width/4*3, height)


# Make application global
application = None


# Game events
def mousePressed():
    pass


def mouseReleased():
    pass


def keyPressed(e):
    application.keys.keyPressed(e)


def keyReleased(e):
    application.keys.keyReleased(e)


def mouseWheel(event):
    pass


# Launch application
def setup():
    global application
    application = Main()


def draw():
    global application
    application.renderFrame()


def settings():
    fullScreen()