from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from openpyxl import load_workbook

Config.set("graphics", "resizable", 1)
Config.set("graphics", "width", 1000)
Config.set("graphics", "height", 600)


class ThemeLabel(Label):
    def __init__(self, **kwargs):
        super(ThemeLabel, self).__init__(**kwargs)
        self.color = [1, 1, 1, 1]
        self.font_size = 20

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.09, .09, .35, 1)
            Rectangle(pos=self.pos, size=self.size)


class QuestionButton(Button):
    def __init__(self, col, row, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.background_color = [.25, .25, 1, 1]
        self.font_size = 20
        self.col = col
        self.row = row


class Main(BoxLayout):
    def main_window(self, instance):
        self.clear_widgets()
        self.orientation = "horizontal"

        themes_layout = BoxLayout(orientation="vertical",
                                  padding=[5, 5, 2.5, 5],
                                  spacing=5,
                                  size_hint=[.45, 1])
        for k in range(6):
            themes_layout.add_widget(ThemeLabel(text=question_table[k][0]))

        price_layout = GridLayout(rows=6, cols=5,
                                  padding=[2.5, 5, 5, 5],
                                  spacing=5,
                                  size_hint=[.55, 1])
        for row in range(price_layout.rows):
            for col in range(price_layout.cols):
                price_layout.add_widget(QuestionButton(row=row, col=col,
                                                       on_press=self.question_window,
                                                       text=price_table[row][col]))

        self.add_widget(themes_layout)
        self.add_widget(price_layout)

    def question_window(self, instance):
        price_table[instance.row][instance.col] = ""
        self.clear_widgets()
        self.orientation = "vertical"
        self.add_widget(ThemeLabel(size_hint=[1, .6], text=question_table[instance.row][instance.col + 1]))
        self.add_widget(Button(background_color=[.25, .25, 1, 1],
                               on_press=self.main_window,
                               size_hint=[1, .4],
                               text="Back"))

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)


class MyOwnGame(App):
    def build(self):
        m = Main()
        m.add_widget(Button(text="START", on_press=m.main_window))
        return m


book = load_workbook('questions.xlsx')
sheet = book.active

question_table = []
price_table = []
letters = ["A", "B", "C", "D", "E", "F"]

for i in range(6):
    q = [str(sheet[letter + str(i + 1)].value) for letter in letters]
    question_table.append(q)
    p = [str((price + 1) * 100) for price in range(5)]
    price_table.append(p)

MyOwnGame().run()
