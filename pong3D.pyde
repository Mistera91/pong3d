def setup():
    global keys, paddle, ball, game, spoofBall
    fullScreen(P3D)
    class game:
        # Config vars
        showFrameRate         = True  # Shows the frameRate on top of the screen
        showShadow            = True  # Shows a shadow under the ball
        showPredictedLocation = True  # Shows the output of botPredict() with a second ball
        scaryBots             = False # The bots will only move the less they can. Not recommended with controlledBall enabled
        botRight              = True  # Enables the right player as a bot
        botLeft               = False # Enables the left player as a bot
        controlledBall        = True  # Enables ball control
        ballControlNerf       = 2     # 1 is for total control, 2 is for half control, etc...
        setPoints             = 5     # How much points are needed for a set
        scoreLeft             = 0     # Starting score for the left player
        scoreRight            = 0     # Starting score for the right player
        setsLeft              = 0     # Starting sets for the left player
        setsRight             = 0     # Starting sets for the right player
        abilityLeft           = -1    # The ability for the left player. Set to -1 to let them choose instead
        abilityRight          = -1    # The ability for the right player. Set to -1 to let them choose instead
        difficulty            = 0     # Starting difficulty. Only occurs for the first point
        abilities = [                 # The list of abilities. Add a "#" symbol at the beginning of a line to disable the ability
["Biggle"      , "a1.png" , "Increases the size of the paddle"                                                                   ],
["Zoom ball"   , "a2.png" , "Increases the speed of the ball after it touches your paddle. Does not triggers every time"         ],
["Sprint pad"  , "a3.png" , "Increases the speed of the paddle"                                                                  ],
["Big freeze"  , "a4.png" , "Briefly frezzes the ball when you use it.\nIt can only be used 3 times per game"                    ],
["Confusion"   , "a5.png" , "Inverts the controls of the opposite player for a short time.\nIt can only be used 3 times per game"],
["Small freeze", "a6.png" , "Slows the ball for a short time.\nIt can only be used 3 times per game"                             ],
["Darkness"    , "a7.png" , "Reduces the light onto the enemy side for a short time.\nIt can only be used 3 times per game"      ],
["Rainbow pad" , "a8.png" , "Changes the color of your paddle. Does nothing else"                                                ]
]
        # Vars
        rainbow               = 0
        abilityCountLeft      = 3
        abilityCountRight     = 3
        rightTextColorBonus   = 0
        leftTextColorBonus    = 0
        menuCompleted         = False
        drawMenuNextCall      = True
        mouseClicked          = False
        onPlatformRight       = False
        onPlatformLeft        = False
        framesConfusionLeft   = 100
        framesConfusionRight  = 100
        framesDarknessLeft    = 300
        framesDarknessRight   = 300
        framesToRestart       = 0
        framesToDifficulty    = 1
        framesForDifficulty   = 600
        announcedText         = ""
        announcedTextFrames   = 0
        buttonsCoords = [None for i in range(len(abilities))]
        if botRight and abilityRight == -1 :
            abilityRight = int(random(0, len(abilities)))
        if botLeft and abilityLeft == -1 :
            abilityLeft = int(random(0, len(abilities)))

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
        I = False
        J = False
        K = False
        L = False
        H = False

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
        vx = int(random(1, 8))
        vxBonus = 0
        vy = -10
        vz = int(random(1, 8))
        vzBonus = 0
        x = 0
        y = 0
        z = 0
        tempvx = 0
        tempvy = 0
        tempvz = 0
        framesSinceFreeze = 52
        framesSinceSlow = 300

    class spoofBall:
        a                                = ball.a
        velocityAfterPaddleCollition     = ball.velocityAfterPaddleCollition
        velocityFactorAfterWallCollition = ball.velocityFactorAfterWallCollition
        fx                               = ball.fx
        vxMin                            = ball.vxMin
        fz                               = ball.fz
        vzMin                            = ball.vzMin
        size                             = ball.size
        # Vars
        vx                               = 0
        vy                               = 0
        vz                               = 0
        x                                = 0
        y                                = 0
        z                                = 0
        predBallX                        = 0
        predBallZ                        = 0
        freeze                           = False
        difficulty                       = 0
        framesToDifficulty               = 0

