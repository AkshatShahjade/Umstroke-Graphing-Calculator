from sympy import *
import multiprocessing
import cProfile, pstats, io
import threading
import re
import tkinter as tk
from tkinter.ttk import *
window = tk.Tk()
window.title("Umstroke")
window.iconbitmap("logo_500x500_px_bdm_icon.ico")


#Graphing Variables
lineList = []
gridList = []
axesList = []
refreshDistance=1000
x_displacement = 0
y_displacement = 0
_x_displacement = 0
_y_displacement = 0
y_Movement = 0
x_Movement = 0
magnification=1
graphingModeOn=false

movementVelocity = 10
gridBoxSideLength = 50
gridRange = 0
xOrigin = 0
yOrigin = 0
equationSlots = 0


# Graph Construction Variables
interval = 0.1
equation_entry_list = []
RedScheme = {
	0:"gold",
	1:"DarkOrange1",
	2:"OrangeRed2",
	3:"red2",
	4:"red4"
}
BlueScheme = {
	0:"aquamarine",
	1:"turquoise3",
	2:"DeepSkyBlue3",
	3:"blue",
	4:"navy"
}
GreenScheme = {
	0:"green yellow",
	1:"lawn green",
	2:"green2",
	3:"green3",
	4:"green4"
}
MixScheme = {
	0:"DarkOrange1",
	1:"red2",
	2:"turquoise3",
	3:"blue",
	4:"green2"
}
ComplementaryScheme= {
	0:"DeepPink3",
	1:"chartreuse2",
	2:"light sea green",
	3:"orange red",
	4:"blue4"
}
colorDecider = {
	0:MixScheme,
	1:RedScheme,
	2:BlueScheme,
	3:GreenScheme,
	4:ComplementaryScheme
}

# # Profiling decorator
# def profile(fnc):
	
#     """A decorator that uses cProfile to profile a function"""
	
