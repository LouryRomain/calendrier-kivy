#coding:utf-8
# Thanks to:Kuldeep Singh, student at LNMIIT,Jaipur,India
# import Statements
import calendar
import time
import datetime
from kivy import resources
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.event import EventDispatcher
from kivy.uix.textinput import TextInput
from sklearn.externals import joblib
from kivy.uix.image import Image
import pandas as pd
import numpy as np
from model import Model
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.scrollview import ScrollView
from datetime import timedelta
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line,Ellipse
import math as math


color_shadow_blue=(.53125,.66796875,.7890625,1)
color_sky_blue=(1/256,158/256,213/256,1)
color_deep_blue=(17/256,64/256,108/256,1)
color_light_blue=(38/256,188/256,213/256,1)
# Builder used to load all the kivy files to be loaded in the main.py file
Builder.load_file('months.kv')
Builder.load_file('dates.kv')
Builder.load_file('status.kv')
Builder.load_file('days.kv')
Builder.load_file('calender.kv')
Builder.load_file('year.kv')
Builder.load_file('hours.kv')
Builder.load_file('clock.kv')

#------Kivy GUI Configuration--
# class for calender.kv file
class Calender(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# Integrating other classes
		self.year=Year()
		self.months=Months()
		self.days=Days()
		self.dates=Dates()
		self.status_=Status()
		# Adding layout
		self.layout_1=BoxLayout(size_hint=(1,.1))
		self.layout_1.add_widget(self.year)



		self.layout_2=BoxLayout()
		self.layout_3=BoxLayout(orientation='vertical')
		self.layout_3.add_widget(self.days)
		self.layout_3.add_widget(self.dates)
		self.layout_2.add_widget(self.months)
		self.layout_2.add_widget(self.layout_3)

		self.layout_4=BoxLayout(size_hint=(1,.1))
		self.layout_4.add_widget(self.status_)

		self.add_widget(self.layout_1)
		self.add_widget(self.layout_2)
		self.add_widget(self.layout_4)                


# class for status.kv file
class Status(BoxLayout,EventDispatcher):

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.orientation='horizontal'

		
		
#------------------------------------------------------------------------------------------------#

class Year(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# Displayed time is defined here
		self.year=datetime.datetime.now().year
		self.month=datetime.datetime.now().month
		self.ids['btn_less'].text=str(self.year-1)
		self.ids['currentyear'].text=str(self.year)
		self.ids['btn_add'].text=str(self.year+1)
	
	def on_press_add(self):
		self.year=self.year+1
		self.ids['btn_less'].text=str(self.year-1)
		self.ids['currentyear'].text=str(self.year)
		self.ids['btn_add'].text=str(self.year+1)
		self.update_date()

	def update_date(self):
		app=App.get_running_app()
		dates=app.calendar.dates
		dates.update_dates(app.calendar.year.year,app.calendar.months.month)
		
	def on_press_less(self):
		self.year=self.year-1
		self.ids['btn_less'].text=str(self.year-1)
		self.ids['currentyear'].text=str(self.year)
		self.ids['btn_add'].text=str(self.year+1)
		self.update_date()

		
		
		

#------------------------------------------------------------------------------------------------#


class MyClockWidget(FloatLayout):
	pass


class Ticks(Widget):
	def __init__(self, **kwargs):
		super(Ticks, self).__init__(**kwargs)
		self.bind(pos=self.update_clock)
		self.bind(size=self.update_clock)

	def update_clock(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(.5,.6,.9,1)
			app=App.get_running_app()
			for i in app.calendar.dates.list_minute:
				Ellipse(pos=(self.center_x-self.r*0.75, self.center_y-self.r*0.75),size=(self.r*1.5,self.r*1.5),angle_start=i*6,angle_end=(i+1)*6)


#------------------------------------------------------------------------------------------------#

# class for Minutes.kv file
class Minutes(BoxLayout):   	
	def __init__(self,text,list_heure,**kwargs):
		super().__init__(**kwargs)
		list_minute=self.get_minute(text,list_heure)
		App.get_running_app().calendar.dates.list_minute=list_minute
		box_infos_pass=BoxLayout(size_hint=(0.5,1),orientation = 'vertical')
		box_infos_pass.add_widget(MyClockWidget())
		self.add_widget(box_infos_pass)

	def get_minute(self,text,list_heure):
		find=0
		if text.split(' ')[1]=='p.m':
			heure=int(text.split(' ')[0])+12
		else:
			heure=int(text.split(' ')[0])
		min=0
		max=0
		for i in range(len(list_heure)):
			if (list_heure[i]==heure) :
				find=find+1
				if i!=len(list_heure)-1:
					if (list_heure[i+1]==list_heure[i]+1):
						max=1
				if i!=0:
					if (list_heure[i-1]==list_heure[i]-1):
						min=1
		if find==0:
			return []
		if ((max==1) and (min==1)):
			return list(range(0,60))
		app=App.get_running_app()
		if find==1:
			if min==1:
				for i in app.calendar.dates.model.list_date:
					if i[1][11:13]==str(heure).zfill(2):
						return list(range(0,int(i[1][14:16])))
			elif max==1:
				for i in app.calendar.dates.model.list_date:
					if i[0][11:13]==str(heure).zfill(2):
						return list(range(int(i[0][14:16]),60))
			else:
				for i in app.calendar.dates.model.list_date:
					if i[0][11:13]==str(heure).zfill(2):
						return list(range(int(i[0][14:16]),int(i[1][14:16])))
		else:
			interval=[]
			for i in app.calendar.dates.model.list_date:
				if i[0][11:13]==str(heure).zfill(2):
					if i[1][11:13]==str(heure).zfill(2):
						interval=interval+list(range(int(i[0][14:16]),int(i[1][14:16])))
					else:
						interval=interval+list(range(int(i[0][14:16]),60))
				elif i[1][11:13]==str(heure).zfill(2):
					interval=interval+list(range(0,int(i[1][14:16])))
			return interval
# ------------------------------------------------------------------------------------------------#

# class for Days.kv file
class Days(GridLayout):   	
	def __init__(self,**kwargs):
		super().__init__(**kwargs)     

# ------------------------------------------------------------------------------------------------#


# class for Hours in Dates
class Hours(BoxLayout):
	def __init__(self,jour,**kwargs):
		super().__init__(**kwargs)
		selfsize_hint=(0.9,0.9)
		# Layout arrangementw
		self.orientation = 'vertical'
		# Elevators information
		box_entete=BoxLayout(size_hint=(0.9,0.2),orientation = 'vertical')
		box_content=BoxLayout(size_hint=(0.9,0.8),pos_hint={'x': .05, 'y': 0.0},orientation = 'vertical')
		box_am=BoxLayout(size_hint=(0.9,1))
		box_pm=BoxLayout(size_hint=(0.9,1))
		self.list_heure=self.get_hour(jour)
		print(self.list_heure)
		for i in range(12):
			add_am=0
			add_pm=0
			if i in self.list_heure:
					box_am.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" a.m",color=(0,0,0,1),background_color=(1,0,0,1)))
					add_am=1
			if i+12 in self.list_heure:
					box_pm.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" p.m",color=(0,0,0,1),background_color=(1,0,0,1)))
					add_pm=1
			if add_am==0:
					box_am.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" a.m",color=(0,0,0,1)))
			if add_pm==0:
					box_pm.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" p.m",color=(0,0,0,1)))


		box_content.add_widget(box_am)
		box_content.add_widget(box_pm)
		self.add_widget(box_entete)
		self.add_widget(box_content)


	def get_hour(self,jour):
		find=0
		app=App.get_running_app()
		print(app.calendar.dates.list_jour_sel)
		for i in app.calendar.dates.list_jour_sel:
			if int(i)==int(jour):
				find=1
				break
		if find==0:
			return []
		interval=[]
		for i in app.calendar.dates.model.list_date:
			min=0
			max=24
			if int(i[0][8:10])==int(jour):
				min=int(i[0][11:13])
			if int(i[1][8:10])==int(jour):
				max=int(i[1][11:13])
			if ((min!=0) or (max!=24)):
				interval=interval+list(range(min, max+1))
		print(app.calendar.dates.list_jour_sel)
		if len(interval)==0:
			return list(range(min, max))
		else:
			return interval
			
	def on_dismiss(self, arg):
		# Do something on close of popup
		print('Popup dismiss')
		pass

	def on_release(self,event):
		print ("Hours OK Clicked!")
		
	def on_press(self,event):
		self.popup = Popup(title='Detail of hour : '+event.text,title_color=(0,0,0,1),
		content = Minutes(str(event.text),self.list_heure),
		size_hint=(0.7,0.7),background='background.png')
		self.popup.bind(on_dismiss = self.on_dismiss)
		self.popup.open() 



