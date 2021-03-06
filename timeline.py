import numpy as np
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from bisect import bisect, bisect_left
from datetime import datetime, timedelta
from decimal import DivisionByZero
from itertools import chain
from kivy.base import runTouchApp
from kivy.core.text import Label as CoreLabel
from kivy.event import EventDispatcher
from kivy.garden.tickline import TickLabeller, Tick, Tickline
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, OptionProperty, \
	DictProperty, ObjectProperty, BoundedNumericProperty, BooleanProperty, \
	AliasProperty
from kivy.uix.accordion import AccordionItem, Accordion
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from math import ceil, floor
from numbers import Number
from pytz import UTC

from tzlocal import get_localzone

def local_now():
	return get_localzone().localize(datetime.now())	

Builder.load_string('''
<AutoSizeLabel>:
	size: self.texture_size
	size_hint: None, None
	
<PassLabel>:
	canvas.before:
		Color:
			rgba:0, 0.5, 0,0.3 # your color here
		Rectangle:
			pos: self.pos
			size: self.size

<ResaLabel>:
	canvas.before:
		Color:
			rgba:0.8, 0.5, 0,0.3 # your color here
		Rectangle:
			pos: self.pos
			size: self.size

''')
class AutoSizeLabel(Label):
	pass



class PassButton(ToggleButton):
	def __init__(self,text_info, **kw):
		super().__init__(**kw)
		self.label=Label(text=text_info,color=(0,0,0,1))
		self.active=False
		self.background_color=(0.5,0.8,0,1)

	def on_press(self):
		app=App.get_running_app()
		if not self.active:
			app.calendar.dates.boxinfo.add_widget(self.label)
			self.active=True
		else:
			self.active=False
			app.calendar.dates.boxinfo.remove_widget(self.label)

class ResaButton(ToggleButton):
	def __init__(self,text_info, **kw):
		super().__init__(**kw)
		self.label=Label(text=text_info,color=(0,0,0,1))
		self.active=False
		self.background_color=(0.8,0.5,0,1)

	def on_press(self):
		app=App.get_running_app()
		if not self.active:
			app.calendar.dates.boxinfo.add_widget(self.label)
			self.active=True
		else:
			self.active=False
			app.calendar.dates.boxinfo.remove_widget(self.label)

class PassLabel(Label):
	pass

class ResaLabel(Label):
	pass