def botPredict():
    spoofBall.framesToDifficulty = game.framesToDifficulty
    spoofBall.difficulty         = game.difficulty
    spoofBall.predBallX          = ball.x
    spoofBall.predBallZ          = ball.z
    spoofBall.vx                 = ball.vx
    spoofBall.vy                 = ball.vy
    spoofBall.vz                 = ball.vz
    spoofBall.x                  = ball.x
    spoofBall.y                  = ball.y
    spoofBall.z                  = ball.z
    spoofBall.velocityFactorAfterWallCollition = ball.velocityFactorAfterWallCollition
    while spoofBall.y < height/2 - ball.size/2 - spoofBall.vy:
        spoofBall.framesToDifficulty += 1
        if spoofBall.framesToDifficulty % game.framesForDifficulty == 0:
            spoofBall.difficulty += 1
        spoofBall.predBallX += spoofBall.vx
        spoofBall.predBallZ += spoofBall.vz
        if spoofBall.x-spoofBall.size <= -width/2 or spoofBall.x+spoofBall.size >= width/2:
            spoofBall.vx = -1 * spoofBall.vx + (spoofBall.velocityFactorAfterWallCollition * (1 + spoofBall.difficulty * 0.25))/(spoofBall.vx)/2
            spoofBall.x = constrain(spoofBall.x, -width/2 + spoofBall.size, width/2 - spoofBall.size)
        if spoofBall.z-spoofBall.size <= -width/4 or spoofBall.z+spoofBall.size >= width/4:
            spoofBall.vz = -1 * spoofBall.vz + (spoofBall.velocityFactorAfterWallCollition * (1 + spoofBall.difficulty * 0.25))/(spoofBall.vz)/2
            spoofBall.z = constrain(spoofBall.z, -width/4 + spoofBall.size, width/4 - spoofBall.size)
        try:
            spoofBall.vx *= spoofBall.fx
            spoofBall.vx = max(abs(spoofBall.vx), abs(spoofBall.vxMin * (1 + spoofBall.difficulty * 0.25)))*(spoofBall.vx / abs(spoofBall.vx))
            spoofBall.vz *= spoofBall.fz
            spoofBall.vz = max(abs(spoofBall.vz), abs(spoofBall.vzMin * (1 + spoofBall.difficulty * 0.25)))*(spoofBall.vz / abs(spoofBall.vz))
        except ZeroDivisionError: pass
        if not spoofBall.freeze:
            spoofBall.x += spoofBall.vx + ball.vxBonus
            spoofBall.z += spoofBall.vz + ball.vzBonus
            spoofBall.y += spoofBall.vy
        else: 
            spoofBall.x += spoofBall.vx/2 + ball.vxBonus
            spoofBall.z += spoofBall.vz/2 + ball.vzBonus
            spoofBall.y += spoofBall.vy/2
        spoofBall.x = constrain(spoofBall.x, -width/2 + ball.size, width/2 - ball.size)
        spoofBall.z = constrain(spoofBall.z, -width/4 + ball.size, width/4 - ball.size)
        spoofBall.vy += spoofBall.a
    spoofBall.x = constrain(spoofBall.x, -width/2 + ball.size, width/2 - ball.size)
    spoofBall.z = constrain(spoofBall.z, -width/4 + ball.size, width/4 - ball.size)
    spoofBall.predBallX = spoofBall.x
    spoofBall.predBallZ = spoofBall.z

def playBall():
    movX, movXneg, movZ, movZneg = False, False, False, False
    ball.vxBonus = 0
    ball.vzBonus = 0
    if keys.I and not keys.K:
        movZneg = True
    if keys.K and not keys.I:
        movZ    = True
    if keys.J and not keys.L:
        movXneg = True
    if keys.L and not keys.J:
        movX    = True
    if movZneg and movXneg:
        ball.vxBonus = abs(ball.vx) / 2 * -0.707106781
        ball.vzBonus = abs(ball.vz) / 2 * -0.707106781
    if movZ and movXneg:
        ball.vxBonus = abs(ball.vx) / 2 * -0.707106781
        ball.vzBonus = abs(ball.vz) / 2 *  0.707106781
    if movZneg and movX:
        ball.vxBonus = abs(ball.vx) / 2 *  0.707106781
        ball.vzBonus = abs(ball.vz) / 2 * -0.707106781
    if movZ and movX:
        ball.vxBonus = abs(ball.vx) / 2 *  0.707106781
        ball.vzBonus = abs(ball.vz) / 2 *  0.707106781
    if movZneg and not movXneg and not movX:
        ball.vzBonus = abs(ball.vz) / 2 * -1
    if movZ and not movXneg and not movX:
        ball.vzBonus = abs(ball.vz) / 2
    if movXneg and not movZneg and not movZ:
        ball.vxBonus = abs(ball.vx) / 2 * -1
    if movX and not movZneg and not movZ:
        ball.vxBonus = abs(ball.vx) / 2

