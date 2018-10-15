import sys
import pandas as pd
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import colors,markers
import six
import ntpath
from os.path import basename, splitext, dirname
from math import log
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

CONFIGURATION="Q3"
Y_SCALE_BARS="nb_candidates_subgroups"


FONTSIZE = 50
LEGENDFONTSIZE = 35
MARKERSIZE = 10
LINEWIDTH = 8
FIGSIZE=(20, 11) #Q1  (20, 7) #Q2  (20, 11) #Q3 (20, 11)
LOG_SCALE_X=False
WIDTHOFBARS=0.6
NB_VALUES_TO_PINCH=1000
XAXISVALUE_REDUCEPRECISION=False
Y_SCALE_BARS="nb_visited_subgroups"
TIME_NORMALIZE=False

dict_map={
	"nb_attributes":r'$'+"nb_{Attributes}"+'$',
	"memory":"Memory MiB",
	"AVG-MEMORY":"Memory MiB",
	"timespent":"timespent (s)",
	"quality":"Collective Wracc",
	"nb_patterns":r'$'+"nb_{Patterns}"+'$',
	"fssd":"FSSD",
	"naive":"BASELINE",
	"AVG-TIMESPENT":r'$'+"Timespent"+'$',
	'AVG-NB-PATTERNS':r'$'+"avg_{\#patterns}"+'$',
	'indiceDataset':r'$'+"{Dataset}"+'$',
	'indiceDatasetQ1Q2':r'$'+"{Dataset}$-$\#{Attributes}"+'$',
	'AVG-QUALITY':r'$'+"avg_{Quality}"+'$',
	'PERCENTAGE-QUAL':r'$'+"\%{Quality}"+'$',
}

if CONFIGURATION=="Q1":
	FONTSIZE = 50
	LEGENDFONTSIZE = 35
	MARKERSIZE = 10
	LINEWIDTH = 8
	FIGSIZE=(20, 7) #Q1  (20, 7) #Q2  (20, 11) #Q3 (20, 11)
	LOG_SCALE_X=False
	WIDTHOFBARS=0.6
	NB_VALUES_TO_PINCH=1000
	XAXISVALUE_REDUCEPRECISION=False
	Y_SCALE_BARS="nb_visited_subgroups"
	TIME_NORMALIZE=False

	dict_map={
		"nb_attributes":r'$'+"nb_{Attributes}"+'$',
		"memory":"Memory MiB",
		"AVG-MEMORY":"Memory MiB",
		"timespent":"timespent (s)",
		"quality":"Collective Wracc",
		"nb_patterns":r'$'+"nb_{Patterns}"+'$',
		"fssd":"FSSD",
		"naive":"BASELINE",
		"AVG-TIMESPENT":r'$'+"Timespent"+'$',
		'AVG-NB-PATTERNS':r'$'+"avg_{\#patterns}"+'$',
		'indiceDatasetQ1Q2':r'$'+"{Dataset}"+'$',
		'indiceDataset':r'$'+"{Dataset}$-$\#{Attributes}"+'$',
		'AVG-QUALITY':r'$'+"avg_{Quality}"+'$',
		'PERCENTAGE-QUAL':r'$'+"\%{Quality}"+'$',
	}

if CONFIGURATION=="Q2":
	FONTSIZE = 50
	LEGENDFONTSIZE = 35
	MARKERSIZE = 10
	LINEWIDTH = 8
	FIGSIZE=(20, 11) #Q1  (20, 7) #Q2  (20, 11) #Q3 (20, 11)
	LOG_SCALE_X=False
	WIDTHOFBARS=0.6
	NB_VALUES_TO_PINCH=1000
	XAXISVALUE_REDUCEPRECISION=False
	Y_SCALE_BARS="nb_visited_subgroups"
	TIME_NORMALIZE=False

	dict_map={
		"nb_attributes":r'$'+"nb_{Attributes}"+'$',
		"memory":"Memory MiB",
		"AVG-MEMORY":"Memory MiB",
		"timespent":"timespent (s)",
		"quality":"Collective Wracc",
		"nb_patterns":r'$'+"nb_{Patterns}"+'$',
		"fssd":"FSSD",
		"naive":"BASELINE",
		"AVG-TIMESPENT":r'$'+"Timespent"+'$',
		'AVG-NB-PATTERNS':r'$'+"avg_{\#patterns}"+'$',
		'indiceDatasetQ1Q2':r'$'+"{Dataset}"+'$',
		'indiceDataset':r'$'+"{Dataset}$-$\#{Attributes}"+'$',
		'AVG-QUALITY':r'$'+"avg_{Quality}"+'$',
		'PERCENTAGE-QUAL':r'$'+"\%{Quality}"+'$',
	}

