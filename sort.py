from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from functools import partial
import threading
import time
import random

# just for sorting so clearing canvas will not remove buttons as well
class SortVisual(Widget):
    start = ObjectProperty(None)
    ten = ObjectProperty(None)
    hund = ObjectProperty(None)
    thou = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SortVisual, self).__init__(**kwargs)
        self.Units = {}
        self.num = 10
        self.wait = 1/10
        self.sorting = False
        self.unitWidth = Window.width / self.num
        self.randomized(self.num, None)

    def randomized(self, num, e):
        self.num = num
        self.unitWidth = Window.width / self.num
        self.canvas.clear()
        if self.num == 10:
            self.wait = 1/100
        elif self.num == 100:
            self.wait = 1/10000
        elif self.num == 1000:
            self.wait = 0
        for i in range(0, self.num):
            randSize = random.randrange(10, Window.height * 0.9)
            with self.canvas:
                self.Units[i] = Rectangle(pos=(i * self.unitWidth, 0), size=(self.unitWidth, randSize))

    def update(self, *args):
        self.canvas.clear()
        for i in range(0, self.num):
            with self.canvas:
                self.Units[i] = Rectangle(pos=(i * self.unitWidth, 0), size=(self.unitWidth, self.Units[i].size[1]))
    
    def clock(self):
        Clock.schedule_interval(self.update, 0)

    def beginSort(self, chosen):
        if chosen == "quick sort":
            self.thread1 = threading.Thread(target=self.quickSort, args=(0, self.num - 1))
            self.thread2 = threading.Thread(target=self.clock)
            self.thread1.start()
            self.thread2.start()
        elif chosen == "bubble sort":
            self.thread1 = threading.Thread(target=self.bubbleSort)
            self.thread2 = threading.Thread(target=self.clock)
            self.thread1.start()
            self.thread2.start()

        elif chosen == "merge sort":
            self.thread1 = threading.Thread(target=self.mergeSort, args=(0, self.num - 1))
            self.thread2 = threading.Thread(target=self.clock)
            self.thread1.start()
            self.thread2.start()

    # quicksort
    def quickSort(self, low, high):
        self.sorting = True
        if low < high:
            pivot = self.Units[high].size[1]

            i = low - 1

            for j in range(low, high):
                if self.Units[j].size[1] < pivot:
                    i += 1
                    self.Units[i].size, self.Units[j].size = self.Units[j].size, self.Units[i].size
                time.sleep(self.wait)
            i += 1
            self.Units[i].size, self.Units[high].size = self.Units[high].size, self.Units[i].size
            self.quickSort(low, i - 1)
            self.quickSort(i + 1, high)
        if low == 0 and high == self.num - 1:
            self.sorting = False


    def bubbleSort(self):
        self.sorting = True
        for i in range(0, self.num - 1):
            for j in range(0, self.num - i - 1):
                if self.Units[j + 1].size[1] < self.Units[j].size[1]:
                    self.Units[j].size, self.Units[j + 1].size = self.Units[j + 1].size, self.Units[j].size
                time.sleep(self.wait)
        self.sorting = False


    def mergeSort(self, low, high):
        self.sorting = True
        if low < high:
            mid = int((low + high) / 2)
            self.mergeSort(low, mid)
            self.mergeSort(mid + 1, high)

            left = [0 for i in range(mid - low + 1)]
            right = [0 for j in range(high - mid)]
            for i in range(0, mid - low + 1):
                left[i] = self.Units[low + i].size[1]
            for j in range(0, high - mid):
                right[j] = self.Units[mid + j + 1].size[1]

            i = j = 0
            k = low
            while i < mid - low + 1 and j < high - mid:
                time.sleep(self.wait)
                if left[i] <= right[j]:
                    self.Units[k].size = (self.unitWidth, left[i])
                    i += 1
                else:
                    self.Units[k].size = (self.unitWidth, right[j])
                    j += 1
                k += 1
            
            while i < mid - low + 1:
                self.Units[k].size = (self.unitWidth, left[i])
                i += 1
                k += 1
            while j < high - mid:
                self.Units[k].size = (self.unitWidth, right[j])
                j += 1
                k += 1
        if low == 0 and high == self.num - 1:
            self.sorting = False


# put everything together
class MainScreen(Widget):
    start = ObjectProperty(None)
    ten = ObjectProperty(None)
    hund = ObjectProperty(None)
    thou = ObjectProperty(None)
    dropDown = ObjectProperty(None)
   
    def __init__(self):
        super(MainScreen, self).__init__()
        self.myApp = SortVisual()
        self.add_widget(self.myApp)
        self.chosen = ""
        self.ten.bind(on_press=partial(self.myApp.randomized, 10))
        self.hund.bind(on_press=partial(self.myApp.randomized, 100))
        self.thou.bind(on_press=partial(self.myApp.randomized, 1000))
        Clock.schedule_interval(self.switch, 0)
    
    def switch(self, *args):
        if self.myApp.sorting:
            self.start.disabled = True
            self.ten.disabled = True
            self.hund.disabled = True
            self.thou.disabled = True
            self.dropDown.disabled = True
        else:
            self.start.disabled = False
            self.ten.disabled = False
            self.hund.disabled = False
            self.thou.disabled = False
            self.dropDown.disabled = False
    
    def clicked(self, val):
        self.dropDown.text = val
        self.chosen = val

    def startSort(self):
        self.myApp.beginSort(self.chosen)
          

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    MainApp().run()