#     def inner(*args, **kwargs):
		
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = fnc(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = 'cumulative'
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         print(s.getvalue())
#         return retval

#     return inner

#########Necessary Functions
def createGraph(event = None):  

	for lineSegment in lineList:
		graphingCanvas.delete(lineSegment)
	lineList.clear()

	parseQuation()
	

def plotGraph(f, lineRenderColor):
	global interval   
	global xOrigin
	global x_displacement
	global y_displacement
	global magnification
	global gridBoxSideLength
	global graphingModeOn
	
	graphingModeOn=true

	x=symbols("x")

	_gridBoxSideLength=magnification*gridBoxSideLength
	_y_displacement=y_displacement*magnification
	_x_displacement=x_displacement*magnification 


	# Generate graph line segment by line segment
	counter = 0
	if(not f == None):
		for count in range(int(((-refreshDistance+xOrigin)/_gridBoxSideLength)/interval),int(((refreshDistance+xOrigin)/_gridBoxSideLength)/interval)):   
			x_val = count*interval
			# if x_val%pi<interval:              
			y_value = N(f.subs(x, x_val))  
			if y_value.is_real:
				if not counter <= 0:
					if y_value in (oo, zoo):
						print(str(x_val) + " oo/zoo")
						y_value=9999
						lineList.append(graphingCanvas.create_line((x_val-interval)*_gridBoxSideLength+canvasWidth/2-_x_displacement, -_gridBoxSideLength*(last_y_value)+canvasHeight/2-_y_displacement, x_val*_gridBoxSideLength+canvasWidth/2-_x_displacement, y_value, fill=lineRenderColor, width=5)) 
						counter=0
					elif y_value == -oo:
						print(str(x_val) + " -oo")                         
						y_value=-9999
						lineList.append(graphingCanvas.create_line((x_val-interval)*_gridBoxSideLength+canvasWidth/2-_x_displacement, -_gridBoxSideLength*(last_y_value)+canvasHeight/2-_y_displacement, x_val*_gridBoxSideLength+canvasWidth/2-_x_displacement, y_value, fill=lineRenderColor, width=5))                             
						counter=0
					elif y_value==nan or last_y_value==nan:
						counter=0
					else:   
						lineList.append(graphingCanvas.create_line((x_val-interval)*_gridBoxSideLength+canvasWidth/2-_x_displacement, -_gridBoxSideLength*(last_y_value)+canvasHeight/2-_y_displacement, x_val*_gridBoxSideLength+canvasWidth/2-_x_displacement, -_gridBoxSideLength*(y_value)+canvasHeight/2-_y_displacement, fill=lineRenderColor, width=5))    
				last_y_value = y_value
				counter+=1

def parseQuation():
	global schemeChosen
	x=symbols("x")

	equationSlotCounter = 0
	# Convert the raw input of user into suitable form
	for equation_entry in equation_entry_list:   
		lineRenderColor = colorDecider.get(schemeChosen.current()).get(equationSlotCounter, "black")
		equationSlotCounter+=1
		raw_equation=equation_entry.get()
		
		if not raw_equation=="":
			raw_equation_copy = raw_equation
			
			multList = []
			multIdentifier = re.compile(r"(?:\+|\-)?\d+\.?\d*[a-z]")
			while true:    
				try:    
					multGroup = multIdentifier.search(raw_equation).group(0)
					multList.append(multGroup)
					raw_equation = raw_equation.replace(multGroup, '')
				except AttributeError:
					break
			raw_equation = raw_equation_copy
			for term in multList:
				num = len(''.join([i for i in term if not i.isdigit()]).replace('+','').replace('-','').replace(".",""))
				new_term = term[:-num]+"*"+term[-num:]
				raw_equation = raw_equation.replace(term, new_term)

			raw_equation = raw_equation.replace("y=","").replace("^","**")
				

			# # For trig degree to radian it creates a crazily maximized graph
			# trigList=[]
			# resultList=[]

			# trigConverter = re.compile(r"((?:sin|cos|tan|cot|sec|cosec)\()(.+)\)")
			# test = re.compile((r".+"))
			# while true:    
			#     try:    
			#         trigGroup = trigConverter.search(raw_equation).group(1)
			#         resGroup = trigConverter.search(raw_equation).group(2)
			#         trigList.append(trigGroup)
			#         resultList.append(resGroup)
			#         raw_equation = raw_equation.replace(trigGroup, '')
			#     except AttributeError:
			#         break
			# raw_equation = raw_equation_copy
			# minicounter = 0
			# trigList.reverse()
			# resultList = resultList[-1:]
			# for term in trigList:
			#     num = len(''.join([i for i in term if not i.isdigit()]).replace('+','').replace('-','').replace(".",""))
			#     new_term = term[:num+1]+"pi/180*("+resultList[minicounter]+")"
			#     resultList.append(new_term)
			#     raw_equation=new_term
			#     minicounter+=1
			# raw_equation = raw_equation+")"

			# interval = float(interval_entry.get().strip() or '1')
			# parse the equation
			f = parse_expr(raw_equation)

			plotGraph(f, lineRenderColor)
			print("THis is runnningn")



def updateGrid():
	global x_Movement
	global y_Movement
	global x_displacement
	global y_displacement
	global _y_displacement
	global _x_displacement
	global xOrigin
	global yOrigin
	global gridRange

	_gridBoxSideLength=gridBoxSideLength*magnification      
	_x_displacement=x_displacement*magnification+x_Movement
	_y_displacement=y_displacement*magnification+y_Movement

	x_displacement+=x_Movement/magnification
	y_displacement+=y_Movement/magnification

	deleteBuffer = _gridBoxSideLength*4*(gridRange+10)
	# deleteBuffer = _gridBoxSideLength*(gridRange+6)


	x_offset = 0
	y_offset = 0

	sign_coefficient = 1

	# move the grid itself
	for gridBlock in gridList:
		graphingCanvas.move(gridBlock, -x_Movement, -y_Movement) 
	for axes in axesList:
		graphingCanvas.move(axes, -x_Movement, -y_Movement)
	for lineSegment in lineList:
		graphingCanvas.move(lineSegment, -x_Movement, -y_Movement)

	if not y_Movement == 0:
		if y_Movement < 0:
			sign_coefficient = -1  
		y_Movement=0          

		if abs(_y_displacement-yOrigin) > refreshDistance-canvasHeight/2:
			
			print("refreshed y")

			for lineSegment in lineList:
				graphingCanvas.delete(lineSegment)
			lineList.clear()

			yOrigin = _y_displacement 
			graphingCanvas.coords(axesList[1], canvasWidth/2-_x_displacement,-refreshDistance, canvasWidth/2-_x_displacement, refreshDistance)

			for gridBox in gridList:
				graphingCanvas.delete(gridBox)
			gridList.clear()
			if(not _y_displacement==0):
				createGraphingPaper()
			else:
				createGraphingPaper()

			if graphingModeOn == true:
				createGraphProcess()

	if not x_Movement == 0:
		if x_Movement < 0:
			sign_coefficient = -1
		x_Movement=0

		if abs(_x_displacement-xOrigin) > refreshDistance-canvasWidth/2 :
			
			print("refreshed x")


			for lineSegment in lineList:
				graphingCanvas.delete(lineSegment)
			lineList.clear()
			graphingCanvas.coords(axesList[0], -refreshDistance, canvasHeight/2-_y_displacement, refreshDistance, canvasHeight/2-_y_displacement)

			for gridBox in gridList:
				graphingCanvas.delete(gridBox)
			gridList.clear()
			if(not _x_displacement==0):
				createGraphingPaper()
			else:
				createGraphingPaper()

			if graphingModeOn == true:
				createGraphProcess()

def clearGraphs(event=None):
	global graphingModeOn
	graphingModeOn=false
	for lineSegment in lineList:
		graphingCanvas.delete(lineSegment)
	lineList.clear()

def createGraphingPaper():
	
	global gridBoxSideLength
	global x_displacement
	global xOrigin
	global y_displacement
	global yOrigin
	global gridRange

	_gridBoxSideLength=gridBoxSideLength*magnification
	_x_displacement=x_displacement*magnification
	_y_displacement=y_displacement*magnification

	gridRange = int(canvasWidth/_gridBoxSideLength)

	print(str(magnification)+" magnification")

	xOrigin=_x_displacement
	yOrigin=_y_displacement

	for gridBox in gridList:
		graphingCanvas.delete(gridBox)
	gridList.clear()
	for axes in axesList:
		graphingCanvas.delete(axes)
	axesList.clear()

	gridBoxZoom=1

	#Create Grid
	
	# Decide on magnification's affect on the gridbox side length
	# if magnification <= 0.4:
	#     _gridBoxSideLength*=2
	# elif magnification >= 2:
	#     _gridBoxSideLength/=2
	#  it is unfinished and not planned to be completed.


	for y in range(0,int(refreshDistance/_gridBoxSideLength)):
		# if (y%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
		for x in range(0,int(refreshDistance/_gridBoxSideLength)):
			# if (x%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
			gridList.append(graphingCanvas.create_rectangle(canvasWidth/2+x*_gridBoxSideLength-_x_displacement%_gridBoxSideLength,canvasHeight/2+y*_gridBoxSideLength-_y_displacement%_gridBoxSideLength,gridBoxZoom*(canvasWidth/2+(x+1)*_gridBoxSideLength-_x_displacement%_gridBoxSideLength),gridBoxZoom*(canvasHeight/2+(y+1)*_gridBoxSideLength-_y_displacement%_gridBoxSideLength)))
			# gridList.append(graphingCanvas.create_rectangle(canvasWidth/2+x*_gridBoxSideLength-_x_displacement, canvasHeight/2+y*_gridBoxSideLength-_y_displacement, canvasWidth/2+(x+1)*_gridBoxSideLength-_x_displacement, canvasHeight/2+(y+1)*_gridBoxSideLength-_y_displacement))

	for y in range(0,int(refreshDistance/_gridBoxSideLength)):
		# if (y%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
		for x in range(0,int(refreshDistance/_gridBoxSideLength)):
			# if (x%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
			gridList.append(graphingCanvas.create_rectangle(canvasWidth/2-x*_gridBoxSideLength-_x_displacement%_gridBoxSideLength,canvasHeight/2+y*_gridBoxSideLength-_y_displacement%_gridBoxSideLength,gridBoxZoom*(canvasWidth/2-(x+1)*_gridBoxSideLength-_x_displacement%_gridBoxSideLength),gridBoxZoom*(canvasHeight/2+(y+1)*_gridBoxSideLength-_y_displacement%_gridBoxSideLength)))
			# gridList.append(graphingCanvas.create_rectangle(canvasWidth/2-x*_gridBoxSideLength-_x_displacement, canvasHeight/2+y*_gridBoxSideLength-_y_displacement, canvasWidth/2-(x+1)*_gridBoxSideLength-_x_displacement, canvasHeight/2+(y+1)*_gridBoxSideLength-_y_displacement))

	for y in range(0,int(refreshDistance/_gridBoxSideLength)):
		# if (y%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
		for x in range(0,int(refreshDistance/_gridBoxSideLength)):
			# if (x%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
			gridList.append(graphingCanvas.create_rectangle(canvasWidth/2+x*_gridBoxSideLength-_x_displacement%_gridBoxSideLength,canvasHeight/2-y*_gridBoxSideLength-_y_displacement%_gridBoxSideLength,gridBoxZoom*(canvasWidth/2+(x+1)*_gridBoxSideLength-_x_displacement%_gridBoxSideLength),gridBoxZoom*(canvasHeight/2-(y+1)*_gridBoxSideLength-_y_displacement%_gridBoxSideLength)))
			# gridList.append(graphingCanvas.create_rectangle(canvasWidth/2+x*_gridBoxSideLength-_x_displacement, canvasHeight/2-y*_gridBoxSideLength-_y_displacement, canvasWidth/2+(x+1)*_gridBoxSideLength-_x_displacement, canvasHeight/2-(y+1)*_gridBoxSideLength-_y_displacement))

	for y in range(0,int(refreshDistance/_gridBoxSideLength)):
		# if (y%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
		for x in range(0,int(refreshDistance/_gridBoxSideLength)):
			# if (x%2==0 and gridBoxZoom==2) or gridBoxZoom==1:
			gridList.append(graphingCanvas.create_rectangle(canvasWidth/2-x*_gridBoxSideLength-_x_displacement%_gridBoxSideLength,canvasHeight/2-y*_gridBoxSideLength-_y_displacement%_gridBoxSideLength,gridBoxZoom*(canvasWidth/2-(x+1)*_gridBoxSideLength-_x_displacement%_gridBoxSideLength),gridBoxZoom*(canvasHeight/2-(y+1)*_gridBoxSideLength-_y_displacement%_gridBoxSideLength)))
			# gridList.append(graphingCanvas.create_rectangle(canvasWidth/2-x*_gridBoxSideLength-_x_displacement, canvasHeight/2-y*_gridBoxSideLength-_y_displacement, canvasWidth/2-(x+1)*_gridBoxSideLength-_x_displacement, canvasHeight/2-(y+1)*_gridBoxSideLength-_y_displacement))

	#Create Axes
		# xaxes
		axesList.append(graphingCanvas.create_line(-_gridBoxSideLength*2*(gridRange+10)+canvasWidth/2-(x_displacement*magnification),canvasHeight/2-_y_displacement,_gridBoxSideLength*2*(gridRange+10)+canvasWidth/2,canvasHeight/2-_y_displacement, fill="black", width=5))
		# yaxes
		axesList.append(graphingCanvas.create_line(canvasWidth/2-_x_displacement,-2*(gridRange+10)*_gridBoxSideLength+canvasHeight/2,canvasWidth/2-_x_displacement,2*(gridRange+10)*_gridBoxSideLength+canvasHeight/2, fill="black", width=5))

def leftMovement(e):
	global x_Movement
	x_Movement=-movementVelocity
	updateGrid()

def rightMovement(e):
	global x_Movement
	x_Movement=movementVelocity
	updateGrid()

def downMovement(e):
	global y_Movement
	y_Movement=+movementVelocity
	updateGrid()

def upMovement(e):
	global y_Movement
	y_Movement=-movementVelocity
	updateGrid()

# counterin = 0
# counterout = 0
def mouseWheelInput(e):
	global magnification
	# global counterin
	# global counterout
	if e.num==5 or e.delta==-120:
		# zoom out
		# counterout += 1
		# if counterout == 2:
		#     counterout=0
		# double rounding to prevent 0.600000000000001, etc.
		magnification = round(round((magnification-0.2)/0.2,1)*0.2,1)
		if not magnification<0.1:
			zoomManager()
		else:
			magnification=0.2
	if e.num==4 or e.delta==120:
		# zoom in
		# counterin += 1
		# if counterin == 1:
		#     counterin=0
		magnification = round(round((magnification+0.2)/0.2,1)*0.2,1)
		if not magnification>3.1:
			zoomManager()
		else:
			magnification=3
	# zoomManager()

def zoomManager():
	global magnification
	global gridBoxSideLength
	global _x_displacement
	global _y_displacement
	global x_displacement
	global y_displacement
	global graphingModeOn

	if _y_displacement < 0:
		_y_displacement+=-(_y_displacement)%(2*gridBoxSideLength*magnification)
	else:
		_y_displacement-=(_y_displacement)%(2*gridBoxSideLength*magnification)
	if _x_displacement < 0:
		_x_displacement+=-(_x_displacement)%(2*gridBoxSideLength*magnification)
	else:
		_x_displacement-=+(_x_displacement)%(2*gridBoxSideLength*magnification)
	y_displacement = _y_displacement/magnification
	x_displacement = _x_displacement/magnification

	# createGraphingPaper()
	createGraphingPaper()
	if graphingModeOn==true:    
		print("Create Graph process is called")
		createGraphProcess()

x_start=0
y_start=0

def startClick(e):
	global x_start
	global y_start
	x_start=e.x
	y_start=e.y

def endClick(e):
	global x_start
	global y_start
	global x_Movement
	global y_Movement
	x_Movement=-(e.x-x_start)
	y_Movement=-(e.y-y_start)
	x_start=0
	y_start=0
	updateGrid()

def bound_to_actions(e):
	graphingCanvas.bind("<a>", leftMovement)
	graphingCanvas.bind("<s>", downMovement)
	graphingCanvas.bind("<d>", rightMovement)
	graphingCanvas.bind("<w>", upMovement)
	graphingCanvas.bind("<MouseWheel>", mouseWheelInput)
	graphingCanvas.bind("<Button-1>", startClick)
	graphingCanvas.bind("<ButtonRelease-1>", endClick)
	graphingCanvas.focus_set()

def unbound_to_actions(e):
	graphingCanvas.unbind("<a>")
	graphingCanvas.unbind("<s>")
	graphingCanvas.unbind("<d>")
	graphingCanvas.unbind("<w>")
	graphingCanvas.unbind("<MouseWheel>")
	graphingCanvas.unbind("<Button-1>")
	graphingCanvas.unbind("<ButtonRelease-1>")

def createGraphProcess(event = None):
	# p1 = multiprocessing.Process(target=createGraph, args=(10, ))
	# p1.start()
	# p1.join()
	# threading.Thread(target=createGraph).start()	
	createGraph()

def changeColorScheme(event=None):
	colour_frame1["bg"]=colorDecider.get(schemeChosen.current()).get(0)
	colour_frame2["bg"]=colorDecider.get(schemeChosen.current()).get(1)
	colour_frame3["bg"]=colorDecider.get(schemeChosen.current()).get(2)
	colour_frame4["bg"]=colorDecider.get(schemeChosen.current()).get(3)
	colour_frame5["bg"]=colorDecider.get(schemeChosen.current()).get(4)

	createGraphProcess()


########General Settings
window.columnconfigure(0, minsize=200, weight=0)
window.columnconfigure(1, minsize=600, weight=1)
window.rowconfigure(0, minsize=600, weight=1)
window.bind("<Return>", createGraphProcess)
window.bind("<Escape>", clearGraphs)

########Frame Settings
frameEquation = tk.Frame(bg="grey")
frameGraph = tk.Frame(bg="red")

frameEquation.grid(row=0, column=0, sticky="nsew")
frameGraph.grid(row=0, column=1, sticky="nsew")

###########Equations Tab UI

# Labels and Entries
equationLabel = tk.Label(master=frameEquation, text="Equations Tab")
equationLabel.config(font=("Century", 15))
equationLabel.pack(fill=tk.X)

# Entry slot 1
equation_entry_frame1 = tk.Frame(master=frameEquation)
equation_entry_frame1.pack(fill=tk.X)
colour_frame1 = tk.Frame(width=20, height=20, bg=colorDecider.get(0).get(0, "black"), master=equation_entry_frame1)
colour_frame1.pack(fill=tk.X, side=tk.LEFT)
equation_entry1 = tk.Entry(master=equation_entry_frame1)
equation_entry1.pack(fill=tk.X)
equation_entry_list.append(equation_entry1)

# entry slot 2
equation_entry_frame2 = tk.Frame(master=frameEquation)
equation_entry_frame2.pack(fill=tk.X)
colour_frame2 = tk.Frame(width=20, height=20, bg=colorDecider.get(0).get(1, "black"), master=equation_entry_frame2)
colour_frame2.pack(fill=tk.X, side=tk.LEFT)
equation_entry2 = tk.Entry(master=equation_entry_frame2)
equation_entry2.pack(fill=tk.X)
equation_entry_list.append(equation_entry2)

# entry slot 3
equation_entry_frame3 = tk.Frame(master=frameEquation)
equation_entry_frame3.pack(fill=tk.X)
colour_frame3 = tk.Frame(width=20, height=20, bg=colorDecider.get(0).get(2, "black"), master=equation_entry_frame3)
colour_frame3.pack(fill=tk.X, side=tk.LEFT)
equation_entry3 = tk.Entry(master=equation_entry_frame3)
equation_entry3.pack(fill=tk.X)
equation_entry_list.append(equation_entry3)

# entry slot 4
equation_entry_frame4 = tk.Frame(master=frameEquation)
equation_entry_frame4.pack(fill=tk.X)
colour_frame4 = tk.Frame(width=20, height=20, bg=colorDecider.get(0).get(3, "black"), master=equation_entry_frame4)
colour_frame4.pack(fill=tk.X, side=tk.LEFT)
equation_entry4 = tk.Entry(master=equation_entry_frame4)
equation_entry4.pack(fill=tk.X)
equation_entry_list.append(equation_entry4)

# entry slot 5
equation_entry_frame5 = tk.Frame(master=frameEquation)
equation_entry_frame5.pack(fill=tk.X)
colour_frame5 = tk.Frame(width=20, height=20, bg=colorDecider.get(0).get(4, "black"), master=equation_entry_frame5)
colour_frame5.pack(fill=tk.X, side=tk.LEFT)
equation_entry5 = tk.Entry(master=equation_entry_frame5)
equation_entry5.pack(fill=tk.X)
equation_entry_list.append(equation_entry5)

SchemeLabel = tk.Label(master=frameEquation, text="Color Scheme")
SchemeLabel.config(font=("Century", 15))
SchemeLabel.pack(fill=tk.X)
 
schemeChosen = tk.ttk.Combobox(state="readonly", master=frameEquation) 
  
# Adding combobox drop down list 
schemeChosen['values'] = ("Default Scheme", "Red Scheme", "Blue Scheme", "Green Scheme", "Complementary Scheme") 
schemeChosen.pack(fill=tk.X)
schemeChosen.current(0)
schemeChosen.bind("<<ComboboxSelected>>", changeColorScheme)

InstructionLabel11 = tk.Label(master=frameEquation, text="Use the scrollwheel to change magnification")
InstructionLabel11.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel10 = tk.Label(master=frameEquation, text="WASD can also be used for movement")
InstructionLabel10.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel9 = tk.Label(master=frameEquation, text="Drag and drop within the graphing paper to move")
InstructionLabel9.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel8 = tk.Label(master=frameEquation, text="Same applies for logarithms. Eg- log(x)")
InstructionLabel8.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel7 = tk.Label(master=frameEquation, text="Eg: sin(x), cos(x), sec(x), csc(x), tan(x), cot(x)")
InstructionLabel7.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel6 = tk.Label(master=frameEquation, text="For trignometry encapsulate using brackets")
InstructionLabel6.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel5 = tk.Label(master=frameEquation, text="For exponents, use ^, like x^2 for x square")
InstructionLabel5.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel4 = tk.Label(master=frameEquation, text="For multiplication, use *, like (x+3)*2 for 2(x+3)")
InstructionLabel4.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel3 = tk.Label(master=frameEquation, text="Write equations in the format y=..... with x as variable")
InstructionLabel3.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel2 = tk.Label(master=frameEquation, text="Press 'Escape' to Clear Graph")
InstructionLabel2.pack(fill=tk.X, side=tk.BOTTOM)
InstructionLabel1 = tk.Label(master=frameEquation, text="Press 'Enter' to Plot Graph")
InstructionLabel1.pack(fill=tk.X, side=tk.BOTTOM)
InstructionHeading= tk.Label(master=frameEquation, text="Instructions")
InstructionHeading.config(font=("Century", 15))
InstructionHeading.pack(fill=tk.X, side=tk.BOTTOM)

# intervalLabel = tk.Label(master=frameEquation, text="Enter the interval Value")
# intervalLabel.pack(fill=tk.X)


# interval_entry = tk.Entry(master=frameEquation)
# interval_entry.pack(fill=tk.X)

# #Buttons
# clear_button = tk.Button(master=frameEquation, text="Clear Graph")
# clear_button.pack(fill=tk.X, side=tk.BOTTOM)
# clear_button.bind("<Button-1>", clearGraphs)  

# create_graph_button = tk.Button(master=frameEquation, text="Create Graph")
# create_graph_button.pack(fill=tk.X, side=tk.BOTTOM)
# create_graph_button.bind("<Button-1>", createGraphProcess)


#Graphing Tab UI
graphingCanvas = tk.Canvas(master=frameGraph, bg="white", width=600, height=600)
graphingCanvas.pack(fill="both", expand=True)
canvasHeight = int(graphingCanvas.cget("height"))
canvasWidth = int(graphingCanvas.cget("width"))

graphingCanvas.bind("<Enter>", bound_to_actions)
graphingCanvas.bind("<Leave>", unbound_to_actions)

createGraphingPaper()

window.mainloop()