class TimeLabeller(TickLabeller):

	date_halign = OptionProperty('right', options=['left', 'right'])   
	'''specifies whether the date labels are on the left or right side of
	the :class:`Timeline` when the timeline is vertical. Has no effect when
	the timeline is horizontal.'''
	
	date_valign = OptionProperty('bottom', options=['top', 'bottom'])
	'''specifies whether the date labels are on top or bottom of
	the :class:`Timeline` when the timeline is horizontal. Has no effect when
	the timeline is vertical.'''

	time_halign = OptionProperty('right', options=['left', 'right'])   
	'''specifies whether the time labels are on the left or right side of
	the :class:`Timeline` when the timeline is vertical. Has no effect when
	the timeline is horizontal.'''

	time_valign = OptionProperty('bottom', options=['top', 'bottom'])
	'''specifies whether the time labels are on top or bottom of
	the :class:`Timeline` when the timeline is horizontal. Has no effect when
	the timeline is vertical.'''

	date_dist_from_edge = NumericProperty('55dp')
	'''distance of the date labels from the edge of the :class:`Timeline`.'''
	
	time_dist_from_edge = NumericProperty('22dp')
	'''distance of the time labels from the edge of the :class:`Timeline`.'''

	date_font_size = NumericProperty('12sp')
	'''font size of the date labels.'''

	time_font_size = NumericProperty('7sp')
	'''font size of the time labels.'''
	
	def __init__(self, tickline, **kw):
		super(TimeLabeller, self).__init__(tickline, **kw)
		self.labels = []
		self.seconds_registrar = {}
		self.have_time = False
		self.instructions = {}
		
	def re_init(self, *args):
		self.labels = []
		self.seconds_registrar = {}
		self.have_time = False
		super(TimeLabeller, self).re_init(*args)
		
	def register(self, tick, tick_index, tick_info):
		assert isinstance(tick_index, Number)
		tick_sc = tick.scale(self.tickline.scale)
		if tick_sc < tick.min_label_space:
			return
		seconds = tick.to_seconds(tick_index)
		if self.seconds_registrar.get(seconds, 0) < tick_sc:
			self.have_time |= tick.mode != 'day'
			self.registrar.setdefault(tick, {})[tick_index] = tick_info
			self.seconds_registrar[seconds] = tick_sc
			
	def _get_texture_pos(self, tick, index, succinct=True, which='time',
						 texture=None):
		tl = self.tickline
		# tick_info should be (x, y, width, height) of tick
		tick_info = self.registrar[tick][index]
		if not texture:
			label_kw = tick.get_label_texture(index, succinct, return_kw=True)
			if not label_kw:
				return
			label_kw['font_size'] = self.time_font_size if which == 'time' else \
									  self.date_font_size
			label_kw['halign'] = 'left' if tl.is_vertical() else 'center'
			label = CoreLabel(**label_kw)
			label.refresh()
			texture = label.texture
		if tl.is_vertical():
			y = tick_info[1] + tick_info[3] / 2 - texture.height / 2
			if which == 'time':
				dist = self.time_dist_from_edge
			else:
				dist = self.date_dist_from_edge			
			dist = max(dist, tick.tick_size[1] + tl.tick_label_padding)
			halign = tick.halign
			if halign == 'left':
				x = tl.x + dist
			elif halign == 'line_left':
				x = tl.line_pos - dist - texture.width
			elif halign == 'line_right':
				x = tl.line_pos + dist
			else:
				x = tl.right - dist - texture.width
		else:
			# TODO horizontal is gonna get crowded with text
			x = tick_info[0] + tick_info[2] / 2 - texture.width / 2
			if which == 'time':
				dist = self.time_dist_from_edge
			else:
				dist = self.date_dist_from_edge
			dist = max(dist, tick.tick_size[1] + tl.tick_label_padding)
			valign = tick.valign
			if valign == 'top':
				y = tl.top - dist - texture.height
			elif valign == 'line_top':
				y = tl.line_pos + dist
			elif valign == 'line_bottom':
				y = tl.line_pos - dist - texture.height
			else:
				y = tl.y + dist	   
		return (texture, [x, y])
	def make_labels(self):
		r = self.registrar
		instructions = self.instructions
		setdefault = instructions.setdefault
		to_pop = set((tick, index) for tick in instructions 
				  for index in instructions[tick])
		tl = self.tickline
		succinct = not any('second' in tick.mode for tick in r)
		get_texture_pos = self._get_texture_pos
		canvas = tl.canvas
		for tick in r:
			instrs = setdefault(tick, {})
			if tick.mode != 'day':
				for index in r[tick]:
					self._update_rect(tick, index, instrs, get_texture_pos,
									  to_pop, succinct, canvas)
			else:
				a = tl.is_vertical()
				b = 1 - a
				bottom_up = sorted(r[tick], reverse=tl.backward)
				if self.have_time:
					last_rect = [None, None]
					for index in bottom_up:
						rect = \
						self._update_rect(tick, index, instrs, get_texture_pos,
										  to_pop, succinct, canvas, which='date')
						last_rect[0] = last_rect[1]
						last_rect[1] = rect
												   
					max_ = tl.top if a else tl.right
					if len(bottom_up) > 1:
						_2ndlast, last = last_rect
						last_coord = max(_2ndlast.pos[a] + _2ndlast.size[a],
									 max_ - last.size[a])
						_2ndlast_coord = min(_2ndlast.pos[a] + _2ndlast.size[a],
										 max_) - _2ndlast.size[a]
						last.pos = (last.pos[b], last_coord) if a else \
									(last_coord, last.pos[b])
						_2ndlast.pos = (_2ndlast.pos[b], _2ndlast_coord) if a \
										else (_2ndlast_coord, _2ndlast.pos[b])
					else:
						new_coord = max_ - last_rect[1].size[a]
						last_rect[1].pos = (last_rect[1].pos[b], new_coord) \
											if a else \
											(new_coord, last_rect[1].pos[b])
				else:
					for index in bottom_up[:-1]:
						self._update_rect(tick, index, instrs, get_texture_pos,
										  to_pop, succinct, canvas, which='date')
		for tick, index in to_pop:
			rect = instructions[tick].pop(index)
			canvas.remove(rect)
			 
	def _update_rect(self, tick, index, instrs, get_texture_pos, to_pop,
					 succinct, canvas, which='time'):
		if index in instrs:
			# old label: change position
			old_rect = instrs[index]
			t_p = get_texture_pos(tick, index, succinct,
								  texture=old_rect.texture, which=which)
			old_rect.pos = t_p[1]
			to_pop.remove((tick, index))
			return old_rect
		else:
			# new label
			t_p = get_texture_pos(tick, index, succinct, which=which) 
			if t_p:
				texture, pos = t_p
				rect = Rectangle(texture=texture, pos=pos,
								 size=texture.size)
				instrs[index] = rect
				canvas.add(rect)
				return rect
						
		