# ------------------------------------------------------------------------------------------------#
# class for dates.kv file
class Dates(GridLayout):                
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.cols = 7
		self.month=Months()
		self.year=Year()
		self.model=Model([['2020-05-13 10:50:00','2020-05-13 12:10:00'],['2020-05-13 12:20:00','2020-05-13 12:45:00'],['2020-05-13 16:00:00','2020-05-20 16:00:00'],['2020-05-25 16:00:00','2020-06-29 16:00:00'],['2021-05-25 16:36:00','2021-06-10 11:48:00']])
		# Update dates paddle when choose different months
		self.list_minute=[]
		self.update_dates(self.year.year,self.month.month)

	def update_dates(self,year,month):
		print('Update dates!')
		self.clear_widgets()
		c  = calendar.monthcalendar(year,month)
		# Look if passes is in current month
		self.list_jour_sel=self.get_date_in_current(year,month)
		# Show the best maintenance date if current month is clicked
		for i in c:
			for j in i:
				if j == 0:
					self.add_widget(Button(on_press = self.on_press,on_release=self.on_release,text = '{j}'.format(j=''),font_size='20sp',color=(0,0,0,1)))
				elif j in self.list_jour_sel:
					self.add_widget(Button(on_press = self.on_press,on_release=self.on_release,text = '{j}'.format(j=j),background_color=(1,0,0,1),font_size='20sp',color=(0,0,0,1)))
				else:
					self.add_widget(Button(on_press = self.on_press, on_release=self.on_release,text = '{j}'.format(j=j),font_size='20sp',color=(0,0,0,1)))

	def get_date_in_current(self,year,month):
		list_out=[]
		for couple in self.model.list_date:
			if ((couple[0][0:7]<=str(year)+'-'+str(month).zfill(2)) and (couple[1][0:7]>=str(year)+'-'+str(month).zfill(2))):
				list_out=list_out +(self.datetime_range(datetime.datetime.strptime(couple[0], '%Y-%m-%d %H:%M:%S'),datetime.datetime.strptime(couple[1], '%Y-%m-%d %H:%M:%S'),year,month))
		return list(set(list_out))

	def datetime_range(self,start,end,year,month):
		span = end - start
		list_tmp=[]
		for i in range(span.days + 1):
			if (start + timedelta(days=i)).year==year and (start + timedelta(days=i)).month==month:
				list_tmp.append((start + timedelta(days=i)).day)
		return list_tmp

	def on_dismiss(self, arg):
		# Do something on close of popup
		print('Popup dismiss')
		pass

	def get_month_and_year(self):
		app=App.get_running_app()
		return [app.calendar.year.year,app.calendar.months.month]
		
	def on_release(self,event):
		pass
		#event.background_color = 154/256,226/256,248/256,1
	
	def on_press(self,event):
		print ("date clicked :" + event.text)
		#event.background_color = 1,0,0,1
		self.popup = Popup(title='Detail of Day : '+str(self.get_month_and_year()[0])+'-'+str(self.get_month_and_year()[1]).zfill(2)+'-'+event.text.zfill(2),title_color=(0,0,0,1),
		content = Hours(str(event.text)),
		size_hint=(0.9,0.9),background='background.png')
		self.popup.bind(on_dismiss = self.on_dismiss)
		self.popup.open() 


