def setup():
    global keys, paddle, ball, game
    fullScreen()
    size(1000, 500, P3D)

    class game:
        rainbow = 0
        scoreLeft = 0
        scoreRight = 0
        abilityLeft = -1
        abilityRight = -1
        rightTextColorBonus = 0
        leftTextColorBonus = 0
        menuCompleted = False
        drawMenuNextCall = True
        stopDrawMenu = True
        mouseClicked = False
        abilities = [
["Biggle"      , "a1.png" , "Increases the size of the paddle"                                                                  ],
["Zoom ball"   , "a2.png" , "Increases the speed of the ball after it touches your paddle. Does not triggers every time"        ],
["Sprint pad"  , "a3.png" , "Increases the speed of the paddle"                                                                 ],
["Big freeze"  , "a4.png" , "Briefly frezzes the ball when you use it.\nIt can only be used 3 times per game"                    ],
["Confusion"   , "a5.png" , "Inverts the controls of the opposite player for a short time.\nIt can only be used 3 times per game"],
["Small freeze", "a6.png" , "Slows the ball for a short time.\nIt can only be used 3 times per game"                             ],
["Darkness"    , "a7.png" , "Reduces the light onto the enemy side for a short time.\nIt can only be used 3 times per game"      ],
["Rainbow pad" , "a8.png" , "Changes the color of your paddle. Does nothing else"                                               ]
]
        buttonsCoords = [None for i in range(len(abilities))]
    class keys:
        Z = False
        Q = False
        S = False
        D = False
        F = False
        UP_ARROW = False
        RIGHT_ARROW = False
        DOWN_ARROW = False
        LEFT_ARROW = False
        INFERIOR = False

    class paddle:
        sideLen = height // 4
        leftX = -width // 4
        leftY = height - height // 4
        leftZ = 0
        rightX = width // 4
        rightY = height - height // 4
        rightZ = 0
        speedX = width / 125
        speedZ = height / 75
        leftMovX = False
        leftMovZ = False
        leftMovXneg = False
        leftMovZneg = False
        rightMovX = False
        rightMovZ = False
        rightMovXneg = False
        rightMovZneg = False

    class ball:
        # Constants
        a = float(0.25)
        velocityAfterPaddleCollition = -15
        velocityFactorAfterWallCollition = 5
        fx = 0.99
        vxMin = 8
        fz = 0.99
        vzMin = 4
        colors = [33, 90, 102]
        colorBonus = 0
        size = height // 20
        # Vars
        vx = 4
        vy = 0
        vz = 4
        x = 0
        y = 0
        z = 0

def isUnderground():
    global ball
    return ball.y > height

def isUnderPaddle():
    global ball
    return ball.y >= height/2 - paddle.sideLen / 16 - ball.size/2

def isOverPaddles():
    global ball, paddle
    onPlatformLeft = ball.x+ball.size > paddle.leftX - paddle.sideLen/2 and ball.x - \
        ball.size < paddle.leftX + paddle.sideLen/2 and \
        ball.z+ball.size > paddle.leftZ - paddle.sideLen/2 and ball.z - \
        ball.size < paddle.leftZ + paddle.sideLen/2
    onPlatformRight = ball.x+ball.size > paddle.rightX - paddle.sideLen/2 and ball.x - \
        ball.size < paddle.rightX + paddle.sideLen/2 and \
        ball.z+ball.size > paddle.rightZ - paddle.sideLen/2 and ball.z - \
        ball.size < paddle.rightZ + paddle.sideLen/2
    return onPlatformLeft or onPlatformRight

def isStrictlyOverPaddles():
    global ball, paddle
    onPlatformLeft = ball.x-ball.size > paddle.leftX - paddle.sideLen/2 and ball.x + \
        ball.size < paddle.leftX + paddle.sideLen/2 and \
        ball.z-ball.size > paddle.leftZ - paddle.sideLen/2 and ball.z + \
        ball.size < paddle.leftZ + paddle.sideLen/2
    onPlatformRight = ball.x-ball.size > paddle.rightX - paddle.sideLen/2 and ball.x + \
        ball.size < paddle.rightX + paddle.sideLen/2 and \
        ball.z-ball.size > paddle.rightZ - paddle.sideLen/2 and ball.z + \
        ball.size < paddle.rightZ + paddle.sideLen/2
    return onPlatformLeft or onPlatformRight

def isCollidingWithWallX():
    global ball
    onWallNegX = ball.x-ball.size <= -width/2  # X
    onWallPosX = ball.x+ball.size >= width/2
    return onWallNegX or onWallPosX