unixepoch = datetime(1970, 1, 1, tzinfo=UTC)


_tail_names = ['microsecond', 'second', 'minute', 'hour', 'day']
_tail_res = {'microsecond': 10 ** -6, 'second': 1, 'minute': 60, 'hour': 3600,
			 'day': 3600 * 24}

def time_tail(dt, length=2, tail_name=None, strict=False):
	'''given a datetime ``dt``, gives its time tail specified by ``length``
	or ``tail_name``::
	
		>>> assert(
			time_tail(datetime(2010, 10, 4, 13, 25, 5, 0.33)) ==
			timedelta(seconds=5.33))
		>>> assert(
			time_tail(datetime(2010, 10, 4, 13, 25, 5, 0.33), 3) ==
			timedelta(minutes=25, seconds=5.33))
		>>> assert(
			time_tail(datetime(2010, 10, 4, 13, 25, 5, 0.33), 
				tail_name='hour') ==
			timedelta(hour=13, minute=25, second=5.33))
		>>> assert(
			time_tail(datetime(2010, 10, 4, 13, 25, 5, 0.33), 
				tail_name='hour', strict=True) ==
			timedelta(minute=25, second=5.33))
	'''
	if tail_name:
		length = _tail_names.index(tail_name) + 1 - strict
	timedelta_kw = {}
	for name in _tail_names[:length]:
		timedelta_kw[name + 's'] = getattr(dt, name)
	return timedelta(**timedelta_kw)

def set_time_tail(dt, time_vector=[0]):
	for name, val in zip(_tail_names, time_vector):
		setattr(dt, name, val)
		
def round_time(dt, grain='second', mode='nearest'):
	'''round datetime ``dt`` to the nearest, next, or previous second, 
	15 seconds, minutes, etc::
	
		>>> round_time(datetime(2013, 2, 3, 5, 23, 56), 'minute', 'nearest')
		datetime.datetime(2013, 2, 3, 5, 24, 0)
		>>> round_time(datetime(2013, 2, 3, 5, 23, 56), 'minute', 'down')
		datetime.datetime(2013, 2, 3, 5, 23, 0)
		>>> round_time(datetime(2013, 2, 3, 5, 23, 56), 'day', 'up')
		datetime.datetime(2013, 2, 4, 0, 0, 0)
		
	:param dt: datetime object to round
	:param grain: the smallest granularity to round toward. Can be any of
		:attr:`TimeTick.mode`. Defaults to 'second'
	:param mode: the rounding mode. Can be any one of 'nearest', 'up', or 'down'.
		Defaults to 'nearest'
	'''
	if mode == 'nearest':
		round_func = round
	elif mode == 'up':
		round_func = ceil
	else:
		round_func = floor
	res = TimeTick.granularity(grain)
	if grain in _tail_names:
		tail = time_tail(dt, _tail_names.index(grain))
	else:
		mult, gr = grain.split(' ')
		tail = time_tail(dt, _tail_names.index(gr[:-1]) + 1)
	trunced = dt - tail
	return timedelta(seconds=res * round_func(tail.total_seconds() / res)) \
		+ trunced