if CONFIGURATION=="Q3":
	FONTSIZE = 50
	LEGENDFONTSIZE = 35
	MARKERSIZE = 10
	LINEWIDTH = 8
	FIGSIZE=(20, 11) #Q1  (20, 7) #Q2  (20, 11) #Q3 (20, 11)
	LOG_SCALE_X=False
	WIDTHOFBARS=0.6
	NB_VALUES_TO_PINCH=1000
	XAXISVALUE_REDUCEPRECISION=False
	Y_SCALE_BARS="nb_visited_subgroups"
	TIME_NORMALIZE=False

	dict_map={
		"nb_attributes":r'$'+"nb_{Attributes}"+'$',
		"memory":"Memory MiB",
		"AVG-MEMORY":"Memory MiB",
		"timespent":"timespent (s)",
		"quality":"Collective Wracc",
		"nb_patterns":r'$'+"nb_{Patterns}"+'$',
		"fssd":"FSSD",
		"naive":"BASELINE",
		"AVG-TIMESPENT":r'$'+"Timespent"+'$',
		'AVG-NB-PATTERNS':r'$'+"avg_{\#patterns}"+'$',
		'indiceDataset':r'$'+"{Dataset}"+'$',
		'indiceDatasetQ1Q2':r'$'+"{Dataset}$-$\#{Attributes}"+'$',
		'AVG-QUALITY':r'$'+"avg_{Quality}"+'$',
		'PERCENTAGE-QUAL':r'$'+"\%{Quality}"+'$',
	}

# if CONFIGURATION=="Q1": #HMT TO ITEMSET
# 	FONTSIZE = 50
# 	LEGENDFONTSIZE = 35
# 	MARKERSIZE = 10
# 	LINEWIDTH = 8
# 	FIGSIZE=(18.5, 9)
# 	LOG_SCALE_X=False
# 	WIDTHOFBARS=0.6
# 	NB_VALUES_TO_PINCH=100
# 	XAXISVALUE_REDUCEPRECISION=False
# 	Y_SCALE_BARS="nb_visited_subgroups"
# 	TIME_NORMALIZE=False

# if CONFIGURATION=="Q2": #COMAPRING ALGORITHMS
# 	FONTSIZE = 50
# 	LEGENDFONTSIZE = 35
# 	MARKERSIZE = 10
# 	LINEWIDTH = 8
# 	FIGSIZE=(18.5, 7)
# 	LOG_SCALE_X=False
# 	WIDTHOFBARS=0.6
# 	NB_VALUES_TO_PINCH=100
# 	XAXISVALUE_REDUCEPRECISION=False
# 	Y_SCALE_BARS="nb_candidates_subgroups"
# elif CONFIGURATION=="Q3": #SCALING
# 	FONTSIZE = 50
# 	LEGENDFONTSIZE = 35
# 	MARKERSIZE = 10
# 	LINEWIDTH = 8
# 	FIGSIZE=(11.5, 7)
# 	LOG_SCALE_X=True
# 	WIDTHOFBARS=0.3
# 	NB_VALUES_TO_PINCH=5
# 	XAXISVALUE_REDUCEPRECISION=True
# 	Y_SCALE_BARS="nb_candidates_subgroups"
# 	#Y_SCALE_BARS="nb_visited_subgroups"
# elif CONFIGURATION=="Q4": #Sampling
# 	FONTSIZE = 40
# 	LEGENDFONTSIZE = 32
# 	MARKERSIZE = 8
# 	LINEWIDTH = 7
# 	FIGSIZE=(13, 6)#(15, 8)
# 	LOG_SCALE_X=False
# 	WIDTHOFBARS=0.3
# 	NB_VALUES_TO_PINCH=5
# 	XAXISVALUE_REDUCEPRECISION=False
# 	Y_SCALE_BARS="nb_candidates_subgroups"


LEGEND=False
SHOWPLOT=False
TIMETHRESHOLD=7000


#332288, 88CCEE, 44AA99, 117733, 999933, DDCC77, CC6677, 882255, AA4499, #117733
optNames={(True,True,1):"DSC+CLOSED+UB1",(True,True,2):"DSC+CLOSED+UB2",(True,False):"DSC+CLOSED",(False,True,1):"UB1",(False,True,2):"UB2",(False,False):"DSC"}
optNamesReversed={v:k for k,v in optNames.items()}


colorByOptBars =  {"groundtruth":"#34495e","fssd":"#117733","naive":"#D64541", "DSSD":"#DDCC77","MCTS4DM":"#e67e22","BSD":"#2980b9","CN2SD":"#9b59b6"}
colorByOptLines =  {"groundtruth":"#34495e","fssd":"#117733","naive":"#D64541", "DSSD":"#DDCC77","MCTS4DM":"#e67e22","BSD":"#2980b9","CN2SD":"#9b59b6"}
colorByOptEdge =  {"groundtruth":None,"fssd":None,"naive":None, "DSSD":None,"MCTS4DM":None,"BSD":None,"CN2SD":None}
markerByOpt = {"groundtruth":"D","fssd":"D","naive":"D", "DSSD":"D","MCTS4DM":"D","BSD":"D","CN2SD":"D"}#{"DISSENT":"D","CONSENT":"D","ITEMSET":"D","HMT":"D","DSC+CLOSED+UB1":"D","DSC+CLOSED+UB2":"D", "DSC+CLOSED" : "^", "UB1":"o","UB2":"o", "DSC":"o","DSC+RandomWalk":'D',"DSC+SamplingPeers+RandomWalk":'D'}
lineTypeByOpt = {"groundtruth":"-","fssd":"-","naive":"-", "DSSD":"-","MCTS4DM":"-","BSD":"-","CN2SD":"-"}#{"DISSENT":"-","CONSENT":"-","ITEMSET":"-","HMT":"-","DSC+CLOSED+UB1":"-","DSC+CLOSED+UB2":"-", "DSC+CLOSED" : "-", "UB1":"--","UB2":"--", "DSC":"-","DSC+RandomWalk":'-',"DSC+SamplingPeers+RandomWalk":'-'}
hatchTypeByOpt = {"groundtruth":"","fssd":"/","naive":"..", "DSSD":"x","MCTS4DM":"-","BSD":"--","CN2SD":"//"}#{"DISSENT":"","CONSENT":"","ITEMSET":"","HMT":"","DSC+CLOSED+UB1":"","DSC+CLOSED+UB2":"", "DSC+CLOSED" : "....", "UB1":"///","UB2":"///", "DSC":"x","DSC+RandomWalk":"","DSC+SamplingPeers+RandomWalk":""}