def botMove():
    if game.botRight and (spoofBall.x > 0 or not game.controlledBall):    
        keys.LEFT_ARROW = False
        keys.RIGHT_ARROW = False
        keys.UP_ARROW = False
        keys.DOWN_ARROW = False
        if game.scaryBots :
            if spoofBall.predBallX > paddle.rightX + paddle.sideLen / 2 + ball.size:
                keys.RIGHT_ARROW = True
            elif spoofBall.predBallX < paddle.rightX - paddle.sideLen / 2 - ball.size:
                keys.LEFT_ARROW = True
            if spoofBall.predBallZ > paddle.rightZ + paddle.sideLen / 2 + ball.size:
                keys.DOWN_ARROW = True
            elif spoofBall.predBallZ < paddle.rightZ - paddle.sideLen / 2 - ball.size:
                keys.UP_ARROW = True
        else:
            if spoofBall.predBallX > paddle.rightX + paddle.sideLen / 16:
                keys.RIGHT_ARROW = True
            elif spoofBall.predBallX < paddle.rightX - paddle.sideLen / 16:
                keys.LEFT_ARROW = True
            if spoofBall.predBallZ > paddle.rightZ + paddle.sideLen / 16:
                keys.DOWN_ARROW = True
            elif spoofBall.predBallZ < paddle.rightZ - paddle.sideLen / 16:
                keys.UP_ARROW = True
    if game.botLeft and (spoofBall.x < 0 or not game.controlledBall):
        keys.Q = False
        keys.D = False
        keys.Z = False
        keys.S = False
        if game.scaryBots:
            if spoofBall.predBallX > paddle.leftX + paddle.sideLen / 2 + ball.size:
                keys.D = True
            elif spoofBall.predBallX < paddle.leftX - paddle.sideLen / 2 - ball.size:
                keys.Q = True
            if spoofBall.predBallZ > paddle.leftZ + paddle.sideLen / 2 + ball.size:
                keys.S = True
            elif spoofBall.predBallZ < paddle.leftZ - paddle.sideLen / 2 - ball.size:
                keys.Z = True
        else:
            if spoofBall.predBallX > paddle.leftX + paddle.sideLen / 16:
                keys.D = True
            elif spoofBall.predBallX < paddle.leftX - paddle.sideLen / 16:
                keys.Q = True
            if spoofBall.predBallZ > paddle.leftZ + paddle.sideLen / 16:
                keys.S = True
            elif spoofBall.predBallZ < paddle.leftZ - paddle.sideLen / 16:
                keys.Z = True

