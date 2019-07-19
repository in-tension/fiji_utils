
from ij import IJ, WindowManager
from ij.plugin.frame import RoiManager


#from fiji_utils import *
import fiji_utils as futils

import os
#script_dir = os.path.dirname(os.path.abspath(__file__))

script_dir = "/Users/baylieslab/Documents/Amelia/code_dev/projects/fiji_utils/"
#test_image_name = "150511_Lim3b-GFP_L4-R2.tif"

cell_imp_name = "fiji-utils-testing_150511_Lim3b-GFP_L4-R2.tif"
cell_imp_path = os.path.join(script_dir, cell_imp_name)
nuc_bin_name = "nuc-bin_fiji-utils-testing_150511_Lim3b-GFP_L4-R2.tif"
nuc_bin_path = os.path.join(script_dir, nuc_bin_name)

cell_roi_name = "vl3_fiji-uitils-testing_150511_Lim3b-GFP_L4-R2.roi"
cell_roi_path = os.path.join(script_dir, cell_roi_name)
nuc_roi_name = "vl3_nuc-0fiji-utils-testing_150511_Lim3b-GFP_L4-R2.roi"
nuc_roi_path = os.path.join(script_dir, nuc_roi_name)



print(futils.getMeasurementInt())


cell_imp = futils.open_get_imp(cell_imp_path)
nuc_bin = futils.open_get_imp(nuc_bin_path)

cell_roi = futils.open_get_roi(cell_roi_path)
nuc_roi = futils.open_get_roi(nuc_roi_path)



#nuc_bin_ip = nuc_bin
#hist = nuc_bin_ip.getHistogram()
#print(hist)

#
#cell_imp = WindowManager.getImage(cell_imp_name)
#
#if cell_imp == None :
#
#	cell_imp = IJ.openImage(cell_imp_path)
#	cell_imp.show()
#
#
#rm = RoiManager.getRoiManager()
#roi_name_to_index = futils.roi_name_index_dict()
#
#
#if test_cell_roi_name in roi_name_to_index :
#	cell_roi = rm.getRoi(roi_name_to_index[test_cell_roi_name])
#else :
##	rm.open(test_cell_roi_path)
#	IJ.openImage(test_cell_roi_path)
#	cell_roi = imp.getRoi()
#	futils.add_roi(cell_roi, test_cell_roi_name)
#
#	
##	cell_ind = rm.getCount() - 1
##	rm.rename(cell_ind, test_cell_roi_name)
##	cell_roi = rm.getRoi(cell_ind)
#
#
#if test_nuc_roi_name in roi_name_to_index :
#	nuc_roi = rm.getRoi(roi_name_to_index[test_nuc_roi_name])
#else :
#	IJ.openImage(test_nuc_roi_path)
#	nuc_roi = imp.getRoi()
#	futils.add_roi(nuc_roi, test_nuc_roi_name)
##	nuc_ind = rm.getCount() - 1
##	rm.rename(nuc_ind, test_nuc_roi_name)
##	nuc_roi = rm.getRoi(nuc_ind)
#
#
##
#cell_ip = cell_imp.getProcessor()
#hist = cell_ip.getHistogram()






