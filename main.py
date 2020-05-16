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
from data import Data
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
		#Selection
		self.year_sel=datetime.datetime.now().year
		self.month_sel=datetime.datetime.now().month
		self.day_sel=None
		self.hour_sel=None
		
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
		app=App.get_running_app()
		self.ids['btn_less'].text=str(datetime.datetime.now().year-1)
		self.ids['currentyear'].text=str(datetime.datetime.now().year)
		self.ids['btn_add'].text=str(datetime.datetime.now().year+1)
	
	def on_press_add(self):
		app.calendar.year_sel=app.calendar.year_sel+1
		self.ids['btn_less'].text=str(app.calendar.year_sel-1)
		self.ids['currentyear'].text=str(app.calendar.year_sel)
		self.ids['btn_add'].text=str(app.calendar.year_sel+1)
		self.update_date()

	def update_date(self):
		app=App.get_running_app()
		dates=app.calendar.dates
		dates.update_dates()
		
	def on_press_less(self):
		app.calendar.year_sel=app.calendar.year_sel-1
		self.ids['btn_less'].text=str(app.calendar.year_sel-1)
		self.ids['currentyear'].text=str(app.calendar.year_sel)
		self.ids['btn_add'].text=str(app.calendar.year_sel+1)
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
		list_minute=self.get_minute()
		with self.canvas:
			Color(.5,.6,.9,1)
			for i in list_minute:
				Ellipse(pos=(self.center_x-self.r*0.75, self.center_y-self.r*0.75),size=(self.r*1.5,self.r*1.5),angle_start=i*6,angle_end=(i+1)*6)

	def get_minute(self):
		find=0
		app=App.get_running_app()
		list_heure=app.calendar.dates.popup.content.list_heure_with_pass
		heure=app.calendar.hour_sel
		if heure.split(' ')[1]=='p.m':
			heure=int(heure.split(' ')[0])+12
		else:
			heure=int(heure.split(' ')[0])
		print(list_heure)
		min=0
		max=0
		for i in range(len(list_heure)):
			if (list_heure[i]==heure) :
				find=find+1
				if i!=len(list_heure)-1:
					if (list_heure[i+1]==heure+1):
						max=1
				if i!=0:
					if (list_heure[i-1]==heure-1):
						min=1
				
		if find==0:
			return []
		if ((max==1) and (min==1)):
			return list(range(0,60))
		app=App.get_running_app()
		year=app.calendar.year_sel
		month=app.calendar.month_sel
		day=app.calendar.day_sel
		if find==1:
			if min==1:
				for i in app.calendar.dates.data.list_date:
					if ((int(i[1][0:4])==int(year)) and (int(i[1][5:7])==int(month)) and (int(i[1][8:10])==int(day)) and (i[1][11:13]==str(heure).zfill(2))):
						if int(i[1][14:16])==0:
							return list(range(0,1))
						else:
							return list(range(0,int(i[1][14:16])))
				return list(range(0,60))
			elif max==1:
				for i in app.calendar.dates.data.list_date:
					if ((int(i[0][0:4])==int(year)) and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(day)) and (i[0][11:13]==str(heure).zfill(2))):
						return list(range(int(i[0][14:16]),60))
				return list(range(0,60))
			else:
				for i in app.calendar.dates.data.list_date:
					if ((int(i[0][0:4])==int(year)) and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(day)) and (i[0][11:13]==str(heure).zfill(2))):
						return list(range(int(i[0][14:16]),int(i[1][14:16])))
		else:
			interval=[]
			for i in app.calendar.dates.data.list_date:
				if ((int(i[0][0:4])==int(year)) and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(day)) and (i[0][11:13]==str(heure).zfill(2))):
					if ((int(i[0][0:4])==int(year)) and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(day)) and (i[1][11:13]==str(heure).zfill(2))):
						interval=interval+list(range(int(i[0][14:16]),int(i[1][14:16])))
					else:
						interval=interval+list(range(int(i[0][14:16]),60))
				elif ((int(i[0][0:4])==int(year)) and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(day)) and (i[1][11:13]==str(heure).zfill(2))):
					interval=interval+list(range(0,int(i[1][14:16])))
			return interval

#------------------------------------------------------------------------------------------------#

# class for Minutes.kv file
class Minutes(BoxLayout):   	
	def __init__(self,list_heure,**kwargs):
		super().__init__(**kwargs)
		box_infos_pass=BoxLayout(size_hint=(0.5,1),orientation = 'vertical')
		box_infos_pass.add_widget(MyClockWidget())
		self.add_widget(box_infos_pass)


# ------------------------------------------------------------------------------------------------#


