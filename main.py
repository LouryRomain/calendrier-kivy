#coding:utf-8
# Thanks to:Kuldeep Singh, student at LNMIIT,Jaipur,India
# import Statements
import calendar
import time
import datetime
from kivy import resources
from kivy.app import App
from kivy.lang import Builder
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
Builder.load_file('reminder.kv')


#------Kivy GUI Configuration--
# class for calender.kv file
class Calender(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# Integrating other classes
		self.year=Year()
		self.months_=Months()
		self.days_=Days()
		self.dates_=Dates()
		self.status_=Status()
		# Adding layout
		self.layout_1=BoxLayout(size_hint=(1,.1))
		self.layout_1.add_widget(self.year)



		self.layout_2=BoxLayout()
		self.layout_3=BoxLayout(orientation='vertical')
		self.layout_3.add_widget(self.days_)
		self.layout_3.add_widget(self.dates_)
		self.layout_2.add_widget(self.months_)
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
		dates=app.calendar_.dates_
		dates.update_dates(app.calendar_.year.year,app.calendar_.months_.month)
		
	def on_press_less(self):
		self.year=self.year-1
		self.ids['btn_less'].text=str(self.year-1)
		self.ids['currentyear'].text=str(self.year)
		self.ids['btn_add'].text=str(self.year+1)
		self.update_date()




#------------------------------------------------------------------------------------------------#


# class for Days.kv file
class Days(GridLayout):   	
	def __init__(self,**kwargs):
		super().__init__(**kwargs)     

# ------------------------------------------------------------------------------------------------#


# class for Reminder in Dates
class Reminder(BoxLayout):
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
		list_heure=self.get_hour(jour)
		print(list_heure)
		for i in range(12):
			add_am=0
			add_pm=0
			if i in list_heure:
					box_am.add_widget(Button(on_press=self.on_press,size_hint=(1/12,0.9),text=str(i)+" a.m",color=(0,0,0,1),background_color=(1,0,0,1)))
					add_am=1
			if i+12 in list_heure:
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
		print(app.calendar_.dates_.list_jour_sel)
		for i in app.calendar_.dates_.list_jour_sel:
			if int(i)==int(jour):
				find=1
				break
		if find==0:
			return []
		interval=[]
		for i in app.calendar_.dates_.model.list_date:
			min=0
			max=24
			if int(i[0][8:10])==int(jour):
				min=int(i[0][11:13])
			if int(i[1][8:10])==int(jour):
				max=int(i[1][11:13])
			if ((min!=0) or (max!=24)):
				interval=interval+list(range(min, max+1))
		print(app.calendar_.dates_.list_jour_sel)
		if len(interval)==0:
			return list(range(min, max))
		else:
			return interval


		#for in app.dates_.model:
			
	
	def on_release(self,event):
		print ("Reminder OK Clicked!")
		
	def on_press(self,event):
		print('ok')



# ------------------------------------------------------------------------------------------------#
# class for dates.kv file
class Dates(GridLayout):                
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.cols = 7
		self.month=Months()
		self.year=Year()
		self.model=Model([['2020-05-13 10:00:00','2020-05-13 12:00:00'],['2020-05-13 16:00:00','2020-05-20 16:00:00'],['2020-05-25 16:00:00','2020-06-29 16:00:00']])
		# Update dates paddle when choose different months
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
		return [app.calendar_.year.year,app.calendar_.months_.month]
		
	def on_release(self,event):
		pass
		#event.background_color = 154/256,226/256,248/256,1
	
	def on_press(self,event):
		print ("date clicked :" + event.text)
		#event.background_color = 1,0,0,1
		self.popup = Popup(title='Detail of Day : '+str(self.get_month_and_year()[0])+'-'+str(self.get_month_and_year()[1]).zfill(2)+'-'+event.text.zfill(2),title_color=(0,0,0,1),
		content = Reminder(str(event.text)),
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
		dates=app.calendar_.dates_
		dates.update_dates(app.calendar_.year.year,self.month)


	def get_month(self,month_name):
		month_names=['Null','Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec']
		return month_names.index(month_name)




# ------------------------------------------------------------------------------------------------#


# mainApp class
class mainApp(App):
	time = StringProperty()
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.calendar_=Calender()
		#self.model_=Model() # Place model into Dates()
		self.year=self.calendar_.year.year
		self.month=self.calendar_.months_.month
		self.day=self.calendar_.months_.day


	def update(self,*args):
		self.now_real=datetime.datetime.now()
		self.t=datetime.datetime(self.year,self.month,self.day,self.now_real.hour,self.now_real.minute,self.now_real.second)
		self.time=self.t.strftime('%Y-%m-%d %H:%M:%S')

	def build(self):
		self.title = "Remplace13"
		Clock.schedule_interval(self.update,1)       
		return self.calendar_

if __name__ =='__main__':
	app = mainApp()
	app.run()
