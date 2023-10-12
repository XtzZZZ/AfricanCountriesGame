class Custom(Screen):
    timeLimit = ObjectProperty(None)
    livesLeft = ObjectProperty(None)

    def btn(self):
        f = open('custommode.txt', 'w')
        f.write(f'{self.timeLimit.text}\n{self.livesLeft.text}')
        f.close()
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Auth'
        f = open('custommode.txt', 'r')
        timeLimit = f.readline()
        livesLeft = f.readline()
        print(timeLimit, livesLeft)
        f.close()