# class for Hours in Dates
class Hours(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.size_hint=(0.9,0.9)
		app=App.get_running_app()
		# Layout arrangementw
		self.orientation = 'vertical'
		# Elevators information
		box_entete=BoxLayout(size_hint=(0.9,0.2),orientation = 'vertical')
		box_content=BoxLayout(size_hint=(0.9,0.8),pos_hint={'x': .05, 'y': 0.0},orientation = 'vertical')
		box_am=BoxLayout(size_hint=(0.9,1))
		box_pm=BoxLayout(size_hint=(0.9,1))
		self.list_heure_with_pass=self.get_hour()
		for i in range(12):
			add_am=0
			add_pm=0
			if i in self.list_heure_with_pass:
					box_am.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" a.m",color=(0,0,0,1),background_color=(1,0,0,1)))
					add_am=1
			if i+12 in self.list_heure_with_pass:
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


	def get_hour(self):
		find=0
		app=App.get_running_app()
		year=app.calendar.year_sel
		month=app.calendar.month_sel
		jour=app.calendar.day_sel
		for i in app.calendar.dates.list_jour_with_pass:
			if int(i)==int(jour):
				find=1
				break
		if find==0:
			return []
		interval=[]
		for i in app.calendar.dates.data.list_date:
			min=0
			max=24
			if ((int(i[0][0:4])==int(year))and (int(i[0][5:7])==int(month)) and (int(i[0][8:10])==int(jour))):
				min=int(i[0][11:13])
			if ((int(i[1][0:4])==int(year))and (int(i[1][5:7])==int(month)) and (int(i[1][8:10])==int(jour))):
				max=int(i[1][11:13])
			if ((min!=0) or (max!=24)):
				interval=interval+list(range(min, max+1))
		if len(interval)==0:
			return list(range(min, max))
		else:
			return interval
			
		
	def on_press(self,event):
		app=App.get_running_app()
		app.calendar.hour_sel=event.text
		self.popup = Popup(title='Detail of hour du '+str(app.calendar.year_sel)+'-'+str(app.calendar.month_sel)+'-'+str(app.calendar.day_sel)+' : '+str(app.calendar.hour_sel),title_color=(0,0,0,1),
		content = Minutes(self.list_heure_with_pass),
		size_hint=(0.7,0.7),background='background.png')
		self.popup.open() 



# ------------------------------------------------------------------------------------------------#
# class for Days.kv file
class Days(GridLayout):   	
	def __init__(self,**kwargs):
		super().__init__(**kwargs)     

# ------------------------------------------------------------------------------------------------#

# class for dates.kv file
class Dates(GridLayout):                
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.cols = 7
		self.data=Data()
		# Update dates paddle when choose different months
		#self.list_minute=None
		self.list_jour_with_pass=None
		self.update_dates()

	def update_dates(self):
		self.clear_widgets()
		app=App.get_running_app()
		try:
			year=app.calendar.year_sel
			month=app.calendar.month_sel
		except:
			print('init')
			year=datetime.datetime.now().year
			month=datetime.datetime.now().month
		c  = calendar.monthcalendar(year,month)
		# Look if passes is in current month
		self.list_jour_with_pass=self.get_date_in_current(year,month)
		# Show the best maintenance date if current month is clicked
		for i in c:
			for j in i:
				if j == 0:
					self.add_widget(Button(on_press = self.on_press,text = '{j}'.format(j=''),font_size='20sp',color=(0,0,0,1)))
				elif j in self.list_jour_with_pass:
					self.add_widget(Button(on_press = self.on_press,text = '{j}'.format(j=j),background_color=(1,0,0,1),font_size='20sp',color=(0,0,0,1)))
				else:
					self.add_widget(Button(on_press = self.on_press,text = '{j}'.format(j=j),font_size='20sp',color=(0,0,0,1)))

	def get_date_in_current(self,year,month):
		list_out=[]
		for couple in self.data.list_date:
			if ((couple[0][0:7]<=str(year)+'-'+str(month).zfill(2)) and (couple[1][0:7]>=str(year)+'-'+str(month).zfill(2))):
				list_out=list_out +(self.datetime_range(datetime.datetime.strptime(couple[0], '%Y-%m-%d %H:%M:%S'),datetime.datetime.strptime(couple[1], '%Y-%m-%d %H:%M:%S'),year,month))
		return list(set(list_out))

	def datetime_range(self,start,end,year,month):
		span = end - start
		if str(end.time()) < str(start.time()):
			span=span.days +1 
		else:
			span=span.days
		list_tmp=[]
		for i in range(span + 1):
			if (start + timedelta(days=i)).year==year and (start + timedelta(days=i)).month==month:
				list_tmp.append((start + timedelta(days=i)).day)
		return list_tmp


	def on_press(self,event):
		app=App.get_running_app()
		app.calendar.day_sel=int(event.text)
		self.popup = Popup(title='Detail of Day : '+str(app.calendar.year_sel)+'-'+str(app.calendar.month_sel).zfill(2)+'-'+str(app.calendar.day_sel).zfill(2),title_color=(0,0,0,1),
		content = Hours(),
		size_hint=(0.9,0.9),background='background.png')
		self.popup.open() 


# ------------------------------------------------------------------------------------------------#

# class for months.kv file
class Months(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# An pointer to current month button
		self.now_btn=Button()
		self.btn_color=(17/256,64/256,108/256,1)
		self.ids['btn_'+self.get_reverse_month(datetime.datetime.now().month).lower()].background_color=0.1,.5,.5,1


	def month_btn_press(self,instance):
		# Renew previous button
		self.now_btn.background_color=(17/256,64/256,108/256,1)
		instance.background_color=1,0,0,1
		#Update the month of the button
		app=App.get_running_app()
		app.calendar.month_sel=self.get_month(instance.text)
		self.now_btn=instance

	def month_btn_release(self,instance):
		instance.background_color=0.1,.5,.5,1
		self.update_date()
		pass

	def update_date(self):
		app=App.get_running_app()
		dates=app.calendar.dates
		dates.update_dates()


	def get_month(self,month_name):
		month_names=['Null','Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
		return month_names.index(month_name)

	def get_reverse_month(self,index):
		month_names=['Null','Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
		return month_names[index]




# ------------------------------------------------------------------------------------------------#


# mainApp class
class mainApp(App):
	time = StringProperty()
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.calendar=Calender()
		


	def update(self,*args):
		self.now_real=datetime.datetime.now()
		self.t=datetime.datetime(self.now_real.year,self.now_real.month,self.now_real.day,self.now_real.hour,self.now_real.minute,self.now_real.second)
		self.time=self.t.strftime('%Y-%m-%d %H:%M:%S')

	def build(self):
		self.title = "Remplace13"
		Clock.schedule_interval(self.update,1)       
		return self.calendar

if __name__ =='__main__':
	app = mainApp()
	app.run()