def drawBall():
    ball.framesSinceFreeze += 1
    ball.framesSinceSlow += 1
    if ball.framesSinceSlow == 300:
            ball.velocityFactorAfterWallCollition *= 2
            ball.vx *= 2
            ball.vz *= 2
            ball.vy *= 2
    if ball.framesSinceSlow == 0:
            ball.velocityFactorAfterWallCollition /= 2
            ball.vx /= 2
            ball.vz /= 2
            ball.vy /= 2
    if isUnderPaddle():
        if isOverPaddles():
            if game.onPlatformLeft and game.abilityLeft == 1 and float(random(1)) < float(0.2): 
                ball.vx *= 5
                ball.vz *= 2.5
                game.announcedText       = "The ball got boosted by blue !"
                game.announcedTextFrames = 300

            if game.onPlatformRight and game.abilityRight == 1 and float(random(1)) < float(0.2):
                ball.vx *= 5
                ball.vz *= 2.5
                game.announcedText       = "The ball got boosted by red !"
                game.announcedTextFrames = 300

            ball.vy = ball.velocityAfterPaddleCollition #* (1 + game.difficulty * 0.05)
            ball.colorBonus = 135

        else:
            if ball.x > 0:
                game.scoreLeft += 1
                game.leftTextColorBonus = 200

            elif ball.x < 0:
                game.scoreRight += 1
                game.rightTextColorBonus = 200
            game.framesToRestart = 0
            ball.vx = int(random(1, 8))

            if float(random(1)) > float(0.5):
                ball.vx *= -1

            ball.vy = -10
            ball.vz = int(random(1, 8))

            if float(random(1)) > float(0.5):
                ball.vz *= -1
            game.difficulty = 0
            game.framesToDifficulty = 0
            ball.x = 0
            ball.y = 0
            ball.z = 0

    if ((keys.F and game.abilityLeft == 3 and game.abilityCountLeft >= 1) or (keys.INFERIOR and game.abilityRight == 3 and game.abilityCountRight >= 1)) and ball.framesSinceFreeze > 50:
        if keys.F:
            game.abilityCountLeft -= 1
            keys.F = False

        else:
            game.abilityCountRight -= 1
            keys.INFERIOR = False

        ball.tempvx = ball.vx
        ball.tempvy = ball.vy
        ball.tempvz = ball.vz
        ball.vx     = 0
        ball.vy     = 0
        ball.vz     = 0
        ball.framesSinceFreeze = 0

    if ((keys.F and game.abilityLeft == 5 and game.abilityCountLeft >= 1) or (keys.INFERIOR and game.abilityRight == 5 and game.abilityCountRight >= 1)) and ball.framesSinceSlow > 300:
        if keys.F:
            game.abilityCountLeft -= 1
            keys.F = False
        else:
            game.abilityCountRight -= 1
            keys.INFERIOR = False
        ball.framesSinceSlow = 0

    if ball.framesSinceFreeze > 50 and game.framesToRestart > 90:

        if ball.framesSinceFreeze == 51:
            ball.vx = ball.tempvx
            ball.vy = ball.tempvy
            ball.vz = ball.tempvz

        if isCollidingWithWallX():
            ball.vx = -1 * ball.vx + (ball.velocityFactorAfterWallCollition * (1 + game.difficulty * 0.25))/(ball.vx)/2#ball.velocityFactorAfterWallCollition * (ball.vx / abs(ball.vx))
            ball.colorBonus = 135

        if isCollidingWithWallZ():
            ball.vz = -1 * ball.vz + (ball.velocityFactorAfterWallCollition * (1 + game.difficulty * 0.25))/(ball.vz)/2#ball.velocityFactorAfterWallCollition * (ball.vz / abs(ball.vz))
            ball.colorBonus = 135

        ball.vx *= ball.fx
        ball.vx = max(abs(ball.vx), abs(ball.vxMin * (1 + game.difficulty * 0.25)))*(ball.vx / abs(ball.vx))
        ball.vz *= ball.fz
        ball.vz = max(abs(ball.vz), abs(ball.vzMin * (1 + game.difficulty * 0.25)))*(ball.vz / abs(ball.vz))
        ball.x += ball.vx + ball.vxBonus
        ball.x = constrain(ball.x, -width/2 + ball.size, width/2 - ball.size)
        ball.z += ball.vz + ball.vzBonus
        ball.z = constrain(ball.z, -width/4 + ball.size, width/4 - ball.size)
        ball.y += ball.vy
        ball.vy += ball.a
    if game.controlledBall:
        playBall()
    noStroke()
    fill(ball.colors[0] + ball.colorBonus,
         ball.colors[1] + ball.colorBonus * ((255 - ball.colors[1]) / 135),
         ball.colors[2] + ball.colorBonus * ((255 - ball.colors[2]) / 135))
    # Sphere
    pushMatrix()
    translate(ball.x, ball.y, ball.z)
    sphere(ball.size)
    popMatrix()
    # Predicted location
    if game.showPredictedLocation:
        pushMatrix()
        fill(255)
        translate(spoofBall.predBallX, height/2, spoofBall.predBallZ)
        sphere(spoofBall.size)
        popMatrix()
    # Blue text
    pushMatrix()
    translate(-width/2 + width/16, -height/2 + height/8, width/4)
    textMode(SHAPE)
    textAlign(LEFT, CENTER)
    textSize(48)
    fill(70 + game.leftTextColorBonus * 1.85, 70 + game.leftTextColorBonus * 1.85, 155 + game.leftTextColorBonus)
    text(str(game.scoreLeft) + " points, " + str(game.setsLeft) + " sets", 0, 0)
    popMatrix()
    # Red text
    pushMatrix()
    translate(width/2 - width/16, -height/2 + height/8, width/4)
    textMode(SHAPE)
    textAlign(RIGHT, CENTER)
    textSize(48)
    fill(155 + game.rightTextColorBonus, 70 + game.rightTextColorBonus * 1.85, 70 + game.rightTextColorBonus * 1.85)
    text(str(game.scoreRight) + " points, " + str(game.setsRight) + " sets", 0, 0)
    popMatrix()
    # Announcement text
    pushMatrix()
    translate(0, -height/4, width/4)
    textMode(SHAPE)
    textAlign(CENTER, CENTER)
    textSize(48)
    fill(255)
    text(game.announcedText, 0, 0)
    popMatrix()
    # Framerate
    if game.showFrameRate:
        pushMatrix()
        translate(0, -height/2.5, width/4)
        textMode(SHAPE)
        textAlign(CENTER, CENTER)
        textSize(48)
        fill(255,  255 * ((frameRate - 30) / 30), 255 * ((frameRate - 30) / 30))
        text(str(int(frameRate)) + "fps", 0, 0)
        popMatrix()
    # Shadow
    if game.showShadow:
        pushMatrix()
        translate(ball.x, height/2 + ball.size/2, ball.z)
        fill(0, 0, 0)
        sphere(ball.size)
        popMatrix()

