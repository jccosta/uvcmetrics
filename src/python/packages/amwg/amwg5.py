# AMWG Diagnostics, plot set 5.
# Here's the title used by NCAR:
# DIAG Set 5 - Horizontal Contour Plots of Seasonal Means

from pprint import pprint
from metrics.packages.amwg.amwg import amwg_plot_plan
from metrics.packages.amwg.tools import src2modobs, src2obsmod, get_textobject, get_format, get_model_case
from metrics.packages.amwg.derivations.vertical import *
from metrics.packages.plotplan import plot_plan
from metrics.computation.reductions import *
from metrics.computation.plotspec import *
from metrics.fileio.findfiles import *
from metrics.common.utilities import *
from metrics.computation.region import *
from unidata import udunits
import cdutil, cdutil.times, numpy, pdb
import logging

logger = logging.getLogger(__name__)

seasonsyr=cdutil.times.Seasons('JFMAMJJASOND')

class amwg_plot_set5(amwg_plot_plan):
    """represents one plot from AMWG Diagnostics Plot Sets 5 and 6  <actually only the contours, set 5>
    NCAR has the same menu for both plot sets, and we want to ease the transition from NCAR
    diagnostics to these; so both plot sets will be done together here as well.
    Each contour plot is a set of three contour plots: one each for model output, observations, and
    the difference between the two.  A plot's x-axis is longitude and its y-axis is the latitude;
    normally a world map will be overlaid."""

    """represents one plot from AMWG Diagnostics Plot Set 5
    Each contour plot is a set of three contour plots: one each for model output, observations, and
    the difference between the two.  A plot's x-axis is longitude and its y-axis is the latitude;
    normally a world map will be overlaid. """
    name = '5 - Horizontal Contour Plots of Seasonal Means'
    number = '5'

    def __init__( self, model, obs,  varid, seasonid=None, regionid=None, aux=None, names={}, plotparms=None ):
        """filetable1, filetable2 should be filetables for model and obs.
        varid is a string identifying the variable to be plotted, e.g. 'TREFHT'.
        seasonid is a string such as 'DJF'."""
        filetable1, filetable2 = self.getfts(model, obs)
        plot_plan.__init__(self,seasonid, regionid)
        self.plottype = 'Isofill'
        if plotparms is None:
            plotparms = { 'model':{'colormap':'rainbow'},
                          'obs':{'colormap':'rainbow'},
                          'diff':{'colormap':'bl_to_darkred'} }
        self.season = cdutil.times.Seasons(self._seasonid)  # note that self._seasonid can differ froms seasonid
        if regionid=="Global" or regionid=="global" or regionid is None:
            self._regionid="Global"
        else:
            self._regionid=regionid
        self.region = interpret_region(regionid)

        self.varid = varid
        self.ft1nom,self.ft2nom = filetable_names(filetable1,filetable2)
        self.ft1nickname,self.ft2nickname = filetable_nicknames(filetable1,filetable2)
        ft1id,ft2id = filetable_ids(filetable1,filetable2)
        self.reduced_variables = {}
        self.derived_variables = {}
        self.plot1_id = ft1id+'_'+varid+'_'+seasonid
        self.plot2_id = ft2id+'_'+varid+'_'+seasonid
        self.plot3_id = ft1id+' - '+ft2id+'_'+varid+'_'+seasonid
        self.plot1var_id = ft1id+'_'+varid+'_var_'+seasonid
        self.plotall_id = ft1id+'_'+ft2id+'_'+varid+'_'+seasonid
        
        if not self.computation_planned:
            self.plan_computation( model, obs, varid, seasonid, aux, names, plotparms )
    @staticmethod
    def _list_variables( model, obs ):
        """returns a list of variable names"""
        allvars = amwg_plot_set5._all_variables( model, obs )
        listvars = allvars.keys()
        listvars.sort()
        return listvars
    @staticmethod
    def _all_variables( model, obs, use_common_derived_vars=True ):
        """returns a dict of varname:varobject entries"""
        allvars = amwg_plot_plan.package._all_variables( model, obs, "amwg_plot_plan" )
        # ...this is what's in the data.  varname:basic_plot_variable
        for varname in amwg_plot_plan.package._list_variables_with_levelaxis(
            model, obs, "amwg_plot_plan" ):
            allvars[varname] = level_variable_for_amwg_set5
            # ...this didn't add more variables, but changed the variable's class
            # to indicate that you can specify a level for it
        if use_common_derived_vars:
            # Now we add varname:basic_plot_variable for all common_derived_variables.
            # This needs work because we don't always have the data needed to compute them...
            # BTW when this part is done better, it should (insofar as it's reasonable) be moved to
            # amwg_plot_plan and shared by all AMWG plot sets.
            for varname in amwg_plot_plan.common_derived_variables.keys():
                allvars[varname] = basic_plot_variable
        return allvars
    def plan_computation( self, model, obs, varid, seasonid, aux, names, plotparms ):
        filetable1, filetable2 = self.getfts(model, obs)
        for filetable in [filetable1, filetable2]:
            if filetable.find_files( 'gw' ):
                # data has Gaussian weights, prefer them over the averager's default
                gw = reduced_variable(
                    variableid='gw', filetable=filetable, season=self.season,
                    reduction_function=(lambda x,vid=None: x) )
                self.reduced_variables[gw.id()] = gw
        if isinstance(aux,Number):
            return self.plan_computation_level_surface( model, obs, varid, seasonid, aux, names, plotparms )
        else:
            return self.plan_computation_normal_contours( model, obs, varid, seasonid, aux, names, plotparms )
    def plan_computation_normal_contours( self, model, obs, varnom, seasonid, aux=None, names={}, plotparms=None ):
        filetable1, filetable2 = self.getfts(model, obs)

        """Set up for a lat-lon contour plot, as in plot set 5.  Data is averaged over all other
        axes."""
        if varnom in filetable1.list_variables():
            vid1,vid1var = self.vars_normal_contours(
                filetable1, varnom, seasonid, aux=None )
        elif varnom in self.common_derived_variables.keys():
            vid1,vid1var = self.vars_commdervar_normal_contours(
                filetable1, varnom, seasonid, aux=None )
        else:
            logger.error("variable %s not found in and cannot be computed from %s",varnom, filetable1)
            return None
        if filetable2 is not None and varnom in filetable2.list_variables():
            vid2,vid2var = self.vars_normal_contours(
                filetable2, varnom, seasonid, aux=None )
        elif varnom in self.common_derived_variables.keys():
            vid2,vid2var = self.vars_commdervar_normal_contours(
                filetable2, varnom, seasonid, aux=None )
        else:
            vid2,vid2var = None,None
        self.single_plotspecs = {}
        ft1src = filetable1.source()
        try:
            ft2src = filetable2.source()
        except:
            ft2src = ''
        all_plotnames = []

        if filetable1 is not None:
            if vid1 is not None:
                self.single_plotspecs[self.plot1_id] = plotspec(
                    vid = ps.dict_idid(vid1),
                    zvars = [vid1],  zfunc = (lambda z: z),
                    plottype = self.plottype,
                    title = ' '.join([varnom, seasonid, 'model']),
                    title1 = ' '.join([varnom, seasonid, 'model']),
                    title2 = 'model',
                    file_descr = 'model',
                    source = names['model'], 
                    plotparms = plotparms[src2modobs(ft1src)])
                all_plotnames.append(self.plot1_id)
                
            if vid1var is not None:
                self.single_plotspecs[self.plot1var_id] = plotspec(
                    vid = ps.dict_idid(vid1var),
                    zvars = [vid1var],  zfunc = (lambda z: z),
                    plottype = self.plottype,
                    title = ' '.join([varnom, seasonid, 'model variance']),
                    title1 = ' '.join([varnom, seasonid, 'model variance']),
                    title2 = 'model variance',
                    file_descr = 'model variance',
                    source = names['model'],
                    plotparms = plotparms[src2modobs(ft1src)] )
                all_plotnames.append(self.plot1var_id)
                
        if filetable2 is not None and vid2 is not None:
            self.single_plotspecs[self.plot2_id] = plotspec(
                vid = ps.dict_idid(vid2),
                zvars = [vid2],  zfunc = (lambda z: z),
                plottype = self.plottype,
                title = ' '.join([varnom, seasonid, 'obs']),
                title1 = ' '.join([varnom, seasonid, 'obs']),
                title2 = "observation",
                file_descr = "obs",
                source = names['obs'], 
                plotparms = plotparms[src2obsmod(ft2src)] )
            all_plotnames.append(self.plot2_id)
            
        if filetable1 is not None and filetable2 is not None and vid1 is not None and vid2 is not None:
            self.single_plotspecs[self.plot3_id] = plotspec(
                vid = ps.dict_id(varnom,'diff',seasonid,filetable1,filetable2),
                zvars = [vid1,vid2],  zfunc = aminusb_2ax,
                plottype = self.plottype,
                title = ' '.join([varnom, seasonid, 'difference']),
                title1 = ' '.join([varnom, seasonid, 'difference']),
                title2 = 'difference',
                file_descr = 'diff',
                plotparms = plotparms['diff'] )
            all_plotnames.append(self.plot3_id)

        if len(all_plotnames)>0:
            self.composite_plotspecs = {
                self.plotall_id: all_plotnames
                }
        else:
            self.composite_plotspecs = {}
        self.computation_planned = True

    def vars_normal_contours( self, filetable, varnom, seasonid, aux=None ):
        reduced_varlis = [
            reduced_variable(
                variableid=varnom, filetable=filetable, season=self.season,
                reduction_function=(lambda x,vid: reduce2latlon_seasonal( x, self.season, self.region, vid) ) ),
            reduced_variable(
                # variance, for when there are variance climatology files
                variableid=varnom+'_var', filetable=filetable, season=self.season,
                reduction_function=(lambda x,vid: reduce2latlon_seasonal( x, self.season, self.region, vid ) ) )
            ]
        for v in reduced_varlis:
            self.reduced_variables[v.id()] = v
        vid = rv.dict_id( varnom, seasonid, filetable )
        vidvar = rv.dict_id( varnom+'_var', seasonid, filetable ) # variance
        return vid, vidvar
    def vars_commdervar_normal_contours( self, filetable, varnom, seasonid, aux=None ):
        """Set up for a lat-lon contour plot, as in plot set 5.  Data is averaged over all other
        axes.  The variable given by varnom is *not* a data variable suitable for reduction.  It is
        a common_derived_variable.  Its inputs will be reduced, then it will be set up as a
        derived_var.
        """
        varid,rvs,dvs = self.commvar2var(
            varnom, filetable, self.season,\
                (lambda x,vid:
                     reduce2latlon_seasonal(x, self.season, self.region, vid, exclude_axes=[
                        'isccp_prs','isccp_tau','cosp_prs','cosp_tau',
                        'modis_prs','modis_tau','cosp_tau_modis',
                        'misr_cth','misr_tau','cosp_htmisr']) ),
        #            ... isccp_prs, isccp_tau etc. are used for cloud variables and need special treatment
            builtin_variables=self.variable_values.keys()
            )
        if varid is None:
            return None,None
        for rv in rvs:
            self.reduced_variables[rv.id()] = rv
        for dv in dvs:
            self.derived_variables[dv.id()] = dv

        return varid, None

    def plan_computation_level_surface( self, model, obs, varnom, seasonid, aux=None, names={}, plotparms=None ):
        filetable1, filetable2 = self.getfts(model, obs)
        """Set up for a lat-lon contour plot, averaged in other directions - except that if the
        variable to be plotted depend on level, it is not averaged over level.  Instead, the value
        at a single specified pressure level, aux, is used. The units of aux are millbars."""
        # In calling reduce_time_seasonal, I am assuming that no variable has axes other than
        # (time, lev,lat,lon).
        # If there were another axis, then we'd need a new function which reduces it as well.
        if not isinstance(aux,Number): return None
        pselect = udunits(aux,'mbar')
        pselect.value=int(pselect.value)
        PSELECT = str(pselect)

        reduced_varlis = [
            reduced_variable(  # var=var(time,lev,lat,lon)
                variableid=varnom, filetable=filetable1, season=self.season,
                reduction_function=(lambda x,vid: reduce_time_seasonal( x, self.season, self.region, vid ) ) ),
            reduced_variable(   # hyam=hyam(lev)
                variableid='hyam', filetable=filetable1, season=self.season,
                reduction_function=(lambda x,vid=None: select_region( x, self.region)) ),
            reduced_variable(   # hybm=hybm(lev)
                variableid='hybm', filetable=filetable1, season=self.season,
                reduction_function=(lambda x,vid=None: select_region( x, self.region)) ),
            reduced_variable(     # ps=ps(time,lat,lon)
                variableid='PS', filetable=filetable1, season=self.season,
                reduction_function=(lambda x,vid: reduce_time_seasonal( x, self.season, self.region, vid ) ) ) ]
        # vid1 = varnom+'_p_1'
        # vidl1 = varnom+'_lp_1'
        vid1 = dv.dict_id(  varnom, 'p', seasonid, filetable1)
        vidl1 = dv.dict_id(varnom, 'lp', seasonid, filetable1)
        self.derived_variables = {
            vid1: derived_var( vid=vid1, inputs =
                               [rv.dict_id(varnom,seasonid,filetable1), rv.dict_id('hyam',seasonid,filetable1),
                                rv.dict_id('hybm',seasonid,filetable1), rv.dict_id('PS',seasonid,filetable1) ],
            #was  vid1: derived_var( vid=vid1, inputs=[ varnom+'_1', 'hyam_1', 'hybm_1', 'PS_1' ],
                               func=verticalize ),
            vidl1: derived_var( vid=vidl1, inputs=[vid1],
                                func=(lambda z,psl=pselect: select_lev(z,psl))) }

        ft1src = filetable1.source()
        #note: the title in the following is parced in customizeTemplate. This is a garbage kludge! Mea culpa. 
        varstr = varnom + '(' + PSELECT + ')'
        self.single_plotspecs = {
            self.plot1_id: plotspec(
                # was vid = varnom+'_1',
                # was zvars = [vid1],  zfunc = (lambda z: select_lev( z, pselect ) ),
                vid = ps.dict_idid(vidl1),
                zvars = [vidl1],  zfunc = (lambda z: z),
                plottype = self.plottype,
                title = ' '.join([varstr, seasonid, 'model', names['model']]),
                title1 = ' '.join([varstr, seasonid, 'model', names['model']]),
                title2 = 'model',
                file_descr = 'model',
                source = names['model'],
                plotparms = plotparms[src2modobs(ft1src)] ) }
           
        if filetable2 is None:
            self.reduced_variables = { v.id():v for v in reduced_varlis }
            self.composite_plotspecs = {
                self.plotall_id: [ self.plot1_id ]
                }
            self.computation_planned = True
            return

        if 'hyam' in filetable2.list_variables() and 'hybm' in filetable2.list_variables():
            # hybrid levels in use, convert to pressure levels
            reduced_varlis += [
                reduced_variable(  # var=var(time,lev,lat,lon)
                    variableid=varnom, filetable=filetable2, season=self.season,
                    reduction_function=(lambda x,vid: reduce_time_seasonal( x, self.season, self.region, vid ) ) ),
                reduced_variable(   # hyam=hyam(lev)
                    variableid='hyam', filetable=filetable2, season=self.season,
                    reduction_function=(lambda x,vid=None: select_region( x, self.region)) ),
                reduced_variable(   # hybm=hybm(lev)
                    variableid='hybm', filetable=filetable2, season=self.season,
                    reduction_function=(lambda x,vid=None: select_region( x, self.region)) ),
                reduced_variable(     # ps=ps(time,lat,lon)
                    variableid='PS', filetable=filetable2, season=self.season,
                    reduction_function=(lambda x,vid: reduce_time_seasonal( x, self.season, self.region, vid ) ) )
                ]
            #vid2 = varnom+'_p_2'
            #vidl2 = varnom+'_lp_2'
            vid2 = dv.dict_id( varnom, 'p', seasonid, filetable2 )
            vid2 = dv.dict_id( vards, 'lp', seasonid, filetable2 )
            self.derived_variables[vid2] = derived_var( vid=vid2, inputs=[
                    rv.dict_id(varnom,seasonid,filetable2), rv.dict_id('hyam',seasonid,filetable2),
                    rv.dict_id('hybm',seasonid,filetable2), rv.dict_id('PS',seasonid,filetable2) ],
                                                        func=verticalize )
            self.derived_variables[vidl2] = derived_var(
                vid=vidl2, inputs=[vid2], func=(lambda z,psl=pselect: select_lev(z,psl) ) )
        else:
            # no hybrid levels, assume pressure levels.
            #vid2 = varnom+'_2'
            #vidl2 = varnom+'_lp_2'
            vid2 = rv.dict_id(varnom,seasonid,filetable2)
            vidl2 = dv.dict_id( varnom, 'lp', seasonid, filetable2 )
            reduced_varlis += [
                reduced_variable(  # var=var(time,lev,lat,lon)
                    variableid=varnom, filetable=filetable2, season=self.season,
                    reduction_function=(lambda x,vid: reduce_time_seasonal( x, self.season, self.region, vid ) ) )
                ]
            self.derived_variables[vidl2] = derived_var(
                vid=vidl2, inputs=[vid2], func=(lambda z,psl=pselect: select_lev(z,psl) ) )
        self.reduced_variables = { v.id():v for v in reduced_varlis }

        try:
            ft2src = filetable2.source()
        except:
            ft2src = ''
        filterid = ft2src.split('_')[-1] #recover the filter id: kludge
        self.single_plotspecs[self.plot2_id] = plotspec(
                #was vid = varnom+'_2',
                vid = ps.dict_idid(vidl2),
                zvars = [vidl2],  zfunc = (lambda z: z),
                plottype = self.plottype,
                title = ' '.join([varstr,seasonid,'observation',names['obs']]),
                title1 = ' '.join([varstr, seasonid, 'observation',names['obs']]),
                title2 = 'observation',
                file_descr = 'obs',
                source = names['obs'],
                plotparms = plotparms[src2obsmod(ft2src)] )
        self.single_plotspecs[self.plot3_id] = plotspec(
                #was vid = varnom+'_diff',
                vid = ps.dict_id(varnom,'diff',seasonid,filetable1,filetable2),
                zvars = [vidl1,vidl2],  zfunc = aminusb_2ax,
                plottype = self.plottype,
                title = ' '.join([varstr,seasonid,'difference']),
                title1 = ' '.join([varstr, seasonid, 'difference']),
                title2 = 'difference',
                file_descr = 'diff',
                plotparms = plotparms['diff'] )
