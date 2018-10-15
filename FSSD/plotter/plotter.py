

FONTSIZE = 15
MARKERSIZE = 2
LINEWIDTH = 2
def plot_timeseries(timeseries,xlogscale=False,ylogscale=False): #timeseries={'timeserieName':(x_axis_values,y_axis_values) or y_axis_values }
    
    import matplotlib.pyplot as plt
    fig,ax = plt.subplots()
    ax.set_xlim([-5,205])
    ax.set_ylim([-0.05,1.05])
    for method in  sorted(timeseries) :
        vector=timeseries[method]
    	if type(vector) is tuple:
    		iterations=vector[0]
    		vector=vector[1]
    	else:
        	iterations = range(1,len(vector)+1)

        plt.plot(iterations, vector, label=method, linewidth=LINEWIDTH)

    if xlogscale : ax.set_xscale("log")
    if ylogscale : ax.set_yscale("log")
    ax.set_xlabel("X_AXIS",fontsize=FONTSIZE)
    ax.set_ylabel("Y_AXIS",fontsize=FONTSIZE)
    legend = ax.legend(loc='lower left', shadow=True, fontsize=FONTSIZE)
    plt.title("TITLE")
    plt.show()