def drawMenu():
    noStroke()
    buttonWidth = width / (len(game.abilities) + 3)
    spaceWidth  = (width - buttonWidth * (len(game.abilities) + 2)) / (len(game.abilities) - 1)
    hoveredAbilityNumber = 0
    hoveredAbility       = False
    game.menuCompleted = game.abilityLeft >= 0 and game.abilityRight >= 0
    if game.drawMenuNextCall:
        game.drawMenuNextCall = False
        if not game.abilityLeft >= 0:
            background(loadImage("stars_blue.png"))#, 0, 0, width, height)
        else:
            background(loadImage("stars_red.png"))#, 0, 0, width, height)
        for ability in range(len(game.abilities)):
            if ability == 0:
                image(loadImage(game.abilities[ability][1]), (ability + 1) * buttonWidth, height/3, buttonWidth, buttonWidth)
                game.buttonsCoords[ability] = [(ability + 1) * buttonWidth, (ability + 1) * buttonWidth + buttonWidth]
            else:
                image(loadImage(game.abilities[ability][1]), (ability + 1) * buttonWidth + ability * spaceWidth, height/3, buttonWidth, buttonWidth)
                game.buttonsCoords[ability] = [(ability + 1) * buttonWidth + ability * spaceWidth, (ability + 1) * buttonWidth + ability * spaceWidth + buttonWidth]        
    for coords in range(len(game.buttonsCoords)):
        if mouseY > height/3 and mouseY < height/3 + buttonWidth:
            if mouseX > game.buttonsCoords[coords][0] and mouseX < game.buttonsCoords[coords][1]:
                handCursor = True
                hoveredAbility = True
                hoveredAbilityNumber = coords

    if hoveredAbility:
        cursor(HAND)
        fill(0)
        rect(width/5, 2 * height/3, width - 2 * width/5, height/3 - height/10)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(width/30)
        text(game.abilities[hoveredAbilityNumber][0], width/5, 2 * height/3, width - 2 * width/5, height/3 - height/4)
        textSize(width/50)
        text(game.abilities[hoveredAbilityNumber][2], width/5, 2 * height/3 + height/20, width - 2 * width/5, height/3 - height/10)
    else: 
        cursor(ARROW)
    if game.mouseClicked:
        game.mouseClicked = False
        if not game.abilityLeft >= 0:
            game.drawMenuNextCall = True
            game.abilityLeft = hoveredAbilityNumber
        else: 
            game.abilityRight = hoveredAbilityNumber

