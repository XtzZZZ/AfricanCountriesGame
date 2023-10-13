import threading

import kivy
import os
import multiprocessing
import time

from kivy.clock import Clock
from kivy.graphics import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from posixpath import dirname
from kivy.uix.popup import Popup
from functools import partial

Builder.load_file(os.path.join(dirname(__file__), 'GamePage.kv'))
Builder.load_file(os.path.join(dirname(__file__), 'GameOverPage.kv'))

Window.size = (500, 550)
Window.clearcolor = (14/88, 0, 30/88, 1)


countries = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Ivory Coast', 'Djibouti', 'Democratic Republic of the Congo', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Republic of the Congo', 'Rwanda', 'Sao Tome & Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']

class CustomAppManager(ScreenManager):
    def __init__(self):
        super(CustomAppManager, self).__init__()
        self.add_widget(Authorization(sm=self, name='Auth'))
        self.add_widget(GameOverPage(sm=self, name='GOP'))
        self.usedCountries = []

    def AddGamePage(self, livesLeft, timeLimit, **kwargs):
        self.add_widget(GamePage(livesLeft=livesLeft, timeLimit=timeLimit, sm=self, name='GP'))
        self.add_widget(Authorization(sm=self, name='Auth'))
        self.add_widget(GameOverPage(sm=self, name='GOP'))

    def refresh(self, Page, **kwargs):
        self.clear_widgets(screens=kwargs['name'])
        self.add_widget(Page(**kwargs))


class GameOverPage(Screen):
    def __init__(self, sm : CustomAppManager, **kwargs):
        self.sm = sm
        super(GameOverPage, self).__init__(**kwargs)

    def pressed(self):
        self.sm.refresh(Page=Authorization, sm=self.sm, name='Auth')
        self.sm.transition = SlideTransition(direction="right")
        self.sm.current = 'Auth'

class P(FloatLayout):
    def __init__(self, sm: CustomAppManager, result : str, **kwargs):
        self.sm = sm
        self.result = result
        super(P, self).__init__(**kwargs)

    def pressed(self):
        self.popup.parent.remove_widget(self.popup)
        self.sm.usedCountries = []
        self.sm.refresh(Page=Authorization, sm=self.sm, name='Auth')
        self.sm.transition = SlideTransition(direction="right")
        self.sm.current = 'Auth'


class CustomPopup(Popup):
    def __init__(self, **kwargs):
        kwargs['content'].popup = self
        super(CustomPopup, self).__init__(**kwargs)


class GamePage(Screen):
    def __init__(self, timeLimit, livesLeft, sm : CustomAppManager, totalScore=0, inARow=0, isGame=False, **kwargs):
        self.timeLimit = str(timeLimit)
        self.livesLeft = str(livesLeft)
        self.totalScore = str(totalScore)
        self.inARow = str(inARow)
        self.sm = sm
        self.maxStreak = 0
        super(GamePage, self).__init__(**kwargs)
        if not isGame:
            self.timeLimitExceed(timeLimit)


    country = ObjectProperty(None)

    def submitted(self):
        guess = self.country.text.title()
        if guess in countries and guess not in self.sm.usedCountries:
            self.totalScore = str(int(self.totalScore) + 1)
            self.inARow = str(int(self.inARow) + 1)
            self.maxStreak = max(self.maxStreak, int(self.inARow))
            self.sm.usedCountries.append(guess)
        elif guess in self.sm.usedCountries:
            print('The country has already been guessed')
        else:
            self.livesLeft = int(self.livesLeft) - 1 #wrong guess -1 life
            self.maxStreak = max(self.maxStreak, int(self.inARow))
            self.inARow = 0
        self.country.text = ""
        if int(self.livesLeft) <= 0:
            with open('data.txt', 'a') as f:
                f.write(f'{self.totalScore} ')
                f.write(f'{self.inARow}\n')#add self.mode to the data

            result = f'    You ran out of lives\n    Your total score is {self.totalScore}\nMaximum streak was {self.maxStreak}'
            show = P(sm=self.sm, result=result)
            popupWindow = CustomPopup(
                title="Game over",
                content=show,
                size_hint=(None, None),
                size=(625, 350),
                separator_color=[0, 255/255, 210/255, .5],
                background_color=[125/255, 0, 1, 1]
            )
            popupWindow.open()

        if len(self.sm.usedCountries) >= 3:
            with open('data.txt', 'a') as f:
                f.write(f'{self.totalScore} ')
                f.write(f'{self.inARow}\n')#add self.mode to the data

            result = f'        Congratz, u won!\nYour maximum streak was {self.maxStreak}'
            show = P(sm=self.sm, result=result)
            CustomPopup(
                title="Game over",
                content=show,
                size_hint=(None, None),
                size=(625, 350),
                separator_color=[0, 255 / 255, 210 / 255, .5],
                background_color=[125 / 255, 0, 1, 1]
            ).open()
        return self.sm.refresh(Page=GamePage, name='GP', timeLimit=int(self.timeLimit), livesLeft=self.livesLeft, sm=self.sm, totalScore=self.totalScore, inARow=self.inARow, isGame=True)

    def showPopup(self, *args):
        result = f'    You ran out of time\n    Your total score is {self.totalScore}\nMaximum streak was {self.maxStreak}'
        show = P(sm=self.sm, result=result)
        popupWindow = CustomPopup(
            title="Game over",
            content=show,
            size_hint=(None, None),
            size=(625, 350),
            separator_color=[0, 255 / 255, 210 / 255, .5],
            background_color=[125 / 255, 0, 1, 1]
        )
        popupWindow.open()

    def timeLimitExceed(self, timeLimit):
        self.event = Clock.schedule_once(partial(self.showPopup), timeLimit)
        return



class Authorization(Screen):
    def __init__(self, sm : CustomAppManager, **kwargs):
        self.sm = sm
        super(Authorization, self).__init__(**kwargs)

    namee = ObjectProperty(None)
    formGroup = ObjectProperty(None)
    livesLeft = ObjectProperty(None)
    timeLimit = ObjectProperty(None)

    def pressed(self, index):
        with open('data.txt', 'a+') as f:
            f.write(f'{self.namee.text}, {self.formGroup.text}\n')

        self.namee.text = ""
        self.formGroup.text = ""
        TL = 0 #time limit
        LL = 0 #life limit
        match index:
            case 1: #easy
                TL = 999999999
                LL = 99999999
            case 2: #medium
                TL = 600
                LL = 10
            case 3: #hardcore
                TL = 150
                LL = 1
        if index == 4: #custom
            TL = int(self.timeLimit.text)
            LL = int(self.livesLeft.text)
            self.timeLimit.text = ""
            self.livesLeft.text = ""

        self.sm.AddGamePage(livesLeft=LL, timeLimit=TL, name='GP')
        #start the game
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'GP'



class AfricaGameApp(App):
    def build(self):
        sm = CustomAppManager()
        return sm


if __name__ == '__main__':
    AfricaGameApp().run()