def isCollidingWithWallZ():
    global ball
    onWallNegZ = ball.z-ball.size <= -width/4  # Z
    onWallPosZ = ball.z+ball.size >= width/4
    return onWallNegZ or onWallPosZ

def render():
    global ball, paddle, game
    if isUnderPaddle():
        if isOverPaddles():
            ball.vy = ball.velocityAfterPaddleCollition
            ball.colorBonus = 200
        else:
            if ball.x > 0:
                game.scoreLeft += 1
                game.leftTextColorBonus = 200
            elif ball.x < 0:
                game.scoreRight += 1
                game.rightTextColorBonus = 200
            print(game.scoreLeft, game.scoreRight)
            ball.vx = int(random(1, 8))
            if float(random(1)) > float(0.5):
                ball.vx *= -1
            ball.vy = -10
            ball.vz = int(random(1, 8))
            if float(random(1)) > float(0.5):
                ball.vz *= -1
            ball.x = 0
            ball.y = 0
            ball.z = 0
    if isCollidingWithWallX():
        ball.vx = -1 * ball.velocityFactorAfterWallCollition * (ball.vx / abs(ball.vx))
        ball.colorBonus = 200
    if isCollidingWithWallZ():
        ball.vz = -1 * ball.velocityFactorAfterWallCollition * (ball.vz / abs(ball.vz))
        ball.colorBonus = 200
    ball.vx *= ball.fx
    ball.vx = max(abs(ball.vx), abs(ball.vxMin))*(ball.vx / abs(ball.vx))
    ball.vz *= ball.fz
    ball.vz = max(abs(ball.vz), abs(ball.vzMin))*(ball.vz / abs(ball.vz))
    ball.x += ball.vx
    ball.z += ball.vz
    ball.y += ball.vy
    ball.vy += ball.a
    noStroke()
    fill(ball.colors[0] + ball.colorBonus, ball.colors[1] +
         ball.colorBonus, ball.colors[2] + ball.colorBonus)
    pushMatrix()
    translate(ball.x, ball.y, ball.z)
    sphere(ball.size)
    popMatrix()
    pushMatrix()
    translate(-width/2 + width/8, -height/2 + height/8, width/4)
    textMode(SHAPE)
    textAlign(CENTER, CENTER)
    textSize(96)
    fill(70 + game.leftTextColorBonus * 1.85, 70 + game.leftTextColorBonus * 1.85, 155 + game.leftTextColorBonus)
    text(game.scoreLeft, 0, 0)
    popMatrix()
    pushMatrix()
    translate(width/2 - width/8, -height/2 + height/8, width/4)
    textMode(SHAPE)
    textAlign(CENTER, CENTER)
    textSize(96)

    fill(155 + game.rightTextColorBonus, 70 + game.rightTextColorBonus * 1.85, 70 + game.rightTextColorBonus * 1.85)
    text(game.scoreRight, 0, 0)
    popMatrix()
    # Shadow
    pushMatrix()
    translate(ball.x, height/2 + ball.size/2, ball.z)
    fill(63, 63, 63)
    sphere(ball.size)
    popMatrix()

def keyPressed():
    global keys
    if keyCode == 60:
        keys.INFERIOR = True
    if keyCode == 70:
        keys.F = True
    if keyCode == 90:
        keys.Z = True
    if keyCode == 81:
        keys.Q = True
    if keyCode == 83:
        keys.S = True
    if keyCode == 68:
        keys.D = True
    if keyCode == 38:
        keys.UP_ARROW = True
    if keyCode == 37:
        keys.LEFT_ARROW = True
    if keyCode == 40:
        keys.DOWN_ARROW = True
    if keyCode == 39:
        keys.RIGHT_ARROW = True

def keyReleased():
    global keys
    if keyCode == 60:
        keys.INFERIOR = False
    if keyCode == 70:
        keys.F = False
    if keyCode == 90:
        keys.Z = False
    if keyCode == 81:
        keys.Q = False
    if keyCode == 83:
        keys.S = False
    if keyCode == 68:
        keys.D = False
    if keyCode == 38:
        keys.UP_ARROW = False
    if keyCode == 37:
        keys.LEFT_ARROW = False
    if keyCode == 40:
        keys.DOWN_ARROW = False
    if keyCode == 39:
        keys.RIGHT_ARROW = False

def mouseClicked():
    global game
    game.mouseClicked = True

