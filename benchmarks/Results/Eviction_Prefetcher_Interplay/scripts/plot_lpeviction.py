# libraries
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import gridspec

#######################
# data extraction section
#######################

# declaration of variables
parent_folder = '../output_logs'

experiment_folder = 'LPEviction'
sub_folders = ['NoOversub', '2MB_110', 'TBN_110', '2MB_125', 'TBN_125']

benchmarks = ['backprop', 'bfs', 'fdtd', 'hotspot', 'nw', 'pathfinder']

rt_NoOversub = []
rt_2MB_110 = []
rt_TBN_110 = []
rt_2MB_125 = []
rt_TBN_125 = []

for b in benchmarks:
	for sf in sub_folders:
		file_name = './' + parent_folder + '/' + experiment_folder + '/' + sf + '/' + b + '.log'
		
		with open(file_name, 'r') as b_file:
			file_content = b_file.read()

			line = re.findall(r"^Tot_kernel_exec_time_and_fault_time.*", file_content, flags=re.MULTILINE)[0]
			rt = float(line[line.find(', ')+2:line.rfind('(us)')])

			if sf == 'NoOversub':
				rt_NoOversub.append(rt)
			elif sf == '2MB_110':
				rt_2MB_110.append(rt)
			elif sf == 'TBN_110':
				rt_TBN_110.append(rt)
			elif sf == '2MB_125':
				rt_2MB_125.append(rt)
			elif sf == 'TBN_125':
				rt_TBN_125.append(rt)			

rt_TBN_110 = np.array(np.divide(rt_TBN_110, rt_2MB_110))
rt_2MB_110 = np.array(np.divide(rt_2MB_110, rt_2MB_110))
rt_TBN_125 = np.array(np.divide(rt_TBN_125, rt_2MB_125))
rt_2MB_125 = np.array(np.divide(rt_2MB_125, rt_2MB_125))

#######################
# plotting section
#######################

# set width of bar
barWidth = 0.3
 
# Set position of bar on X axis
r1 = np.arange(len(rt_NoOversub), dtype=float)

r1a = [0, 1.6, 3.2, 4.8, 6.4, 8.0]

for i in range(len(rt_NoOversub)):
	r1[i] = r1[i] + 0.3

for i in range(len(rt_NoOversub)):
	r1a[i] = r1a[i] + 0.3

r2 = [x + barWidth for x in r1a]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]

plt.figure(1)
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 12}

plt.rc('font', **font)

plt.rcParams['hatch.linewidth'] = 1.5

plt.figure(figsize=(10,4))

plt.bar(r2, rt_2MB_110, hatch="--", color='r', width=barWidth, edgecolor='black', label='2MB Eviction with Working set == gddr size * 110%')
plt.bar(r3, rt_TBN_110, hatch="++", color='c', width=barWidth, edgecolor='black', label='TBN Eviction with Working set == gddr size * 110%')
plt.bar(r4, rt_2MB_125, hatch="xx", color='yellow', width=barWidth, edgecolor='black', label='2MB Eviction with Working set == gddr size * 125%')
plt.bar(r5, rt_TBN_125, hatch="\\\\", color='g', width=barWidth, edgecolor='black', label='TBN Eviction with Working set == gddr size * 125%')


plt.xticks([r + 0.3 + barWidth for r in r1a], benchmarks)

ax = plt.gca()
ax.yaxis.grid(b=True, which='major', color='grey', linestyle='-')

ax.axes.set_ylim(bottom=0.4)
#ax.set_yscale('log', nonposy='clip')

plt.ylabel('Kernel Execution Time \n(Normalized to 2MB eviction)')

ax.xaxis.set_ticks_position('none')

# Create legend & Show graphic
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.36), prop={'size': 12})

plt.savefig('../plots/LPEviction/lp_eviction.png',  dpi=300, bbox_inches="tight")
