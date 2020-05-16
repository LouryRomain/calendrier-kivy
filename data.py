import pandas as pd
import numpy as np
import calendar
import datetime



class Data:
	def __init__(self):
		self.list_date=[['2020-05-13 10:50:00','2020-05-13 12:10:00'],['2020-05-13 12:20:00','2020-05-13 12:45:00'],['2020-05-13 16:00:00','2020-05-20 16:00:00'],['2020-05-25 16:00:00','2020-06-29 16:00:00'],['2021-05-25 16:36:00','2021-06-10 11:48:00']]
		self.df_reservation=pd.read_csv('reservation.csv', sep=',')

 


if __name__ == "__main__":
    data=Data()