#                zerocontour=-1 )
        self.composite_plotspecs = {
            self.plotall_id: [ self.plot1_id, self.plot2_id, self.plot3_id ]
            }
        self.computation_planned = True

    def customizeTemplates( self, templates, data=None, varIndex=None, graphicMethod=None, var=None,
                            uvcplotspec=None ):
        """This method does what the title says.  It is a hack that will no doubt change as diags changes."""
        (cnvs1, tm1), (cnvs2, tm2) = templates
        

        # Lat lon?
        if 150 < graphicMethod.datawc_y2-graphicMethod.datawc_y1 < 190:
            graphicMethod.datawc_y2 = 90
            graphicMethod.datawc_y1 = -90
            graphicMethod.datawc_x2 = 360
            graphicMethod.datawc_x1 = 0
        # UNtil Jonathas fixes this, we simply figure out the template number to get from what Jonathas gave us
        tm2 = cnvs1.gettemplate("plotset5_0_x_%s" % (tm2.name.split("_")[2]))

        header = None
        source = None
        if uvcplotspec is None:  # old kludge, tries to extract information from var.title
            logger.warning( "running old section of plot set 5 customizeTemplates because uvcplotspec==None" )
            #more kludgy than ever before
            #var seems to be the only way to get the required titles.
            #I think this was a result of another kludge:
            s = var.title.split(' ')
            if len(s) == 5:
                header = s[0] + ' ' + s[1] + ' ' + s[2]
                var.title = s[3]
                source = s[4]
            if len(s) == 4:
                header = s[0] + ' ' + s[1]
                var.title = s[2]
                source = s[3]
            elif len(s) == 2:
                var.title = s[0]
                source = s[1]
            else:
                source = None
        else:
            psid = uvcplotspec.id()
            ftid = data.filetableid
            #source = ftid.ftid         # source for simple plot, not used
            source = uvcplotspec.source # None should work, but it doesn't right now.
            #sourcenn = ftid.nickname   # not used at present
            if tm2.title.y > 0.8:   # top of the compound plot, the only case where we want a header
                # header = ' '.join([psid.vars[0], psid.season])   # TO DO: restore something like this once aux is in psid
                auxl = var.title.split(') ')[0].split('(')  # if title=="Var(aux)...", this is ["Var", "aux"]
                # ... if title=="Var..." without (aux), then this is [title]
                if len(auxl)>1:
                    aux = auxl[1]  # e.g. '850 mbar'
                    varstr = psid.vars + '(' + aux + ')'
                else:
                    varstr = psid.vars
                header = ' '.join( [varstr, psid.season] )

        #pdb.set_trace()

        tm1.yname.priority  = 1
        tm1.xname.priority  = 1
        tm1.legend.priority = 1
        # Fix units if needed
        if data is not None:
            if (getattr(data, 'units', '') == ''):
                data.units = 'K'
            if data.getAxis(0).id.count('lat'):
                data.getAxis(0).id = 'Latitude'
            if data.getAxis(0).id.count('lon'):
                data.getAxis(0).id = 'Longitude'
            elif len(data.getAxisList()) > 1:
                if data.getAxis(1).id.count('lat'):
                    data.getAxis(1).id = 'Latitude'
                if data.getAxis(1).id.count('lon'):
                    data.getAxis(1).id = 'Longitude'

        #cnvs1.landscape()
        #cnvs1.setcolormap("categorical")
        #colormap = vcs.matplotlib2vcs('viridis')
        #cnvs1.setcolormap(colormap)

        # Adjust labels and names for single plots
        ynameOri                  = cnvs1.gettextorientation(tm1.yname.textorientation)
        ynameOri.height           = 16
        tm1.yname.textorientation = ynameOri

        xnameOri                  = cnvs1.gettextorientation(tm1.xname.textorientation)
        xnameOri.height           = 16
        tm1.xname.textorientation = xnameOri

        meanOri                  = cnvs1.gettextorientation(tm1.mean.textorientation)
        meanOri.height           = 14
        tm1.mean.textorientation = meanOri
        tm1.mean.y              -= 0.005

        titleOri                  = cnvs1.gettextorientation(tm1.title.textorientation)
        titleOri.height           = 22
        tm1.title.textorientation = titleOri
       
        sourceOri                  = cnvs1.gettextorientation(tm1.source.textorientation)
        sourceOri.height           = 11.0
        tm1.source.textorientation = sourceOri
        tm1.source.y               = tm1.units.y - 0.02
        tm1.source.x               = tm1.data.x1
        tm1.source.priority        = 1

        # We want units at axis names
        tm1.units.y       -= 0.01
        tm1.units.priority = 1
        
        #for some reason the source is not being put on the combined graphic
        # So put it there.
        # jfp 2015.09.13: For another unknown reason, the source is getting on properly now.
        #   In case the problem recurs, I'll leave the code here, commented-out, for a while.
        #if source is not None":
        #    text = cnvs2.createtext()
        #    text.string = source
        #    text.x = tm2.data.x1
        #    text.y = tm2.data.y2 + 0.01
        #    text.height = 10
        #    cnvs2.plot(text, bg=1)  
        
        #create the header for the plot    
        if header is not None:
            text = cnvs2.createtext()
            text.string = header
            text.x = (tm2.data.x1 + tm2.data.x2)/2
            text.y = tm2.data.y2 + 0.03
            text.height = 16
            text.halign = 1
            cnvs2.plot(text, bg=1)  
        #pdb.set_trace()
        try:
            #this is for the output of RMSE and CORRELATION
            tm1, tm2 = self.extraCustomizeTemplates((cnvs1, tm1), (cnvs2, tm2), var=var,
                                                    uvcplotspec=uvcplotspec)
        except Exception,err:
            pass
        return tm1, tm2
    
    def extraCustomizeTemplates(self, (cnvs1, tm1), (cnvs2, tm2), data=None, varIndex=None,
                                graphicMethod=None, var=None, uvcplotspec=None):
        """This method does what the title says.  It is a hack that will no doubt change as diags changes.
        It is a total hack. I'm embarassed to be part of it. Please find a better way!!!"""
        #(cnvs1, tm1), (cnvs2, tm2) = templates
        if hasattr(var, 'model') and hasattr(var, 'obs'): #these come from aminusb_2ax
            from metrics.graphics.default_levels import default_levels
            from metrics.computation.units import scale_data
            from metrics.computation.compute_rmse import compute_rmse    
            if self.varid in default_levels.keys():
                #convert to the units specified in the default levels dictionay
                displayunits = default_levels[self.varid].get('displayunits', None)
                if displayunits is not None and var.model is not None and var.obs is not None:
                    var.model = scale_data( displayunits, var.model)
                    var.obs   = scale_data( displayunits, var.obs) 

            RMSE, CORR = compute_rmse( var.model, var.obs )
            RMSE = round(RMSE, 2)
            CORR = round(CORR, 2)
            lst = ["min","max","comment1","comment2"]
        else:
            lst = ["min","max"]


        x=cnvs2
        t = tm2

        try:
            mean_val = float(var.mean)
        except Exception,err:
            season = uvcplotspec.id().season
            region = uvcplotspec.id().region
            varid = getattr( var, 'id', '' )
            if varid == '':
                varid = getattr( var, '_id', '' )
            if varid.find(uvcplotspec.id().ft1)>=0:
                ft1 = uvcplotspec.id().ft1
            elif varid.find(uvcplotspec.id().ft2)>=0:
                ft1 = uvcplotspec.id().ft2
            else:
                ft1 = None
            if False:
                # unfinished; this late in the game gw may be the wrong shape, due to regridding; see my notes 2016.10.07.
                gwid = reduced_variable.IDtuple( classid='rv', var='gw', season=season, region=region, ft1=ft1, ffilt1='' )
                gw_rv = self.reduced_variables.get(gwid,None)
                if gw_rv is None:
                    gw = None
                else:
                    gw = uvcplotspec.varvals[gw_rv.id()]
            set_mean( var, season, region, gw )
            mean_val = float(var.mean)

        mean = get_textobject(t,"mean","Mean   %.2f" % mean_val)
        exts = x.gettextextent(mean)
        x.plot(mean)
        for att in lst:
            nmin = get_textobject(t,att,"some text")
            if att in ["min","max"]:
                nmin.string=att.capitalize()
            elif att == "comment1":
                nmin.string=["RMSE"]
            elif att == "comment2":
                nmin.string=["CORR"]
            x.plot(nmin)
            to=x.createtextorientation(source=nmin.To_name)
            to.halign="right"
            nmin=vcs.createtext(To_source=to.name,Tt_source=nmin.Tt_name) 
            if att in ["min","max"]:
                nmin.string=[get_format(getattr(numpy.ma,att)(var.asma()))]
            elif att == "comment1":
                nmin.string=[ get_format(RMSE)]
            elif att == "comment2":
                nmin.string=[get_format(CORR)]
            nmin.x=[exts[0][1]]
            x.plot(nmin)
        return tm1, tm2          

    def _results(self,newgrid=0):
        results = plot_plan._results(self,newgrid)
        if results is None: return None
        psv = self.plotspec_values
        if self.plot1_id in psv and self.plot2_id in psv and\
                psv[self.plot1_id] is not None and psv[self.plot2_id] is not None:
            psv[self.plot1_id].synchronize_ranges(psv[self.plot2_id])
        else:
            logger.warning("not synchronizing ranges for %s and %s",self.plot1_id, self.plot2_id)
        for key,val in psv.items():
            if type(val) is not list: val=[val]
            for v in val:
                if v is None: continue
                v.finalize()
        if self.plotall_id in self.plotspec_values:
            return self.plotspec_values[self.plotall_id]
        else:
            return None
