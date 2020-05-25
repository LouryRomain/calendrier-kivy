
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random
from math import sqrt


class SelectionnerInterval(FloatLayout):
	def __init__(self,**kw):
		super(SelectionnerInterval, self).__init__(**kw)
		

	def on_touch_down(self, touch):
		win = self.get_parent_window()
		ud = touch.ud
		ud['group'] = g = str(touch.uid)
		ud['color'] = random()
		with self.canvas:
			Color(0, 1, 0, .5, group=g)
			ud['lines']=Rectangle(pos=(win.width*0.07, touch.y), size=(win.width*0.45, 1), group=g)
		touch.grab(self)
		self.y_start=touch.y
		return True

	def on_touch_move(self, touch):
		win = self.get_parent_window()
		if touch.grab_current is not self:
			return
		ud = touch.ud
		if self.y_start-touch.y>0:
			ud['lines'].pos = win.width*0.07, touch.y
			ud['lines'].size = win.width*0.45, abs(self.y_start-touch.y)
		else:
			ud['lines'].pos = win.width*0.07, self.y_start
			ud['lines'].size = win.width*0.45, abs(self.y_start-touch.y)


	def on_touch_up(self, touch):
		self.y_end=touch.y
		if touch.grab_current is not self:
			return
		touch.ungrab(self)
		ud = touch.ud
		app=App.get_running_app()
		app.calendar.dates.registerbutton.on_press()
		app.calendar.dates.registerbutton.state='normal'
		self.canvas.remove_group(ud['group'])



class TouchtracerApp(App):
	title = 'Touchtracer'
	icon = 'icon.png'

	def build(self):
		return SelectionnerInterval()

	def on_pause(self):
		return True


if __name__ == '__main__':
	TouchtracerApp().run()