def drawFrame():
    global leftSizeFactor, rightSizeFactor
    if game.botLeft or game.botRight or game.showPredictedLocation:
        botPredict()
    botMove()
    if game.botRight  :
        if random(1) < 0.001:
            keys.INFERIOR = True
    game.framesToDifficulty += 1
    if game.framesToDifficulty % game.framesForDifficulty == 0:
        game.difficulty         += 1
        game.announcedText       = "Difficulty increased !"
        game.announcedTextFrames = 255
    game.announcedTextFrames  -= 1
    game.framesConfusionLeft  += 1
    game.framesConfusionRight += 1
    game.framesDarknessLeft   += 1
    game.framesDarknessRight  += 1
    game.framesToRestart      += 1
    leftSizeFactor = 1
    leftSpeedFactor = 1
    if game.announcedTextFrames < 1:
        game.announcedText = ""
    if game.abilityLeft == 0:
        leftSizeFactor = 1.25
    elif game.abilityLeft == 2:
        leftSpeedFactor = 1.25
    rightSizeFactor = 1
    rightSpeedFactor = 1
    if game.abilityRight == 0:
        rightSizeFactor = 1.25
    elif game.abilityRight == 2:
        rightSpeedFactor = 1.25
    if game.framesConfusionLeft < 100:
        leftSpeedFactor *= -1
    if game.framesConfusionRight < 100:
        rightSpeedFactor *= -1
    if (keys.F and game.abilityLeft == 4 and game.abilityCountLeft >= 1) and game.framesConfusionRight > 100 and not game.botRight:
        keys.F                    = False
        game.announcedText        = "Red got confused !"
        game.announcedTextFrames  = 300
        game.framesConfusionRight = 0
        game.abilityCountLeft    -= 1
    if (keys.INFERIOR and game.abilityRight == 4 and game.abilityCountRight >= 1) and game.framesConfusionLeft > 100 and not game.botLeft:
        keys.INFERIOR = False
        game.announcedText       = "Blue got confused !"
        game.announcedTextFrames = 300
        game.framesConfusionLeft = 0
        game.abilityCountRight  -= 1
    if (keys.F and game.abilityLeft == 6 and game.abilityCountLeft >= 1) and game.framesDarknessRight > 300 and game.framesDarknessLeft > 300:
        keys.F = False
        game.announcedText       = "Lights off for red !"
        game.announcedTextFrames = 300
        game.framesDarknessRight = 0
        game.abilityCountLeft   -= 1
    if (keys.INFERIOR and game.abilityRight == 6 and game.abilityCountRight >= 1) and game.framesDarknessRight > 300 and game.framesDarknessRight > 300:
        keys.INFERIOR = False
        game.announcedText       = "Lights off for blue !"
        game.announcedTextFrames = 300
        game.framesDarknessLeft  = 0
        game.abilityCountRight  -= 1
    noCursor()
    game.rainbow += 1
    if game.rainbow == 256: game.rainbow = 0
    fill(255)
    ball.colorBonus = constrain(ball.colorBonus - 5, 0, 150)
    game.leftTextColorBonus = constrain(game.leftTextColorBonus - 3, 0, 100)
    game.rightTextColorBonus = constrain(game.rightTextColorBonus - 3, 0, 100)
    camera(width/2.0, height/2, (height/2.0) / tan(PI*30.0 / 180.0) -
           00, width/2.0, height/2.0, 0, 0, 1, 0)
    if game.framesDarknessRight < 300:
        spotLight(255, 255, 255, width/2, 0, 0, -1, 1, -0.5, TAU/4, 0.75)

    elif  game.framesDarknessLeft < 300:
        spotLight(255, 255, 255, width/2, 0, 0, 1, 1, -0.5, TAU/4, 0.75)

    else:
        spotLight(255, 255, 255, width/2, height/5, width/4, 0, 1, -0.5, TAU, 0)

    translate(width/2, height/2, -width/4)
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
        paddle.leftX -= paddle.speedX * leftSpeedFactor * 0.707106781
        paddle.leftZ -= paddle.speedZ * leftSpeedFactor * 0.707106781
    if paddle.leftMovZ and paddle.leftMovXneg:
        paddle.leftX -= paddle.speedX * leftSpeedFactor * 0.707106781
        paddle.leftZ += paddle.speedZ * leftSpeedFactor * 0.707106781
    if paddle.leftMovZneg and paddle.leftMovX:
        paddle.leftX += paddle.speedX * leftSpeedFactor * 0.707106781
        paddle.leftZ -= paddle.speedZ * leftSpeedFactor * 0.707106781
    if paddle.leftMovZ and paddle.leftMovX:
        paddle.leftX += paddle.speedX * leftSpeedFactor * 0.707106781
        paddle.leftZ += paddle.speedZ * leftSpeedFactor * 0.707106781
    if paddle.leftMovZneg and not paddle.leftMovXneg and not paddle.leftMovX:
        paddle.leftZ -= paddle.speedZ * leftSpeedFactor
    if paddle.leftMovZ and not paddle.leftMovXneg and not paddle.leftMovX:
        paddle.leftZ += paddle.speedZ * leftSpeedFactor
    if paddle.leftMovXneg and not paddle.leftMovZneg and not paddle.leftMovZ:
        paddle.leftX -= paddle.speedX * leftSpeedFactor
    if paddle.leftMovX and not paddle.leftMovZneg and not paddle.leftMovZ:
        paddle.leftX += paddle.speedX * leftSpeedFactor
    paddle.leftX = constrain(paddle.leftX, -width/2 + (paddle.sideLen * leftSizeFactor)/2, 0 - (paddle.sideLen * leftSizeFactor)/2)
    paddle.leftZ = constrain(paddle.leftZ, -width/4 + (paddle.sideLen * leftSizeFactor)/2, width/4 - (paddle.sideLen * leftSizeFactor)/2)

    # Drawing the left box
    rectMode(CENTER)
    noStroke()
    fill(0, 0, 255)
    stroke(127, 0, 255)
    noFill()
    box(width, height, width/2)
    # Drawing the middle line
    pushMatrix()
    translate(0, height/4 + height/4, 0)
    box(0, 0, width/2)
    popMatrix()
    # Drawing fixed assets
    pushMatrix()
    translate(0, height/2, 0)
    fill("#1C1C2C")
    box(width, 0, width/2)
    popMatrix()
    pushMatrix()
    translate(0, 0, -width/4)
    box(width, height, 0)
    popMatrix()
    pushMatrix()
    translate(-width/2, 0, 0)
    box(0, height, width/2)
    popMatrix()
    pushMatrix()
    translate(width/2, 0, 0)
    box(0, height, width/2)
    popMatrix()
    pushMatrix()
    translate(0, -height/2, 0)
    box(width, 0, width/2)
    popMatrix()
    if game.abilityLeft == 7: colorMode(HSB); fill(game.rainbow, 255, 127); stroke(game.rainbow, 255, 255)
    else: fill(0, 0, 127); stroke(0, 0, 255)
    translate(paddle.leftX, height/2 - paddle.sideLen / 32, paddle.leftZ)
    box(paddle.sideLen * leftSizeFactor, paddle.sideLen / 16, paddle.sideLen * leftSizeFactor)
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
        paddle.rightX -= paddle.speedX * rightSpeedFactor * 0.707106781
        paddle.rightZ -= paddle.speedZ * rightSpeedFactor * 0.707106781
    if paddle.rightMovZ and paddle.rightMovXneg:
        paddle.rightX -= paddle.speedX * rightSpeedFactor * 0.707106781
        paddle.rightZ += paddle.speedZ * rightSpeedFactor * 0.707106781
    if paddle.rightMovZneg and paddle.rightMovX:
        paddle.rightX += paddle.speedX * rightSpeedFactor * 0.707106781
        paddle.rightZ -= paddle.speedZ * rightSpeedFactor * 0.707106781
    if paddle.rightMovZ and paddle.rightMovX:
        paddle.rightX += paddle.speedX * rightSpeedFactor * 0.707106781
        paddle.rightZ += paddle.speedZ * rightSpeedFactor * 0.707106781
    if paddle.rightMovZneg and not paddle.rightMovXneg and not paddle.rightMovX:
        paddle.rightZ -= paddle.speedZ * rightSpeedFactor
    if paddle.rightMovZ and not paddle.rightMovXneg and not paddle.rightMovX:
        paddle.rightZ += paddle.speedZ * rightSpeedFactor
    if paddle.rightMovXneg and not paddle.rightMovZneg and not paddle.rightMovZ:
        paddle.rightX -= paddle.speedX * rightSpeedFactor
    if paddle.rightMovX and not paddle.rightMovZneg and not paddle.rightMovZ:
        paddle.rightX += paddle.speedX * rightSpeedFactor
    paddle.rightX = constrain(paddle.rightX, 0 + (paddle.sideLen * rightSizeFactor)/2, width/2 - (paddle.sideLen * rightSizeFactor)/2)
    paddle.rightZ = constrain(paddle.rightZ, -width/4 + (paddle.sideLen * rightSizeFactor)/2, width/4 - (paddle.sideLen * rightSizeFactor)/2)
    if game.abilityRight == 7: colorMode(HSB); fill(game.rainbow, 255, 127); stroke(game.rainbow, 255, 255)
    else: fill(127, 0, 0); stroke(255, 0, 0)
    rectMode(CENTER)
    popMatrix()
    pushMatrix()
    translate(paddle.rightX, height/2 - paddle.sideLen / 32, paddle.rightZ)
    box(paddle.sideLen * rightSizeFactor, paddle.sideLen / 16, paddle.sideLen * rightSizeFactor)
    colorMode(RGB)
    popMatrix()
    drawBall()

