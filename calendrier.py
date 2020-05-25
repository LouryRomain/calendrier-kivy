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
from kivy.uix.togglebutton import ToggleButton
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
import timeline
from kivy.core.window import Window
from tzlocal import get_localzone
import selection


def local_now(date):
	return get_localzone().localize(date)  

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
class RegisterButton(ToggleButton):
	def __init__(self, **kw):
		super().__init__(**kw)
		self.active=False
		self.background_color=(0.5,0.8,0,1)

	def on_press(self):
		app=App.get_running_app()
		if not self.active:
			self.boxregister=selection.SelectionnerInterval(size_hint=(0.0001,1))
			app.calendar.dates.box.add_widget(self.boxregister)
			self.active=True
		else:
			self.active=False
			app.calendar.dates.box.remove_widget(self.boxregister)
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
		app=App.get_running_app()
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
		app=App.get_running_app()
		app.calendar.year_sel=app.calendar.year_sel-1
		self.ids['btn_less'].text=str(app.calendar.year_sel-1)
		self.ids['currentyear'].text=str(app.calendar.year_sel)
		self.ids['btn_add'].text=str(app.calendar.year_sel+1)
		self.update_date()

		
		
		

#------------------------------------------------------------------------------------------------#





#------------------------------------------------------------------------------------------------#
"""
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
			Color(0.5,0.5,0.8,1)
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
	def __init__(self,status,**kwargs):
		super().__init__(**kwargs)
		box_infos_pass=BoxLayout(size_hint=(0.5,1),orientation = 'vertical')
		box_infos_pass.add_widget(MyClockWidget())
		box_infos_pass.add_widget(ColoredLabel(text="Detail per minute",size_hint=(0.6,0.1),pos_hint={"x":0.2,"y":0.0},color=(1,1,1,1)))
		self.add_widget(box_infos_pass)
		if status=='Free':
			box_get_hour=FloatLayout(size_hint=(0.5,1))
			box_get_hour.add_widget(Label(text='Your name:',size_hint=(0.3,0.07),pos_hint={"x":0.1,"y":0.6},color=(0,0,0,1)))
			self.entry=TextInput(size_hint=(0.5,0.1),pos_hint={"x":0.45,"y":0.585})
			box_get_hour.add_widget(self.entry)
			box_get_hour.add_widget(Button(on_press=self.on_press,text='Register',size_hint=(0.4,0.2),pos_hint={"x":0.3,"y":0.2},background_color=(0.3,0.3,0.3,1)))
			self.add_widget(box_get_hour)
			
	def on_press(self,event):
		app=App.get_running_app()
		year=app.calendar.year_sel
		month=app.calendar.month_sel
		day=app.calendar.day_sel
		hour=app.calendar.hour_sel
		file=open('reservation.csv','a+')
		file.write(str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+","+str(hour)+",test1,"+str(datetime.datetime.now())+','+self.entry.text+'\n')
		file.close()
		app.calendar.dates.popup.content.popup.dismiss()
		app.calendar.dates.popup.dismiss()
		app.calendar.dates.data=Data()
		

# ------------------------------------------------------------------------------------------------#
class ColoredLabel(Label):
	pass
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
		box_entete=BoxLayout(size_hint=(1,0.1),orientation = 'vertical')
		box_entete.add_widget(Label(text="Choose your reservation's hour",font_size=25,color=(0,0,0,1)))
		box_content=BoxLayout(size_hint=(1,0.8),orientation = 'vertical')
		box_legend_am=BoxLayout(size_hint=(1,0.07))
		box_am=BoxLayout(size_hint=(1,0.4))
		box_legend_pm=BoxLayout(size_hint=(1,0.07))
		box_pm=BoxLayout(size_hint=(1,0.4))
		year=str(app.calendar.year_sel).zfill(4)
		month=str(app.calendar.month_sel).zfill(2)
		day=str(app.calendar.day_sel).zfill(2)
		self.list_heure_with_pass=self.get_hour()
		df_reservation=app.calendar.dates.data.df_reservation
		list_reservation_am=list(df_reservation[((df_reservation['date']==year+'-'+month+'-'+day) & (df_reservation.heure.str.contains('a.m')))]['heure'].apply(lambda x:int(x.split(' ')[0])))
		list_reservation_pm=list(df_reservation[((df_reservation['date']==year+'-'+month+'-'+day) & (df_reservation.heure.str.contains('p.m')))]['heure'].apply(lambda x:int(x.split(' ')[0])))
		for i in range(12):
			box_legend_am.add_widget(ColoredLabel(text=str(i)+" a.m",color=(1,1,1,1)))
			box_legend_pm.add_widget(ColoredLabel(text=str(i)+" p.m",color=(1,1,1,1)))
			if i in list_reservation_am:
					box_am.add_widget(Button(id=str(i)+" a.m",on_press=self.on_press,size_hint=(1/12,0.9),text="Closed",color=(0,0,0,1),background_color=(1,0,0,1)))
			elif i in self.list_heure_with_pass:
					box_am.add_widget(Button(id=str(i)+" a.m",on_press=self.on_press,size_hint=(1/12,0.9),text="Free",color=(0,0,0,1),background_color=(0.5,0.8,0,1)))
			else:
					box_am.add_widget(Button(id=str(i)+" a.m",on_press=self.on_press,size_hint=(1/12,0.9),color=(0,0,0,1)))

			if i in list_reservation_pm:
					box_pm.add_widget(Button(id=str(i)+" p.m",on_press=self.on_press,size_hint=(1/12,0.9),text="Closed",color=(0,0,0,1),background_color=(1,0,0,1)))
			elif i+12 in self.list_heure_with_pass:
					box_pm.add_widget(Button(id=str(i)+" p.m",on_press=self.on_press,size_hint=(1/12,0.9),text="Free",color=(0,0,0,1),background_color=(0.5,0.8,0,1)))
			else:
					box_pm.add_widget(Button(id=str(i)+" p.m",on_press=self.on_press,size_hint=(1/12,0.9),color=(0,0,0,1)))

		box_content.add_widget(box_legend_am)
		box_content.add_widget(box_am)
		box_content.add_widget(BoxLayout(size_hint=(1,0.05)))
		box_content.add_widget(box_legend_pm)
		box_content.add_widget(box_pm)
		box_content.add_widget(BoxLayout(size_hint=(1,0.05)))
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
		app.calendar.hour_sel=event.id
		self.popup = Popup(title='Detail of hour du '+str(app.calendar.year_sel)+'-'+str(app.calendar.month_sel).zfill(2)+'-'+str(app.calendar.day_sel).zfill(2)+' : '+str(app.calendar.hour_sel),title_color=(0,0,0,1),
		content = Minutes(event.text),
		size_hint=(0.7,0.7),background='background.png')
		self.popup.open() 


"""
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
					self.add_widget(Button(on_press = self.on_press,text = '{j}'.format(j=j),background_color=(0.5,0.8,0,1),font_size='20sp',color=(0,0,0,1)))
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
		self.popup_content=BoxLayout(orientation='vertical')

		self.box=BoxLayout(orientation='horizontal')
		self.boxentete=BoxLayout(size_hint=(1,0.1),orientation='horizontal')
		self.boxentete.add_widget(Label(text='Timeline',size_hint=(0.22,1),color=(0,0,0,1)))
		self.boxentete.add_widget(Label(text='Passes',size_hint=(0.17,1),color=(0,0,0,1)))
		self.boxentete.add_widget(Label(text='Reservations',size_hint=(0.15,1),color=(0,0,0,1)))
		self.boxentete.add_widget(Label(text='Information',size_hint=(0.4,1),color=(0,0,0,1)))
		self.registerbutton=RegisterButton(text='Register',size_hint=(0.1,0.7),pos_hint={"x":0,"y":0.15},color=(0,0,0,1))
		self.boxentete.add_widget(self.registerbutton)
		self.boxinfo=BoxLayout(size_hint=(0.5,1),orientation='vertical')
		self.boxbtn=FloatLayout(size_hint=(0.15,1))
		self.boxresa=FloatLayout(size_hint=(0.15,1))
		self.timeline = timeline.Timeline(size_hint=(0.2,1),
					backward=False,
					orientation='vertical',
					ticks=(timeline.selected_time_ticks()),
					line_width =1,
					line_offset=Window.size[1]*0.2*0.5
					)


		self.box.add_widget(self.timeline)
		self.box.add_widget(self.boxbtn)
		self.box.add_widget(self.boxresa)
		self.box.add_widget(self.boxinfo)
		self.popup_content.add_widget(self.boxentete)
		self.popup_content.add_widget(self.box)
		now=local_now(datetime.datetime(app.calendar.year_sel,app.calendar.month_sel,app.calendar.day_sel))
		self.timeline.center_on_timeframe(now ,now+ datetime.timedelta(days=1))
		self.popup = Popup(title='Detail of Day : '+str(app.calendar.year_sel)+'-'+str(app.calendar.month_sel).zfill(2)+'-'+str(app.calendar.day_sel).zfill(2),title_color=(0,0,0,1),
		content = self.popup_content,
		size_hint=(0.9,0.9),background='background.png')
		self.popup.open() 


# ------------------------------------------------------------------------------------------------#

# class for months.kv file
class Months(BoxLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		# An pointer to current month button
		self.now_btn=self.ids['btn_'+self.get_reverse_month(datetime.datetime.now().month).lower()]
		self.btn_color=(17/256,64/256,108/256,1)
		self.ids['btn_'+self.get_reverse_month(datetime.datetime.now().month).lower()].background_color=(0.1,.5,.5,1)


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