def drawMenu():
    global game
    noStroke()
    buttonWidth = width / (len(game.abilities) + 3)
    spaceWidth  = (width - buttonWidth * (len(game.abilities) + 2)) / (len(game.abilities) - 1)
    hoveredAbilityNumber = 0
    hoveredAbility       = False
    game.menuCompleted = game.abilityLeft >= 0 and game.abilityRight >= 0
    if game.abilityLeft >= 0 and game.stopDrawMenu:
        game.drawMenuNextCall = True
        game.stopDrawMenu = False
    if game.drawMenuNextCall:
        game.drawMenuNextCall = False
        background(0)
        image(loadImage("stars.png"), 0, 0, width, height)
        fill(0, 0, 0, 127)
        rect(0,0, width, height)
        textAlign(CENTER, CENTER)
        textSize(width/15)
        if not game.abilityLeft >= 0:
            fill(127, 127, 255)
            text("Blue, choose your ability", 0, 0, width, height/4)
        else:
            fill(255, 127, 127)
            text("Red, choose your ability", 0, 0, width, height/4)
        fill(255)
        for ability in range(len(game.abilities)):
            if ability == 0:
                image(loadImage(game.abilities[ability][1]), (ability + 1) * buttonWidth, height/3, buttonWidth, buttonWidth)
                game.buttonsCoords[ability] = [(ability + 1) * buttonWidth, (ability + 1) * buttonWidth + buttonWidth]
            else:
                image(loadImage(game.abilities[ability][1]), (ability + 1) * buttonWidth + ability * spaceWidth, height/3, buttonWidth, buttonWidth)
                game.buttonsCoords[ability] = [(ability + 1) * buttonWidth + ability * spaceWidth, (ability + 1) * buttonWidth + ability * spaceWidth + buttonWidth]        
        fill(0)
        rect(0, height/2, width, height/2)
    for coords in range(len(game.buttonsCoords)):
        if mouseY > height/3 and mouseY < height/3 + buttonWidth :
            if mouseX > game.buttonsCoords[coords][0] and mouseX < game.buttonsCoords[coords][1]:
                handCursor = True
                hoveredAbility = True
                hoveredAbilityNumber = coords

    if hoveredAbility:
        cursor(HAND)
        fill(0)
        rect(0, height/2, width, height/2)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(width/25)
        text(game.abilities[hoveredAbilityNumber][0], 0, height/2, width, height/3)
        textSize(width/40)
        text(game.abilities[hoveredAbilityNumber][2], 0, height - height/4, width, height/4)
    else: 
        cursor(ARROW)
    if game.mouseClicked:
        game.mouseClicked = False
        if not game.abilityLeft >= 0:
            game.abilityLeft = hoveredAbilityNumber
        else: 
            game.abilityRight = hoveredAbilityNumber

