__author__ = '8.Ball'

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.animation import Animation


#Keeping a fixed window size
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'width', '500')

"""
Builder .kv specs
"""
Builder.load_string("""
<HomeScreen>
    GridLayout:
        #Displaying the icon
        Image:
            source: 'images/icon_generator.png'
            size: (350, 350)
            x: 75
            y: 110

        #Displaying the entry area
        TextInput:
            id: inputArea
            hint_text: 'Enter text here'
            multiline: False
            size: (470, 30)
            x: 15
            y: 190
            on_text_validate: root.generate()
            focus: True

        #Displaying the Generate Button
        Button:
            text: 'Generate'
            size: (100,30)
            x: 192
            y: 150
            background_color: (0, 255, 1, 1)
            on_press: root.generate()

        #Displaying the Clear Button
        Button:
            text: '×'
            font_size: 22
            color: (215, 215, 215, 1)
            background_color: (228, 228, 228, .1)
            size: (29, 27)
            x: 456
            y: 192
            on_press: root.clearText()

        #Displaying Help Button
        Button:
            text: 'Help   |'
            font_size: 10
            background_color: (0, 0, 0, 0)
            size: (45, 20)
            x: 420
            y: 0
            on_press: root.showHelp()

        #Displaying the About Button
        Button:
            text: 'About'
            font_size: 10
            background_color: (0, 0, 0, 0)
            size: (45, 20)
            x: 455
            y: 0
            on_press: root.showAbout()

        #Displaying copyright tag
        Label:
            text: 'Copyright © 2019  |_aiben'
            font_size: 11
            x: 27
            y: -40

<helpPopup>
    title: 'Help'
    GridLayout:
        Button:
            text: 'Close'
            size: (100, 30)
            x: 385
            y: 20
            on_press: root.dismiss()

        Image:
            source: 'images/helpIcon.png'
            size: (85, 85)
            x: 15
            y: 230

        Label:
            text: 'Type any string(combination of characters) and '
            font_size: 14
            markup: True
            x: 220
            y: 240

        Label:
            text: ' Palindrome Generator 1.0.0 will generate all the possible'
            font_size: 14
            markup: True
            x: 242
            y: 221

        Label:
            text: 'palindromic sub-strings.'
            font_size: 14
            markup: True
            x: 145
            y: 205

        Label:
            text: 'Everything is accessible in the environment.'
            font_size: 14
            markup: True
            x: 204
            y: 160

        Label:
            text: 'The environment will display the list of all possible'
            font_size: 14
            markup: True
            x: 220
            y: 110

        Label:
            text: 'palindromic sub-string(s) from your input.'
            font_size: 14
            markup: True
            x: 198
            y: 93

        Label:
            text: 'Contact us on  [size=12]info@palindrome.org  [size=14]if you face any challenges.'
            font_size: 14
            markup: True
            x: 198
            y: 30

<aboutPopup>
    title: 'About'
    GridLayout:
        Button:
            text: 'Close'
            size: (100, 30)
            x: 385
            y: 20
            on_press: root.dismiss()

        Image:
            source: 'images/icon.png'
            size: (125, 125)
            x: 30
            y: 150

        Label:
            text: 'Copyright © 2019  |_aiben'
            font_size: 11
            x: 31
            y: -33

        Label:
            text: '[b]Palindrome  Generator'
            markup: True
            font_size: 23
            x: 252
            y: 270

        Label:
            text: '1.0.0  Maiden'
            markup: True
            font_size: 17
            x: 188
            y: 240

        Label:
            text: 'Palindrome Generator is full-featured environment '
            markup: True
            font_size: 13
            x: 280
            y: 193

        Label:
            text: 'aiming to show all possible palindromic sub-strings '
            markup: True
            font_size: 13
            x: 282
            y: 178

        Label:
            text: 'of your input.'
            markup: True
            font_size: 13
            x: 173
            y: 163

        Label:
            text: 'A palindrome is a string(combination of characters)'
            markup: True
            font_size: 13
            x: 282
            y: 130

        Label:
            text: 'that reads the same backwards and forwards.'
            markup: True
            font_size: 13
            x: 267
            y: 115

        Label:
            text: 'ENJOY!'
            markup: True
            font_size: 13
            x: 159
            y: 100

        Label:
            text: 'Help and join us!'
            markup: True
            font_size: 12
            x: 183
            y: 55

        Label:
            text: 'info@palindrome.org'
            markup: True
            font_size: 11
            x: 188
            y: 38

        Label:
            text: 'http://wwww.palindrome.org'
            markup: True
            font_size: 11
            x: 208
            y: 23

<GenerateScreen>
    GridLayout:
        #Back button
        Button:
            text: 'Back'
            size: (70, 30)
            x: 420
            y: 10
            on_press: root.manager.current = 'home'
""")

