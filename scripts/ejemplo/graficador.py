import sys
import numpy as np
import matplotlib.pyplot as plt

def graficador(xs,ys):

	n = len(xs)
	index = np.arange(n)

	bar_width = 0.4
	opacity = 0.4

	rects1 = plt.bar(index, ys, alpha=opacity, color='green')

	plt.xlabel('File size (KB)')
	plt.ylabel('Throughput (KB/s)')

	plt.ylim([0,700])
	plt.title('Throughput x File Size')
	plt.xticks(index+bar_width, xs)
	plt.xticks(rotation = -60)
	plt.legend()
	plt.tight_layout()
	plt.savefig("../../graficos/test")	
	plt.show()		