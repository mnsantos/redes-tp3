import sys
import numpy as np
import matplotlib.pyplot as plt

def graficador(xs,ys,ys1,ys2,name,color1,color2,color3):

	n = len(xs)
	index = np.arange(n)

	bar_width = 0.4
	opacity = 0.4

	rects1 = plt.bar(index, ys, alpha=opacity, color=color1)
	rects1 = plt.bar(index, ys1, alpha=opacity, color=color2)
	rects1 = plt.bar(index, ys2, alpha=opacity, color=color3)


	plt.xlabel('File size (KB)')
	plt.ylabel('Throughput (KB/s)')

	plt.ylim([0,140])
	plt.title('Throughput x File Size')
	plt.xticks(index+bar_width, xs)
	plt.xticks(rotation = -60)
	plt.legend()
	plt.tight_layout()
	plt.savefig("../../graficos/"+name)	
	#plt.show()		