class TimeTick(Tick):  
	
	size_dict = \
		{'day': [dp(5), dp(48)],
		 '12 hours': [dp(4.5), dp(25)],
		 '6 hours': [dp(4.5), dp(25)],
		 '4 hours': [dp(4), dp(20)],
		 '2 hours': [dp(4), dp(20)],
		 'hour': [dp(4), dp(20)],
		 '30 minutes': [dp(3), dp(12)],
		 '15 minutes': [dp(3), dp(12)],
		 '10 minutes': [dp(2), dp(8)],
		 '5 minutes': [dp(2), dp(8)],
		 'minute': [dp(2), dp(8)],
		 '30 seconds': [dp(1.5), dp(7)],
		 '15 seconds': [dp(1.5), dp(7)],
		 '10 seconds': [dp(1), dp(4)],
		 '5 seconds': [dp(1), dp(4)],
		 'second': [dp(1), dp(4)]} 
		
	scale_factor_dict = \
		{'day': 1,
		 '12 hours': 2,
		 '6 hours': 4,
		 '4 hours': 6,
		 '2 hours': 12,
		 'hour': 24,
		 '30 minutes': 48,
		 '15 minutes': 96,
		 '10 minutes': 48 * 3,
		 '5 minutes': 3 * 96,
		 'minute': 24 * 60,
		 '30 seconds': 24 * 120,
		 '15 seconds': 24 * 240,
		 '10 seconds': 24 * 360,
		 '5 seconds': 24 * 720,
		 'second': 24 * 3600}
		
	mode_options = ['day',
		   '12 hours',
		   '6 hours',
		   '4 hours',
		   '2 hours',
		   'hour',
		   '30 minutes',
		   '15 minutes',
		   '10 minutes',
		   '5 minutes',
		   'minute',
		   '30 seconds',
		   '15 seconds',
		   '10 seconds',
		   '5 seconds',
		   'second']
	
	mode = OptionProperty('day', options=mode_options)
	# 188 is good to be an entire header for the date
	_tick_size = ListProperty(None)
	def get_tick_size(self, *args):
		return self._tick_size or self.size_dict[self.mode]
	def set_tick_size(self, val):
		self._tick_size = val
	tick_size = AliasProperty(get_tick_size, set_tick_size,
							  bind=['_tick_size', 'mode'])
	tz = ObjectProperty(get_localzone())
	def __init__(self, *args, **kw):
		super(TimeTick, self).__init__(*args, **kw)
		self.halign='line_left'
	@classmethod
	def granularity(cls, mode):
		'''gives the multiplicity of this mode in terms of seconds.'''
		return cls.scale_factor_dict['second'] / cls.scale_factor_dict[mode]
	def time_min_max(self, tl, extended=False):
		'''gives either (:meth:`time_0`, :meth`time_1`) or 
		(:meth:`time_1`, :meth`time_0`) applied to ``tl``
		so that the first time is not later than the second. In essence,
		provide the minimal and maximal time that can be shown on the screen
		at the time of method call.
		
		If ``extended``, then time corresponding 1 ``tl.densest_tick``
		below and 1 above the current window will be given instead.
		
		:param tl: :class:`Tickline` instance.
		:param extended: If True, gives a slightly larger window, as discussed
			above. Defaults to False.
		'''
		
		min_, max_ = (tl.time_1, tl.time_0) if tl.backward else \
						(tl.time_0, tl.time_1)
					
		if extended:
			interval = TimeTick.granularity(tl.densest_tick.mode)
			min_ -= timedelta(seconds=interval)
			max_ += timedelta(seconds=interval)

		return min_, max_
		
	def tick_iter(self, tl):
		'''Overrides :meth:`Tick.tick_iter`.
		
		Provides an iterator of the times that correspond to ticks that 
		should be drawn on screen, depending on :attr:`mode`. Note that
		for the "day" mode, the day past the last day shown on screen is also
		given, for the push graphics (see :class:`TimeLabeller` for details).
		'''
		if self.scale(tl.scale) < self.min_space:
			raise StopIteration		
		time_min, time_max = self.time_min_max(tl, extended=True)
		time = round_time(time_min, self.mode, 'up')
		delta = timedelta(seconds=self.granularity(self.mode))
		if self.mode == 'day' and tl.backward:
			yield time - timedelta(days=1)
		while time <= time_max:
			yield time
			time += delta
		if self.mode == 'day' and not tl.backward:
			yield time
		raise StopIteration
	
	def draw(self, tickline, time):
		'''Override :meth:`Tick.draw`.
		
		Instead of taking a pair (pos, index) of the tick to be drawn, takes
		the time of such a tick, and internally convert it to (pos, index)
		using :meth:`index_of` and :meth:`index2pos`.
		'''
		super(TimeTick, self).draw(tickline, self.pos_index_of(tickline, time))

		
	def pos_index_of(self, tickline, time):
		tick_index = self.index_of(time)
		tick_pos = tickline.index2pos(self.globalize(tick_index))
		return tick_pos, tick_index
	
	def pos_of(self, tickline, time):
		return self.pos_index_of(tickline, time)[0]
	
	def on_mode(self, *args):
		self.scale_factor = self.scale_factor_dict[self.mode]
		
	def datetime_of(self, tick_index):
		if self.mode in ('day', 'hour', 'minute', 'second'):
			t = timedelta(**{self.mode + 's': tick_index}) + unixepoch
		else:
			mult, mode = self.mode.split(' ')
			t = timedelta(**{mode: int(mult) * tick_index}) + unixepoch
		t = t.astimezone(self.tz)
		return t
	
	def to_seconds(self, tick_index):
		'''converts the ``tick_index`` to the number of seconds since 
		unix epoch. Always returns the nearest integer.'''
		
		return round(tick_index * self.scale_factor_dict['second'] 
					 / self.scale_factor)
		
	def pos2time(self, pos, tl):
		return self.datetime_of(self.localize(tl.pos2index(pos)))

	def index_of(self, dt, global_=False):
		'''return a local index corresponding to a datetime. If ``global_``
		is true, then return the global index (the index of the owning 
		:class:`Tickline`).
		
		:param dt: a datetime to be converted to index.
		:param global_: flag that indicates the index returned should be global.
			Defaults to False.
		'''
		
		secs = (dt - unixepoch).total_seconds() 
		global_idx = secs / self.scale_factor_dict['second']
		if global_:
			return global_idx
		return self.localize(global_idx)
			
	def get_label_texture(self, index, succinct=True, return_kw=False,
						  return_label=False, **kw):
		if isinstance(index, Number):
			t = self.datetime_of(index)
		else:
			t = index
		if self.mode == 'second':
			return None
		if self.mode == 'day':
			# need to get the datetime of the previous day
			text = (t).strftime('%a\n%m-%d-%y')
			kw.setdefault('height', 50)
		elif 'second' not in self.mode and succinct:
			text = str(t.time())[:-3]
		else:
			text = str(t.time())
		kw.setdefault('height', 20)
		kw['text'] = text
		if return_kw:
			return kw
		if not return_label:
			return CoreLabel(**kw).texture
		label = AutoSizeLabel(**kw)
		label.texture_update()
		return label
	