def plot_Q1(testResultFile,varcolumn,show_legend=True,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False): #QUALITY
	x=1


def plot_Q2(testResultFile,var_column,target_bars,target_lines,plot_bars = True, plot_curves = True,show_legend=True,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False,file_to_draw_in=None,methods_to_print=None): #MEMORY/VISITED + TIME
	
	PLOT_FIXED=True
	var_column_to_get_label=var_column
	fileparent = dirname(testResultFile)
	filename = splitext(basename(testResultFile))[0]
	exportPath = (fileparent+"/" if len(fileparent) > 0 else "")+filename+".pdf"
	if file_to_draw_in is not None:
		exportPath=(fileparent+"/" if len(fileparent) > 0 else "")+file_to_draw_in+".pdf"
	basedf = pd.read_csv(testResultFile,sep='\t',header=0)
	
	xAxis = np.array(sorted(set(basedf[var_column])))
	if len(xAxis)>NB_VALUES_TO_PINCH:
		xAxis=np.array(sorted([xAxis[len(xAxis)-1-int(round((k/float(NB_VALUES_TO_PINCH))*len(xAxis)))] for k in range(NB_VALUES_TO_PINCH)]))
		xAxis_set=set(xAxis)
		print (xAxis_set)
	xAxisFixed = range(1,len(xAxis)+1)
	if PLOT_FIXED:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxisFixed)}
	else:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxis)}
	#print (set(basedf["method"]))
	activated=list(set(basedf["method"]))
	if methods_to_print is not None:
		activated=methods_to_print
	optCount = len(activated)
	barWidth = np.float64(WIDTHOFBARS/optCount) #Affects space between bars
	offset = -barWidth*(optCount-1)/2
	fig, baseAx = plt.subplots(figsize=FIGSIZE)
	baseAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column),fontsize=FONTSIZE)
	baseAx.set_xlim([0,max(xAxisFixed)+1])
	baseAx.tick_params(axis='x', labelsize=FONTSIZE-10)
	baseAx.tick_params(axis='y', labelsize=FONTSIZE)
	plt.xticks(rotation=rotateDegree)
	
	
	if plot_bars : 
		barsAx = baseAx
		#barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
		
		# if CONFIGURATION=="Q1":
		# 	barsAx.set_ylabel(r'\#explored $\times 10^6$',fontsize=FONTSIZE)
		# else:
		# 	barsAx.set_ylabel(r'\#evaluated',fontsize=FONTSIZE)
		
		barsAx.set_ylabel(dict_map.get(target_bars,target_bars),fontsize=FONTSIZE)
		if BAR_LOG_SCALE : barsAx.set_yscale("log",basey=10)
		else: barsAx.set_yscale("linear")
		barsAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column),fontsize=FONTSIZE)
		#barsAx.set_ylim([0,1.2*np.amax(basedf["#all_visited_context"])])
		#barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

	if plot_curves :
		if plot_bars :
			timeAx = baseAx.twinx()
			timeAx.yaxis.tick_left()
			timeAx.yaxis.set_label_position("left")
			barsAx.yaxis.tick_right()
			barsAx.yaxis.set_label_position("right")
		else :
			timeAx = baseAx 

		# if CONFIGURATION=="Q1" and TIME_NORMALIZE: 
		# 	timeAx.set_ylabel(r'Time (s) $\times 10^3$',fontsize=FONTSIZE)   
		# else:
		# 	timeAx.set_ylabel("Execution time (s)",fontsize=FONTSIZE) 

		timeAx.set_ylabel(dict_map.get(target_lines,target_lines),fontsize=FONTSIZE) 
		if TIME_LOG_SCALE : timeAx.set_yscale("log",basey=10)
		else: timeAx.set_yscale("linear")
		timeAx.tick_params(axis='y', labelsize=FONTSIZE)
		if PLOT_FIXED:
			timeAx.set_xlim([0,max(xAxisFixed)+1])
	
	if plot_bars and not plot_curves:
		timeAx = baseAx 
		# timeAx.yaxis.tick_left()
		# timeAx.yaxis.set_label_position("left")
		barsAx.yaxis.tick_right()
		barsAx.yaxis.set_label_position("right")
	
	plt.xticks(xAxisFixed,xAxis)#, rotation='vertical')
	#varVectorX = np.array(basedf[basedf["algorithm"]==activated[-1]][var_column])
	distinctVarVectorX = sorted(set(xAxis))
	distinctVarVectorX_adapted=distinctVarVectorX
	# if XAXISVALUE_REDUCEPRECISION:
	# 	divide_by_exponent=(int(log(float(distinctVarVectorX[-1]),10))/3)*3
	# 	distinctVarVectorX_adapted=[float("%.2f"% (float(x)/(10**divide_by_exponent))) for x in distinctVarVectorX]
	# 	if divide_by_exponent>0:
	# 		barsAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column)+ r' $\times10^'+str(divide_by_exponent)+'$',fontsize=FONTSIZE)

		#r'$'+item+'^'+(('%.f'%((float(str(item))/exauhaustive_time_spent)*100))+'\%')+'$' 
	if False:
		timeAx.set_xticklabels([r'$'+str(x if x!=int(x) else int(x))+'$'  for x in distinctVarVectorX_adapted])
	# if LOG_SCALE_X : 
	# 	timeAx.set_xscale("linear")
		#barsAx.set_xscale("linear")

	for optName in activated:
		
		df = basedf[basedf["method"]==optName]
		LabelOptName=dict_map.get(optName,optName)
		varVector = np.array(df[var_column])
		#print varVector
		if len(varVector)>NB_VALUES_TO_PINCH:
			#varVector=[varVector[int(round((k/float(NB_VALUES_TO_PINCH))*len(varVector)))] for k in range(NB_VALUES_TO_PINCH)]
			varVector=sorted(set(varVector)&xAxis_set)
		#raw_input('...')
		distinctVarVector = sorted(set(varVector))

		distinctVarVectorFixed = [xAxisMapping[x] for x in distinctVarVector]
		nbVisitedVector = np.array(list(map(np.max, [df[df[var_column]==element][target_bars] for element in distinctVarVector])))
		print(optName,nbVisitedVector)
		execTimeVector = np.array(list(map(np.max, [df[df[var_column]==element][target_lines] for element in distinctVarVector])))
		execMeanTimeVector = execTimeVector
		execErrorTimeVector = 0
		if len(distinctVarVectorFixed)>0:
			if plot_bars : 
				# if CONFIGURATION=="Q1":
				# 	barsAx.bar(distinctVarVectorFixed+offset, np.array([x/float(10**6) for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOptBars[optName],label=optName,edgecolor=colorByOptEdge[optName],alpha=0.8)
				# else:
				barsAx.bar(distinctVarVectorFixed+offset, np.array([x for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOptBars[optName],label=LabelOptName,edgecolor=colorByOptEdge[optName],alpha=0.8)
			
			if plot_curves : 
				#timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH+2,markersize=MARKERSIZE,label=optName, color= 'black')
				# if CONFIGURATION=="Q1" and TIME_NORMALIZE:
				# 	timeAx.errorbar(distinctVarVectorFixed, np.array([x/float(10**3) for x in execMeanTimeVector]), yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=LabelOptName, color= colorByOptLines[optName])
				# else:
				timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=LabelOptName, color= colorByOptLines[optName])

			if show_legend : 
				legend = timeAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) if plot_curves else barsAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) #'upper left' 'lower right'
				timeAx.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=5,fancybox=True,fontsize=LEGENDFONTSIZE, framealpha=0.85)
		offset+=barWidth
	
	#timeAx.set_yticklabels([r'$'+str(x)+'$' for x in timeAx.get_yticklabels()])
	#timeAx.set_xticklabels([r'$'+str(x)+'$' for x in distinctVarVectorX])

	fig.tight_layout()
	
	plt.savefig(exportPath)
	if SHOWPLOT : plt.show()