def draw():
    if game.scoreLeft >= game.setPoints:
        game.announcedText       = "Set won by Blue, abilities reset"
        game.announcedTextFrames = 400
        game.leftTextColorBonus  = 100
        game.scoreRight          = 0
        game.scoreLeft           = 0
        game.setsLeft           += 1
        game.abilityCountLeft    = 3
        game.abilityCountRight   = 4
    if game.scoreRight >= game.setPoints:
        game.announcedText       = "Set won by Red, abilities reset"
        game.announcedTextFrames = 300
        game.rightTextColorBonus = 100
        game.scoreRight          = 0
        game.scoreLeft           = 0
        game.setsRight          += 1
        game.abilityCountLeft    = 3
        game.abilityCountRight   = 4
    if game.menuCompleted:
        drawFrame()
    else: drawMenu()

def keyPressed():
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
    if keyCode == 73:
        keys.I = True
    if keyCode == 74:
        keys.J = True
    if keyCode == 75:
        keys.K = True
    if keyCode == 76:
        keys.L = True
    if keyCode == 72:
        keys.H = True
    
def keyReleased():
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
    if keyCode == 73:
        keys.I = False
    if keyCode == 74:
        keys.J = False
    if keyCode == 75:
        keys.K = False
    if keyCode == 76:
        keys.L = False
    if keyCode == 72:
        keys.H = False