def selected_time_ticks():
	'''returns a list of :class:`TimeTick`s with intervals of
	1 day, 4 hours, 1 hour, 15 minutes, 5 minutes, 1 minute, 15 seconds,
	5 seconds, and 1 second.'''
	return [TimeTick(mode=TimeTick.mode.options[i]) for i in 
			[0, 5, 7, 9, 10]]
	
	
class Timeline(Tickline):
	'''subclass of :class:`Tickline` specialized for displaying time 
	information. See module documentation for more details.'''
	
	labeller_cls = ObjectProperty(TimeLabeller)
	
	tz = ObjectProperty(get_localzone())
	
	def get_min_time(self, *args):
		return self.datetime_of(self.min_index)
	def set_min_time(self, val):
		self.min_index = self.index_of(val)
	min_time = AliasProperty(get_min_time, set_min_time, cache=True,
							 bind=['min_index'])
	'''the minimal time beyond which this :class:`Timeline` cannot go.
	This is a time version of :attr:`Tickline.min_index`.'''
	
	def get_max_time(self, *args):
		return self.datetime_of(self.max_index)
	def set_max_time(self, val):
		self.max_index = self.index_of(val)
	max_time = AliasProperty(get_max_time, set_max_time, cache=True,
							 bind=['max_index'])
	'''the maximal time beyond which this :class:`Timeline` cannot go.
	This is a time version of :attr:`Tickline.max_index`.'''
		
	def get_time_0(self, *args):
		return self.datetime_of(self.index_0)
	def set_time_0(self, val):
		self.index_0 = self.datetime_of(val)
	time_0 = AliasProperty(get_time_0, set_time_0,
						   bind=['index_0'])  
	'''gives the time that that sits on top of
	``self.x`` if :attr:`orientation` is 'vertical', or ``self.y``
	if :attr:`orientation` is 'horizontal'. Note that this doesn't 
	depend on :attr:`Tickline.backward`.
	
	This is the time version of :class:`Tickline.index_0`.'''	
	
	def get_time_1(self, *args):
		return self.datetime_of(self.index_1)
	def set_time_1(self, val):
		self.index_1 = self.datetime_of(val)
	time_1 = AliasProperty(get_time_1, set_time_1,
						   bind=['index_1'])  
	'''gives the time that that sits on top of
	``self.right`` if :attr:`orientation` is 'vertical', or ``self.top``
	if :attr:`orientation` is 'horizontal'. Note that this doesn't 
	depend on :attr:`Tickline.backward`.
	
	This is the time version of :class:`Tickline.index_1`.'''	   

	def __init__(self, **kw):
		now = local_now().astimezone(UTC)
		self.center_on_timeframe(now - timedelta(days=1),
								 now + timedelta(days=1))
		self.ticks = selected_time_ticks()
		super(Timeline, self).__init__(**kw)
	def on_tz(self, *args):
		for tick in self.ticks:
			tick.tz = self.tz
	def pos2time(self, pos):
		return self.datetime_of(self.pos2index(pos))
	def datetime_of(self, index):
		return (timedelta(days=index) + unixepoch).astimezone(self.tz)
	def index_of(self, dt):
		'''return a global index corresponding to a datetime. '''
		secs = (dt - unixepoch).total_seconds() 
		global_idx = secs / TimeTick.scale_factor_dict['second']
		return global_idx
	def pos_of_time(self, time):
		return self.index2pos(self.index_of(time))
	def timedelta2dist(self, td):
		return td.days * self.scale
	def center_on_timeframe(self, start, end):
		self.index_0 = self.index_of(start)
		self.index_1 = self.index_of(end)

	def intersection_date(self,t1start,t1end,t2start,t2end):
		latest_start = max(t1start,t2start)
		earliest_end = min(t1end,t2end)
		if latest_start<earliest_end:
			return latest_start,earliest_end
		else:
			return sys.exit()

	def add_button(self,border_inf,border_sup,fenetre_inf,fenetre_sup,ref_second,box,label,button):
		try:
			min_f,max_f=self.intersection_date(border_inf,border_sup,fenetre_inf,fenetre_sup)
			second_inf=(min_f-border_inf).total_seconds()
			second_int=(max_f-min_f).total_seconds()
			if (second_int/ref_second)<0.035:
				box.add_widget(label(size_hint=(0.9,second_int/ref_second),pos_hint={"x":0.2,"y":(second_inf/ref_second)}))
			else:
				box.add_widget(button(size_hint=(0.9,second_int/ref_second),pos_hint={"x":0.2,"y":(second_inf/ref_second)},text_info="start pass :"+str(fenetre_inf)+"\n end pass :"+str(fenetre_sup)))
			return [fenetre_inf,fenetre_sup]
		except:
			pass


	def translate_by(self, distance):
		self._versioned_scale = self.scale
		self.index_0 += distance
		self.index_1 += distance
		self.resatime=[]
		app=App.get_running_app()
		app.calendar.dates.boxbtn.clear_widgets()
		app.calendar.dates.boxresa.clear_widgets()
		app.calendar.dates.boxinfo.clear_widgets()
		self.border_inf=self.datetime_of(self.index_0)
		self.border_sup=self.datetime_of(self.index_1)
		self.ref_second=(self.border_sup-self.border_inf).total_seconds()
		self.df_reservation=np.array(app.calendar.dates.data.df_reservation[['start_date','end_date']])
		for couple in app.calendar.dates.data.list_date:
			self.add_button(self.border_inf,
							self.border_sup,
							get_localzone().localize(datetime.strptime(couple[0], '%Y-%m-%d %H:%M:%S')),
							get_localzone().localize(datetime.strptime(couple[1], '%Y-%m-%d %H:%M:%S')),
							self.ref_second,
							app.calendar.dates.boxbtn,
							PassLabel,
							PassButton)
		for couple in self.df_reservation:
			self.resatime.append(self.add_button(self.border_inf,
							self.border_sup,
							get_localzone().localize(datetime.strptime(couple[0], '%Y-%m-%d %H:%M:%S'))
							,get_localzone().localize(datetime.strptime(couple[1], '%Y-%m-%d %H:%M:%S')),
							self.ref_second,
							app.calendar.dates.boxresa,
							ResaLabel,
							ResaButton))


