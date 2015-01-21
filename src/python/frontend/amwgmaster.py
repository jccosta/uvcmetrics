diags_varlist = {}
diags_collection = {}
diags_obslist = {}

# These are special "variables" that we need to skip over when iterating over real variables. 
# They are usually flags or parameters for the entire collection.
# Make sure no actual variables have these names, but that shouldn't be a problem.
collection_special_vars = ['desc', 'preamble', 'regions', 'seasons', 'package', 'options', 'combined']


# There are three sections to this file.
# The first section (diags_collection) is used to define the diagnostics collections.
# Each collection starts with an empty dictionary, then has a few basic parameters -
# 1) desc - a brief (1 or 2 sentences) description of the plot, used to generate an index page
# 2) preamble - a longer description of the set. used as the introduction before plot links in the classic viewer
#        preamble is assumed empty if nothing is provided.
#
# After that, additional optional arguments that encompass the entire collection can be specified. The additional arguments are:
# seasons - a collection-level set of seasons. all variables in the collection will iterate over this list of seasons. 
#           if this is not specified the code will look for seasons in individual variable definitions.
#           if no seasons are found in individual variable definitions ANN is assumed
# regions - a collection-level set of regions. all variables in the collection will iterate over this list of regions.
#           if this is not specified, the code will look for regions in individual variable definitions.
#           if not regions are found in individual variable definitions, Global is assumed
# package - a collection-level indicate of what package the plots are from. e.g. AMWG or LMWG
#           if this is not specified, the code will look for packages in individual variable definitions.
#           No assumptions are made on package. It must be collection-defined or all variables need to define it
# options - A dictionary of options specific to the collection. These are passed as command line options to diags.py
#           The current primary one is:
#           'logo':'no' - does not draw the UVCDAT logo on output plots.
# Collection-level Flags:
#           combined:True - indicates this collection produces combined single image plots which are model, 
#              then obs, then model-obs. This helps classic viewer. 
#              Note: This is only for plots that want the 3-pane view. If obs and model data are 
#              combined on the plot as plot production (e.g. set amwg 10) you don't need to set this.
# Once any optional additional arguments have been specified, the variables that make up the set are defined.
# A typical variable entry has the variable name (as found in the obs sets and model output) as a key, then a plottype, 
# a list of observation sets, and optional paraemeters.
# Optional parameters include a list of seasons, regions, and variable options, and  specific to a variable
# All arguments (except plot type) are lists. Here is a complicated example:
# 
# diags_collection['example']['Z3'] = {'plottype': '10', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['300', '500'], 'regions':['Global', 'Tropics'], 'seasons':['ANN', 'DJF']}
# This would create a total of 4*2*2*2 plots (each obs set, each pressure level, each region, and each season).
# metadiags attempts to group as many of these together as possible for efficient IO
# A much simpler minimal example would just be:
# diags_collection['example']['T'] = {'plottype': '5', 'obs':['ECMWF_1']}
 
# The second part of the file is a list of variables.
# A typical entry looks like:
# diags_varlist['TREFHT'] = {'desc': '2-meter temperature (land) (Northern)'}
# This is primarily used in web-page creation to have a description for a given variable.
# Eventually, other metadata about a variable might be included. Note: This section is primarily required
# because of the lack of consistency in CF-compliance in data sets and observation sets.

# The third part of the file is a list of observatino sets.
# A typical entry looks like:
# diags_obslist['HADISST_PD_1'] = {'filekey': 'HADISST_PD', 'desc': 'HadISST/OI.v2 (Present Day) 1999-2008'}
# This converts the obs set keys specified in the collections sections to a filename key (ie, HADISST_PD* has the data we need)
# and a description (again for web page generation)