def mouseClicked():
    game.mouseClicked = True

def isUnderground():
    return ball.y > height

def isUnderPaddle():
    return ball.y >= height/2 - paddle.sideLen / 16 - ball.size/2

def isOverPaddles():
    game.onPlatformLeft = ball.x+ball.size > paddle.leftX - (paddle.sideLen * leftSizeFactor)/2 and ball.x - \
        ball.size < paddle.leftX + (paddle.sideLen * leftSizeFactor)/2 and \
        ball.z+ball.size > paddle.leftZ - (paddle.sideLen * leftSizeFactor)/2 and ball.z - \
        ball.size < paddle.leftZ + (paddle.sideLen * leftSizeFactor)/2
    game.onPlatformRight = ball.x+ball.size > paddle.rightX - (paddle.sideLen * rightSizeFactor)/2 and ball.x - \
        ball.size < paddle.rightX + (paddle.sideLen * rightSizeFactor)/2 and \
        ball.z+ball.size > paddle.rightZ - (paddle.sideLen * rightSizeFactor)/2 and ball.z - \
        ball.size < paddle.rightZ + (paddle.sideLen * rightSizeFactor)/2
    return game.onPlatformLeft or game.onPlatformRight

def isStrictlyOverPaddles():
    game.onPlatformLeft = ball.x-ball.size > paddle.leftX - paddle.sideLen/2 and ball.x + \
        ball.size < paddle.leftX + paddle.sideLen/2 and \
        ball.z-ball.size > paddle.leftZ - paddle.sideLen/2 and ball.z + \
        ball.size < paddle.leftZ + paddle.sideLen/2
    game.onPlatformRight = ball.x-ball.size > paddle.rightX - paddle.sideLen/2 and ball.x + \
        ball.size < paddle.rightX + paddle.sideLen/2 and \
        ball.z-ball.size > paddle.rightZ - paddle.sideLen/2 and ball.z + \
        ball.size < paddle.rightZ + paddle.sideLen/2
    return game.onPlatformLeft or game.onPlatformRight

def isCollidingWithWallX():
    onWallNegX = ball.x-ball.size <= -width/2  # X
    onWallPosX = ball.x+ball.size >= width/2
    return onWallNegX or onWallPosX

def isCollidingWithWallZ():
    onWallNegZ = ball.z-ball.size <= -width/4  # Z
    onWallPosZ = ball.z+ball.size >= width/4
    return onWallNegZ or onWallPosZ