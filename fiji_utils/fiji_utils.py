"""
utilities/convenience functions for fiji

col -> column
col_dict -> column dictionary, keys are column headings, values are columns -> dict {column_heading(str) : [column_data](list)}

"""



import os

from ij import IJ, WindowManager
from ij.gui import Toolbar
from ij.measure import ResultsTable
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager
from ij.plugin.filter import Analyzer


""" int to use to set measurements to all"""
MEAS_ALL = 2092799

# ## need to add close the other images
# def force_close_all() :
# 	while WindowManager.getImageCount() > 0 :
# 		imp = IJ.getImage()
# 		imp.changes = False
# 		imp.close()

def force_close_all_images() :
	"""close all open images without save dialog box"""
	while WindowManager.getImageCount() > 0 :
		imp = IJ.getImage()
		imp.changes = False
		imp.close()


def force_close(imp) :
	"""close imp without save dialog box"""
	imp.changes = False
	imp.close()

def add_roi(roi, name=None) :
	"""add roi to RoiManager, if name is given, sets its name to name"""
	rm = RoiManager.getRoiManager()
	rm.addRoi(roi)
	if name is not None :
		rm.rename(rm.getCount() - 1, name)


## obj should be a collection
def jpprint(obj) :
	"""
		pretty print for java collections as well as python collections
		obj is assumed to be a collection
	"""
	for item in obj :
		print(item)


def getMeasurementInt() :
	"""returns the int value of the measurements setting, made as a hack to translate a set of checkboxes to its corresponding number"""
	a = Analyzer()
	i = a.getMeasurements()
	return i


def setMeasurementInt(i) :
	"""sets the measurements setting to the int value i, made as a hack to translate an number to its corresponding checkboxes"""
	a = Analyzer()
	a.setMeasurements(i)


def swap_ground_colors() :
	"""swap background and foreground color settings"""
	cur_fore = Toolbar.getForegroundColor()
	cur_back = Toolbar.getBackgroundColor()

	Toolbar.setForegroundColor(cur_back)
	Toolbar.setBackgroundColor(cur_fore)

def roi_box_xy(roi) :
	"""returns (x,y) values of rois bounding box as tuple"""

	return (roi.getXBase(), roi.getYBase())

def roi_cent(roi, integer=False) :
	"""returns (x,y) values of centroid as tuple"""
	stats = roi.getStatistics()
	if integer :
		return (int(stats.xCentroid), int(stats.yCentroid))
	else :
		return (stats.xCentroid, stats.yCentroid)


def rt_to_col_dict() :
	"""takes the ResultsTable and return its contents as an col_dict(dictionary whose keys are heads of columns and values are the columns)"""
	rt = ResultsTable.getResultsTable()

	headings = rt.getHeadings()

	col_dict = {}
	for i in range(len(headings)) :
		temp = rt.getColumn(i)
		if temp is not None :
			col_dict[rt.getColumnHeading(i)] = list(temp)

	return col_dict


def measure(imp, roi=None, headings=None) :
	"""measures imp and returns all columns or only those in headings
		warning.. changes measurement settings to all as a col_dict(dictionary whose keys are heads of columns and values are the columns)"""

	setMeasurementInt(MEAS_ALL)

	## possibly don't include roi at all - setRoi may overwite an existing roi
	if roi is not None :
		imp.setRoi(roi)

	IJ.run(imp, "Measure", "");

	col_dict = rt_to_col_dict()

	if headings is not None :
		return col_dict
	else :
		out_col_dict = {}
		for heading in heading :
			## LBYL
			try :
				out_col_dict[heading] = col_dict[heading]
			except KeyError :
				IJ.log('fiji_conv.measure() : no heading {}'.format(heading))
		return out_col_dict


def dup_and_crop(imp, roi) :
	"""returns a duplicate of imp cropped to roi"""
	imp.setRoi(roi)
	d = Duplicator()
	cropped_imp = d.crop(imp)
	return cropped_imp


def more_black_than_white(imp) :
	"""returns True if the count of black pixels is greater than the count of white pixels, black->lowest_value, white->highest_value"""

	ip = imp.getProcessor()
	hist = ip.getHistogram()
	black_count = hist[0]
	white_count = hist[-1]

	return black_count > white_count


def roi_name_index_dict() :
	"""create and return a dict that takes an image_name(str) and returns it's index(int)"""
	rm = RoiManager.getRoiManager()

	str_ind_dict = {}
	for i in range(rm.getCount()) :
		str_ind_dict[rm.getName(i)] = i
	return str_ind_dict


def open_get_imp(imp_path) :
	"""open or get image - uses filename for the image in WindowManager"""

	imp_name = os.path.basename(imp_path)
	imp = WindowManager.getImage(imp_name)

	if imp == None :

		imp = IJ.openImage(imp_path)
		imp.show()

	return imp



def open_get_roi(roi_path) :
	"""open or get roi - uses filename for the roi in RoiManager"""
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