def plot_Q3(testResultFile,varcolumn_bars,varcolumn_lines,plot_bars = True, plot_curves = True,show_legend=True,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False): #Quality + TIME
	X=1



def plotPerf(testResultFile, var_column, activated = list(optNames.values()), plot_bars = True, plot_time = True,show_legend=True,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False) :
	PLOT_FIXED=True
	var_column_to_get_label=var_column
	if var_column[:7]=='CONSENT' or var_column[:5]=='RATIO':
		var_column='quality_threshold'

	if not plot_bars and not plot_time : raise Exception("Are you kidding me ?")
	fileparent = dirname(testResultFile)
	filename = splitext(basename(testResultFile))[0]
	exportPath = (fileparent+"/" if len(fileparent) > 0 else "")+filename+".pdf"
	basedf = pd.read_csv(testResultFile,sep='\t',header=0)
	xAxis = np.array(sorted(set(basedf[var_column])))
	xAxis_set=set(xAxis)
	if len(xAxis)>NB_VALUES_TO_PINCH:
		xAxis=np.array(sorted([xAxis[len(xAxis)-1-int(round((k/float(NB_VALUES_TO_PINCH))*len(xAxis)))] for k in range(NB_VALUES_TO_PINCH)]))
		xAxis_set=set(xAxis)
		print (xAxis_set)
	xAxisFixed = range(1,len(xAxis)+1)
	if PLOT_FIXED:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxisFixed)}
	else:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxis)}
	optCount = len(activated)
	barWidth = np.float64(WIDTHOFBARS/optCount) #Affects space between bars
	offset = -barWidth*(optCount-1)/2
	fig, baseAx = plt.subplots(figsize=FIGSIZE)
	baseAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column),fontsize=FONTSIZE)
	baseAx.set_xlim([0,max(xAxisFixed)+1])
	baseAx.tick_params(axis='x', labelsize=FONTSIZE)
	baseAx.tick_params(axis='y', labelsize=FONTSIZE)
	plt.xticks(rotation=rotateDegree)
	
	
	if plot_bars : 
		barsAx = baseAx
		#barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
		
		if CONFIGURATION=="Q1":
			barsAx.set_ylabel(r'\#explored $\times 10^6$',fontsize=FONTSIZE)
		else:
			barsAx.set_ylabel(r'\#evaluated',fontsize=FONTSIZE)
		

		if BAR_LOG_SCALE : barsAx.set_yscale("log",basey=10)
		else: barsAx.set_yscale("linear")
		barsAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column),fontsize=FONTSIZE)
		#barsAx.set_ylim([0,1.2*np.amax(basedf["#all_visited_context"])])
		#barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

	if plot_time :
		if plot_bars :
			timeAx = baseAx.twinx()
			timeAx.yaxis.tick_left()
			timeAx.yaxis.set_label_position("left")
			barsAx.yaxis.tick_right()
			barsAx.yaxis.set_label_position("right")
		else :
			timeAx = baseAx 

		if CONFIGURATION=="Q1" and TIME_NORMALIZE: 
			timeAx.set_ylabel(r'Time (s) $\times 10^3$',fontsize=FONTSIZE)   
		else:
			timeAx.set_ylabel("Execution time (s)",fontsize=FONTSIZE) 


		if TIME_LOG_SCALE : timeAx.set_yscale("log",basey=10)
		else: timeAx.set_yscale("linear")
		timeAx.tick_params(axis='y', labelsize=FONTSIZE)
		if PLOT_FIXED:
			timeAx.set_xlim([0,max(xAxisFixed)+1])
		
	
	plt.xticks(xAxisFixed,xAxis, rotation='vertical')
	#varVectorX = np.array(basedf[basedf["algorithm"]==activated[-1]][var_column])
	distinctVarVectorX = sorted(set(xAxis))
	distinctVarVectorX_adapted=distinctVarVectorX
	if XAXISVALUE_REDUCEPRECISION:
		divide_by_exponent=(int(log(float(distinctVarVectorX[-1]),10))/3)*3
		distinctVarVectorX_adapted=[float("%.2f"% (float(x)/(10**divide_by_exponent))) for x in distinctVarVectorX]
		if divide_by_exponent>0:
			barsAx.set_xlabel(dict_map.get(var_column_to_get_label,var_column)+ r' $\times10^'+str(divide_by_exponent)+'$',fontsize=FONTSIZE)

		#r'$'+item+'^'+(('%.f'%((float(str(item))/exauhaustive_time_spent)*100))+'\%')+'$' 

	timeAx.set_xticklabels([r'$'+str(x if x!=int(x) else int(x))+'$'  for x in distinctVarVectorX_adapted])
	# if LOG_SCALE_X : 
	# 	timeAx.set_xscale("linear")
		#barsAx.set_xscale("linear")

	for optName in activated:
		
		df = basedf[basedf["algorithm"]==optName]
		LabelOptName=dict_map.get(optName,optName)
		varVector = np.array(df[var_column])
		#print varVector
		if len(varVector)>NB_VALUES_TO_PINCH:
			#varVector=[varVector[int(round((k/float(NB_VALUES_TO_PINCH))*len(varVector)))] for k in range(NB_VALUES_TO_PINCH)]
			varVector=sorted(set(varVector)&xAxis_set)
		#raw_input('...')
		distinctVarVector = sorted(set(varVector))

		distinctVarVectorFixed = [xAxisMapping[x] for x in distinctVarVector]
		nbVisitedVector = np.array(map(np.max, [df[df[var_column]==element][Y_SCALE_BARS] for element in distinctVarVector]))
		execTimeVector = np.array(map(np.max, [df[df[var_column]==element]["timespent"] for element in distinctVarVector]))
		execMeanTimeVector = execTimeVector
		execErrorTimeVector = 0
		if len(distinctVarVectorFixed)>0:
			if plot_bars : 
				if CONFIGURATION=="Q1":
					barsAx.bar(distinctVarVectorFixed+offset, np.array([x/float(10**6) for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOptBars[optName],label=optName,edgecolor=colorByOptEdge[optName],alpha=0.8)
				else:
					barsAx.bar(distinctVarVectorFixed+offset, np.array([x for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOptBars[optName],label=LabelOptName,edgecolor=colorByOptEdge[optName],alpha=0.8)
			
			if plot_time : 
				#timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH+2,markersize=MARKERSIZE,label=optName, color= 'black')
				if CONFIGURATION=="Q1" and TIME_NORMALIZE:
					timeAx.errorbar(distinctVarVectorFixed, np.array([x/float(10**3) for x in execMeanTimeVector]), yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=LabelOptName, color= colorByOptLines[optName])
				else:
					timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=LabelOptName, color= colorByOptLines[optName])

			if show_legend : 
				legend = timeAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) if plot_time else barsAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) #'upper left' 'lower right'
				timeAx.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3,fancybox=True,fontsize=LEGENDFONTSIZE, framealpha=0.85)
		offset+=barWidth
	
	#timeAx.set_yticklabels([r'$'+str(x)+'$' for x in timeAx.get_yticklabels()])
	#timeAx.set_xticklabels([r'$'+str(x)+'$' for x in distinctVarVectorX])

	fig.tight_layout()
	
	plt.savefig(exportPath)
	if SHOWPLOT : plt.show()