# *** Collection 11 ***
diags_collection['11'] = {}
diags_collection['11']['desc'] = 'Pacific annual cycle, Scatter plot plots'
diags_collection['11']['package'] = 'AMWG'
diags_collection['11']['SWCF_LWCF'] = {'plottype':'11', 'obs':['CERES2_1', 'CERES_1', 'ERBE_1']}
diags_collection['11']['LHFLX'] = {'plottype':'11', 'obs':['ECMWF_1','WHOI_1']}
diags_collection['11']['PRECT'] = {'plottype':'11', 'obs':['GPCP_1']}
diags_collection['11']['SST'] = {'plottype':'11', 'obs':['HADISST_1']}
diags_collection['11']['SWCF'] = {'plottype':'11', 'obs':['ERBE_1']}
diags_collection['11']['TAUX'] = {'plottype':'11', 'obs':['ERS_1', 'LARYEA_1']}
diags_collection['11']['TAUY'] = {'plottype':'11', 'obs':['ERS_1', 'LARYEA_1']}
# *** Collection 10 ***
diags_collection['10'] = {}
diags_collection['10']['desc'] = 'Annual cycle line plots of global means'
diags_collection['10']['package'] = 'AMWG'
diags_collection['10']['CLDMED'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['FSDS'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['FSNTOA'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['CLDLOW'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['LWCF'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['FSNTOAC'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['TS'] = {'plottype': '10', 'obs': ['NCEP_1']}
diags_collection['10']['T'] = {'plottype': '10', 'obs': ['ECMWF_1', 'JRA25_1', 'AIRS_1', 'ERA40_1', 'NCEP_1'], 'varopts':['200', '850']}
diags_collection['10']['SWCF'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['ALBEDO'] = {'plottype': '10', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['10']['CLDTOT'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['U'] = {'plottype': '10', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['200']}
diags_collection['10']['FLUTC'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['FSNS'] = {'plottype': '10', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['10']['Z3'] = {'plottype': '10', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['300', '500']}
diags_collection['10']['RESTOA'] = {'plottype': '10', 'obs': ['ERBE_1']}
diags_collection['10']['TGCLDLWP'] = {'plottype': '10', 'obs': ['SSMI_1', 'NVAP_1']}
diags_collection['10']['FLUT'] = {'plottype': '10', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['10']['CLDTOT_VISIR'] = {'plottype': '10', 'obs': ['ISCCP_1'], 'modelvar':'CLDTOT'}
diags_collection['10']['LHFLX'] = {'plottype': '10', 'obs': ['WHOI_1', 'ECMWF_1', 'ERA40_1']}
diags_collection['10']['SHFLX'] = {'plottype': '10', 'obs': ['JRA25_1', 'NCEP_1', 'LARYEA_1']}
diags_collection['10']['TREFHT'] = {'plottype': '10', 'obs': ['WILLMOTT_1', 'LEGATES_1', 'JRA25_1']}
diags_collection['10']['FLDS'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['ALBEDOC'] = {'plottype': '10', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['10']['CLDHGH_VISIR'] = {'plottype': '10', 'obs': ['ISCCP_1'], 'modelvar':'CLDHGH'}
diags_collection['10']['EP'] = {'plottype': '10', 'obs': ['ECMWF_1', 'ERA40_1']}
diags_collection['10']['CLDMED_VISIR'] = {'plottype': '10', 'obs': ['ISCCP_1'], 'modelvar':'CLDMED'}
diags_collection['10']['QFLX'] = {'plottype': '10', 'obs': ['WHOI_1', 'ECMWF_1', 'ERA40_1', 'LARYEA_1']}
diags_collection['10']['PSL'] = {'plottype': '10', 'obs': ['JRA25_1', 'NCEP_1']}
diags_collection['10']['SST'] = {'plottype': '10', 'obs': ['HADISST_1']}
diags_collection['10']['FLNS'] = {'plottype': '10', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['10']['ICEFRAC'] = {'plottype': '10', 'obs': ['SSMI_1', 'HADISST_1'], 'regions':['N_Hemisphere_Land', 'S_Hemisphere_Land']}
diags_collection['10']['CLDLOW_VISIR'] = {'plottype': '10', 'obs': ['ISCCP_1'], 'modelvar':'CLDLOW'}
diags_collection['10']['PRECT'] = {'plottype': '10', 'obs': ['XA_1', 'GPCP_1', 'LEGATES_1', 'TRMM_1', 'SSMI_1']}
diags_collection['10']['CLDHGH'] = {'plottype': '10', 'obs': ['ISCCP_1']}
diags_collection['10']['PREH2O'] = {'plottype': '10', 'obs': ['NCEP_1', 'NVAP_1', 'JRA25_1', 'ERA40_1', 'ECMWF_1', 'SSMI_1']}
# *** Collection 13 ***
# Another special case. Should we treat the station names as Regions perhaps? That would make this pretty easy to not special case
diags_collection['13'] = {}
diags_collection['13']['desc'] = 'ISCCP cloud simulator plots '
diags_collection['13']['regions'] = ['Global', 'Tropics'] #, .... etc
diags_collection['13']['package'] = 'AMWG'
diags_collection['13']['seasons'] = ['DJF', 'JJA', 'ANN']
# *** Collection 12 ***
diags_collection['12'] = {}
diags_collection['12']['desc'] = 'Vertical profile plots from 17 selected stations'
diags_collection['12']['package'] = 'AMWG'
# 3 variables, treat the stations like regions maybe? or as obs sets for the vars?
# *** Collection 15 ***
diags_collection['15'] = {}
diags_collection['15']['desc'] = 'Annual Cycle at Select Stations plots'
diags_collection['15']['package'] = 'AMWG'
diags_collection['15']['TMQ'] = {'plottype': '15', 'obs': ['NSA_1', 'TWP1_1', 'TWP2_1', 'SGP_1', 'TWP3_1']}
diags_collection['15']['FSDS'] = {'plottype': '15', 'obs': ['SHEBA_1', 'TWP2_1', 'TWP1_1', 'SGP_1', 'TWP3_1', 'NSA_1']}
diags_collection['15']['LHFLX'] = {'plottype': '15', 'obs': ['SGP_1']}
diags_collection['15']['SHFLX'] = {'plottype': '15', 'obs': ['SGP_1']}
diags_collection['15']['CLDTOT'] = {'plottype': '15', 'obs': ['TWP1_1', 'TWP3_1', 'SGP_1', 'TWP2_1', 'NSA_1']}
diags_collection['15']['FLDS'] = {'plottype': '15', 'obs': ['SHEBA_1', 'TWP2_1', 'TWP1_1', 'SGP_1', 'TWP3_1', 'NSA_1']}
diags_collection['15']['Q'] = {'plottype': '15', 'obs': ['NSA_1', 'TWP1_1', 'TWP2_1', 'SGP_1', 'TWP3_1']}
diags_collection['15']['T'] = {'plottype': '15', 'obs': ['NSA_1', 'TWP2_1', 'TWP1_1', 'SGP_1', 'TWP3_1']}
diags_collection['15']['MSE'] = {'plottype': '15', 'obs': ['NSA_1', 'TWP1_1', 'TWP2_1', 'SGP_1', 'TWP3_1']}
diags_collection['15']['PRECT'] = {'plottype': '15', 'obs': ['SGP_1']}
diags_collection['15']['TGCLDLWP'] = {'plottype': '15', 'obs': ['TWP1_1', 'TWP3_1', 'NSA_1', 'SGP_1', 'TWP2_1']}
diags_collection['15']['CLOUD'] = {'plottype': '15', 'obs': ['NSA_1', 'TWP1_1', 'TWP2_1', 'SGP_1', 'TWP3_1']}
# *** Collection 14 ***
### This will need some tweaking when set 14 is defined and working.
diags_collection['14'] = {}
diags_collection['14']['desc'] = 'Taylor Diagram plots '
diags_collection['14']['preamble'] = '<p>Taylor Diagrams were developed by Karl Taylor at PCMDI (<a href="http://www.agu.org/pubs/crossref/2001/2000JD900719.shtml">paper</a>|<a href="http://www-pcmdi.llnl.gov/publications/pdf/55.pdf">tech note</a>) and aim to condense information about variance and RMSE characteristics of a particular model run when compared with observations in a single diagram. The tables summarize the individual metrics for each variable considered including: <ul><br> <li>bias, as absolute percentage difference from observations <li>variance, as a ratio of the observed variance <li>correlation, correlation coefficient with observations </ul><p>'
diags_collection['14']['package'] = 'AMWG'
# *** Collection 3 ***
diags_collection['3'] = {}
diags_collection['3']['desc'] = 'Line plots of DJF, JJA and ANN zonal means'
diags_collection['3']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['3']['package'] = 'AMWG'
diags_collection['3']['combined'] = True
diags_collection['3']['CLDMED'] = {'plottype': '3', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['3']['FSDS'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['FSNTOA'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['CLDLOW'] = {'plottype': '3', 'obs': ['ISCCP_1', 'WARREN_1', 'CLOUDSAT_1']}
diags_collection['3']['LWCF'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['FSNTOAC'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['TS'] = {'plottype': '3', 'obs': ['NCEP_1']}
diags_collection['3']['SWCF'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['SWCFSRF'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['FLDSC'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['CLDTOT'] = {'plottype': '3', 'obs': ['ISCCP_1', 'WARREN_1']}
diags_collection['3']['FLUTC'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['FSNS'] = {'plottype': '3', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['3']['TGCLDLWP'] = {'plottype': '3', 'obs': ['SSMI_1', 'NVAP_1', 'MODIS_1']}
diags_collection['3']['FLUT'] = {'plottype': '3', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['3']['CLDTOT_VISIR'] = {'plottype': '3', 'obs': ['ISCCP_1'], 'modelvar':'CLDTOT'}
diags_collection['3']['LHFLX'] = {'plottype': '3', 'obs': ['WHOI_1', 'ECMWF_1', 'JRA25_1', 'ERA40_1']}
diags_collection['3']['SHFLX'] = {'plottype': '3', 'obs': ['JRA25_1', 'NCEP_1', 'LARYEA_1']}
diags_collection['3']['TREFHT'] = {'plottype': '3', 'obs': ['WILLMOTT_1', 'LEGATES_1', 'JRA25_1', 'CRU_1']}
diags_collection['3']['FLNSC'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['FLDS'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['FSDSC'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['LWCFSRF'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['FSNSC'] = {'plottype': '3', 'obs': ['ISCCP_1']}
diags_collection['3']['CLDHGH_VISIR'] = {'plottype': '3', 'obs': ['ISCCP_1'], 'modelvar':'CLDHGH'}
diags_collection['3']['PREH2O'] = {'plottype': '3', 'obs': ['NCEP_1', 'NVAP_1', 'JRA25_1', 'ERA40_1', 'MODIS_1', 'ECMWF_1', 'AIRS_1', 'SSMI_1']}
diags_collection['3']['CLDMED_VISIR'] = {'plottype': '3', 'obs': ['ISCCP_1'], 'modelvar':'CLDMED'}
diags_collection['3']['QFLX'] = {'plottype': '3', 'obs': ['WHOI_1', 'ECMWF_1', 'LARYEA_1']}
diags_collection['3']['PSL'] = {'plottype': '3', 'obs': ['JRA25_1', 'NCEP_1']}
diags_collection['3']['FLNS'] = {'plottype': '3', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['3']['CLDLOW_VISIR'] = {'plottype': '3', 'obs': ['ISCCP_1'], 'modelvar':'CLDLOW'}
diags_collection['3']['PRECT'] = {'plottype': '3', 'obs': ['XA_1', 'GPCP_1', 'LEGATES_1', 'TRMM_1', 'SSMI_1']}
diags_collection['3']['CLDHGH'] = {'plottype': '3', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
# *** Collection 1 ***
diags_collection['1'] = {}
diags_collection['1']['desc'] = 'Tables of ANN, DJF, JJA, global and regional means and RMSE.'
diags_collection['1']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['1']['package'] = 'AMWG'
diags_collection['1']['regions'] = ['Global', 'Tropics', 'Southern_Extratropics', 'Northern_Extratropics']
# *** Collection so (southern ocean) (part of Tier 1B) ***
diags_collection['so'] = {}
diags_collection['so']['desc'] = 'Tier 1B Diagnostics (Southern Ocean)'
diags_collection['so']['package'] = 'AMWG'
diags_collection['so']['combined'] = True
diags_collection['so']['options'] = {'logo':'no'}
diags_collection['so']['SHFLX'] = {'plottype': '3', 'obs': ['LARYEA_1'], 'regions':['S_Hemisphere_Land']}
diags_collection['so']['QFLX'] = {'plottype': '5', 'obs':['LARYEA_1'], 'regions':['S_Hemisphere_Land']}
diags_collection['so']['FSNS'] = {'plottype': '7', 'obs':['LARYEA_1'] }
diags_collection['so']['FLDS'] = {'plottype': '3', 'obs':['ISCCP_1'], 'regions':['S_Hemisphere_Land']}
diags_collection['so']['OMEGA'] = {'plottype': '4', 'obs':['ERAI_1'] } 
diags_collection['so']['T'] = {'plottype': '4', 'obs':['ERAI_1'] }
diags_collection['so']['LHFLX'] = {'plottype': '4', 'obs':['WHOI_1'] }
diags_collection['so']['SWCF'] = {'plottype': '5', 'obs':['CERES-EBAF_1'] }
diags_collection['so']['PRECT'] = {'plottype': '5', 'obs':['GPCP_1'] }
diags_collection['so']['TREFHT'] = {'plottype': '5', 'obs':['WILLMOTT_1'] }
diags_collection['so']['LWCF'] = {'plottype': '5', 'obs':['CERES-EBAF_1'] }
diags_collection['so']['AODVIS'] = {'plottype': '5', 'obs':['AOD_550_1'] }
diags_collection['so']['SURF_WIND'] = {'plottype': '6', 'obs':['NCEP_1'], 'regions':['S_Hemisphere_Land'] }
diags_collection['so']['STRESS'] = {'plottype': '6', 'obs':['ERS_1'] }
diags_collection['so']['CLDTOT'] = {'plottype': '9', 'obs':['CLOUDSAT_1'], 'regions':['S_Hemisphere_Land'] }
# *** Collection topten aka Tier 1A***
diags_collection['topten'] = {}
diags_collection['topten']['combined'] = True
diags_collection['topten']['desc'] = 'Tier 1A Diagnostics'
diags_collection['topten']['package'] = 'AMWG'
diags_collection['topten']['PSL'] = {'plottype': '5', 'obs': ['ERAI_1']}
diags_collection['topten']['STRESS'] = {'plottype': '6', 'obs': ['ERS_1']}
#diags_collection['topten']['SURF_STRESS'] = {'plottype': '6', 'obs': ['ERS_1']}
diags_collection['topten']['TREFHT'] = {'plottype': '5', 'obs': ['WILLMOTT_1']}
diags_collection['topten']['LWCF'] = {'plottype': '5', 'obs': ['CERES-EBAF_1']}
diags_collection['topten']['PRECT'] = {'plottype': '5', 'obs': ['GPCP_1']}
diags_collection['topten']['AODVIS'] = {'plottype': '5', 'obs': ['AOD_550_1']}
diags_collection['topten']['U'] = {'plottype': '5', 'obs': ['ERAI_1']}
diags_collection['topten']['T'] = {'plottype': '4', 'obs': ['ERAI_1']}
diags_collection['topten']['SWCF'] = {'plottype': '5', 'obs': ['CERES-EBAF_1']}
diags_collection['topten']['RELHUM'] = {'plottype': '4', 'obs': ['ERAI_1']}
# *** Collection 2 ***
diags_collection['2'] = {}
diags_collection['2']['desc'] = 'Line plots of annual implied northward transports.'
diags_collection['2']['preamble'] = '<p>The computation of the implied northward transports follows the conventions described in the paper by <a href="http://www.cgd.ucar.edu/cas/papers/jclim2001a/transpts.html">Trenberth and Caron (2001)</a>. Their corrections applied to the southern oceans poleward of 30S are not used in the calculations, and the NCEP derived values plotted here are their unadjusted values. Webpage about the NCEP derived data. A plot of the ocean basins used in the calculations.'
diags_collection['2']['package'] = 'AMWG'
diags_collection['2']['Atmospheric_Heat'] = {'plottype': '2', 'obs': ['NCEP_1']}
diags_collection['2']['Ocean_Freshwater'] = {'plottype': '2', 'obs': ['ECMWF_1']}
diags_collection['2']['Ocean_Heat'] = {'plottype': '2', 'obs': ['NCEP_1']}
diags_collection['2']['Surface_Heat'] = {'plottype': '2', 'obs': ['NA_1']}
# *** Collection 5 ***
diags_collection['5'] = {}
diags_collection['5']['desc'] = 'Horizontal contour plots of DJF, JJA and ANN means'
diags_collection['5']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['5']['package'] = 'AMWG'
diags_collection['5']['combined'] = True
diags_collection['5']['CLDMED'] = {'plottype': '5', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['5']['FSDS'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['FSNTOA'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['5']['LWCF'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['5']['FSNTOAC'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['5']['TS'] = {'plottype': '5', 'obs': ['NCEP_1']}
diags_collection['5']['T'] = {'plottype': '5', 'obs': ['ECMWF_1', 'JRA25_1', 'AIRS_1', 'ERA40_1', 'NCEP_1'], 'varopts':['200', '850']}
diags_collection['5']['MEANTAU'] = {'plottype': '5', 'obs': ['ISCCP_1', 'MODIS_1']}
diags_collection['5']['SWCFSRF'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['ALBEDO'] = {'plottype': '5', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['5']['SWCF'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1'], 'regions':['Global', 'Tropics']}
diags_collection['5']['MEANTTOP'] = {'plottype': '5', 'obs': ['ISCCP_1', 'MODIS_1']}
# TRMM only has data in the tropics, but there is no trivial way to split just that out without lots of special casing.
diags_collection['5']['PRECT'] = {'plottype': '5', 'obs': ['XA_1', 'GPCP_1', 'LEGATES_1', 'SSMI_1', 'TRMM_1'], 'regions':['Global','Tropics']}
diags_collection['5']['U'] = {'plottype': '5', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['200']}
diags_collection['5']['TTRP'] = {'plottype': '5', 'obs': ['ECMWF_1', 'NCEP_1']}
diags_collection['5']['FLUTC'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['5']['FLDSC'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['FSNS'] = {'plottype': '5', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['5']['Z3'] = {'plottype': '5', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['500', '300']}
diags_collection['5']['TGCLDLWP'] = {'plottype': '5', 'obs': ['SSMI_1', 'NVAP_1', 'SSMI_1', 'NVAP_1', 'MODIS_1'], 'regions':['Global', 'Tropics']}
diags_collection['5']['FLUT'] = {'plottype': '5', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['5']['CLDTOT_VISIR'] = {'plottype': '5', 'obs': ['ISCCP_1'], 'modelvar':'CLDTOT'}
diags_collection['5']['LHFLX'] = {'plottype': '5', 'obs': ['WHOI_1', 'ECMWF_1', 'JRA25_1', 'ERA40_1']}
diags_collection['5']['SHFLX'] = {'plottype': '5', 'obs': ['JRA25_1', 'NCEP_1', 'LARYEA_1']}
diags_collection['5']['TREFHT'] = {'plottype': '5', 'obs': ['WILLMOTT_1', 'LEGATES_1', 'JRA25_1', 'CRU_1']}
diags_collection['5']['FLNSC'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['CLDTOT'] = {'plottype': '5', 'obs': ['ISCCP_1', 'WARREN_1', 'CLOUDSAT_1']}
diags_collection['5']['FLDS'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['TCLDAREA'] = {'plottype': '5', 'obs': ['ISCCP_1', 'MODIS_1']}
diags_collection['5']['ALBEDOC'] = {'plottype': '5', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['5']['MEANPTOP'] = {'plottype': '5', 'obs': ['ISCCP_1', 'MODIS_1']}
diags_collection['5']['LWCFSRF'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['FSNSC'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['CLDHGH_VISIR'] = {'plottype': '5', 'obs': ['ISCCP_1'], 'modelvar':'CLDHGH'}
diags_collection['5']['EP'] = {'plottype': '5', 'obs': ['ECMWF_1']}
diags_collection['5']['CLDMED_VISIR'] = {'plottype': '5', 'obs': ['ISCCP_1'], 'modelvar':'CLDMED'}
diags_collection['5']['QFLX'] = {'plottype': '5', 'obs': ['WHOI_1', 'ECMWF_1', 'LARYEA_1']}
diags_collection['5']['PSL'] = {'plottype': '5', 'obs': ['JRA25_1', 'NCEP_1']}
diags_collection['5']['SST'] = {'plottype': '5', 'obs': ['HADISST_PD_1', 'HADISST_PI_1', 'HADISST_1']}
diags_collection['5']['FLNS'] = {'plottype': '5', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['5']['CLDLOW'] = {'plottype': '5', 'obs': ['ISCCP_1', 'WARREN_1', 'CLOUDSAT_1']}
diags_collection['5']['CLDLOW_VISIR'] = {'plottype': '5', 'obs': ['ISCCP_1'], 'modelvar':'CLDLOW'}
diags_collection['5']['PRECT_LAND'] = {'plottype': '5', 'obs': ['PRECL_1']}
diags_collection['5']['PRECIP'] = {'plottype': '5', 'obs': ['WILLMOTT_1']}
diags_collection['5']['FSDSC'] = {'plottype': '5', 'obs': ['ISCCP_1']}
diags_collection['5']['CLDHGH'] = {'plottype': '5', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['5']['PREH2O'] = {'plottype': '5', 'obs': ['NCEP_1', 'NVAP_1', 'JRA25_1', 'ERA40_1', 'MODIS_1', 'ECMWF_1', 'SSMI_1'], 'regions':['Global', 'Tropics']}
# *** Collection 4 ***
diags_collection['4'] = {}
diags_collection['4']['desc'] = 'Vertical contour plots of DJF, JJA and ANN zonal means'
diags_collection['4']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['4']['combined'] = True
diags_collection['4']['package'] = 'AMWG'
diags_collection['4']['U'] = {'plottype': '4', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1']}
diags_collection['4']['SHUM'] = {'plottype': '4', 'obs': ['ECMWF_1', 'JRA25_1', 'AIRS_1', 'ERA40_1', 'NCEP_1']}
diags_collection['4']['RELHUM'] = {'plottype': '4', 'obs': ['ECMWF_1', 'NCEP_1', 'AIRS_1', 'ERA40_1']}
diags_collection['4']['OMEGA'] = {'plottype': '4', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1']}
diags_collection['4']['T'] = {'plottype': '4', 'obs': ['NCEP_1', 'JRA25_1', 'ERA40_1', 'ECMWF_1', 'AIRS_1']}
# *** Collection 7 ***
diags_collection['7'] = {}
diags_collection['7']['desc'] = 'Polar contour and vector plots of DJF, JJA and ANN means'
diags_collection['7']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['7']['regions'] = ['N_Hemisphere_Land', 'S_Hemisphere_Land']
diags_collection['7']['package'] = 'AMWG'
diags_collection['7']['PSL'] = {'plottype': '7', 'obs': ['JRA25_1', 'NCEP_1']}
diags_collection['7']['CLDLOW'] = {'plottype': '7', 'obs': ['ISCCP_1', 'WARREN_1', 'CLOUDSAT_1']}
diags_collection['7']['TREFHT'] = {'plottype': '7', 'obs': ['WILLMOTT_1']}
diags_collection['7']['Z3'] = {'plottype': '7', 'obs': ['ECMWF_1', 'JRA25_1', 'NCEP_1', 'ERA40_1'], 'varopts':['500']}
diags_collection['7']['FSNS'] = {'plottype': '7', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['7']['CLDHGH'] = {'plottype': '7', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['7']['CLDMED'] = {'plottype': '7', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['7']['FSDSC'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['QFLX'] = {'plottype': '7', 'obs': ['LARYEA_1']}
diags_collection['7']['FSDS'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['FLDS'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['SHFLX'] = {'plottype': '7', 'obs': ['LARYEA_1']}
diags_collection['7']['ALBEDO'] = {'plottype': '7', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['7']['TS'] = {'plottype': '7', 'obs': ['NCEP_1']}
diags_collection['7']['FLNSC'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['FLUT'] = {'plottype': '7', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['7']['FLDSC'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['FLUTC'] = {'plottype': '7', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['7']['PRECT'] = {'plottype': '7', 'obs': ['GPCP_1']}
diags_collection['7']['FSNSC'] = {'plottype': '7', 'obs': ['ISCCP_1']}
diags_collection['7']['ALBEDOC'] = {'plottype': '7', 'obs': ['CERES2_1', 'CERES_1']}
diags_collection['7']['SURF_WIND'] = {'plottype': '7', 'obs': ['NCEP_1']}
diags_collection['7']['PS'] = {'plottype': '7', 'obs': ['NCEP_1']}
diags_collection['7']['ICEFRAC'] = {'plottype': '7', 'obs': ['SSMI_1', 'HADISST_1']}
diags_collection['7']['FLNS'] = {'plottype': '7', 'obs': ['ISCCP_1', 'LARYEA_1']}
diags_collection['7']['FSNTOA'] = {'plottype': '7', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['7']['CLDTOT'] = {'plottype': '7', 'obs': ['ISCCP_1', 'WARREN_1', 'CLOUDSAT_1']}
diags_collection['7']['FSNTOAC'] = {'plottype': '7', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
# These 4 are northern only.
diags_collection['7']['CLDHGH_VISIR'] = {'plottype': '7', 'obs': ['ISCCP_1'], 'regions':['N_Hemisphere_Land'], 'modelvar':'CLDHGH'}
diags_collection['7']['CLDLOW_VISIR'] = {'plottype': '7', 'obs': ['ISCCP_1'], 'regions':['N_Hemisphere_Land'], 'modelvar':'CLDLOW'}
diags_collection['7']['CLDMED_VISIR'] = {'plottype': '7', 'obs': ['ISCCP_1'], 'regions':['N_Hemisphere_Land'], 'modelvar':'CLDMED'}
diags_collection['7']['CLDTOT_VISIR'] = {'plottype': '7', 'obs': ['ISCCP_1'], 'regions':['N_Hemisphere_Land'], 'modelvar':'CLDTOT'}
# *** Collection 6 ***
diags_collection['6'] = {}
diags_collection['6']['desc'] = 'Horizontal vector plots of DJF, JJA and ANN means'
diags_collection['6']['combined'] = True
diags_collection['6']['regions'] = ['Tropics', 'Global']
diags_collection['6']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['6']['package'] = 'AMWG'
#diags_collection['6']['SURF_STRESS'] = {'plottype': '6', 'obs': ['NCEP_1', 'JRA25_1', 'LARYEA_1', 'ERS_1']}
diags_collection['6']['STRESS'] = {'plottype': '6', 'obs': ['NCEP_1', 'JRA25_1', 'LARYEA_1', 'ERS_1']}
# *** Collection 9 ***
diags_collection['9'] = {}
diags_collection['9']['desc'] = 'Horizontal contour plots of DJF-JJA differences'
diags_collection['9']['package'] = 'AMWG'
diags_collection['9']['combined'] = True
diags_collection['9']['CLDTOT'] = {'plottype': '9', 'obs': ['ISCCP_1', 'CLOUDSAT_1']}
diags_collection['9']['PSL'] = {'plottype': '9', 'obs': ['NCEP_1']}
diags_collection['9']['T'] = {'plottype': '9', 'obs': ['ECMWF_1', 'JRA25_1', 'AIRS_1', 'ERA40_1', 'NCEP_1'], 'varopts':['850']}
diags_collection['9']['TREFHT'] = {'plottype': '9', 'obs': ['LEGATES_1', 'NCEP_1']}
diags_collection['9']['LWCF'] = {'plottype': '9', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['9']['PRECT'] = {'plottype': '9', 'obs': ['XA_1', 'GPCP_1']}
diags_collection['9']['SWCF'] = {'plottype': '9', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['9']['PREH2O'] = {'plottype': '9', 'obs': ['NCEP_1', 'NVAP_1', 'JRA25_1', 'ERA40_1', 'ECMWF_1']}
# *** Collection 8 ***
diags_collection['8'] = {}
diags_collection['8']['desc'] = 'Annual cycle contour plots of zonal means'
diags_collection['8']['package'] = 'AMWG'
diags_collection['8']['PREH2O'] = {'plottype': '8', 'obs': ['NCEP_1', 'NVAP_1', 'JRA25_1', 'ERA40_1', 'ECMWF_1']}
diags_collection['8']['PRECT'] = {'plottype': '8', 'obs': ['XA_1', 'GPCP_1']}
diags_collection['8']['FLUT'] = {'plottype': '8', 'obs': ['ERBE_1', 'CERES2_1', 'CERES_1']}
diags_collection['8']['U'] = {'plottype': '8', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1'], 'varopts':['200']}
# *** Collection 4a ***
diags_collection['4a'] = {}
diags_collection['4a']['desc'] = 'Vertical (XZ) contour plots of DJF, JJA and ANN meridional means'
diags_collection['4a']['seasons'] = ['DJF', 'JJA', 'ANN']
diags_collection['4a']['package'] = 'AMWG'
diags_collection['4a']['U'] = {'plottype': '4a', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1']}
diags_collection['4a']['SHUM'] = {'plottype': '4a', 'obs': ['ECMWF_1', 'JRA25_1', 'AIRS_1', 'ERA40_1', 'NCEP_1']}
diags_collection['4a']['RELHUM'] = {'plottype': '4a', 'obs': ['ECMWF_1', 'NCEP_1', 'AIRS_1', 'ERA40_1']}
diags_collection['4a']['OMEGA'] = {'plottype': '4a', 'obs': ['ECMWF_1', 'NCEP_1', 'JRA25_1', 'ERA40_1']}
diags_collection['4a']['T'] = {'plottype': '4a', 'obs': ['NCEP_1', 'JRA25_1', 'ERA40_1', 'ECMWF_1', 'AIRS_1']}


# *** Variables List ***
# Right now this is just used for creating descriptive names on web pages. It could have more useful info about the
# variable. It could also go away if data was more CF compliant and we could just extract this info from datasets
diags_varlist['TREFHT'] = {'desc': '2-meter temperature (land) (Northern)'}
diags_varlist['FSNTOAC'] = {'desc': 'TOA clearsky new SW flux'}
diags_varlist['CLDHGH'] = {'desc': 'High cloud amount (IR clouds) (Northern)'}
diags_varlist['TTRP'] = {'desc': 'Tropopause temperature'}
diags_varlist['Z3'] = {'desc': 'Geopotential height (Northern)'}
diags_varlist['FSNS'] = {'desc': 'Surf Net SW flux'}
diags_varlist['CLDLOW'] = {'desc': 'Low cloud amount (IR clouds) (Northern)'}
diags_varlist['TS'] = {'desc': 'Surface temperature (Northern)'}
diags_varlist['TCLDAREA'] = {'desc': 'Total cloud area (Day)'}
diags_varlist['T'] = {'desc': 'Temperature'}
diags_varlist['PRECT'] = {'desc': 'Precipitation rate (Northern)'}
diags_varlist['PS'] = {'desc': 'Surface pressure (Northern)'}
diags_varlist['PREH2O'] = {'desc': 'Total precipitable water'}
diags_varlist['CLDMED'] = {'desc': 'Mid cloud amount (IR clouds)'}
diags_varlist['FSDS'] = {'desc': 'Surf SW downwelling flux'}
diags_varlist['FSNTOA'] = {'desc': 'TOA new SW flux'}
diags_varlist['CLDLOW'] = {'desc': 'Low cloud amount (IR clouds)'}
diags_varlist['FLDSC'] = {'desc': 'Clearsky Surf LW downwelling flux (Northern)'}
diags_varlist['FSNTOA'] = {'desc': 'TOA net SW flux (Northern)'}
diags_varlist['CLDMED_VISIR'] = {'desc': 'Mid cloud amount (VIS/IR/NIR) clouds) (Northern)'}
diags_varlist['MEANTAU'] = {'desc': 'Mean cloud optical thickness (Day)'}
diags_varlist['SWCF'] = {'desc': 'TOA shortwave cloud forcing'}
diags_varlist['ALBEDO'] = {'desc': 'TOA Albedo'}
diags_varlist['MEANTTOP'] = {'desc': 'Mean cloud top temperature (Day)'}
diags_varlist['FLDS'] = {'desc': 'Surf LW downwelling flux (Northern)'}
diags_varlist['FSNSC'] = {'desc': 'Clearsky Surf Net SW flux (Northern)'}
diags_varlist['RESTOA'] = {'desc': 'TOA residual energy flux'}
diags_varlist['SHFLX'] = {'desc': 'Surface sensible heat flux (Northern)'}
diags_varlist['SHFLX'] = {'desc': 'Surface sensible heat flux'}
diags_varlist['FLNSC'] = {'desc': 'Clearsky Surf Net LW Flux'}
diags_varlist['ALBEDOC'] = {'desc': 'TOA clearsky albedo (Northern)'}
diags_varlist['ALBEDOC'] = {'desc': 'TOA clearsky albedo'}
diags_varlist['RELHUM'] = {'desc': 'Relative humidity'}
diags_varlist['EP'] = {'desc': 'Evaporation - precipitation'}
diags_varlist['QFLX'] = {'desc': 'Surface water flux'}
diags_varlist['PSL'] = {'desc': 'Sea-level pressure'}
diags_varlist['CLDTOT_VISIR'] = {'desc': 'Total cloud amount (VIS/IR/NIR) clouds) (Northern)'}
diags_varlist['SST'] = {'desc': 'Sea surface temperature'}
diags_varlist['FLNS'] = {'desc': 'Surf Net LW flux'}
diags_varlist['ICEFRAC'] = {'desc': 'Sea-ice area (Northern)'}
diags_varlist['CLDLOW_VISIR'] = {'desc': 'Low cloud amount (VIS/IR/NIR clouds)'}
diags_varlist['PRECT'] = {'desc': 'Precipitation rate'}
diags_varlist['PRECT_LAND'] = {'desc': 'Precipitation rate (land)'}
diags_varlist['PRECIP'] = {'desc': 'Cumulative precipitation (land)'}
diags_varlist['TMQ'] = {'desc': 'Precipitable Water'}
diags_varlist['LWCF'] = {'desc': 'TOA longwave cloud forcing'}
diags_varlist['FLDS'] = {'desc': 'Surf LW downwelling flux'}
diags_varlist['SWCFSRF'] = {'desc': 'Surf SW Cloud Forcing'}
diags_varlist['OMEGA'] = {'desc': 'Pressure vertical velocity'}
diags_varlist['FLUT'] = {'desc': 'TOA upward LW flux'}
diags_varlist['FLUT'] = {'desc': 'TOA upward LW flux (Northern)'}
diags_varlist['TREFHT'] = {'desc': '2-meter air temperature (land)'}
diags_varlist['CLDLOW_VISIR'] = {'desc': 'Low cloud amount (VIS/IR/NIR) clouds) (Northern)'}
diags_varlist['Atmospheric_heat'] = {'desc': 'Atmospheric Heat', 'filekey':'ATM_HEAT'}
diags_varlist['FSDSC'] = {'desc': 'Clearsky Surf SW downwelling flux'}
diags_varlist['QFLX'] = {'desc': 'Surface water flux (Northern)'}
diags_varlist['CLDHGH_VISIR'] = {'desc': 'High cloud amount (VIS/IR/NIR clouds)'}
diags_varlist['SURF_STRESS'] = {'desc': 'Surface wind stress (ocean)'}
diags_varlist['FLDSC'] = {'desc': 'Clearsky Surf LW downwelling flux'}
diags_varlist['CLDHGH'] = {'desc': 'High cloud amount (IR clouds)'}
diags_varlist['FSNS'] = {'desc': 'Surf Net SW flux (Northern)'}
diags_varlist['FLUTC'] = {'desc': 'TOA clearsky upward LW flux'}
diags_varlist['Ocean_Freshwater'] = {'desc': 'Ocean Freshwater', 'filekey':'OCN_FRESH'}
diags_varlist['CLDTOT'] = {'desc': 'Total cloud amount (IR clouds) (Northern)'}
diags_varlist['MSE'] = {'desc': 'Moist Static Energy'}
diags_varlist['SHUM'] = {'desc': 'Specific humidity'}
diags_varlist['FLNS'] = {'desc': 'Surf Net LW flux (Northern)'}
diags_varlist['FSDSC'] = {'desc': 'Clearsky Surf SW downwelling flux (Northern)'}
diags_varlist['ALBEDO'] = {'desc': 'TOA albedo (Northern)'}
diags_varlist['TS'] = {'desc': 'Surface temperature'}
diags_varlist['TGCLDLWP'] = {'desc': 'Cloud liquid water'}
diags_varlist['CLOUD'] = {'desc': 'Cloud Fraction'}
diags_varlist['CLDTOT_VISIR'] = {'desc': 'Total cloud amount (VIS/IR/NIR clouds)'}
diags_varlist['LHFLX'] = {'desc': 'Surface latent heat flux'}
diags_varlist['FLUTC'] = {'desc': 'TOA clearsky upward LW flux (Northern)'}
diags_varlist['CLDTOT'] = {'desc': 'Mid cloud amount (IR clouds)'}
diags_varlist['CLDMED'] = {'desc': 'Mid cloud amount (IR clouds) (Northern)'}
diags_varlist['Q'] = {'desc': 'Specific Humidity'}
diags_varlist['FSDS'] = {'desc': 'Surf SW downwelling flux (Northern)'}
diags_varlist['U'] = {'desc': 'Zonal Wind'}
diags_varlist['Ocean_Heat'] = {'desc': 'Ocean Heat', 'filekey':'OCN_HEAT'}
diags_varlist['LWCFSRF'] = {'desc': 'Surf LW Cloud Forcing'}
diags_varlist['SWCF_LWCF'] = {'desc': 'SW/LW Cloud Forcing'}
diags_varlist['FSNSC'] = {'desc': 'Clearsky Surf Net SW Flux'}
diags_varlist['SURF_WIND'] = {'desc': 'Near surface wind (Northern)'}
diags_varlist['CLDMED_VISIR'] = {'desc': 'Mid cloud amount (VIS/IR/NIR clouds)'}
diags_varlist['MEANPTOP'] = {'desc': 'Mean cloud top pressure (Day)'}
diags_varlist['CLDHGH_VISIR'] = {'desc': 'High cloud amount (VIS/IR/NIR) clouds) (Northern)'}
diags_varlist['FLNSC'] = {'desc': 'Clearsky Surf Net LW flux (Northern)'}
diags_varlist['PSL'] = {'desc': 'Sea-level pressure (Northern)'}
diags_varlist['AODVIS'] = {'desc': 'Aerosol optical depth'}
diags_varlist['FSNTOAC'] = {'desc': 'TOA clearsky net SW flux (Northern)'}


# *** Observation sets ***
diags_obslist['HADISST_PD_1'] = {'filekey': 'HADISST_PD', 'desc': 'HadISST/OI.v2 (Present Day) 1999-2008'}
diags_obslist['WARREN_1'] = {'filekey': 'WARREN', 'desc': 'Warren Cloud Surface OBS'}
diags_obslist['LEGATES_1'] = {'filekey': 'LEGATES', 'desc': 'Legates and Willmott 1920-80'}
diags_obslist['SGP_1'] = {'filekey': 'SGP', 'desc': 'Southern Great Plains (SGP)'}
diags_obslist['ERA40_1'] = {'filekey': 'ERA40', 'desc': 'ERA40 Reanalysis 1980-2001'}
diags_obslist['ERS_1'] = {'filekey': 'ERS', 'desc': 'ERS Scatterometer 1992-2000'}
diags_obslist['CLOUDSAT_1'] = {'filekey': 'CLOUDSAT', 'desc': 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008'}
diags_obslist['WHOI_1'] = {'filekey': 'WHOI', 'desc': 'Woods Hole OAFLUX 1958-2006'}
diags_obslist['NCEP_1'] = {'filekey': 'NCEP', 'desc': 'NCEP Reanalysis 1979-98'}
diags_obslist['AOD_550_1'] = {'filekey': 'sat', 'desc': 'AOD Data'}
diags_obslist['NSA_1'] = {'filekey': 'NSA', 'desc': 'North Slope of Alaska (NSA)'}
diags_obslist['JRA25_1'] = {'filekey': 'JRA25', 'desc': 'JRA25 Reanalysis 1979-04'}
diags_obslist['TWP2_1'] = {'filekey': 'TWP2', 'desc': 'Tropical Western Pacific--Region 2 (TWP2)'}
diags_obslist['ERBE_1'] = {'filekey': 'ERBE', 'desc': 'ERBE Feb1985-Apr1989'}
diags_obslist['CERES_1'] = {'filekey': 'CERES', 'desc': 'CERES 2000-2003'}
diags_obslist['WILLMOTT_1'] = {'filekey': 'WILLMOTT', 'desc': 'Willmott and Matsuura 1950-99'}
diags_obslist['PRECL_1'] = {'filekey': 'PRECL', 'desc': 'PREC/L (CMAP) 1948-2001'}
diags_obslist['TWP3_1'] = {'filekey': 'TWP3', 'desc': 'Tropical Western Pacific--Region 3 (TWP3)'}
diags_obslist['TWP1_1'] = {'filekey': 'TWP1', 'desc': 'Tropical Western Pacific--Region 1 (TWP1)'}
diags_obslist['GPCP_1'] = {'filekey': 'GPCP', 'desc': 'GPCP 1979-2003'}
diags_obslist['CERES2_1'] = {'filekey': 'CERES2', 'desc': 'CERES2 March 2000-October 2005'}
diags_obslist['CRU_1'] = {'filekey': 'CRU', 'desc': 'IPCC/CRU Climatology 1961-90'}
diags_obslist['ERAI_1'] = {'filekey': 'ERAI', 'desc': 'ERA Interim Reanalysis'}
diags_obslist['HADISST_PI_1'] = {'filekey': 'HADISST_PI', 'desc': 'HadISST/OI.v2 (Pre-Indust) 1870-1900'}
diags_obslist['TRMM_1'] = {'filekey': 'TRMM', 'desc': 'TRMM (3B43) 1998-Feb2004 - Tropics'}
diags_obslist['CERES-EBAF_1'] = {'filekey': 'CERES-EBAF', 'desc': 'CERES-EBAF'}
diags_obslist['AIRS_1'] = {'filekey': 'AIRS', 'desc': 'AIRS IR Sounder 2002-06'}
diags_obslist['NVAP_1'] = {'filekey': 'NVAP', 'desc': 'NVAP 1988-1999'}
diags_obslist['SHEBA_1'] = {'filekey': 'SHEBA', 'desc': 'Surface Heat Budget of the Arctic Ocean (SHEBA)'}
diags_obslist['LARYEA_1'] = {'filekey': 'LARYEA', 'desc': 'Large-Yeager 1984-2004'}
diags_obslist['NA_1'] = {'filekey': 'N/A', 'desc': 'NA'}
diags_obslist['MODIS_1'] = {'filekey': 'MODIS', 'desc': 'MODIS Mar2000-Aug2004'}
diags_obslist['ISCCP_1'] = {'filekey': 'ISCCP', 'desc': 'ISCCP D1 Daytime Jul1983-Sep2001'}
diags_obslist['HADISST_1'] = {'filekey': 'HADISST', 'desc': 'HadISST/OI.v2 (Climatology) 1982-2001'}
diags_obslist['XA_1'] = {'filekey': 'XA', 'desc': 'CMAP (Xie-Arkin) 1979-98'}
diags_obslist['SSMI_1'] = {'filekey': 'SSMI', 'desc': 'SSM/I (Wentz) 1987-2000'}
diags_obslist['ECMWF_1'] = {'filekey': 'ECMWF', 'desc': 'ECMWF Reanalysis 1979-93'}


# Code testing collection. These will not be run but will generate the command line for testing/verification
diags_collection['dontrun'] = {}
diags_collection['dontrun']['desc'] = 'Tier 1B Diagnostics (Southern Ocean)'
diags_collection['dontrun']['package'] = 'AMWG'
diags_collection['dontrun']['options'] = {'logo':'no'}
diags_collection['dontrun']['SHFLX'] = {'plottype': '3', 'obs': ['LARYEA_1'], 'regions':['S_Hemisphere_Land'], 'seasons':['ANN','DJF']}
diags_collection['dontrun']['QFLX'] = {'plottype': '5', 'obs':['LARYEA_1'], 'regions':['S_Hemisphere_Land', 'Tropics']}
diags_collection['dontrun']['FSNS'] = {'plottype': '7', 'obs':['LARYEA_1'] }
diags_collection['dontrun']['FLDS'] = {'plottype': '3', 'obs':['ISCCP_1'], 'regions':['S_Hemisphere_Land']}
diags_collection['dontrun']['T'] = {'plottype': '4', 'obs':['ERAI_1'] }
diags_collection['dontrun']['LHFLX'] = {'plottype': '4', 'obs':['ECMWF_1'] }
diags_collection['dontrun']['SWCF'] = {'plottype': '5', 'obs':['CERES-EBAF_1'] }
diags_collection['dontrun']['PRECT'] = {'plottype': '5', 'obs':['GPCP_1'] }
diags_collection['dontrun']['LWCF'] = {'plottype': '5', 'obs':['CERES-EBAF_1'] }
diags_collection['dontrun']['AODVIS'] = {'plottype': '5', 'obs':['AOD_550_1'] }
diags_collection['dontrun']['SURF_WIND'] = {'plottype': '6', 'obs':['NCEP_1'], 'regions':['S_Hemisphere_Land', 'Global', 'Tropics'] }
diags_collection['dontrun']['PBOT'] = {'plottype':'2', 'obs':['NA_1'], 'package':'LMWG'}
diags_collection['dontrun']['TSA'] = {'plottype':'2', 'obs':['NA_1'], 'package':'LMWG'}
