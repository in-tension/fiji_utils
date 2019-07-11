import os

from ij import IJ, WindowManager
from ij.gui import Toolbar
from ij.measure import ResultsTable
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager
from ij.plugin.filter import Analyzer


""" int to use to set measurements to all"""
MEAS_ALL = 2092799

## need to add close the other images
def force_close_all() :
	while WindowManager.getImageCount() > 0 :
		imp = IJ.getImage()
		imp.changes = False
		imp.close()

def force_close_all_images() :
	while WindowManager.getImageCount() > 0 :
		imp = IJ.getImage()
		imp.changes = False
		imp.close()


def force_close(imp) :
	imp.changes = False
	imp.close()

def add_roi(roi, name=None) :
	rm = RoiManager.getRoiManager()
	rm.addRoi(roi)
	if name is not None :
		rm.rename(rm.getCount() - 1, name)


## obj should be a collection
def jpprint(obj) :
	"""
		pprints java collections as well as python collections
		obj should be a collection
	"""
	for item in obj :
		print(item)


def getMeasurementInt() :
	a = Analyzer()
	i = a.getMeasurements()
	return i


def setMeasurementInt(i) :
	a = Analyzer()
	a.setMeasurements(i)


def swap_ground_colors() :
	cur_fore = Toolbar.getForegroundColor()
	cur_back = Toolbar.getBackgroundColor()

	Toolbar.setForegroundColor(cur_back)
	Toolbar.setBackgroundColor(cur_fore)

def roi_xy(roi) :
	return (roi.getXBase(), roi.getYBase())

def roi_cent(roi, integer=False) :
	stats = roi.getStatistics()
	if integer :
		return (int(stats.xCentroid), int(stats.yCentroid))
	else :
		return (stats.xCentroid, stats.yCentroid)


def rt_to_arr_dict() :
	rt = ResultsTable.getResultsTable()

	headings = rt.getHeadings()

	arr_dict = {}
	for i in range(len(headings)) :
		temp = rt.getColumn(i)
		if temp is not None :
			arr_dict[rt.getColumnHeading(i)] = list(temp)

	return arr_dict


def measure(imp, roi=None, headings=None) :
	setMeasurementInt(MEAS_ALL)

	## possibly don't include roi
	if roi is not None :
		imp.setRoi(roi)

	IJ.run(imp, "Measure", "");

	arr_dict = rt_to_arr_dict()

	if headings is not None :
		return arr_dict
	else :
		out_arr_dict = {}
		for heading in heading :
			## LBYL
			try :
				out_arr_dict[heading] = arr_dict[heading]
			except KeyError :
				IJ.log('fiji_conv.measure() : no heading {}'.format(heading))
		return out_arr_dict


def dup_and_crop(imp, roi) :
	imp.setRoi(roi)
	d = Duplicator()
	cropped_imp = d.crop(imp)
	return cropped_imp


def more_black_than_white(imp) :

	ip = imp.getProcessor()
	hist = ip.getHistogram()
	black_count = hist[0]
	white_count = hist[-1]

	return black_count > white_count


def roi_name_index_dict() :
	rm = RoiManager.getRoiManager()

	str_ind_dict = {}
	for i in range(rm.getCount()) :
		str_ind_dict[rm.getName(i)] = i
	return str_ind_dict


def open_get_imp(imp_path) :
	imp_name = os.path.basename(imp_path)
	imp = WindowManager.getImage(imp_name)

	if imp == None :

		imp = IJ.openImage(imp_path)
		imp.show()

	return imp



def open_get_roi(roi_path) :
	rm = RoiManager.getRoiManager()
	roi_name_to_index = roi_name_index_dict()

	roi_name = os.path.basename(roi_path)

	if roi_name in roi_name_to_index :
		roi = rm.getRoi(roi_name_to_index[roi_name])
	else :
		IJ.openImage(roi_path)
		roi = imp.getRoi()
		futils.add_roi(cell_roi, test_cell_roi_name)

	return roi
