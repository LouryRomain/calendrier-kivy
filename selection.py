
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random
from math import sqrt
from pytz import UTC
from datetime import datetime, timedelta
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from tzlocal import get_localzone
from data import Data
	
Builder.load_string('''
<ResaLabelLive>:
	canvas.before:
		Color:
			rgba:0.8, 0.5, 0.5,0.3 # your color here
		Rectangle:
			pos: self.pos
			size: self.size
''')

class ResaLabelLive(Label):
	pass

class ResaButtonLive(ToggleButton):
	def __init__(self,text_info, **kw):
		super().__init__(**kw)
		self.label=Label(text=text_info,color=(0,0,0,1))
		self.active=False
		self.background_color=(0.8,0.5,0.5,1)

	def on_press(self):
		app=App.get_running_app()
		if not self.active:
			app.calendar.dates.boxinfo.add_widget(self.label)
			self.active=True
		else:
			self.active=False
			app.calendar.dates.boxinfo.remove_widget(self.label)
	
class RegistrationButton(Button):
	def on_press(self):
		app=App.get_running_app()
		start_resa=app.calendar.dates.registerbutton.boxregister.start_entry.text
		end_resa=app.calendar.dates.registerbutton.boxregister.end_entry.text
		try:
			start_resa_dt=get_localzone().localize(datetime.strptime(start_resa, '%Y-%m-%d %H:%M:%S'))
			end_resa_dt=get_localzone().localize(datetime.strptime(end_resa, '%Y-%m-%d %H:%M:%S'))
		except:
			self.popup=Popup(title='Error',title_color=(1,0,0,1),
			content = Label(text='Error date format',color=(0,0,0,1)),
			size_hint=(0.4,0.4),pos_hint={"x":0.3,"y":0.3},background='background.png')
			self.popup.open()
			return
		app.calendar.dates.registerbutton.boxregister.enable_selection(start_resa_dt,end_resa_dt,0,app.calendar.dates.timeline.df_reservation)
		if app.calendar.dates.registerbutton.boxregister.enable==1:
			app.calendar.dates.timeline.resatime.append(app.calendar.dates.timeline.add_button(app.calendar.dates.timeline.border_inf,
							app.calendar.dates.timeline.border_sup,
							start_resa_dt,
							end_resa_dt,
							app.calendar.dates.timeline.ref_second,
							app.calendar.dates.boxresa,
							ResaLabelLive,
							ResaButtonLive))
			file=open('reservation.csv','a+')
			file.write(start_resa+","+end_resa+",test1,"+str(datetime.now())+','+app.calendar.dates.registerbutton.boxregister.name_entry.text+'\n')
			file.close()
			app.calendar.dates.data=Data()
			app.calendar.dates.registerbutton.boxregister.popup.dismiss()
		else:
			self.popup=Popup(title='Error',title_color=(1,0,0,1),
			content = Label(text='Overlapping',color=(0,0,0,1)),
			size_hint=(0.4,0.4),pos_hint={"x":0.3,"y":0.3},background='background.png')
			self.popup.open()
