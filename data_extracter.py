import pandas as pd

class DataExtracter:
	def __init__(self, filename):
		self.filename = filename
		self.df = None
		self.month=None
		self.year=None
		self.drop_list = {'Category': ['Transfers', 'Carry Over', 'Rewards']}
		self.main()

	# Try and do for all columns if possible
	def fillgaps(self):
		self.df.Comments.fillna('No Comments', inplace=True)
		if 'Tags' in self.df.columns: 
			self.df['Tags'].fillna('None', inplace=True)
		if 'Special Occasion' in self.df.columns: 
			self.df['Special Occasion'].fillna('None', inplace=True)			
		if 'Name' in self.df.columns: 
			self.df['Name'].fillna('None', inplace=True)			
		if 'Category' in self.df.columns: 
			self.df['Category'].fillna('Artificial', inplace=True)						
		if 'Payment Mode' in self.df.columns: 
			self.df['Payment Mode'].fillna('Artificial', inplace=True)									
		if 'INR' in self.df.columns: 
			self.df['INR'].fillna(0.0, inplace=True)			
		if 'USD' in self.df.columns: 
			self.df['USD'].fillna(0.0, inplace=True)						
		if 'EUR' in self.df.columns: 
			self.df['EUR'].fillna(0.0, inplace=True)

	# With no real expense or income. Just for neat plots
	def fakerows(self):
		num_days = pd.Period(self.df.Date[0]).days_in_month
		year = self.df.Date[0].split(',')[-1]
		month = self.df.Date[0].split(',')[0].split(' ')[0]		
		for date in range(1, num_days+1):
			self.df = self.df.append(pd.Series(), ignore_index=True)
			self.df.loc[[len(self.df)-1], 'Date'] = month + ' ' + str(date) + ', ' + year
		self.df['Date'] = pd.to_datetime(self.df.Date)

	def drop(self):
		for key, values in self.drop_list.items():
			for value in values:
				self.df.drop(self.df[(self.df[key] == value)].index, inplace=True)

	def sort(self, date):
		self.df.sort_values(by=[date], inplace=True)

	def main(self):
		self.read()
		self.fakerows()
		self.fillgaps()
		self.drop()
		self.sort('Date')
		self.extract_titles()

	def read(self):
		self.df = pd.read_csv(self.filename)

	def get_df(self):
		return self.df

	def extract_titles(self):
		names = self.filename.split('/')
		if len(names) >= 2:
			self.year = names[-2]
			self.month = names[-1].split('.')[0]