# ------------------------------------------------------------------------------------------------#

# class for months.kv file
class Months(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# Displayed time is defined here
		self.now=datetime.datetime.now()
		self.month=self.now.month
		self.day=self.now.day
		# An pointer to current month button
		self.now_btn=Button()
		self.btn_color=(17/256,64/256,108/256,1)


	def month_btn_press(self,instance):
		# Renew previous button
		self.now_btn.background_color=(17/256,64/256,108/256,1)
		instance.background_color=1,0,0,1
		#Update the month of the button
		self.month=self.get_month(instance.text)
		self.now_btn=instance

	def month_btn_release(self,instance):
		instance.background_color=0.1,.5,.5,1
		self.update_date()
		pass

	def update_date(self):
		app=App.get_running_app()
		dates=app.calendar.dates
		dates.update_dates(app.calendar.year.year,self.month)


	def get_month(self,month_name):
		month_names=['Null','Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
		return month_names.index(month_name)




# ------------------------------------------------------------------------------------------------#


# mainApp class
class mainApp(App):
	time = StringProperty()
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.calendar=Calender()
		#self.model_=Model() # Place model into Dates()
		self.year=self.calendar.year.year
		self.month=self.calendar.months.month
		self.day=self.calendar.months.day


	def update(self,*args):
		self.now_real=datetime.datetime.now()
		self.t=datetime.datetime(self.year,self.month,self.day,self.now_real.hour,self.now_real.minute,self.now_real.second)
		self.time=self.t.strftime('%Y-%m-%d %H:%M:%S')

	def build(self):
		self.title = "Remplace13"
		Clock.schedule_interval(self.update,1)       
		return self.calendar

if __name__ =='__main__':
	app = mainApp()
	app.run()