class SelectionnerInterval(FloatLayout):
	def __init__(self,**kw):
		super(SelectionnerInterval, self).__init__(**kw)
		self.enable=1



	def enable_selection(self,touchy,starttouch,pos=1,list_resa=None):
		if list_resa==None:
			list_resa=self.timeline.resatime
			print(self.timeline.resatime)
		else:
			list_resa=[[get_localzone().localize(datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S')),get_localzone().localize(datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S'))] for i in list_resa]
		if pos==1:
			time_touchy=self.time_t0+timedelta(seconds=int(((touchy-self.pos_t0)/self.pos_interval)*self.time_interval))
			time_start=self.time_t0+timedelta(seconds=int(((starttouch-self.pos_t0)/self.pos_interval)*self.time_interval))
		else:
			time_touchy=touchy
			time_start=starttouch
		self.enable=1
		try:
			for i in list_resa:
				if i !=None:
					if (((time_touchy <i[0])and (time_start <i[0]))
						or ((time_touchy >i[1]) and (time_start >i[1]))):
						self.enable=1
					else:
						self.enable=0
						break
		except:
			self.enable=1

	def on_touch_down(self, touch):
		win = self.get_parent_window()
		self.timeline=App.get_running_app().calendar.dates.timeline
		self.pos_t0=self.timeline.pos_of_time(self.timeline.get_time_0())
		self.pos_t1=self.timeline.pos_of_time(self.timeline.get_time_1())
		self.time_t0=self.timeline.get_time_0()
		self.time_t1=self.timeline.get_time_1()
		self.time_interval=(self.time_t1-self.time_t0).total_seconds()
		self.pos_interval=(self.pos_t1-self.pos_t0)
		ud = touch.ud
		ud['group'] = g = str(touch.uid)
		ud['color'] = random()
		self.enable_selection(touch.y,touch.y)
		if self.enable==1:
			with self.canvas:
				Color(0, 1, 0, .5, group=g)
				ud['lines']=Rectangle(pos=(win.width*0.07, touch.y), size=(win.width*0.45, 1), group=g)
			self.y_start=touch.y
			touch.grab(self)
			return True
		else:
			return False

	def on_touch_move(self, touch):
		win = self.get_parent_window()
		if touch.grab_current is not self:
			return
		self.enable_selection(touch.y,self.y_start)
		if self.enable==1:
			ud = touch.ud
			if ((touch.y>self.pos_t0) and (touch.y<self.pos_t1)):
				if self.y_start-touch.y>0:
					ud['lines'].pos = win.width*0.07, touch.y
					ud['lines'].size = win.width*0.45, abs(self.y_start-touch.y)
				else:
					ud['lines'].pos = win.width*0.07, self.y_start
					ud['lines'].size = win.width*0.45, abs(self.y_start-touch.y)
			elif (touch.y>=self.timeline.pos_of_time(self.timeline.get_time_1())):
				ud['lines'].size = win.width*0.45, abs(self.y_start-self.pos_t1)


	def on_touch_up(self, touch):
		if touch.grab_current is not self:
			return
		touch.ungrab(self)
		ud = touch.ud
		app=App.get_running_app()
		app.calendar.dates.registerbutton.on_press()
		app.calendar.dates.registerbutton.state='normal'
		self.canvas.remove_group(ud['group'])
		start_time=self.time_t0+timedelta(seconds=int(((ud['lines'].pos[1]-self.pos_t0)/self.pos_interval)*self.time_interval))
		end_time=start_time+timedelta(seconds=int((ud['lines'].size[1]/self.pos_interval)*self.time_interval))
		box=FloatLayout()
		start_label=Label(pos_hint={'x':0.15,'y':0.80},size_hint=(0.2, 0.07),text='Starting Date :',color=(0,0,0,1))
		end_label=Label(pos_hint={'x':0.15,'y':0.60},size_hint=(0.2, 0.07),text='End Date :',color=(0,0,0,1))
		self.start_entry=TextInput(pos_hint={'x':0.45,'y':0.75},size_hint=(0.45, 0.14),text=str(start_time.strftime("%Y-%m-%d %H:%M:"+'00')))
		self.end_entry=TextInput(pos_hint={'x':0.45,'y':0.55},size_hint=(0.45, 0.14),text=str(end_time.strftime("%Y-%m-%d %H:%M:"+'00')))
		name_label=Label(pos_hint={'x':0.15,'y':0.35},size_hint=(0.2, 0.07),text='Name :',color=(0,0,0,1))
		self.name_entry=TextInput(pos_hint={'x':0.45,'y':0.30},size_hint=(0.43, 0.14))
		button=RegistrationButton(text='OK',pos_hint={'x':0.2,'y':0.1},size_hint=(0.2, 0.1))

		self.buttonCancel=Button(text='Cancel',pos_hint={'x':0.6,'y':0.1},size_hint=(0.2, 0.1))
		box.add_widget(self.end_entry)
		box.add_widget(self.start_entry)
		box.add_widget(end_label)
		box.add_widget(start_label)
		box.add_widget(name_label)
		box.add_widget(self.name_entry)
		box.add_widget(button)
		box.add_widget(self.buttonCancel)
		self.popup=Popup(title='Register',title_color=(0,0,0,1),
		content = box,
		size_hint=(0.45,0.45),pos_hint={"x":0.07,"y":0.25},background='background.png')
		self.buttonCancel.bind(on_press=self.popup.dismiss)
		self.popup.open()



class TouchtracerApp(App):
	title = 'Touchtracer'
	icon = 'icon.png'

	def build(self):
		return SelectionnerInterval()

	def on_pause(self):
		return True


if __name__ == '__main__':
	TouchtracerApp().run()