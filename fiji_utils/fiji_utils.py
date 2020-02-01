"""
utilities/convenience functions for fiji

col -> column
col_dict -> column dictionary, keys are column headings, values are columns -> dict {column_heading(str) : [column_data](list)}

"""



import os

from ij import IJ, WindowManager
from ij.gui import Toolbar
from ij.measure import ResultsTable
from ij.plugin import Duplicator, ZProjector
from ij.plugin.frame import RoiManager
from ij.plugin.filter import Analyzer
from ij.gui import WaitForUserDialog

from constants import *

# def duplicate(imp,, ze, ) :
def duplicate_channel(imp, start_slice, end_slice, channel) :
    d = Duplicator()
    new_imp = d.run(imp, channel, channel, start_slice, end_slice, 1, 1)
    return new_imp
    
def results_label_to_roi_label(results_label) :
    parts = results_label.split(':')
    return parts[1]



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


def open_get_imp(imp_path) :
    """open or get image - uses filename for the image in WindowManager"""

    imp_name = os.path.basename(imp_path)
    imp = WindowManager.getImage(imp_name)

    if imp == None :

        imp = IJ.openImage(imp_path)
        imp.show()

    return imp



def swap_ground_colors() :
    """swap background and foreground color settings"""
    cur_fore = Toolbar.getForegroundColor()
    cur_back = Toolbar.getBackgroundColor()

    Toolbar.setForegroundColor(cur_back)
    Toolbar.setBackgroundColor(cur_fore)

def more_black_than_white(imp) :
    """returns True if the count of black pixels is greater than the count of white pixels, black->lowest_value, white->highest_value"""

    ip = imp.getProcessor()
    hist = ip.getHistogram()
    black_count = hist[0]
    white_count = hist[-1]

    return black_count > white_count


def make_projection(imp, method, slices) :
    z_prjor = ZProjector(imp)
    prj_imp = z_prjor.run(imp, method, slices[0], slices[1])
    return prj_imp




def jpprint(obj) :
    """
        pretty print for java collections as well as python collections
        obj is assumed to be a collection
    """
    for item in obj :
        print(item)

def wait(message=None) :
    if message == None :
        message = 'press ok to continue'
    wfug = WaitForUserDialog('Waiting for user', message)
    wfug.show()
