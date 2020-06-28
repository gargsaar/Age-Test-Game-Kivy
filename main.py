from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import datetime
import random
import kivy.utils

class AgeTestGame(GridLayout):

    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)
    randomlist1 = []
    randomlist2 = []
    indexlist = []
    dialog = None
    score = """
        Scoring:
        < 30 secs: Usian Bolt!!
        31-45 secs: Almost There!
        46-60 secs: U Can Do It!
        61-90 secs: Once More!
        > 90 secs: Delete the App!
        """

    def __init__(self, **kwargs):
        super(AgeTestGame, self).__init__(**kwargs)
        self.sound = SoundLoader.load('bell.wav')
        self.initial_grid()
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0):
        self.number_grid()

    # generate the list of numbers, and shuffle the numbers in the lists
    def generate_numbers(self):
        self.randomlist1.clear()
        for i in range(1, 26):
            self.randomlist1.append(i)
            self.randomlist2.append(i+25)
        self.indexlist = self.randomlist1 + self.randomlist2
        random.shuffle(self.randomlist1)
        random.shuffle(self.randomlist2)

    # populate the number grid with 'X' before starting the game
    def initial_grid(self):
        self.minutes = '00'
        self.seconds = '00.00'
        for i in range(1, 26):
            self.randomlist1.append('X')

    # populate the number grid with random numbers
    def number_grid(self):
        number_grid = self.ids['number_grid']
        # create a Button object
        for i in range(0, 25):
            # store the grid_button object in a list
            grid_button = Button(id=str(i), text=str(self.randomlist1[i]),
                                 color=kivy.utils.get_color_from_hex("#dcd71f"),
                                 markup=True, on_release=self.click)
            # on_release button action, click function will pass the grid_button object as an instance
            number_grid.add_widget(grid_button)
            # Note: kivy widgets added through the python code are Object and can be accessed as grid_button.id

    # change the button text and background_color on click
    def click(self, instance):
        # if condition to ensure the buttons are clicked in the correct sequence
        if (instance.text != 'X') and (int(instance.text) == self.indexlist[0]):
            del self.indexlist[0]
            instance.background_color = kivy.utils.get_color_from_hex("#848b96")
            # if the button text is less than 25, replace the text with a number greater than 25
            if int(instance.id) < 25:
                instance.text = str(self.randomlist2[0])
                del self.randomlist2[0]
                instance.id = str(int(instance.id) + 25)
            # replace the button text with 'X'
            elif (int(instance.id) >= 25) and (instance.text != '50'):
                instance.text = 'X'
                instance.background_color = kivy.utils.get_color_from_hex("#e4eaf1")
            else:
                self.game_over()

    # function to be called on click of Start button
    def start_timer(self):
        # clear the number grid
        self.ids['number_grid'].clear_widgets()
        # generate new numbers and shuffle
        self.generate_numbers()
        # populate the number grid
        self.number_grid()
        # reset the timer to 00:00.00
        self.delta = datetime.datetime.now() - datetime.timedelta(0, 0)
        self.update_timer()
        # play the bell sound
        self.sound.play()
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update_timer, 0.05)

    # function to be called on click of Reset button
    def reset_timer(self, *kwargs):
        self.ids['number_grid'].clear_widgets()
        self.randomlist1.clear()
        self.initial_grid()
        self.number_grid()
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)

    def update_timer(self, *kwargs):
        # start the timer
        delta = datetime.datetime.now() - self.delta
        self.minutes = str(delta).split(":")[1:][0]
        self.seconds = str(delta).split(":")[1:][1][:5]

        #automatically stop the game if the time exceeds 3 minutes
        if int(self.minutes) == 3:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 20:
                    self.seconds = "00.00"
                    self.game_over()

    # game over pop-up (dialog)
    def game_over(self):
        self.ids['label_timer'].text = self.minutes + ':' + self.seconds
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)
        # game over dialog
        if not self.dialog:
            self.dialog = Popup(
                title="Your Score: " + self.minutes + ':' + self.seconds,
                content=Label(text=self.score),
                size_hint=(.8, .5)
            )
        self.dialog.open()
        self.reset_timer()

class MainApp(App):
    def build(self):
        return AgeTestGame()

if __name__ == '__main__':
    MainApp().run()
