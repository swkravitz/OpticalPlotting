import numpy as np
import matplotlib.pyplot as plt
from gaussian_fit import gaussian_get_params
from TSTR_fit_new import BRIDF_plotter

# takes a single run, list of runs, or list of lists of runs. For a list of lists, it gives each inner list the same color and label.
def plot_runs(runs, title="", rot=False, voltage=False, labels=False, show=False, xlabel="", ylabel="", figure=True, smooth=True, legend_loc=0, include_legend=True, linestyle="-", log=False):
	if type(runs) != type([]): # if runs is a single run
		runs = [runs] # make it a list

	if type(runs[0]) != type([]):
		nested = False
	else:
		nested = True

	if figure:
		plt.figure()

	color_list = ["r", "g", "b", "m", "c", "y", "k", "lightpink", "darksalmon", "slategray", "plum", "lightcoral", "indigo", "darkorange"]

	minx = 1000
	maxx = -1000

	miny = 1000
	maxy = -1000

	if nested == False:

		for i in range(len(runs)):
			run = runs[i]
			if rot:
				x = run.rot_angles
			else:
				x = run.angles
			minx = np.min([minx, np.min(x)])
			maxx = np.max([maxx, np.max(x)])
			# voltage means use absolute intensities, not normalized ones
			if voltage:
				y = run.intensities
			else:
				y = run.relative_intensities
			maxy = np.max([maxy, np.max(y)])
			miny = np.min([miny, np.min(y)])

			# smooth means a line will be plotted, not just points
			if smooth:
				if labels:
					plt.plot(x, y, c=color_list[i], label=labels[i], linestyle=linestyle)
				else:
					plt.plot(x, y, c=color_list[i], label=run.name, linestyle=linestyle)
			else:
				if labels:
					plt.scatter(x, y, marker="x", c=color_list[i], s=5, label=labels[i])
				else:
					plt.scatter(x, y, marker="x", c=color_list[i], s=5, label=run.name)
	else:
		for i in range(len(runs)):
			inner_runs = runs[i]
			for j in range(len(inner_runs)):
				run = inner_runs[j]
				# rot means that angles are relative to the rotation stage rather than to the sample normal
				if rot:
					x = run.rot_angles
				else:
					x = run.angles
				minx = np.min([minx, np.min(x)])
				maxx = np.max([maxx, np.max(x)])

				if voltage:
					y = run.intensities
				else:
					y = run.relative_intensities
				maxy = np.max([maxy, np.max(y)])
				miny = np.min([miny, np.min(y)])


				if j == 0: # make label
					if smooth:
						if labels:
							plt.plot(x, y, c=color_list[i], label=labels[i], linestyle=linestyle)
						else:
							plt.plot(x, y, c=color_list[i], label=run.name, linestyle=linestyle)
					else:
						if labels:
							plt.scatter(x, y, marker="x", c=color_list[i], s=5, label=labels[i])
						else:
							plt.scatter(x, y, marker="x", c=color_list[i], s=5, label=run.name)
				else:
					if smooth:
						plt.plot(x, y, c=color_list[i])
						
					else:
						plt.scatter(x, y, marker="x", c=color_list[i], s=5)

	if xlabel:
		plt.xlabel(xlabel)
	else:
		if rot:
			plt.xlabel("rotation stage angle \n(0 is looking directly into beam, 180 is blocking beam)")
		else:
			plt.xlabel("angle relative to sample normal (degrees)")

	if ylabel:
		plt.ylabel(ylabel)
	else:
		if voltage:
			plt.ylabel("rate (Hz)")
		else:
			plt.ylabel("intensity (reflected rate/str)/(incident rate)")
	if log:
		plt.ylim(0.5 * miny, 1.1 * maxy)
		plt.yscale("log")
	else:
		plt.ylim(0, 1.1 * maxy)
	plt.xlim(minx, maxx)

	plt.title(title)
	if include_legend:
		plt.legend(loc=legend_loc)
	if show:
		plt.show()

def plot_gaussian_fit(run, mu=1000):
	params = gaussian_get_params(run, mu)

	A, B, sigma, mu = params

	label = "gaussian fit\nA: " + str(A) + "\nB: " + str(B) + "\nsigma: " + str(sigma) + "\nmu: " + str(mu)
	plot_fit_by_params(min(x), max(x), params, label)

def plot_TSTR_fit(theta_i, n, fit_params, label="", color=""):
	x = np.linspace(0, 85, 1000)
	if label:
		plt.plot(x, BRIDF_plotter(x, 0., theta_i, n, 0.5, fit_params), label=label, color=color)
	else:
		plt.plot(x, BRIDF_plotter(x, 0., theta_i, n, 0.5, fit_params), color=color)
	plt.legend()