def drawFrame():
    noCursor()
    game.rainbow += 1
    if game.rainbow == 256: game.rainbow = 0
    fill(255)
    ball.colorBonus = constrain(ball.colorBonus - 5, 0, 150)
    game.leftTextColorBonus = constrain(game.leftTextColorBonus - 3, 0, 100)
    game.rightTextColorBonus = constrain(game.rightTextColorBonus - 3, 0, 100)
    camera(width/2.0, height/2, (height/2.0) / tan(PI*30.0 / 180.0) -
           00, width/2.0, height/2.0, 0, 0, 1, 0)
    spotLight(255, 255, 255, width/2, 1, width/4, 0, 1, 0, TAU, 0)
    translate(width/2, height/2, -width/4)
    text(game.scoreLeft, width/8, height/8, 110)
    text(game.scoreRight, width - width/8, height - height/8, 100)
    pushMatrix()
    background(0)
    fill(127)
    paddle.leftMovZneg = False
    paddle.leftMovZ = False
    paddle.leftMovXneg = False
    paddle.leftMovX = False
    if keys.Z and not keys.S:
        paddle.leftMovZneg = True
    if keys.S and not keys.Z:
        paddle.leftMovZ = True
    if keys.Q and not keys.D:
        paddle.leftMovXneg = True
    if keys.D and not keys.Q:
        paddle.leftMovX = True
    if paddle.leftMovZneg and paddle.leftMovXneg:
        paddle.leftX -= paddle.speedX * 0.707106781
        paddle.leftZ -= paddle.speedZ * 0.707106781
    if paddle.leftMovZ and paddle.leftMovXneg:
        paddle.leftX -= paddle.speedX * 0.707106781
        paddle.leftZ += paddle.speedZ * 0.707106781
    if paddle.leftMovZneg and paddle.leftMovX:
        paddle.leftX += paddle.speedX * 0.707106781
        paddle.leftZ -= paddle.speedZ * 0.707106781
    if paddle.leftMovZ and paddle.leftMovX:
        paddle.leftX += paddle.speedX * 0.707106781
        paddle.leftZ += paddle.speedZ * 0.707106781
    if paddle.leftMovZneg and not paddle.leftMovXneg and not paddle.leftMovX:
        paddle.leftZ -= paddle.speedZ
    if paddle.leftMovZ and not paddle.leftMovXneg and not paddle.leftMovX:
        paddle.leftZ += paddle.speedZ
    if paddle.leftMovXneg and not paddle.leftMovZneg and not paddle.leftMovZ:
        paddle.leftX -= paddle.speedX
    if paddle.leftMovX and not paddle.leftMovZneg and not paddle.leftMovZ:
        paddle.leftX += paddle.speedX
    paddle.leftX = constrain(paddle.leftX, -width/2 + paddle.sideLen/2, 0 - paddle.sideLen/2)
    paddle.leftZ = constrain(paddle.leftZ, -width/4 + paddle.sideLen/2, width/4 - paddle.sideLen/2)

    # Drawing the left box
    rectMode(CENTER)
    noStroke()
    fill(0, 0, 255)
    stroke(255)
    noFill()
    box(width, height, width/2)
    pushMatrix()
    translate(0, height/4 + height/4, 0)
    box(0, 0, width/2)
    popMatrix()
    pushMatrix()
    translate(0, height/2, 0)
    fill("#1C1C2C")
    box(width, 0, width/2)
    popMatrix()
    if game.abilityLeft == 7: colorMode(HSB); fill(game.rainbow, 255, 127); stroke(game.rainbow, 255, 255)
    else: fill(0, 0, 127); stroke(0, 0, 255)
    translate(paddle.leftX, height/2 - paddle.sideLen / 32, paddle.leftZ)
    box(paddle.sideLen, paddle.sideLen / 16, paddle.sideLen)
    colorMode(RGB)
    # Right paddle
    paddle.rightMovZneg = False
    paddle.rightMovZ = False
    paddle.rightMovXneg = False
    paddle.rightMovX = False
    if keys.UP_ARROW and not keys.DOWN_ARROW:
        paddle.rightMovZneg = True
    if keys.DOWN_ARROW and not keys.UP_ARROW:
        paddle.rightMovZ = True
    if keys.LEFT_ARROW and not keys.RIGHT_ARROW:
        paddle.rightMovXneg = True
    if keys.RIGHT_ARROW and not keys.LEFT_ARROW:
        paddle.rightMovX = True
    if paddle.rightMovZneg and paddle.rightMovXneg:
        paddle.rightX -= paddle.speedX * 0.707106781
        paddle.rightZ -= paddle.speedZ * 0.707106781
    if paddle.rightMovZ and paddle.rightMovXneg:
        paddle.rightX -= paddle.speedX * 0.707106781
        paddle.rightZ += paddle.speedZ * 0.707106781
    if paddle.rightMovZneg and paddle.rightMovX:
        paddle.rightX += paddle.speedX * 0.707106781
        paddle.rightZ -= paddle.speedZ * 0.707106781
    if paddle.rightMovZ and paddle.rightMovX:
        paddle.rightX += paddle.speedX * 0.707106781
        paddle.rightZ += paddle.speedZ * 0.707106781
    if paddle.rightMovZneg and not paddle.rightMovXneg and not paddle.rightMovX:
        paddle.rightZ -= paddle.speedZ
    if paddle.rightMovZ and not paddle.rightMovXneg and not paddle.rightMovX:
        paddle.rightZ += paddle.speedZ
    if paddle.rightMovXneg and not paddle.rightMovZneg and not paddle.rightMovZ:
        paddle.rightX -= paddle.speedX
    if paddle.rightMovX and not paddle.rightMovZneg and not paddle.rightMovZ:
        paddle.rightX += paddle.speedX
    paddle.rightX = constrain(paddle.rightX, 0 + paddle.sideLen/2, width/2 - paddle.sideLen/2)
    paddle.rightZ = constrain(paddle.rightZ, -width/4 + paddle.sideLen/2, width/4 - paddle.sideLen/2)
    if game.abilityRight == 7: colorMode(HSB); fill(game.rainbow, 255, 127); stroke(game.rainbow, 255, 255)
    else: fill(127, 0, 0); stroke(255, 0, 0)
    rectMode(CENTER)
    popMatrix()
    pushMatrix()
    translate(paddle.rightX, height/2 - paddle.sideLen / 32, paddle.rightZ)
    box(paddle.sideLen, paddle.sideLen / 16, paddle.sideLen)
    colorMode(RGB)
    popMatrix()
    render()

def draw():
    global keys, paddle, ball, game
    if game.menuCompleted:
        drawFrame()
    else: drawMenu()
