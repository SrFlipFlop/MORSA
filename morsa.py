#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget

class Morsa(Widget):
    pass

class MorsaApp(App):
    def build(self):
        return Morsa()

if __name__ == '__main__':
    MorsaApp().run()
