class StyleGenerator:
	def __init__(self):
		self.sidebar_style = {}
		self.content_style = {}

	def getSidebarStyle(self):
		return self.sidebar_style

	def getContentStyle(self):
		return self.content_style	

	def setSidebarStyle(self, position="fixed", top=0, left=0, bottom=0, width="0rem", padding="0rem 0rem", backgroundcolor="#f8f9fa"):
		self.sidebar_style = {
								"position": position, 
								"top":top, 
								"left":left, 
								"bottom":bottom, 
								"width":width, 
								"padding":padding, 
								"background-color":backgroundcolor
							  }
	def setContentStyle(self, marginleft="0rem", marginright="0rem", padding="0rem 0rem"):
		self.content_style = {
								"margin-left":marginleft,
								"margin-right":marginright,
								"padding":padding
							 }