def plotRW(testResultFile, var_column, activated = list(optNames.values()), plot_bars = False, plot_time = True,show_legend=True,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False,sampling_algorithm='DSC+RandomWalk') :
	PLOT_FIXED=False
	YLABEL=""#'Similarity'
	if not plot_bars and not plot_time : raise Exception("Are you kidding me ?")
	fileparent = dirname(testResultFile)
	filename = splitext(basename(testResultFile))[0]
	exportPath = (fileparent+"/" if len(fileparent) > 0 else "")+filename+".pdf"
	basedf = pd.read_csv(testResultFile,sep='\t',header=0)
	xAxis = np.array(sorted(set(basedf[basedf["algorithm"]==activated[0]][var_column])))
	xAxisFixed = range(1,len(xAxis)+1)
	if PLOT_FIXED:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxisFixed)}
	else:
		xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxis)}
	optCount = len(activated)
	barWidth = np.float64(0.3/optCount) #Affects space between bars
	offset = -barWidth*(optCount-1)/2
	#FIGSIZE2=(13, 6)
	fig, baseAx = plt.subplots(figsize=FIGSIZE)
	#baseAx.set_xlabel(dict_map.get(var_column,var_column),fontsize=FONTSIZE)
	#baseAx.set_xlabel(r'$timespent(s)_{exhaustive\_time\%}$',fontsize=FONTSIZE-5)
	baseAx.set_xlabel(r'$timespent (s)$',fontsize=FONTSIZE-5)
	if PLOT_FIXED:
		baseAx.set_xlim([0,max(xAxisFixed)+1])
	baseAx.tick_params(axis='x', labelsize=FONTSIZE)
	baseAx.tick_params(axis='y', labelsize=FONTSIZE)
	#print rotateDegree
	#plt.xticks(rotation=rotateDegree)
	
	
	if plot_bars : 
		barsAx = baseAx
		barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
		barsAx.set_ylabel("#nb_patterns_found",fontsize=FONTSIZE)
		if BAR_LOG_SCALE : barsAx.set_yscale("log",basey=10)
		barsAx.set_xlabel(dict_map.get(var_column,var_column),fontsize=FONTSIZE)
		#barsAx.set_ylim([0,1.2*np.amax(basedf["#all_visited_context"])])
		barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

	if plot_time :
		if plot_bars :
			timeAx = baseAx.twinx()
			timeAx.yaxis.tick_left()
			timeAx.yaxis.set_label_position("left")
			barsAx.yaxis.tick_right()
			barsAx.yaxis.set_label_position("right")
		else :
			timeAx = baseAx  
		timeAx.set_ylabel(YLABEL,fontsize=FONTSIZE)    
		if TIME_LOG_SCALE : timeAx.set_yscale("log",basey=10)
		timeAx.tick_params(axis='y', labelsize=FONTSIZE)
		if PLOT_FIXED:
			timeAx.set_xlim([0,max(xAxisFixed)+1])
		else:
			print (xAxis)
			timeAx.set_xlim([min(xAxis)-5.,max(xAxis)+5.])
	if PLOT_FIXED:
		plt.xticks(xAxisFixed,xAxis, rotation='vertical')
	else:
		plt.xticks(xAxis,xAxis, rotation='vertical')
	colors=[ '#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
	ind_color=0
	

	exauhaustive_time_spent=float(basedf[basedf["algorithm"]=='DSC+CLOSED+UB2']['timespent'][0])
	
	# old_labels=['%.f'%float(str(item.get_text()))  for item in timeAx.get_xticklabels()][:]
	# labels = [('%.f'%((float(str(item))/exauhaustive_time_spent)*100))+'\%'  for item in old_labels]
	# labels = [r'$'+item+'_{'+ itemnew+'}$'  for item,itemnew in zip(old_labels,labels)]
	# timeAx.set_xticklabels(labels)

	#LOG_SCALE_X=True
	if LOG_SCALE_X : timeAx.set_xscale("log",basey=10)#timeAx.set_xscale("log",basey=10)#
	else: timeAx.set_xscale("linear")
	#labels = [r'$'+item+'^'+(('%.f'%((float(str(item))/exauhaustive_time_spent)*100))+'\%')+'$'  for item in old_labels]
	#labels=[r"$"+x+"$" for x in labels]
	#print old_labels
	#print labels
	for optName in activated:
		for target in ['precision','recall','f1_score']: 
			target_label=dict_map.get(target,target)
			df = basedf[basedf["algorithm"]==optName]

			varVector = np.array(df[var_column])
			
			distinctVarVector = sorted(set(varVector))

			distinctVarVectorFixed = [xAxisMapping[x] for x in distinctVarVector]
			#print distinctVarVectorFixed
			nbVisitedVector = np.array(map(np.max, [df[df[var_column]==element]["nb_patterns"] for element in distinctVarVector]))
			execTimeVector = np.array(map(np.max, [df[df[var_column]==element][target] for element in distinctVarVector]))
			execMeanTimeVector = execTimeVector
			
			

			execErrorTimeVector = 0
			if len(distinctVarVectorFixed)>0:
				if plot_bars : 
					barsAx.bar(distinctVarVectorFixed+offset, np.array([x for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOptBars[optName],label=optName,edgecolor=colorByOptEdge[optName],alpha=0.8)
				if plot_time : 
					#timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH+2,markersize=MARKERSIZE,label=optName, color= 'black')
					#timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=target, color= colorByOptLines[optName])
					timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=target_label,color=colors[ind_color])
					timeAx.set_ylim([-0.05,1.05])
					
					timeAx.axvline(exauhaustive_time_spent, 0, 1,color="red",linewidth=2.5,linestyle="--",markersize=10)
					# timeAx.axvline(3600, 0, 1,color="green",linewidth=2.5,linestyle="--",markersize=10)
					# timeAx.axhline(0.8, 0, 1,color="green",linewidth=2.5,linestyle="--",markersize=10)


				if show_legend : 
					legend = timeAx.legend(loc='lower left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) if plot_time else barsAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE, framealpha=0.7) #'upper left' 'lower right'
					timeAx.legend(loc='lower center', bbox_to_anchor=(0.5, 0.01),ncol=3,fancybox=True,fontsize=LEGENDFONTSIZE, framealpha=0.85)
			offset+=barWidth
			ind_color+=1
	
	plt.xticks(rotation=rotateDegree)
	fig.tight_layout()
	plt.savefig(exportPath)
	fig.tight_layout()
	if SHOWPLOT : plt.show()



def plot_bars_vector(vector,exportPath):
	N = 5
	#vector = (20, 35, 30, 35, 27)
	
	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars

	fig, ax = plt.subplots(figsize=(14, 5))
	rects1 = ax.bar(ind, vector, width, color='#5f27cd',alpha=0.8,hatch='//')




	ax.set_ylabel('nb outcomes',fontsize=42)
	ax.set_xlabel('scores',fontsize=42)
	ax.set_ylim([0.,max(vector)+2.])
	ax.set_xlim([-1.,N])
	#ax.set_title('Scores by group and gender')
	ax.set_xticks(ind + width / 2)

	ax.set_xticklabels(('1', '2', '3', '4', '5'))

	ax.tick_params(axis='x', labelsize=42)
	ax.tick_params(axis='y', labelsize=42)

	#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


	# def autolabel(rects):
	#     """
	#     Attach a text label above each bar displaying its height
	#     """
	#     for rect in rects:
	#         height = rect.get_height()
	#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	#                 '%d' % int(height),
	#                 ha='center', va='bottom')

	# autolabel(rects1)
	# autolabel(rects2)

	fig.tight_layout()
	plt.savefig(exportPath)
	fig.tight_layout()


def plot_bars_vector_many_populations(dict_vectors,exportPath): #dict_vectors={'pop1':v1,'pop2':v2}
	N = 5
	#vector = (20, 35, 30, 35, 27)
	
	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars
	arr_colors=['#5f27cd','#ff9f43']
	fig, ax = plt.subplots(figsize=(14, 7))
	k=0
	offset=-width/2.
	for v in dict_vectors:
		dict_vectors[v]=[(x/float(sum(dict_vectors[v])))*100. for x in dict_vectors[v]]
		vector=dict_vectors[v]
		#vector=[(x/float(sum(vector)))*100. for x in vector]
		rects1 = ax.bar(ind+offset, vector, width, color=arr_colors[k % 2],alpha=0.8,hatch='//',label=v)
		offset+=width
		k+=1

	#rects1 = ax.bar(ind, vector, width, color='#5f27cd',alpha=0.8,hatch='//',label=target_label)



	ax.set_ylabel('\% outcomes',fontsize=42)
	ax.set_xlabel('scores',fontsize=42)

	#ax.set_ylim([0.,max((max(v) for v in dict_vectors.values()))+2.])
	
	#ax.set_ylim([0.,max((max(v) for v in dict_vectors.values()))+2.])
	
	ax.set_ylim([0.,100.])
	ax.set_xlim([-1.,N])
	#ax.set_title('Scores by group and gender')
	ax.set_xticks(ind + width / 2)

	ax.set_xticklabels(('1', '2', '3', '4', '5'))

	ax.tick_params(axis='x', labelsize=42)
	ax.tick_params(axis='y', labelsize=42)

	#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


	# def autolabel(rects):
	#     """
	#     Attach a text label above each bar displaying its height
	#     """
	#     for rect in rects:
	#         height = rect.get_height()
	#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	#                 '%d' % int(height),
	#                 ha='center', va='bottom')

	# autolabel(rects1)
	# autolabel(rects2)
	#ax.legend(loc='lower left', shadow=True, fontsize=35, framealpha=0.7) #'upper left' 'lower right'
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=3,fancybox=True,fontsize=35, framealpha=0.85)

	fig.tight_layout()
	plt.savefig(exportPath)
	fig.tight_layout()




def plot_bars_vector_many_populations_openmedic(dict_vectors,exportPath,order_of_keys=None,title_for_this='- -'): #dict_vectors={'pop1':{'a1':v1,'a2':v2},'pop2':v2}
	N = len(dict_vectors.values()[0])
	#vector = (20, 35, 30, 35, 27)
	
	if order_of_keys is None:
		order_of_keys=sorted(dict_vectors.values()[0].keys())

	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars
	arr_colors=['#5f27cd','#ff9f43']
	fig, ax = plt.subplots(figsize=(14, 7))
	k=0
	offset=-width/2.
	#for v in dict_vectors:
	

	#dict_vectors[v]=[(x/float(sum(dict_vectors[v])))*100. for x in dict_vectors[v]]
	
	iterator_dict = dict_vectors.items() 
	key1,v1= next(iterator_dict)
	key2,v2= next(iterator_dict)

	vector1=[v1[x]/v2[x] for x in order_of_keys]
	vector2=[1. for x in order_of_keys]
	# print vector1
	# print vector2

	rects1 = ax.bar(ind+offset, vector1, width, color=arr_colors[k % 2],alpha=0.8,hatch='//',label=key1)
	k+=1
	offset+=width
	rects2 = ax.bar(ind+offset, vector2, width, color=arr_colors[k % 2],alpha=0.8,hatch='//',label=key2)
	offset+=width
	k+=1

	#rects1 = ax.bar(ind, vector, width, color='#5f27cd',alpha=0.8,hatch='//',label=target_label)



	#ax.set_ylabel('Ratio',fontsize=42)
	ax.set_ylabel('Ratio   ',fontsize=42)
	ax.set_xlabel(title_for_this,fontsize=42)



	#ax.set_ylim([0.,max((max(v) for v in dict_vectors.values()))+2.])
	
	ax.set_ylim([0.,max(1.+0.2,max(vector1)+max(vector1)/5.)])
	
	#ax.set_ylim([0.,100.])
	ax.set_xlim([-0.5,N])
	#ax.set_title('Scores by group and gender')
	ax.set_xticks(ind + width / 2)

	ax.set_xticklabels(order_of_keys)
	#ax.set_yticklabels([])

	ax.tick_params(axis='x', labelsize=42)
	ax.tick_params(axis='y', labelsize=42)

	#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))


	def autolabel(rects,vector_associated):
		import humanize
		"""
		Attach a text label above each bar displaying its height
		"""
		i=0
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
					humanize.intcomma(vector_associated[order_of_keys[i]]),
					ha='center', va='bottom',fontsize=30)
			i+=1

	autolabel(rects1,v1)
	autolabel(rects2,v2)
	#ax.legend(loc='lower left', shadow=True, fontsize=35, framealpha=0.7) #'upper left' 'lower right'
	ax.legend(loc='upper center', bbox_to_anchor=(0.73, 0.18),ncol=3,fancybox=True,fontsize=33, framealpha=0.85)

	fig.tight_layout()
	plt.savefig(exportPath)
	fig.tight_layout()




def plot_boxplot_chart(method_f_score_patterns={}):
    colors=[ '#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
    x_ticks=["DEBuNk","Quick-DEBuNk","COSMIC","SD-Cartesian","SD-Majority"]
    #x_ticks=sortedmethod_f_score_patterns.keys()
    usedLineWidth=1.

    # if maxY==-1:
    #     maxY=max(max(dataSias)+max(dataCenergetics)+max(dataSubspace))*1.3
    
    #MAPCOLOR={"Quick-DEBuNk":'#0E0DD5',"DEBuNk": '#187A1D',"SD-Majority": '#C7241B',"SD-Cartesian": '#38B8B5',"COSMIC": '#A616B0'}
    MAPCOLOR={"Quick-DEBuNk":'g',"DEBuNk": 'b',"SD-Majority": 'm',"SD-Cartesian": 'c',"COSMIC": 'r'}
    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
    
    plt.figure(figsize=FIGSIZE)
    #plt.clf()
    i=0
    for i,name in enumerate(sorted(method_f_score_patterns)):
    	print (method_f_score_patterns[name])
    	bpl = plt.boxplot(method_f_score_patterns[name],  positions=[i*3.0],sym='', widths=1.,medianprops={'linewidth': usedLineWidth},boxprops={'linewidth': usedLineWidth},whiskerprops={'linewidth': usedLineWidth},capprops={'linewidth': usedLineWidth},flierprops={'linewidth': usedLineWidth})
    	#print name
    #bpr = plt.boxplot(dataCenergetics, positions=np.array(range(len(dataCenergetics)))*2.0+0, sym='', widths=0.3,medianprops={'linewidth': usedLineWidth},boxprops={'linewidth': usedLineWidth},whiskerprops={'linewidth': usedLineWidth},capprops={'linewidth': usedLineWidth},flierprops={'linewidth': usedLineWidth})
    #bpg = plt.boxplot(dataSubspace, positions=np.array(range(len(dataSubspace)))*2.0+0.4, sym='', widths=0.3,medianprops={'linewidth': usedLineWidth},boxprops={'linewidth': usedLineWidth},whiskerprops={'linewidth': usedLineWidth},capprops={'linewidth': usedLineWidth},flierprops={'linewidth': usedLineWidth})
    	set_box_color(bpl, colorByOptBars['fssd']) # colors are from http://colorbrewer2.org/
    plt.plot([], colorByOptBars['fssd'], label='FSSD')

    # set_box_color(bpr, '#2C7BB6')
    # set_box_color(bpg, '#16A085')
    
    # draw temporary red and blue lines and use them to create a legend
    
    # plt.plot([], c='#2C7BB6', label=legends[1])
    # plt.plot([], c='#16A085', label=legends[2])
    #leg=plt.legend(fontsize=usedFontSize,framealpha=0.7,loc=legendsLoc)
    if False:
	    leg=plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=5,fancybox=True, framealpha=0.85,fontsize=30)
	    for legobj in leg.legendHandles:
	        legobj.set_linewidth(usedLineWidth)
    

    plt.ylabel(r'$'+"\%{Quality}"+'$', fontsize=34)
    plt.yticks(fontsize=34)    
    plt.xticks(range(0, len(method_f_score_patterns) * 3, 3), sorted(method_f_score_patterns),fontsize=27)
    plt.tick_params(axis='y', labelsize=34)
    plt.xlim(-2, len(method_f_score_patterns)*3)
    

    plt.ylim(0, 1.)
    plt.tight_layout()
    plt.savefig(".//TMP.pdf")
    