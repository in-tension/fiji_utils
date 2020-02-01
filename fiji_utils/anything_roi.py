import os

from ij import IJ, WindowManager
from ij.gui import Toolbar
from ij.measure import ResultsTable
from ij.plugin import Duplicator, ZProjector
from ij.plugin.frame import RoiManager
from ij.plugin.filter import Analyzer
from ij.gui import WaitForUserDialog

# from futils
from constants import *



def getMeasurementInt() :
    """returns the int value of the measurements setting, made as a hack to translate a set of checkboxes to its corresponding number"""
    a = Analyzer()
    i = a.getMeasurements()
    return i

def setMeasurementInt(i) :
    """sets the measurements setting to the int value i, made as a hack to translate an number to its corresponding checkboxes"""
    a = Analyzer()
    a.setMeasurements(i)

def rt_to_col_dict() :
    """takes the ResultsTable and return its contents as an col_dict(dictionary whose keys are heads of columns and values are the columns)"""
    # print("rt_to_col_dict")

    rt = ResultsTable.getResultsTable()

    # print(headings)



    col_dict = {}


    col_dict["Label"] = []

    for n in range(rt.size()) :
        col_dict['Label'].append(rt.getLabel(n))



    headings = rt.getHeadings()



    for heading in headings :
        if heading == "Label" :
            continue
        col_ind = rt.getColumnIndex(heading)
        # print(col_ind)
        # print(heading)
        col = rt.getColumn(col_ind)
        col_dict[heading] = col

    #
    # for i in range(len(headings)) :
    #     temp = rt.getColumn(i)
    #     # t = temp is not None
    #     print("{}. {} = {}".format(i, headings[i], temp is not None))
    #
    #     if temp is not None :
    #         col_dict[rt.getColumnHeading(i)] = list(temp)
    #



    col_dict["Label"] = []

    for n in range(rt.size()) :
        col_dict['Label'].append(rt.getLabel(n))

    return col_dict


def open_get_roi(roi_path) :
    """open or get roi - uses filename for the roi in RoiManager"""
    rm = RoiManager.getRoiManager()
    roi_name_to_index = roi_name_index_dict()

    roi_name = os.path.basename(roi_path)

    if roi_name in roi_name_to_index :
        roi = rm.getRoi(roi_name_to_index[roi_name])
    else :

        IJ.openImage(roi_path)
        imp = IJ.getImage()

        roi = imp.getRoi()
        add_roi(roi, roi_name)

    return roi


def add_roi(roi, name=None) :
    """add roi to RoiManager, if name is given, sets its name to name"""
    rm = RoiManager.getRoiManager()
    # print(rm)
    # rm.show()
    rm.addRoi(roi)
    # print('fiji_utils.add_roi: {}: {}'.format(name, roi))
    if name is not None :
        rm.rename(rm.getCount() - 1, name)

def add_rois(rois, names=None) :

    if names is None :
        names = [None]*len(rois)

    if len(rois) != len(names) :
        raise ValueError("len of rois must be the same as len of names")

    for roi, name in zip(rois, names) :
        add_roi(roi, name=name)


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


def roi_name_index_dict() :
    """create and return a dict that takes an image_name(str) and returns it's index(int)
    image_name or roi_name??"""
    rm = RoiManager.getRoiManager()

    str_ind_dict = {}
    for i in range(rm.getCount()) :
        str_ind_dict[rm.getName(i)] = i
    return str_ind_dict


def dup_and_crop(imp, roi) :
    """returns a duplicate of imp cropped to roi"""
    imp.setRoi(roi)
    d = Duplicator()
    cropped_imp = d.crop(imp)
    return cropped_imp


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


def measure_roi_set(roi_set, imp, set_measure=MEAS_ALL) :
    """requires imp because it won't measure without one
    note.. side effects: ResultsTable and RoiManager cleared"""
    # imp.show()
    rt = ResultsTable.getResultsTable()
    rt.reset()

    rm = RoiManager.getRoiManager()
    rm.reset()


    if roi_set is not None :

        for roi in roi_set :
            add_roi(roi)

    rm.setSelectedIndexes([x for x in range(rm.getCount())])
    setMeasurementInt(set_measure)
    print("before rm measure")
    # IJ.setActiveImage(imp)
    # IJ.selectWindow(imp.getTitle())
    # imp.show()
    try :
    # input()
    # for roi in roi_set :
        # imp.
        rm.runCommand(imp, "Measure")
    except :
        input()
    print("after rm measure")

    results = rt_to_col_dict()
    # imp.hide()
    return results

def meas_rset_geo(roi_set, imp) :
    return measure_roi_set(roi_set, imp, set_measure=MEAS_GEO)

def meas_rset_intens(roi_set, imp) :
    return measure_roi_set(roi_set, imp, set_measure=MEAS_INTENS_XY)


def measure_roi_dict(imp, roi_dict, set_measure=MEAS_ALL) :
    # imp.show()
    rt = ResultsTable.getResultsTable()
    rt.reset()

    rm = RoiManager.getRoiManager()
    rm.reset()

    for roi_name, roi in roi_dict.items() :
        add_roi(roi, name=roi_name)

    rm.setSelectedIndexes([x for x in range(rm.getCount())])
    setMeasurementInt(set_measure)

    ## imp.show()

    rm.runCommand(imp, "Measure")

    results = rt_to_col_dict()
    # imp.hide()
    return results

def meas_rdict_geo(imp, roi_dict) :
    """same as roi_dict_geo, wanted to rename but wasn't sure if it would break anything"""
    return measure_roi_dict(imp, roi_dict, set_measure=MEAS_GEO)

def meas_rdict_intens(imp, roi_dict) :
    """same as roi_dict_intens, wanted to rename but wasn't sure if it would break anything"""
    return measure_roi_dict(imp, roi_dict, set_measure=MEAS_INTENS_XY)