#Create Screens
class HomeScreen(Screen):
    #Function to show help pop up
    def showHelp(self):
        helpPopup().open()

    #Function to show about pop up
    def showAbout(self):
        aboutPopup().open()

    def clearText(self):
        self.ids.inputArea.text = ''

    #Function for screen transition
    def generate(self):
        if self.ids.inputArea.text == '':
            self.showHelp()
        else:
            sm.current = 'generator'
            self.start()

    def start(self, *args):
        #Function to generate palindromic sub-strings
        '''
        Manacher's Algorithm
        [To get all palindromic sub-strings]
        '''
        #Getting input into a variable
        global userInput
        userInput = self.ids.inputArea.text

        s = self.ids.inputArea.text
        m = dict()
        n = len(s)

        # table for storing results (2 rows for odd-
        # and even-length palindromes
        R = [[0 for x in range(n+1)] for x in range(2)]

        # Find all sub-string palindromes from the given input
        # string insert 'guards' to iterate easily over s
        s = "@" + s + "#"

        for j in range(2):
            rp = 0    # length of 'palindrome radius'
            R[j][0] = 0

            i = 1
            while i <= n:

                # Attempt to expand palindrome centered at i
                while s[i - rp - 1] == s[i + j + rp]:
                    rp += 1 # Incrementing the length of palindromic
                            # radius as and when we find valid palindrome

                # Assigning the found palindromic length to odd/even
                # length array
                R[j][i] = rp
                k = 1
                while (R[j][i - k] != rp - k) and (k < rp):
                    R[j][i+k] = min(R[j][i-k], rp - k)
                    k += 1
                rp = max(rp - k, 0)
                i += k

        # remove guards
        s = s[1:len(s)-1]

        # Put all obtained palindromes in a hash map to
        # find only distinct palindrome
        m[s[0]] = 1
        for i in range(1,n):
            for j in range(2):
                for rp in range(R[j][i],0,-1):
                    m[s[i - rp - 1 : i - rp - 1 + 2 * rp + j]] = 1
            m[s[i]] = 1

        #Getting the sub-strings into a single list
        global palindromeList
        palindromeList = []

        for key, value in m.items():
            palindromeList.append(key)

        self.manager.get_screen('generator').display()
    pass

class helpPopup(Popup):
    pass

class aboutPopup(Popup):
    pass

class GenerateScreen(Screen):
    #Fade in animation function
    def animate(self, what):
        anim = Animation(opacity=0, duration=0)
        anim += Animation(opacity=1, duration=1)
        anim.start(what)


    def display(self):
        self.palindromeList = palindromeList
        '''Function to display sub-strings go here'''
        #Clearing the entire area
        self.add_widget(Image(source= 'images/clear.png'))
        self.add_widget(Image(source= 'images/clear.png', x= 0, y= 90))

        numPal = len(self.palindromeList)

        #When there is only one sub-string
        if numPal == 1:
            self.add_widget(Label(text= "The possible palindromic sub-string in"+" '"+userInput+"' "+ "is:",
                                  x= -15,
                                  y= 40))
            label = Label(text= self.palindromeList[0],
                            x = -10,
                            y = 15,
                            font_size= 35)
            self.add_widget(label)
            self.animate(label)


        #When there are 2 sub-strings
        if numPal == 2:
            #Position
            x = -60
            y = 5

            #Font Size
            fontSize  = 35

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 40))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)
                x += 70

        #When there are 3 sub-strings
        if numPal == 3:
            #Position
            x = -80
            y = 5

            #Font Size
            fontSize  = 35

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 40))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)

                x += 70

        #When there are 4 sub-strings
        if numPal == 4:
            #Position
            x = -100
            y = 5

            #Font Size
            fontSize  = 35

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 40))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)

                x += 70

        #When there are between 5 and 10 sub-strings
        if numPal >= 5 and numPal <= 10:
            #Position
            x = -190
            y = 110

            #Font Size
            fontSize  = 35

            #Counter
            count = 0

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 180))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)

                x += 170

                #Count increments
                count += 1

                if count == 3:
                    x = -190
                    y -= 70

                if count == 6:
                    x = -190
                    y -= 70

                if count == 9:
                    x = -190
                    y -= 70

        #When there are between 10 and 20 sub-strings
        if numPal > 10 and numPal <= 20:
            #Position
            x = -190
            y = 150

            #Font Size
            fontSize  = 25

            #Counter
            count = 0

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 180))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)

                x += 170

                #Count increments
                count += 1

                if count == 3:
                    x = -190
                    y -= 45

                if count == 6:
                    x = -190
                    y -= 45

                if count == 9:
                    x = -190
                    y -= 45

                if count == 12:
                    x = -190
                    y -= 45

                if count == 15:
                    x = -190
                    y -= 45

                if count == 18:
                    x = -190
                    y -= 45

        #When there are 20 or more sub-strings
        if numPal > 20:
            #Position
            x = -190
            y = 160

            #Font Size
            fontSize  = 17

            #Counter
            count = 0

            self.add_widget(Label(text= "The possible palindromic sub-strings in"+" '"+userInput+"' "+ "are:",
                                  x= -15,
                                  y= 180))

            for i in range(0, numPal):
                label = Label(text= self.palindromeList[i],
                                x = x,
                                y = y,
                                font_size= fontSize)
                self.add_widget(label)
                self.animate(label)

                x += 170

                #Count increments
                count += 1

                if count == 3:
                    x = -190
                    y -= 30

                if count == 6:
                    x = -190
                    y -= 30

                if count == 9:
                    x = -190
                    y -= 30

                if count == 12:
                    x = -190
                    y -= 30

                if count == 15:
                    x = -190
                    y -= 30

                if count == 18:
                    x = -190
                    y -= 30

                if count == 21:
                    x = -190
                    y -= 30

                if count == 24:
                    x = -190
                    y -= 30

                if count == 27:
                    x = -190
                    y -= 30

                if count == 30:
                    x = -190
                    y -= 30

                if count == 33:
                    x = -190
                    y -= 30

                if count == 36:
                    x = -190
                    y -= 30

                if count == 39:
                    x = -190
                    y -= 30

                if count == 42:
                    x = -190
                    y -= 30

                if count == 45:
                    x = -190
                    y -= 30

                if count == 48:
                    x = -190
                    y -= 30

                if count == 51:
                    x = -190
                    y -= 30
    pass

#Create Screen Manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(GenerateScreen(name='generator'))

class PalindromeGenerator(App):
    def build(self):
        self.title = 'Palindrome Generator'
        self.icon = 'images/icon.png'

        return sm

PalindromeGenerator().run()