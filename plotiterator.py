## Generate plots of quantities from a measurment set
##
## $Id: plotiterator.py,v 1.25 2017-02-21 09:10:05 jive_cc Exp $
##
## $Log: plotiterator.py,v $
## Revision 1.25  2017-02-21 09:10:05  jive_cc
## HV: * DesS requests normalized vector averaging - complex numbers are first
##       normalized before being averaged. See "help avt" or "help avc".
##
## Revision 1.24  2017-01-27 13:50:28  jive_cc
## HV: * jplotter.py: small edits
##         - "not refresh(e)" => "refresh(e); if not e.plots ..."
##         - "e.rawplots.XXX" i.s.o. "e.plots.XXX"
##     * relatively big overhaul: in order to force (old) pyrap to
##       re-read tables from disk all table objects must call ".close()"
##       when they're done.
##       Implemented by patching the pyrap.tables.table object on the fly
##       with '__enter__' and '__exit__' methods (see "ms2util.opentable(...)")
##       such that all table access can be done in a "with ..." block:
##          with ms2util.opentable(...) as tbl:
##             tbl.getcol('DATA') # ...
##       and then when the with-block is left, tbl gets automagically closed
##
## Revision 1.23  2015-12-09 07:02:11  jive_cc
## HV: * big change! the plotiterators now return a one-dimensional dict
##       of label => dataset. The higher level code reorganizes them
##       into plots, based on the 'new plot' settings. Many wins in this one:
##         - the plotiterators only have to index one level in stead of two
##         - when the 'new plot' setting is changed, we don't have to read the
##           data from disk again [this is a *HUGE* improvement, especially for
##           larger data sets]
##         - the data set expression parser is simpler, it works on the
##           one-dimensional 'list' of data sets and it does not have to
##           flatten/unflatten any more
##     * The code to deal with refreshing the plots has been rewritten a bit
##       such that all necessary steps (re-organizing raw plots into plots,
##       re-running the label processing, re-running the post processing,
##       re-running the min/max processing) are executed only once; when
##       necessary. And this code is now shared between the "pl" command and
##       the "load/store" commands.
##
## Revision 1.22  2015-09-23 12:28:36  jive_cc
## HV: * Lorant S. requested sensible requests (ones that were already in the
##       back of my mind too):
##         - option to specify the data column
##         - option to not reorder the spectral windows
##       Both options are now supported by the code and are triggered by
##       passing options to the "ms" command
##
## Revision 1.21  2015-04-29 14:34:55  jive_cc
## HV: * add support for plotting quantity vs UV-distance
##
## Revision 1.20  2015-04-08 14:34:12  jive_cc
## HV: * Correct checking of wether dataset.[xy] are of the numpy.ndarray
##       persuasion
##
## Revision 1.19  2015-02-16 12:56:53  jive_cc
## HV: * Now that we do our own slicing, found that some of the index limits
##       were off-by-one
##
## Revision 1.18  2015-02-02 08:55:22  jive_cc
## HV: * support for storing/loading plots, potentially manipulating them
##       via arbitrary arithmetic expressions
##     * helpfile layout improved
##
## Revision 1.17  2015-01-09 14:27:57  jive_cc
## HV: * fixed copy-paste error in weight-thresholded quantity-versus-time fn
##     * sped up SOLINT processing by factor >= 2
##     * output of ".... took    XXXs" consistentified & beautified
##     * removed "Need to convert ..." output; the predicted expected runtime
##       was usually very wrong anyway.
##
## Revision 1.16  2015-01-09 00:02:27  jive_cc
## HV: * support for 'solint' - accumulate data in time bins of size 'solint'
##       now also in "xxx vs time" plots. i.e. can be used to bring down data
##       volume by e.g. averaging down to an arbitrary amount of seconds.
##     * solint can now be more flexibly be set using d(ays), h(ours),
##       m(inutes) and/or s(econds). Note that in the previous versions a
##       unitless specification was acceptable, in this one no more.
##
## Revision 1.15  2014-11-28 14:25:04  jive_cc
## HV: * spelling error in variable name ...
##
## Revision 1.14  2014-11-26 14:56:21  jive_cc
## HV: * pycasa autodetection and use
##
## Revision 1.13  2014-05-14 17:35:15  jive_cc
## HV: * if weight threshold is applied this is annotated in the plot
##     * the plotiterators have two implementations now, one with weight
##       thresholding and one without. Until I find a method that is
##       equally fast with/without weight masking
##
## Revision 1.12  2014-05-14 17:02:01  jive_cc
## HV: * Weight thresholding implemented - but maybe I'll double the code
##       to two different functions, one with weight thresholding and one
##       without because weight thresholding is sloooooow
##
## Revision 1.11  2014-05-12 21:27:28  jive_cc
## HV: * IF time was an essential part of a label, its resolution of 1second
##       was not enough - made it 1/100th of a second. So now you can safely
##       plot data sets with individual time stamps even if they're << 1 second
##       apart
##
## Revision 1.10  2014-05-06 14:20:39  jive_cc
## HV: * Added marking capability
##
## Revision 1.9  2014-04-15 07:53:17  jive_cc
## HV: * time averaging now supports 'solint' = None => average all data in
##       each time-range selection bin
##
## Revision 1.8  2014-04-14 21:04:44  jive_cc
## HV: * Information common to all plot- or data set labels is now stripped
##       and displayed in the plot heading i.s.o in the plot- or data set label
##
## Revision 1.7  2014-04-14 14:46:05  jive_cc
## HV: * Uses pycasa.so for table data access waiting for pyrap to be fixed
##     * added "indexr" + scan-based selection option
##
## Revision 1.6  2014-04-10 21:14:40  jive_cc
## HV: * I fell for the age-old Python trick where a default argument is
##       initialized statically - all data sets were integrating into the
##       the same arrays! Nice!
##     * Fixed other efficiency measures: with time averaging data already
##       IS in numarray so no conversion needs to be done
##     * more improvements
##
## Revision 1.5  2014-04-09 08:26:46  jive_cc
## HV: * Ok, moved common plotiterator stuff into baseclass
##
## Revision 1.4  2014-04-08 23:34:13  jive_cc
## HV: * Minor fixes - should be better now
##
## Revision 1.3  2014-04-08 22:41:11  jive_cc
## HV: Finally! This might be release 0.1!
##     * python based plot iteration now has tolerable speed
##       (need to test on 8M row MS though)
##     * added quite a few plot types, simplified plotters
##       (plotiterators need a round of moving common functionality
##        into base class)
##     * added generic X/Y plotter
##
## Revision 1.2  2014-04-02 17:55:30  jive_cc
## HV: * another savegame, this time with basic plotiteration done in Python
##
## Revision 1.1  2013-12-12 14:10:16  jive_cc
## HV: * another savegame. Now going with pythonic based plotiterator,
##       built around ms2util.reducems
##
##
import ms2util, hvutil, plots, jenums, itertools, copy, operator, numpy, math, imp, time, collections, functional
import pyrap.quanta

# Auto-detect of pycasa
havePyCasa = True
try:
    import pycasa
    print "*** using PyCasa for measurementset data access ***"
except:
    havePyCasa = False

## Introduce some shorthands
NOW      = time.time
CP       = copy.deepcopy
AX       = jenums.Axes
AVG      = jenums.Averaging
YTypes   = plots.YTypes
Quantity = collections.namedtuple('Quantity', ['quantity_name', 'quantity_fn'])

# We support different kinds of averaging
def avg_vectornorm(ax):
    # produce a function which will do vectornorm averaging
    # along the requested axis
    # numpy 1.11.0 (...!) does not support keepdims=... on
    #    many numpy.ma.* calls ffs!
    def do_it(x):
        summed = numpy.ma.sum(x, axis=ax, keepdims=True)
        return summed / numpy.ma.max(numpy.ma.abs(summed), axis=ax, keepdims=True)
    return do_it

def avg_arithmetic(ax):
    # normal arithmetic mean, should work both on complex or scalar data
    def do_it(x):
        return numpy.ma.mean(x, axis=ax, keepdims=True)
    return do_it

def avg_sum(ax):
    def do_it(x):
        return numpy.ma.sum(x, axis=ax, keepdims=True)
    return do_it

def avg_none(_):
    return functional.identity


## The base class holds the actual table object -
## makes sure the selection etc gets done
class plotbase(object):
    def __enter__(self, *args, **kwargs):
        return self
    def __exit__(self, *args, **kwargs):
        if hasattr(self, 'table'):
            self.table.close()

    # depending on combination of query or not and read flags or not
    # we have optimum call sequence for processing a table
    # key = (qryYesNo, readFlagYesNo)
    # I think that executing an empty query
    #   tbl.query('') 
    # takes longer than 
    #   tbl.query()
    _qrycolmapf = {
            (False, False): lambda tbl, q, c: tbl,                    # no query, no flagcolum reading
            (True , False): lambda tbl, q, c: tbl.query(q),           # only query
            (False, True ): lambda tbl, q, c: tbl.query(columns=c),   # only different columns
            (True,  True ): lambda tbl, q, c: tbl.query(q, columns=c) # the works
        }

    ## selection is a selection object from 'selection.py'
    def __init__(self, msname, selection, mapping, **kwargs):

        self.verbose  = kwargs.setdefault('verbose', True)
        self.flags    = kwargs.get('readflags', True)
        self.datacol  = CP(mapping.domain.column)

        self.table    = pycasa.table(msname) if havePyCasa else ms2util.opentable(msname)
        # when reading flags is enabled let the C++ do the OR'ing of FLAG_ROW, FLAG columns for us
        colnames      = "*, (FLAG_ROW || FLAG) AS FLAGCOL" if self.flags else None

        ## apply selection if necessary
        qry = selection.selectionTaQL()
        s = NOW()
        self.table = plotbase._qrycolmapf[(bool(qry), bool(colnames))](self.table, qry, colnames)
        e = NOW()
        if not self.table:
            raise RuntimeError("No data available for your selection criteria")
        if qry and self.verbose:
            print "Query took\t\t{0:.3f}s".format(e-s)

        # we'll provide overrides for specific column readers
        # for efficiency for the WEIGHT and/or FLAG data
        #
        # Subclasses can request 'WEIGHTCOL' and/or 'FLAGCOL'
        # in their call to reducems2(...), provided they pass
        # in the self.slicers{..} object which we'll have prepared
        self.slicers = dict()

        # Set up weight thresholding.
        # We have to be able to deal with the following weight shapes:
        #    numpy.Inf              (weights not read)
        #    (n_int, n_pol)         [WEIGHT column read]
        #    (n_int, n_freq, n_pol) [WEIGHT_SPECTRUM read]
        #
        # In order to turn the weight criterion (if any) into a mask we must
        # potentially broadcast the WEIGHT shape (one weight per polarization)
        # to all channels; the data always has shape:
        #    (n_int, n_freq, n_pol)
        #
        # We can do that efficiently by transposing the data array in that case to be:
        #    (n_freq, n_int, n_pol)  
        # Now the data mask also has this shape.
        # Then, numpy.logical_or(data.mask, weight_mask) does the right thing:
        #     weight_mask == (n_int, n_pol)   -> dimensions match on both data.mask and weight_mask
        #                                        but for the first -> broadcasted along dim 0, which
        #                                        is n_freq, i.e. each spectral point gets the same weight per pol
        self.threshold = CP(selection.weightThreshold) if selection.weightThreshold is not None else -numpy.Inf
        transpose      = weight_rd = None
        if self.threshold == -numpy.Inf:
            # No weight thresholding? Return an infinite weight to effectively disable thresholding
            weight_rd = lambda _a,_b,_c,_d: numpy.Inf
            # Also no need to transpose/untranspose the data array for this 'shape'
            transpose = functional.identity
        else:
            # weight read from MS, choose which column to use
            weight_col = 'WEIGHT_SPECTRUM' if 'WEIGHT_SPECTRUM' in self.table.colnames() else 'WEIGHT'
            weight_rd  = lambda tab, _, s, n: tab.getcol(weight_col, startrow=s, nrow=n)
            # the need to transpose/untranspose the data array depends on which is the weight column
            transpose  = operator.methodcaller('transpose', (1,0,2)) if weight_col == 'WEIGHT' else functional.identity

        # install the appropriate weight reader for the 'WEIGHTCOL' column
        self.slicers['WEIGHTCOL'] = weight_rd
        self.transpose            = transpose

        # Set up FLAG reading
        if self.flags:
            # if self.flags is set, then TaQL will be requested to add the computed FLAGCOL column
            flag_rd   = lambda tab, _, s, n: tab.getcol('FLAGCOL', startrow=s, nrow=n)
        else:
            # no flags to be read ie nothing will be flagged
            flag_rd   = lambda _a,_b,_c,_d: False
        self.slicers['FLAGCOL']  = flag_rd

        ## Parse data-description-id selection into a map:
        ## self.ddSelection will be 
        ##   map [ DATA_DESC_ID ] => (FQ, SB, POLS)
        ## 
        ## With FQ, SB integer - the indices,
        ##      POLS = [ (idx, str), ... ]
        ##        i.e. list of row indices and the polarization string
        ##             to go with it, such that the polarization data
        ##             is put in the correct plot/data set immediately
        ##
        # The matter of the fact is that the polarization row index ('idx'
        # above) is not a unique mapping to physical polarization so we cannot
        # get away with using the numerical label, even though that would be
        # faster

        _pMap    = mapping.polarizationMap
        _spwMap  = mapping.spectralMap
        GETF     = _spwMap.frequenciesOfFREQ_SB
        # Frequencies get done in MHz 
        scale    = 1e6 if mapping.domain.domain == jenums.Type.Spectral else 1

        ## if user did not pass DATA_DESC_ID selection, default to all
        if selection.ddSelection:
            ## An element in "ddSelection" is a 4-element tuple with
            ## fields (FQ, SB, POLID, [product indices])
            ## So all we need is to pair the product indices with the
            ## appropriate polarization strings
            GETDDID = _spwMap.datadescriptionIdOfFREQ_SB_POL
            ITEMGET = hvutil.itemgetter
            def ddIdAdder(acc, ddSel):
                (fq, sb, pid, l) = ddSel
                ddId             = GETDDID(fq, sb, pid)
                polStrings       = _pMap.getPolarizations(pid)
                acc[0][ ddId ]   = (fq, sb, zip(l, ITEMGET(*l)(polStrings)))
                acc[1][ ddId ]   = GETF(fq, sb)/scale
                return acc
            (self.ddSelection, self.ddFreqs)   = reduce(ddIdAdder, selection.ddSelection, [{}, {}])
        else:
            ddids     = _spwMap.datadescriptionIDs()
            UNMAPDDID = _spwMap.unmapDDId
            def ddIdAdder(acc, dd):
                # Our data selection is rather simple: all the rows!
                r         = UNMAPDDID(dd)
                acc[0][ dd ] = (r.FREQID, r.SUBBAND, list(enumerate(_pMap.getPolarizations(r.POLID))))
                acc[1][ dd ] = GETF(r.FREQID, r.SUBBAND)/scale
                return acc
            (self.ddSelection, self.ddFreqs)   = reduce(ddIdAdder, ddids, [{}, {}])

        ## Provide for a label unmapping function.
        ## After creating the plots we need to transform the labels - some
        ## of the numerical indices must be unmapped into physical quantities
        #unmapBL   = mapping.baselineMap.baselineName
        #unmapFQ   = mapping.spectralMap.freqGroupName
        #unmapSRC  = mapping.fieldMap.field

        unmap_f   = { AX.BL:   mapping.baselineMap.baselineName,
                      AX.FQ:   mapping.spectralMap.freqGroupName,
                      AX.SRC:  mapping.fieldMap.field,
                      AX.TIME: lambda t: pyrap.quanta.quantity(t, "s").formatted("time", precision=8) }
        identity  = lambda x: x
        def unmap( (fld, val) ):
            return (fld, unmap_f.get(fld, identity)(val))
        # flds is the list of field names that the values in the tuple mean
        self.MKLAB = lambda flds, tup: plots.label( dict(map(unmap, zip(flds, tup))), flds )

    ##
    ##   Should return the generated plots according to the following
    ##   structure:
    ##
    ##   Update: Dec 2015 - we start doing things a little different
    ##                      the raw data sets will be delivered as a dict of
    ##                      Dict: Key -> Value, where Key is the full data set
    ##                      label and Value the dataset() object.
    ##                      The division into plots will be done at a higher
    ##                      level. Reasons:
    ##                        - generation of raw data is faster as only one level
    ##                          of dict indexing is needed i.s.o. two
    ##                        - if user changes the new plot settings, we don't
    ##                          have to read from disk no more, it then is a mere
    ##                          rearrangement of the raw data sets
    ##                        - load/store with expressions on data sets now work
    ##                          on the one-dimensional 'list' of data sets, no need
    ##                          to flatten/unflatten anymore
    ##
    ##   plots = dict( Key -> Value ) with
    ##              Key   = <plot index>  # contains physical quantities/labels
    ##              Value = DataSet
    ##   DataSet = instance of 'dataset' (see below) with
    ##             attributes ".x" and ".y"
    def makePlots(self, *args):
        raise RuntimeError, "Someone forgot to implement this function for this plottype"


## Unfortunately, our code relies on the fact that the numarrays returned 
## from "ms.getcol()" are 3-dimensional: (nintg x npol x nchannel)
## Sadly, casa is smart/stoopid enough to return no more dimensions
## than are needed; no degenerate axes are present.
## So if your table consists of one row, you get at best a matrix:
##     npol x nchannel
## Further, if you happen to read single-pol data, guess what, 
## you get a matrix at best and a vector at worst!:
##    matrix: nintg x nchannel 
##    vector: nchannel   (worst case: a table with one row of single pol data!)
##
## m3d() can be used to reshape an array to always be at least 3d,
##   it inserts degenerate axis from the end, assuming that there 
##   won't be data sets with only one row ...
##   (single pol does happen! a lot!)
def m3d(ar):
    shp = list(ar.shape)
    while len(shp)<3:
        shp.insert(-1, 1)
    return ar.reshape( shp )

def m2d(ar):
    shp = list(ar.shape)
    while len(shp)<2:
        shp.insert(-1, 1)
    return ar.reshape( shp )

class dataset_org:
    __slots__ = ['x', 'y', 'n', 'a', 'sf', 'm']

    @classmethod
    def add_sumy(self, obj, xs, ys, m):
        obj.y = obj.y + ys
        obj.n = obj.n + 1
        obj.m = numpy.logical_and(obj.m, m)

    @classmethod
    def init_sumy(self, obj, xs, ys, m):
        obj.x  = numpy.array(xs)
        obj.y  = numpy.array(ys)
        obj.sf = dataset.add_sumy
        obj.m  = m

    def __init__(self, x=None, y=None, m=None):
        if x is not None and len(x)!=len(y):
            raise RuntimeError, "attempt to construct data set where len(x) != len(y)?!!!"
        self.x  = list() if x is None else x
        self.y  = list() if y is None else y
        self.m  = list() if m is None else m
        self.n  = 0 if x is None else 1
        self.sf = dataset.init_sumy if x is None else dataset.add_sumy
        self.a  = False

    def append(self, xv, yv, m):
        self.x.append(xv)
        self.y.append(yv)
        self.m.append(m)

    # integrate into the current buffer
    def sumy(self, xs, ys, m):
        self.sf(self, xs, ys, m)

    def average(self):
        if not self.a and self.n>1:
            self.y = self.y / self.n
        self.a = True

    def is_numarray(self):
        return (type(self.x) is numpy.ndarray and type(self.y) is numpy.ndarray)

    def as_numarray(self):
        if self.is_numarray():
            return self
        # note to self: float32 has insufficient precision for e.g.
        # <quantity> versus time
        self.x  = numpy.array(self.x, dtype=numpy.float64)
        self.y  = numpy.array(self.y, dtype=numpy.float64)
        self.m  = numpy.array(self.m, dtype=numpy.bool)
        return self

    def __str__(self):
        return "DATASET: {0} MASK: {1}".format(zip(self.x, self.y), self.m)

    def __repr__(self):
        return str(self)

class dataset_fixed:
    __slots__ = ['x', 'y', 'm']

    def __init__(self, x=None, y=None):
        if x is not None and len(x)!=len(y):
            raise RuntimeError, "attempt to construct data set where len(x) != len(y)?!!!"
        self.x  = list() if x is None else x
        self.y  = list() if y is None else y
        self.m  = False

    def append(self, xv, yv, m):
        raise NotImplemented("append() does not apply to dataset_fixed!")

    # integrate into the current buffer
    def sumy(self, xs, ys, m):
        raise NotImplemented("sumy() does not apply to dataset_fixed!")

    def average(self):
        raise NotImplemented("average() does not apply to dataset_fixed!")

    def is_numarray(self):
        return (type(self.x) is numpy.ndarray and type(self.y) is numpy.ndarray)

    def as_numarray(self):
        if self.is_numarray():
            return self
        # note to self: float32 has insufficient precision for e.g.
        # <quantity> versus time
        self.x  = numpy.array(self.x, dtype=numpy.float64)
        self.y  = numpy.array(self.y, dtype=numpy.float64)
        return self

    def __str__(self):
        return "DATASET<fixed>: {0}".format(zip(self.x, self.y))

    def __repr__(self):
        return str(self)

# append means append to list, fastest for collecting individual samples
class dataset_list:
    __slots__ = ['x', 'y', 'n', 'a', 'm']

    @classmethod
    def add_sumy(self, obj, xs, ys, m):
        obj.y = obj.y + ys
        obj.n = obj.n + 1
        obj.m = numpy.logical_and(obj.m, m)

    @classmethod
    def init_sumy(self, obj, xs, ys, m):
        obj.x  = numpy.array(xs)
        obj.y  = numpy.array(ys)
        obj.sf = dataset.add_sumy
        obj.m  = m

    def __init__(self, x=None, y=None, m=None):
        if x is not None and len(x)!=len(y):
            raise RuntimeError, "attempt to construct data set where len(x) != len(y)?!!!"
        self.x  = list() if x is None else x
        self.y  = list() if y is None else y
        self.m  = list() if m is None else m
        self.n  = 0 if x is None else 1
        #self.sf = dataset.init_sumy if x is None else dataset.add_sumy
        self.a  = False

    def append(self, xv, yv, m):
        self.x.append(xv)
        self.y.append(yv)
        self.m.append(m)

    # integrate into the current buffer
    #def sumy(self, xs, ys, m):
    #    self.sf(self, xs, ys, m)

    def average(self, method):
        if method != AVG.None:
            raise RuntimeError("dataset_list was not made for time averaging")
        #if not self.a and self.n>1:
        #    self.y = self.y / self.n
        #self.a = True

    def is_numarray(self):
        return (type(self.x) is numpy.array and type(self.y) is numpy.ma.MaskedArray)

    def as_numarray(self):
        if self.is_numarray():
            return self
        # note to self: float32 has insufficient precision for e.g.
        # <quantity> versus time
        self.x  = numpy.array(self.x, dtype=numpy.float64)
        self.y  = numpy.ma.MaskedArray(self.y, mask=self.m, dtype=numpy.float64)
        return self

    def __str__(self):
        return "DATASET<list>: {0} MASK: {1}".format(zip(self.x, self.y), self.m)

    def __repr__(self):
        return str(self)


# .append() does an implicit group-by on the x value
class dataset_solint:
    __slots__ = ['x', 'y', 'a', 'd', 'm']

    @classmethod
    def add_sumy(self, obj, xs, ys, m):
        obj.y = obj.y + ys
        obj.n = obj.n + 1
        obj.m = numpy.logical_and(obj.m, m)

    @classmethod
    def init_sumy(self, obj, xs, ys, m):
        obj.x  = numpy.array(xs)
        obj.y  = numpy.array(ys)
        obj.sf = dataset.add_sumy
        obj.m  = m

    def __init__(self):#, x=None, y=None, m=None):
        self.x = self.y = None
        self.a = None
        self.d = collections.defaultdict(int)
        self.m = collections.defaultdict(int)
#        if x is not None and len(x)!=len(y):
#            raise RuntimeError, "attempt to construct data set where len(x) != len(y)?!!!"
#        self.x  = list() if x is None else x
#        self.y  = list() if y is None else y
#        self.m  = list() if m is None else m
#        self.n  = 0 if x is None else 1
#        self.sf = dataset.init_sumy if x is None else dataset.add_sumy
#        self.a  = False

    def append(self, xv, yv, m):
        self.d[xv] = numpy.ma.add(xv, self.d[xv])
        self.m[xv] = numpy.ma.add(~m, self.m[xv])

    # integrate into the current buffer
#    def sumy(self, xs, ys, m):
#        self.sf(self, xs, ys, m)

    def average(self, method):
        if self.a is None:
            # normal average = arithmetic mean i.e. summed value / count of valid values
            fn = numpy.divide
            if method==AVG.Vectornorm:
                # for vector norm we divide by the largest complex amplitude
                fn = lambda x, _: x/numpy.max(numpy.abs(x))
            elif method==AVG.None:
                fn = lambda x, _: x
            # construct a new dict with the averaged data values and set mask based on
            # number of unmasked 
            self.a = dict()
            while self.d:
                (x, ys) = self.d.popitem()
                counts  = self.m.pop(x)
                self.a[x] = numpy.ma.MaskedArray(fn(ys, self.m[x]), mask=numpy.array(counts, dtype=numpy.bool))
            #self.y = self.y / self.n

    def is_numarray(self):
        return (type(self.x) is numpy.ndarray and type(self.y) is numpy.ma.MaskedArray)

    def as_numarray(self):
        if self.is_numarray():
            return self
        # note to self: float32 has insufficient precision for e.g.
        # <quantity> versus time
        if self.a is None:
            raise RuntimeError("solint dataset has not been averaged yet")
        self.x  = numpy.array(self.a.iterkeys(), dtype=numpy.float64)
        self.y  = numpy.ma.vstack(self.a.itervalues())
        return self

    def __str__(self):
        return "DATASET<solint>: {0} MASK: {1}".format(zip(self.x, self.y), self.m)

    def __repr__(self):
        return str(self)

## Partition a data set into two separate data sets,
## one with those elements satisfying the predicate,
## the other those who dont.
## Returns (ds_true, ds_false)
##
## Implementation note:
##  Yes, there is hvutil.partition() which does much the same but
##  using a reduce(). The problem is that it expects a single list of values
##  to which to apply the predicate.
##  In order to turn a dataset() into a single list, we'd have to
##   zip() the ".x" and ".y" lists. After having partition'ed the list,
##  we'd have to unzip them again into separate ".x" and ".y" arrays,
##  for the benefit of PGPLOT.
##  Summarizing: in order to use hvutil.partition() we'd have to do two (2)
##  cornerturning operations, which seems to be wasteful.
class partitioner:
    def __init__(self, expr):
        # solution found in:
        # http://stackoverflow.com/questions/10303248/true-dynamic-and-anonymous-functions-possible-in-python
        self.code = compile(
                "from numpy import *\n"+
                "from math  import *\n"+
                "avg  = None\n"+
                "sd   = None\n"+
                "xmin = None\n"+
                "xmax = None\n"+
                "ymin = None\n"+
                "ymax = None\n"+
                "f   = lambda x, y: "+expr,
                'dyn-mark-string', 'exec')
        self.mod  = imp.new_module("dyn_marker_mod")
        exec self.code in self.mod.__dict__

    def __call__(self, x, y):
        ds_true       = []
        self.mod.avg  = numpy.mean(y)
        self.mod.sd   = numpy.std(y)
        self.mod.xmin = numpy.min(x)
        self.mod.xmax = numpy.max(x)
        self.mod.ymin = numpy.min(y)
        self.mod.ymax = numpy.max(y)
        for i in xrange(len(x)):
            if self.mod.f(x[i], y[i]):
                ds_true.append(i)
        return ds_true


## Turn an array of channel indices (the channels that we're interested in)
## into a 3D mask function
## Assumes that the indices have been shifted to 0 by slicing the column
## This implies that IF chanidx is a list of length 1, it must automatically
## be channel 0
def mk3dmask_fn_idx(nrow, chanidx, npol):
    return lambda x: x[:,chanidx,:]

def mk3dmask_fn_mask(nrow, chanidx, npol):
    if len(chanidx)>1 and (len(chanidx)!=(chanidx[-1]+1)):
        # Start off with all channels masked, up to the last index
        m              = numpy.ones( (nrow, chanidx[-1]+1, npol), dtype=numpy.int8 )
        # all indexed channels have no mask
        m[:,chanidx,:] = 0
        return lambda x: numpy.ma.MaskedArray(x, mask=m)
    else:
        # single channel - or all channels
        if len(chanidx)==1 and chanidx[0]!=0:
            raise RuntimeError, "consistency problem, chanidx[0] isn't 0 for single channel selection"
        return lambda x: numpy.ma.MaskedArray(x, mask=numpy.ma.nomask)


def genrows(bls, ddids, fldids):
    tm = 0
    while True:
        for (bl, dd, fld) in itertools.product(bls, ddids, fldids):
            yield (tm, bl, dd, fld)
        tm = tm + 1

import itertools, operator
class fakems:
    def __init__(self, ms, mapping):
        #self.ms      = ms
        self.length  = len(ms)

        #(self.a1, self.a2) = zip( *mapping.baselineMap.baselineIndices() )
        self.bls     = mapping.baselineMap.baselineIndices()
        self.ddids   = mapping.spectralMap.datadescriptionIDs()
        self.flds    = mapping.fieldMap.getFieldIDs()
        shp = ms[0]["LAG_DATA" if "LAG_DATA" in ms.colnames() else "DATA"].shape
        while len(shp)<2:
            shp.append(1)
        self.shp   = shp
        self.rowgen = genrows(self.bls, self.ddids, self.flds)
        self.chunk = {}
        print "fakems/",len(self.bls)," baselines, ",len(self.ddids)," SB, ",len(self.flds)," SRC, shape:",self.shp

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        theshape = self.shp
        class column:
            def __init__(self, shp):
                self.shape = shp

        class row:
            def __init__(self):
                self.rdict = { 'DATA': column(theshape), 'LAG_DATA': column(theshape) }

            def __getitem__(self, colnm):
                return self.rdict[colnm]

        return row()

    def getcol(self, col, **kwargs):
        nrow     = kwargs['nrow']
        startrow = kwargs['startrow']
        if not startrow in self.chunk:
            # new block of rows. delete existing
            del self.chunk
            i = [0]
            def predicate(x):
                i[0] = i[0] + 1
                return i[0]<=nrow
            self.chunk = {startrow: list(itertools.takewhile(predicate, self.rowgen))}
        # rows = [ (tm, (a1, a2), dd, fld), .... ]
        rows = self.chunk[startrow]

        coldict = {
                "ANTENNA1"    : (lambda x: map(lambda (tm, (a1, a2), dd, fl): a1, x), numpy.int32),
                "ANTENNA2"    : (lambda x: map(lambda (tm, (a1, a2), dd, fl): a2, x), numpy.int32),
                "TIME"        : (lambda x: map(lambda (tm, (a1, a2), dd, fl): tm, x), numpy.float64),
                "DATA_DESC_ID": (lambda x: map(lambda (tm, (a1, a2), dd, fl): dd, x), numpy.int32),
                "FIELD_ID"    : (lambda x: map(lambda (tm, (a1, a2), dd, fl): fl, x), numpy.int32)
                }
        (valfn, tp) = coldict.get(col, (None, None))
        #print "getcol[{0}]/var={1}".format(col, var)
        if valfn:
            return numpy.array(valfn(rows), dtype=tp)
        if col=="WEIGHT":
            # nrow x npol
            shp = (nrow, self.shp[1])
            rv = numpy.ones( reduce(operator.mul, shp), dtype=numpy.float32 )
            rv.shape = shp
            return rv
        if col=="DATA" or col=="LAG_DATA":
            shp = (nrow, self.shp[0], self.shp[1])
            rv = numpy.zeros( reduce(operator.mul, shp), dtype=numpy.complex64 )
            rv.shape = shp
            return rv
        raise RuntimeError,"Unhandled column {0}".format(col)


#### Different solint functions

def solint_none(dsref):
    return 0.0

# Tried a few different approaches for solint processing.
# The functions below are kept as illustrative references.
# 
# They are ordered from slowest to fastest operation, as benchmarked on running
# on the same data set with the same settings.
#
#  solint_numpy_indexing:       7.2s runtime
#  solint_numpy_countbin:       5.9s  
#  solint_pure_python:          3.8s
#  solint_pure_python3:         3.2s
#  solint_pure_python2:         2.8s


def solint_numpy_indexing(dsref):
    start = time.time()

    dsref.as_numarray()
    tms = numpy.unique(dsref.x)

    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    newds = dataset()
    for tm in tms:
        idxs = numpy.where(dsref.x==tm)
        newds.append(tm, numpy.average(dsref.y[idxs]), numpy.any(dsref.m[idxs]) )
    dsref.x = newds.x
    dsref.y = newds.y
    return time.time() - start

def solint_numpy_countbin(dsref):
    start = time.time()
    dsref.as_numarray()

    # get the unique time stamps 
    tms   = numpy.unique(dsref.x)
    
    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    # "bins" will be the destination bin where the quantity
    # will be summed into for each unique time stamp
    # i.e. all data having time stamp tms[0] will be summed into
    #      bin 0, all data having time stamp tms[x] will be summed
    #      into bin x
    #bins  = range( len(tms) )
    # Now we must transform the array of times (dsref.x) into an
    # array with bin indices
    dests = reduce(lambda acc, (ix, tm): \
                      numpy.put(acc, numpy.where(dsref.x==tm), ix) or acc, \
                   enumerate(tms), \
                   numpy.empty(dsref.x.shape, dtype=numpy.int32))
    # Good, now that we have that ...
    sums  = numpy.bincount(dests, weights=dsref.y)
    count = numpy.bincount(dests)
    dsref.y = sums/count
    dsref.x = tms
    return time.time() - start


def solint_pure_python(dsref):
    start = time.time()
    tms   = set(dsref.x)

    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    # accumulate data into bins of the same time
    r = reduce(lambda acc, (tm, y): acc[tm].append(y) or acc, \
               itertools.izip(dsref.x, dsref.y), \
               collections.defaultdict(list))
    # do the averaging
    (x, y) = reduce(lambda (xl, yl), (tm, ys): (xl+[tm], yl+[sum(ys)/len(ys)]), \
                    r.iteritems(), (list(), list()))
    dsref.x = x
    dsref.y = y
    return time.time() - start

class average(object):
    __slots__ = ['total', 'n']

    def __init__(self):
        self.total = 0.0
        self.n     = 0

    def add(self, other):
        self.total += other
        self.n     += 1
        return None

    def avg(self):
        return self.total/self.n

def solint_pure_python3(dsref):
    start = time.time()
    tms   = set(dsref.x)

    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    # accumulate data into bins of the same time
    r = reduce(lambda acc, (tm, y): acc[tm].add(y) or acc, \
               itertools.izip(dsref.x, dsref.y), \
               collections.defaultdict(average))
    # do the averaging
    (x, y) = reduce(lambda (xl, yl), (tm, ys): (xl.append(tm) or xl, yl.append(ys.avg()) or yl), \
                    r.iteritems(), (list(), list()))
    dsref.x = x
    dsref.y = y
    return time.time() - start

def solint_pure_python2(dsref):
    start = time.time()
    tms   = set(dsref.x)

    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    # accumulate data into bins of the same time
    r = reduce(lambda acc, (tm, y): acc[tm].append(y) or acc, \
               itertools.izip(dsref.x, dsref.y), \
               collections.defaultdict(list))
    # do the averaging
    (x, y) = reduce(lambda (xl, yl), (tm, ys): (xl.append(tm) or xl, yl.append(sum(ys)/len(ys)) or yl), \
                    r.iteritems(), (list(), list()))
    dsref.x = x
    dsref.y = y
    return time.time() - start

def solint_pure_python2a(dsref):
    start = time.time()
    tms   = set(dsref.x)

    # check if there is something to be averaged at all
    if len(tms)==len(dsref.x):
        return time.time() - start

    # accumulate data into bins of the same time
    acc = collections.defaultdict(list)
    y   = dsref.y
    m   = dsref.m
    for (i, tm) in enumerate(dsref.x):
        if m[i] == False:
            acc[ tm ].append( y[i] )
    # do the averaging
    (xl, yl) = (list(), list())
    for (tm, ys) in acc.iteritems():
        xl.append(tm)
        yl.append( sum(ys)/len(ys) )
    dsref.x = xl
    dsref.y = yl
    dsref.m = numpy.zeros(len(xl), dtype=numpy.bool)
    return time.time() - start

# In solint_pure_python4 we do not check IF we need to do something, just DO it
def solint_pure_python4(dsref):
    start = time.time()

    # accumulate data into bins of the same time
    r = reduce(lambda acc, (tm, y): acc[tm].append(y) or acc, \
               itertools.izip(dsref.x, dsref.y), \
               collections.defaultdict(list))
    # do the averaging
    (dsref.x, dsref.y) = reduce(lambda (xl, yl), (tm, ys): (xl.append(tm) or xl, yl.append(sum(ys)/len(ys)) or yl), \
                                r.iteritems(), (list(), list()))
    return time.time() - start

# solint_pure_python5 is solint_pure_python4 with the lambda's removed; replaced by
# calls to external functions. This shaves off another 2 to 3 milliseconds (on large data sets)
def grouper(acc, (tm, y)):
    acc[tm].append(y)
    return acc

def averager((xl, yl), (tm, ys)):
    xl.append(tm)
    yl.append(sum(ys)/len(ys))
    return (xl, yl)

def solint_pure_python5(dsref):
    start = time.time()

    # accumulate data into bins of the same time
    r = reduce(grouper, itertools.izip(dsref.x, dsref.y), collections.defaultdict(list))
    # do the averaging
    (dsref.x, dsref.y) = reduce(averager, r.iteritems(), (list(), list()))
    return time.time() - start

## This plotter will iterate over "DATA" or "LAG_DATA"
## and produce a number of quantities per data point, possibly averaging over time and/or channels
class data_quantity_time(plotbase):

    # should set up a choice table based on the combination of averaging methods
    # key into the lookup is '(avgChannelMethod, avgTimeMethod)'
    # Also return wether the quantities must be postponed
    _averaging = {
        # no averaging at all, no need to postpone computing the quantity(ies)
        (AVG.None, AVG.None):             (avg_none, avg_none, False),
        # only time averaging requested
        # scalar in time means we can collect the quantities themselves
        (AVG.None, AVG.Scalar):           (avg_none, avg_arithmetic, False),
        # when vector(norm) averaging we must first collect all time data
        # before we can compute the quantities, i.e. their computation  must be postponed
        (AVG.None, AVG.Vector):           (avg_none, avg_arithmetic, True),
        (AVG.None, AVG.Vectornorm):       (avg_none, avg_vectornorm, True),
        # When scalar averaging the channels no vector averaging in time possible
        # Also no need to postpone computing the quantities
        (AVG.Scalar, AVG.None):           (avg_arithmetic, avg_none, False),
        (AVG.Scalar, AVG.Scalar):         (avg_arithmetic, avg_arithmetic, False),
        # When vector averaging the channels, the time averaging governs 
        # the choice of when to compute the quantity(ies)
        (AVG.Vector, AVG.None):           (avg_arithmetic, avg_none, False),
        (AVG.Vector, AVG.Scalar):         (avg_arithmetic, avg_arithmetic, False),
        # when doing vector in both dims we must first add up all the complex numbers
        # for each channel(selection) and then in time and THEN compute the quantity(ies)
        (AVG.Vector, AVG.Vector):         (avg_arithmetic, avg_arithmetic, True),
        (AVG.Vector, AVG.Vectornorm):     (avg_arithmetic, avg_vectornorm, True),
        # vectornorm averaging over the channels, see what's requested in time
        (AVG.Vectornorm, AVG.None):       (avg_vectornorm, avg_none, False),
        (AVG.Vectornorm, AVG.Scalar):     (avg_vectornorm, avg_arithmetic, False),
        (AVG.Vectornorm, AVG.Vector):     (avg_vectornorm, avg_arithmetic, True),
        (AVG.Vectornorm, AVG.Vectornorm): (avg_vectornorm, avg_vectornorm, True)
    }


    ## our construct0r
    ##   qlist = [ (quantity_name, quantity_fn), ... ]
    ##
    def __init__(self, qlist):
        self.quantities = list(itertools.starmap(Quantity, qlist))

    def makePlots(self, msname, selection, mapping, **kwargs):
        # Deal with channel averaging
        #   Scalar => average the derived quantity
        #   Vector => compute average cplx number, then the quantity
        avgChannel = CP(selection.averageChannel)
        avgTime    = CP(selection.averageTime)
        solchan    = CP(selection.solchan)
        solint     = CP(selection.solint)
        timerng    = CP(selection.timeRange)

        # some sanity checks
        if solchan is not None and avgChannel==AVG.None:
            raise RuntimeError("solchan value was set without specifiying a channel averaging method; please tell me how you want them averaged")
        # Test if the selected combination of averaging settings makes sense
        setup = data_quantity_time._averaging.get((avgChannel, avgTime), None)
        if setup is None:
            raise RuntimeError("the combination of {0} channel + {1} time averaging is not supported".format(avgChannel, avgTime))
        (avgchan_fn, avgtime_fn, postpone) = setup

        ## initialize the base class
        super(data_quantity_time, self).__init__(msname, selection, mapping, **kwargs)

        # Support "time averaging" by aggregating data points in time bins of 'solint' length
        solint_fn       = solint_none
        # How integration/averaging actually is implemented is by modifying the
        # time stamp.  By massaging the time stamp into buckets of size
        # 'solint', we influence the label of the TIME field, which will make
        # all data points with the same TIME stamp be integrated into the same
        # data set
        self.timebin_fn = functional.identity
        if avgTime!=AVG.None:
            if solint is None:
                # Ah. Hmm. Have to integrate different time ranges
                # Let's transform our timerng list of (start, end) intervals into
                # a list of (start, end, mid) such that we can easily map
                # all time stamps [start, end] to mid

                # It is important to KNOW that "selection.timeRange" (and thus our
                # local copy 'timerng') is a list or sorted, non-overlapping time ranges
                timerng = map(lambda (s, e): (s, e, (s+e)/2.0), timerng)
                if len(timerng)==1:
                    print "WARNING: averaging all data into one point in time!"
                    print "         This is because no solint was set. Your plot"
                    print "         may contain less useful info than expected"

                # try to be a bit optimized in time stamp replacement - filter the 
                # list of time ranges to those applying to the time stamps we're 
                # replacing
                def do_it(x):
                    mi,ma  = numpy.min(x), numpy.max(x)
                    ranges = filter(lambda tr: not (tr[0]>ma or tr[1]<mi), timerng)
                    return reduce(lambda acc, (s, e, m): numpy.put(acc, numpy.where((acc>=s) & (acc<=e)), m) or acc, ranges, x) 
                self.timebin_fn = do_it
                #self.timebin_fn = lambda x: \
                #        reduce(lambda acc, (s, e, m): numpy.put(acc, numpy.where((acc>=s) & (acc<=e)), m) or acc, timerng, x)
            else:
                # Check if solint isn't too small
                ti = mapping.timeRange.inttm[0]
                if solint<ti: 
                    raise RuntimeError("solint value {0:.3f} is less than integration time {1:.3f}".format(solint, ti))
                self.timebin_fn = lambda x: (numpy.trunc(x/solint)*solint) + solint/2.0
            solint_fn = solint_pure_python2a

        # channel selection+averaging schemes; support averaging over channels (or chunks of channels)
        chansel  = Ellipsis #None
        n_chan   = self.table[0]['DATA'].shape[0]
        if selection.chanSel:
            channels = list(sorted(set(CP(selection.chanSel))))
            max_chan = max(channels)
            # if any of the indexed channels > n_chan that's an error
            if max_chan>=n_chan:
                raise RuntimeError("At least one selected channel ({0}) > largest channel index ({1})".format(max_chan, n_chan-1))
            # if the user selected all channels (by selection
            # 'ch 0:<last>' in stead of 'ch none' we don't 
            # override the channel selection
            if channels!=range(n_chan):
                chansel = channels

        # chansel now is Ellipsis (all channels) or a list of some selected channels
        self.chanidx   = list()
        self.vectorAvg = functional.identity
        self.scalarAvg = functional.identity
        self.tmVectAvg = functional.identity
        self.tmScalAvg = functional.identity

        if avgChannel==AVG.None:
            # No channel averaging - each selected channel goes into self.chanidx
            self.chanidx = list(enumerate(range(n_chan) if chansel is Ellipsis else chansel)) #map(lambda ch: (ch, ch), range(n_chan) if not chansel else chansel)
            # The vector average step will be misused to just apply the channel selection such that all selected channels
            # are mapped to 0..n-1. This is only necessary in case not all channels were selected
            if chansel is not Ellipsis:
                self.vectorAvg = lambda x: x[:,chansel,:]
        else:
            # ok channel averaging requested
            chbin_fn = None
            if solchan is None:
                # average all selected channels down to one
                # data array 'x' has shape (n_int, n_chan, n_pol)
                #self.chbin_fn = lambda x: normalize_ch(1)(numpy.ma.mean(x[:,avg_over,:], axis=1, keepdims=True))
                # average the selected channels according the requested averaging method
                chbin_fn      = lambda x: avgchan_fn(1)(x[:,chansel,:])
                self.chanidx  = [(0, '*')]
            else:
                # average bins of solchan channels down to one
                # Create a mask which is the complement of the selected channels
                # (remember: chansel == None => all channels
                ch_mask       = (numpy.ones if chansel is None else numpy.zeros)(n_chan, dtype=numpy.bool)
                # only in case chansel != everything we must modify the mask
                if chansel:
                    ch_mask[chansel] = False

                # Since we're going to use zap masked values (replace by 0) we can usefully use
                # reduceat! So all we then need is an index array, informing reduceat what the 
                # reduction boundaries are!
                # First up: the actual bin numbers we're interested in, we compute the actual
                #           start + end indices from that
                bins    = set(numpy.array(chansel)//4) if chansel else range(0, n_chan, solchan)
                indices = map(lambda s: (s*solchan, min((s+1)*solchan, n_chan)), bins)
                # for display + loopindexing create list of (array_index, "CH label") tuples
                for (ch_idx, start_end) in enumerate(indices):
                    self.chanidx.append( (ch_idx, "{0}*".format(start_end[0])) )
                # now we should be able to come up with a function that 
                # applies the channel averaging efficiently ...
                # The input 'x' is masked array (n_int, n_chan, n_pol)
                # We must broadcast the channel mask (the channels we're interested in in averaging)
                # so let's transpose the data to read (n_int, n_pol, n_chan) because then numpy.logical_or()
                # will broadcast Just Fine across all times & polarizations
                transpose_ch = operator.methodcaller('transpose', (0, 2, 1))
                def do_it(x):
                    tmpx = transpose_ch(x)
                    # mask out channels that we don't want averaged, joining it
                    # with the mask that excludes flagged data (by the user) and/or
                    # whatever was weight-thresholded ...
                    tmpx.mask = numpy.logical_or(tmpx.mask, ch_mask)
                    # set all masked values to 0 such that they don't count towards the average
                    tmpx.data[tmpx.mask] = 0
                    # do the summation
                    result = numpy.add.reduceat(tmpx.data,  indices, axis=2)
                    # also count the number of unmasked values that went into each point
                    # we may use it for averaging, definitely be using it to create the mask
                    counts = numpy.add.reduceat(~tmpx.mask, indices, axis=2)
                    # Because we do things different here than in the ordinary averaging,
                    # we must look at what was requested in order to mimic that behaviour
                    if avgchan_fn is avg_vectornorm:
                        # ok need to find the maximum complex number in each bin to scale it by
                        result  = result / numpy.maximum.reduceat(numpy.abs(tmpx.data), indices, axis=2)
                    else:
                        # ordinary arithmetic mean
                        result /= counts
                    # return masked array - can reuse the counts array by converting them
                    # to bool and inverting: no counts => False
                    return tranpose_ch(numpy.ma.array(result, mask=~numpy.array(counts, dtype=numpy.bool)))
                chbin_fn = doit
            # Some channel averaging is to be applied so chbin_fn must not be None
            if chbin_fn is None:
                raise RuntimeError("chbin_fn is None whilst some channel averaging requested. Please yell at H. Verkouter (verkouter@jive.eu)")
            # depending on which kind of channel averaging, we apply it to the complex data before
            # producing quantities or on the scalars after computing the quantities
            if avgChannel == AVG.Scalar:
                self.scalarAvg = chbin_fn
            else:
                self.vectorAvg = chbin_fn

        # Now we must come up with a strategy for organizing the data processing chain
        #
        # If avgTime is Vector-like then we can only compute the quantities after all data's been
        # read & averaged. We've already ruled out that avgChannel == Scalar (for that makes no sense)
        #
        # So we may have to postpone computing of the quantities until after having collected + integrated all data
        post_quantities = lambda tp, x: [(tp, x)]
        if postpone:
            # create data sets based on the averaged data in a dataset
            post_quantities = lambda _, x: map(lambda q: (q.quantity_name, q.quantity_fn(x)), CP(self.quantities))
            self.quantities = [('raw', functools.identity)]

        # if we're doing time averaging, ask the system to bin by x-axis value (time stamp) on the fly
        # and extract the channels later. Also when doing large number of channels, it may be beneficial
        # to accumulate many channels and extract the channels later
        post_channel  = lambda ch, x: [(ch, x)]
        dataset_proto = None
        if avgTime == AVG.None:
            dataset_proto = dataset_list
            if float(len(self.chanidx))/n_chan > 0.1:
                post_channel       = lambda _, x: map(lambda chi: (chi[1], x[chi[0]]), CP(self.chanidx))
                self.chanidx       = [(Ellipsis, None)]
        else:
            dataset_proto = dataset_solint
            post_channel       = CP(self.chanidx)
            self.chanidx       = [(Ellipsis, None)]

        ## Now we can start the reduction of the table
        # Note: there will /always/ be WEIGHT+FLAGCOL - either read from the table or invented
        #          0        1      2      3      4       5     6
        fields  = [AX.TYPE, AX.BL, AX.FQ, AX.SB, AX.SRC, AX.P, AX.CH]
        columns = ["ANTENNA1", "ANTENNA2", "TIME", "DATA_DESC_ID", "FIELD_ID", "WEIGHTCOL", "FLAGCOL", self.datacol]
        #pts     =  ms2util.reducems2(self, self.table, {}, columns, verbose=True, slicers=self.slicers, chunksize=5000)
        pts     =  ms2util.reducems2(self, self.table, collections.defaultdict(dataset_proto), columns, verbose=True, slicers=self.slicers, chunksize=5000)

        # after the reduction's done we can put back our quantities if we did remove them before
        if post_quantities is not None:
            self.quantities = post_quantities

        rv  = {}
        for (label, dataset) in pts.iteritems():
            dl = list(label)
            dataset.average( avgTime )
            # convert x,y to numarrays
            dataset.as_numarray()
            for qn,qd in post_quantities(label[0], dataset.y):
                for chn,chd in post_channel(label[6], dataset.y):
                    dl[0] = qn
                    dl[6] = chn
                    rv[ self.MKLAB(fields, dl) ] = dataset_fixed(dataset.x, chd)
            # do time averaging - find all data points with the same x-value and scalar average them
            # [the time stamps have been changed into integer multiples of solint, if solint!=None]
            #rv[ self.MKLAB(fields, label) ] = dataset
        #if solint:
        #    print "SOLINT processing took\t{0:.3f}s".format( dt )
        #for k in rv.keys():
        #    print "Plot:",str(k),"/",map(str, rv[k].keys())
        #for plt in rv.keys():
        #    for ds in rv[plt].keys():
        #        print "Plot:",str(plt),"/",str(ds)," dataset=",rv[plt][ds]
        return rv

    ## Here we make the plots
    def __call__(self, acc, a1, a2, tm, dd, fld, weight, flags, data):

        # Create masked array from the data with invalid data already masked off
        data = numpy.ma.masked_invalid(data)
        # now we can easily add in flag information;
        # flags either has shape of data or it's a single bool False
        data.mask = numpy.logical_or(data.mask, flags)
        # weight handling. It's been set up such that whatever the weight was
        # (WEIGHT, WEIGHT_SPECTRUM, no weight thresholding) the following sequence
        # always works
        data      = self.transpose(data)
        data.mask = numpy.logical_or(data.mask, weight<self.threshold)
        data      = self.transpose(data)

        # possibly vector-average the data
        data      = self.vectorAvg(data)
        # Now create the quantity data - map the quantity functions over the (vector averaged)
        # data and, if needed, scalar average them
        qd        = map(lambda q: (q.quantity_name, self.scalarAvg(q.quantity_fn(data))), self.quantities)

        # Transform the time stamps, if necessary
        tm        = self.timebin_fn(tm)

        # Now we can loop over all the rows in the data
        dds  = self.ddSelection
        ci   = self.chanidx
        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(data.shape[0]):
            (fq, sb, plist) = dds[ dd[row] ]
            for (chi, chn) in ci:
                for (pidx, pname) in plist:
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        acc[tuple(l)].append(tm[row], qval[row, chi, pidx], qval.mask[row, chi, pidx])
                        #acc.setdefault(tuple(l), self.dataset_proto()).append(tm[row], qval[row, chi, pidx], qval.mask[row, chi, pidx])
        return acc


    def old_stuff(self):
        #print "__call__: ",a1,a2,tm,dd,fld,data.shape
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape

        # compute weight mask
        w3d  = numpy.zeros(shp, dtype=numpy.float)
        for i in xrange(shp[0]):
            # we have weights per polzarization but we must
            # expand them to per channel ...
            cw = numpy.vstack( shp[1]*[weight[i]] )
            w3d[i] = cw
        w3m =  w3d<self.threshold
        wfn = lambda a: numpy.ma.MaskedArray(a.data, numpy.logical_and(a.mask, w3m))
        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking + vector averaging
        #         'vamd' = vector averaged masked data
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])
        vamd = self.vectorAvg( wfn(mfn(d3d)) )

        # Now create the quantity data - map the quantity functions over the
        # (potentially) vector averaged data and (potentially) scalar
        # average them
        qd   = map(lambda (qnm, qfn): (qnm, self.scalarAvg(qfn(vamd))), self.quantities)
        #for (qn, qv) in qd:
        #    print qn,": shape=",qv.shape

        # Transform the time stamps [rounds time to integer multiples of solint, if that is set]
        tm   = self.timebin_fn( tm )
        flag = flag[0] if flag else None
        flg  = (lambda row, ch, p: False) if flag is None else (lambda row, ch, p: flag[row, ch, p])

        # Now we can loop over all the rows in the data
        dds = self.ddSelection
        ci  = self.chanidx

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(shp[0]):
            (fq, sb, plist) = dds[ dd[row] ]
            for (chi, chn) in ci:
                for (pidx, pname) in plist:
                    if self.reject_f(w3d[row, chi, pidx]):
                        self.nreject = self.nreject + 1
                        continue
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        #pi       = self.plot_idx(l)
                        #di       = self.ds_idx(l)
                        #print "row #",row,"/l=",l," => pi=",pi," di=",di," qval.shape=",qval.shape
                        acc.setdefault(tuple(l), dataset()).append(tm[row], qval[row, chi, pidx], flg(row, chi, pidx))
        return acc
        return self.actual_fn(*args)

    #### This is the version WITHOUT WEIGHT THRESHOLDING
    def withoutWeightOneLabel(self, acc, a1, a2, tm, dd, fld, data, *flag):
        #print "__call__: ",a1,a2,tm,dd,fld,data.shape
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape

        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking + vector averaging
        #         'vamd' = vector averaged masked data
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])
        vamd = self.vectorAvg( mfn(d3d) )

        # Now create the quantity data - map the quantity functions over the
        # (potentially) vector averaged data and (potentially) scalar
        # average them
        qd   = map(lambda (qnm, qfn): (qnm, self.scalarAvg(qfn(vamd))), self.quantities)

        # Transform the time stamps [rounds time to integer multiples of solint, if that is set]
        tm   = self.timebin_fn( tm )
        flag = flag[0] if flag else None
        flg  = (lambda row, ch, p: False) if flag is None else (lambda row, ch, p: flag[row, ch, p])

        # Now we can loop over all the rows in the data

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        dds = self.ddSelection
        ci  = self.chanidx
        for row in range(shp[0]):
            (fq, sb, plist) = dds[ dd[row] ]
            for (chi, chn) in ci:
                for (pidx, pname) in plist:
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        acc.setdefault(tuple(l), dataset()).append(tm[row], qval[row, chi, pidx], flg(row, chi, pidx))
        return acc

    #### This is the version WITH WEIGHT THRESHOLDING
    def withWeightOneLabel(self, acc, a1, a2, tm, dd, fld, weight, data, *flag):
        #print "__call__: ",a1,a2,tm,dd,fld,data.shape
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape

        # compute weight mask
        w3d  = numpy.zeros(shp, dtype=numpy.float)
        for i in xrange(shp[0]):
            # we have weights per polzarization but we must
            # expand them to per channel ...
            cw = numpy.vstack( shp[1]*[weight[i]] )
            w3d[i] = cw
        w3m =  w3d<self.threshold
        wfn = lambda a: numpy.ma.MaskedArray(a.data, numpy.logical_and(a.mask, w3m))
        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking + vector averaging
        #         'vamd' = vector averaged masked data
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])
        vamd = self.vectorAvg( wfn(mfn(d3d)) )

        # Now create the quantity data - map the quantity functions over the
        # (potentially) vector averaged data and (potentially) scalar
        # average them
        qd   = map(lambda (qnm, qfn): (qnm, self.scalarAvg(qfn(vamd))), self.quantities)
        #for (qn, qv) in qd:
        #    print qn,": shape=",qv.shape

        # Transform the time stamps [rounds time to integer multiples of solint, if that is set]
        tm   = self.timebin_fn( tm )
        flag = flag[0] if flag else None
        flg  = (lambda row, ch, p: False) if flag is None else (lambda row, ch, p: flag[row, ch, p])

        # Now we can loop over all the rows in the data
        dds = self.ddSelection
        ci  = self.chanidx

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(shp[0]):
            (fq, sb, plist) = dds[ dd[row] ]
            for (chi, chn) in ci:
                for (pidx, pname) in plist:
                    if self.reject_f(w3d[row, chi, pidx]):
                        self.nreject = self.nreject + 1
                        continue
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        #pi       = self.plot_idx(l)
                        #di       = self.ds_idx(l)
                        #print "row #",row,"/l=",l," => pi=",pi," di=",di," qval.shape=",qval.shape
                        acc.setdefault(tuple(l), dataset()).append(tm[row], qval[row, chi, pidx], flg(row, chi, pidx))
        return acc

## This plotter will iterate over "DATA" or "LAG_DATA"
## and produce a number of quantities per frequency
class data_quantity_chan(plotbase):

    ## our construct0r
    ##   qlist = [ (quantity_name, quantity_fn), ... ]
    ##
    ##  Note that 'time averaging' will be implemented on a per-plot
    ##  basis, not at the basic type of plot instance
    def __init__(self, qlist, **kwargs):
        self.quantities  = qlist
        self.byFrequency = kwargs.get('byFrequency', False)

    def makePlots(self, msname, selection, mapping, **kwargs):
        datacol = CP(mapping.domain.column)

        # Deal with time averaging
        #   Scalar => average the derived quantity
        #   Vector => compute average cplx number, then the quantity
        avgTime = CP(selection.averageTime)
        solint  = CP(selection.solint)
        timerng = CP(selection.timeRange)

        # need a function that (optionally) transforms the FQ/SB/CH idx to real frequencies
        self.changeXaxis = lambda dd, chanidx: chanidx
        if self.byFrequency:
            if mapping.spectralMap is None:
                raise RuntimeError("Request to plot by frequency but no spectral mapping available")
            self.changeXaxis = lambda dd, chanidx: self.ddFreqs[ dd ][ chanidx ]

        # solint must be >0.1 OR must be equal to None 
        # solint==None implies "aggregate all data into the selected time ranges in
        #   their separate bins"
        if avgTime!=AVG.None and not (selection.solint is None or selection.solint>0.1):
            raise RuntimeError, "time averaging requested but solint is not none or >0.1: {0}".format(selection.solint)
        # If solint is a number and averaging is not set, default to Scalar averaging
        if selection.solint and avgTime==AVG.None:
            avgTime = AVG.Scalar
            print "WARN: solint is set but no averaging method was specified. Defaulting to ",avgTime

        if selection.averageChannel!=AVG.None:
            print "WARN: {0} channel averaging ignored for this plot".format(selection.averageChannel)

        # If time averaging requested but solint==None and timerange==None, this means we
        # have to set up a time range to integrate. timerange==None => whole data set
        if avgTime!=AVG.None and solint is None and timerng is None:
            timerng = [(mapping.timeRange.start, mapping.timeRange.end)]

        ## initialize the base class
        super(data_quantity_chan, self).__init__(msname, selection, mapping, **kwargs)

        ## Some variables must be stored in ourselves such 
        ## that they can be picked up by the callback function
        slicers    = {}

        # For data sets with a large number of channels
        # (e.g. UniBoard data, 1024 channels spetral resolution)
        # it makes a big (speed) difference if there is a channel
        # selection to let the casa stuff [the ms column] do
        # the (pre)selection so we do not get *all* the channels
        # into casa

        # 1) the channel selection. it is global; ie applies to
        #    every data description id.
        #    also allows us to create a slicer
        #    default: iterate over all channels
        shape           = self.table[0][datacol].shape
        self.chunksize  = 5000
        self.maskfn     = lambda x: numpy.ma.MaskedArray(x, mask=numpy.ma.nomask)
        self.chanidx    = numpy.arange(shape[0])
        self.chansel    = numpy.arange(shape[0])

        # After having read the data, first we apply the masking function
        # which disables the unselected channels
        if selection.chanSel:
            channels         = sorted(CP(selection.chanSel))
            indices          = map(lambda x: x-channels[0], channels)
            self.chanidx     = numpy.array(channels, dtype=numpy.int32)
            self.chansel     = numpy.array(indices, dtype=numpy.int32)
            self.maskfn      = mk3dmask_fn_mask(self.chunksize, indices, shape[-1])
            slicers[datacol] = ms2util.mk_slicer((channels[0],  0), (channels[-1]+1, shape[-1]))

        # This is how we're going to go about dealing with time averaging
        # The model is that, after having read the data, there is a function
        # being called which produces (a list of) data products
        #   * with scalar averaging, we produce a list of scalar quantities, the result
        #     of calling self.quantities on the data. the .TYPE field in the data set
        #     label is the actual quantity type
        #   * with vector averaging, we produce nothing but the raw data itself; it is
        #     the complex numbers that we must integrate/average. we give these data sets
        #     the .TYPE of 'raw'.
        #   * with no averaging at all, we also return the 'raw' data
        #
        # Then all the data is accumulated
        # After the whole data set has been processed, we do the averaging and
        # apply another transformation function:
        #   * with scalar averaging, we don't have to do anything; the quantities have already
        #     been produced
        #   * with vector averaging, we take all data sets with type 'raw' and map our
        #     quantity producing functions over the averaged data, producing new data sets
        #     The raw data can now be deleted

        # How integration/averaging actually is implemented is by modifying the
        # time stamp.  By massaging the time stamp into buckets of size
        # 'solint', we influence the label of the TIME field, which will make
        # all data points with the same TIME stamp be integrated into the same
        # data set
        self.timebin_fn = lambda x: x
        if avgTime!=AVG.None:
            if solint is None:
                # Ah. Hmm. Have to integrate different time ranges
                # Let's transform our timerng list of (start, end) intervals into
                # a list of (start, end, mid) such that we can easily map
                # all time stamps [start, end] to mid

                # It is important to KNOW that "selection.timeRange" (and thus our
                # local copy 'timerng') is a list or sorted, non-overlapping time ranges
                timerng = map(lambda (s, e): (s, e, (s+e)/2.0), timerng)
                self.timebin_fn = lambda x: \
                        reduce(lambda acc, (s, e, m): numpy.put(acc, numpy.where((acc>=s) & (acc<=e)), m) or acc, timerng, x)
            else:
                # we have already checked the validity of solint
                self.timebin_fn = lambda x: (numpy.trunc(x/solint)*solint) + solint/2.0

        # With no time averaging or with Scalar averaging, we can immediately produce
        # the quantities. Only when doing Vector averaging, we must produce the quantities
        # after having read all the data
        self.preProcess = lambda x: map(lambda (qnm, qfn): (qnm, qfn(x)), self.quantities)
        if avgTime in [AVG.Vector, AVG.Vectornorm]:
            doNormalize     = (lambda x: x) if avgTime==AVG.Vector else (lambda x: x/numpy.abs(x))
            self.preProcess = lambda x: [('raw', doNormalize(x))]

        fields = [AX.TYPE, AX.BL, AX.FQ, AX.SB, AX.SRC, AX.P, AX.TIME]

        # weight filtering
        self.nreject   = 0
        self.reject_f  = lambda weight: False
        self.threshold = -10000000
        if selection.weightThreshold is not None:
            self.threshold = CP(selection.weightThreshold)
            self.reject_f  = lambda weight: weight<self.threshold

        ## Now we can start the reduction of the table
        if selection.weightThreshold is None:
            columns        = ["ANTENNA1", "ANTENNA2", "TIME", "DATA_DESC_ID", "FIELD_ID", datacol]
            self.actual_fn = self.withoutWeightThresholding
        else:
            columns        = ["ANTENNA1", "ANTENNA2", "TIME", "DATA_DESC_ID", "FIELD_ID", "WEIGHT", datacol]
            self.actual_fn = self.withWeightThresholding
        if self.flags:
            columns.append( "FLAGCOL" )
        pts     =  ms2util.reducems2(self, self.table, {}, columns, verbose=True, slicers=slicers, chunksize=self.chunksize)

        if self.nreject:
            print "Rejected ",self.nreject," points because of weight criterion"

        ## Excellent. Now start post-processing
        rv  = {}
        for (label, ds) in pts.iteritems():
            ds.average()
            if label[0]=='raw':
                dl = list(label)
                for (qnm, qd) in map(lambda (qnm, qfn): (qnm, qfn(ds.y)), self.quantities):
                    dl[0] = qnm
                    rv[ self.MKLAB(fields, dl) ] = dataset(ds.x, qd, ds.m)
            else:
                rv[ self.MKLAB(fields, label) ] = ds
        #for k in rv.keys():
        #    print "Plot:",str(k),"/",map(str, rv[k].keys())
        return rv


    ## Here we make the plots
    def __call__(self, *args):
        return self.actual_fn(*args)

    # This is the one WITHOUT WEIGHT THRESHOLDING
    def withoutWeightThresholding(self, acc, a1, a2, tm, dd, fld, data, *flag):
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape

        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking, such that any averaging later on
        #         will skip the masked data.
        #         'md' is "masked data"
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])

        # Now create the quantity data 
        # qd will be a list of (quantity_name, quantity_data) tuples
        #   original: qd = map(lambda (qnm, qfn): (qnm, qfn(mfn(d3d))), self.quantities)
        qd   = self.preProcess( mfn(d3d) )

        # Transform the time stamps [rounds time to integer multiples of solint
        # if that is set or the midpoint of the time range if solint was None]
        tm   = self.timebin_fn( tm )
        flag = flag[0] if flag else numpy.zeros(data.shape, dtype=numpy.bool)

        # Now we can loop over all the rows in the data

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        dds = self.ddSelection
        cx  = self.changeXaxis
        ci  = self.chanidx
        cs  = self.chansel
        for row in range(shp[0]):
            ddr             = dd[row]
            (fq, sb, plist) = dds[ ddr ] 
            # we can already precompute most of the label
            # potentially, modify the TIME value to be a time bucket such
            # that we can intgrate into it
            l = ["", (a1[row], a2[row]), fq, sb, fld[row], "", tm[row]]
            # we don't iterate over channels, only over polarizations
            for (pidx, pname) in plist:
                l[5] = pname
                for (qnm, qval) in qd:
                    l[0] = qnm
                    acc.setdefault(tuple(l), dataset()).sumy(cx(ddr, ci), qval[row, cs, pidx], flag[row, cs, pidx])
        return acc

    # This is the one WITH WEIGHT THRESHOLDING
    def withWeightThresholding(self, acc, a1, a2, tm, dd, fld, weight, data):
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape

        # compute weight mask
        w3d  = numpy.zeros(shp, dtype=numpy.float)
        for i in xrange(shp[0]):
            # we have weights per polzarization but we must
            # expand them to per channel ...
            cw = numpy.vstack( shp[1]*[weight[i]] )
            w3d[i] = cw
        w3m =  w3d<self.threshold
        wfn = lambda a: numpy.ma.MaskedArray(a.data, numpy.logical_and(a.mask, w3m))

        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking, such that any averaging later on
        #         will skip the masked data.
        #         'md' is "masked data"
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])

        # Now create the quantity data 
        # qd will be a list of (quantity_name, quantity_data) tuples
        #   original: qd = map(lambda (qnm, qfn): (qnm, qfn(mfn(d3d))), self.quantities)
        qd   = self.preProcess( wfn(mfn(d3d)) )

        # Transform the time stamps [rounds time to integer multiples of solint
        # if that is set or the midpoint of the time range if solint was None]
        tm   = self.timebin_fn( tm )
        flag = flag[0] if flag else numpy.zeros(data.shape, dtype=numpy.bool)

        # Now we can loop over all the rows in the data
        dds = self.ddSelection
        ci  = self.chanidx
        cs  = self.chansel
        cx  = self.changeXaxis
        rf  = self.reject_f
        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(shp[0]):
            ddr             = dd[row]
            (fq, sb, plist) = dds[ ddr ]
            # we can already precompute most of the label
            # potentially, modify the TIME value to be a time bucket such
            # that we can intgrate into it
            l = ["", (a1[row], a2[row]), fq, sb, fld[row], "", tm[row]]
            # we don't iterate over channels, only over polarizations
            for (pidx, pname) in plist:
                if rf(w3d[row, 0, pidx]):
                    self.nreject = self.nreject + 1
                    continue
                l[5] = pname
                for (qnm, qval) in qd:
                    l[0] = qnm
                    acc.setdefault(tuple(l), dataset()).sumy(cx(ddr, ci), qval[row, cs, pidx], flag[row, cs, pidx])
        return acc


class unflagged(object):
    def __getitem__(self, idx):
        return False

class weight_time(plotbase):
    def __init__(self):
        # nothing yet ...
        pass

    def makePlots(self, msname, selection, mapping, **kwargs):
        ## initialize the base class (opens table, does selection)
        super(weight_time, self).__init__(msname, selection, mapping, **kwargs)

        # Support "time averaging" by aggregating data points in time bins of 'solint' length
        solint          = CP(selection.solint)
        solint_fn       = solint_none
        self.timebin_fn = lambda x: x 
        if solint is not None:
            ti = mapping.timeRange.inttm[0]
            if solint<ti: 
                raise RuntimeError, "solint value {0:.3f} is less than integration time {1:.3f}".format(solint, ti)
            self.timebin_fn = lambda x: (numpy.trunc(x/solint)*solint) + solint/2.0

            # decide which solint function to use
            solint_fn = solint_pure_python2a
        
        ## we plot using the WEIGHT column

        fields = [AX.TYPE, AX.BL, AX.FQ, AX.SB, AX.SRC, AX.P]

        #self.cnt = 0
        #self.ts  = set()
        ## Now we can start the reduction of the table
        columns = ["ANTENNA1", "ANTENNA2", "TIME", "DATA_DESC_ID", "FIELD_ID", "WEIGHT"] + ["FLAG_ROW"] if self.flags else []
        pts     =  ms2util.reducems2(self, self.table, {}, columns, verbose=True, chunksize=5000)

        #print "WE SHOULD HAVE ",self.cnt," DATA POINTS"
        #print "ANDALSO ",len(self.ts)," TIME STAMPS"

        rv  = {}
        dt  = 0.0
        for (label, dataset) in pts.iteritems():
            dt += solint_fn( dataset )
            rv[ self.MKLAB(fields, label) ] = dataset
        if solint:
            print "SOLINT processing took\t{0:.3f}s".format( dt )
        return rv

    def __call__(self, acc, a1, a2, tm, dd, fld, weight, *flag_row):
        #print "__call__: ",a1,a2,tm,dd,fld,weight.shape
        # ok, process all the rows!
        shp   = weight.shape
        flags = unflagged() if not flag_row else flag_row[0]
        # single-pol data will have shape (nrow,) 
        # but our code really would like it to be (nrow, npol), even if 'npol' == 1. (FFS casacore!)
        tm  = self.timebin_fn( tm )
        d2d = m2d(weight)
        for row in range(shp[0]):
            (fq, sb, plist) = self.ddSelection[ dd[row] ]
            # we don't iterate over channels
            for (pidx, pname) in plist:
                acc.setdefault((YTypes.weight, (a1[row], a2[row]), fq, sb, fld[row], pname), dataset()).append(tm[row], weight[row, pidx], flags[row])
        return acc

class uv(plotbase):
    def __init__(self):
        # nothing yet ...
        pass

    def makePlots(self, msname, selection, mapping, **kwargs):
        ## initialize the base class (opens table, does selection)
        super(uv, self).__init__(msname, selection, mapping, **kwargs)
        
        ## we plot using the UVW column
        ## UVW is not a function of POL (it should be a function
        ##     of CH but that would mean we'd have to actually
        ##     do computations - yikes)

        fields = [AX.TYPE, AX.BL, AX.FQ, AX.SB, AX.SRC]

        ## Now we can start the reduction of the table
        columns = ["ANTENNA1", "ANTENNA2", "DATA_DESC_ID", "FIELD_ID", "UVW"] + ["FLAG_ROW"] if self.flags else []
        pts     =  ms2util.reducems2(self, self.table, {}, columns, verbose=True, chunksize=5000)

        rv  = {}
        for (label, dataset) in pts.iteritems():
            rv[ self.MKLAB(fields, label) ] = dataset
        #for k in rv.keys():
        #    print "Plot:",str(k),"/",map(str, rv[k].keys())
        return rv

    def __call__(self, acc, a1, a2, dd, fld, uvw, *flag_row):
        # ok, process all the rows!
        flags = unflagged() if not flag_row else flag_row[0]
        for row in range(uvw.shape[0]):
            (fq, sb, _plist) = self.ddSelection[ dd[row] ]
            # we don't iterate over channels nor over polarizations
            ds = acc.setdefault(('V', (a1[row], a2[row]), fq, sb, fld[row]), dataset())
            f  = flags[row]
            ds.append( uvw[row, 0],  uvw[row, 1], f)
            ds.append(-uvw[row, 0], -uvw[row, 1], f)
        return acc

## This plotter will iterate over "DATA" or "LAG_DATA"
## and produce a number of quantities per data point
class data_quantity_uvdist(plotbase):

    ## our construct0r
    ##   qlist = [ (quantity_name, quantity_fn), ... ]
    ##
    ##  Note that 'channel averaging' will be implemented on a per-plot
    ##  basis, not at the basic type of plot instance
    def __init__(self, qlist):
        self.quantities = qlist

    def makePlots(self, msname, selection, mapping, **kwargs):
        datacol = CP(mapping.domain.column)

        # Deal with channel averaging
        #   Scalar => average the derived quantity
        #   Vector => compute average cplx number, then the quantity
        avgChannel = CP(selection.averageChannel)

        if selection.averageTime!=AVG.None:
            print "Warning: {0} time averaging ignored for this plot".format(selection.averageTime)

        ## initialize the base class
        super(data_quantity_uvdist, self).__init__(msname, selection, mapping, **kwargs)

        ## Some variables must be stored in ourselves such 
        ## that they can be picked up by the callback function
        slicers    = {}

        # For data sets with a large number of channels
        # (e.g. UniBoard data, 1024 channels spetral resolution)
        # it makes a big (speed) difference if there is a channel
        # selection to let the casa stuff [the ms column] do
        # the (pre)selection so we do not get *all* the channels
        # into casa

        # 1) the channel selection. it is global; ie applies to
        #    every data description id.
        #    also allows us to create a slicer
        #    default: iterate over all channels
        shape           = self.table[0][datacol].shape
        self.chunksize  = 5000
        self.chanidx    = zip(range(shape[0]), range(shape[0]))
        self.maskfn     = lambda x: numpy.ma.MaskedArray(x, mask=numpy.ma.nomask)
        self.chansel    = range(shape[0])

        # We must translate the selected channels to a frequency (or wavelength) - such that we can 
        # compute the uvdist in wavelengths
        _spwMap  = mapping.spectralMap
        ddids    = _spwMap.datadescriptionIDs()

        # preallocate an array of dimension (nDDID, nCHAN) such that we can put 
        # the frequencies of DDID #i at row i - makes for easy selectin'
        self.factors = numpy.zeros((max(ddids)+1, shape[0]))
        for ddid in ddids:
            fqobj                = _spwMap.unmap( ddid )
            self.factors[ ddid ] = _spwMap.frequenciesOfFREQ_SB(fqobj.FREQID, fqobj.SUBBAND)

        # After having read the data, first we apply the masking function
        # which disables the unselected channels
        if selection.chanSel:
            channels         = sorted(CP(selection.chanSel))
            indices          = map(lambda x: x-channels[0], channels)
            self.chanidx     = zip(indices, channels)
            self.chansel     = indices
            # select only the selected channels
            self.factors     = self.factors[:, channels]
            #print "channels=",channels," indices=",indices," self.chanidx=",self.chanidx
            self.maskfn      = mk3dmask_fn_mask(self.chunksize, indices, shape[-1])
            slicers[datacol] = ms2util.mk_slicer((channels[0],  0), (channels[-1]+1, shape[-1]))

        # right - factors now contain *frequency*
        # divide by speed of lite to get the multiplication factor
        # to go from UV distance in meters to UV dist in lambda
        self.factors /= 299792458.0
        # older numpy's have a numpy.linalg.norm() that does NOT take an 'axis' argument
        # so we have to write the distance computation out ourselves. #GVD
        self.uvdist_f = lambda uvw: numpy.sqrt( numpy.square(uvw[...,0]) + numpy.square(uvw[...,1]) )

        # If there is vector averaging to be done, this is done in the step after reading the data
        # (default: none)
        self.vectorAvg  = lambda x: x

        if avgChannel==AVG.Vector:
            self.vectorAvg = lambda x: numpy.average(x, axis=1).reshape( (x.shape[0], 1, x.shape[2]) )
            self.chanidx   = [(0, '*')]

        # Scalar averaging is done after the quantities have been computed
        self.scalarAvg  = lambda x: x

        if avgChannel==AVG.Scalar:
            self.scalarAvg = lambda x: numpy.average(x, axis=1).reshape( (x.shape[0], 1, x.shape[2]) )
            self.chanidx   = [(0, '*')]

        if avgChannel!=AVG.None:
            self.factors   = numpy.average(self.factors[:,self.chansel], axis=1)

        fields = [AX.TYPE, AX.BL, AX.FQ, AX.SB, AX.SRC, AX.P, AX.CH]

        # weight filtering
        self.nreject   = 0
        self.reject_f  = lambda weight: False
        self.threshold = -10000000
        if selection.weightThreshold is not None:
            self.threshold = CP(selection.weightThreshold)
            self.reject_f  = lambda weight: weight<self.threshold

        ## Now we can start the reduction of the table
        ## INCORPORATE THE WEIGHT COLUMN
        if selection.weightThreshold is None:
            columns        = ["ANTENNA1", "ANTENNA2", "UVW", "DATA_DESC_ID", "FIELD_ID", datacol]
            self.actual_fn = self.withoutWeightThresholding
        else:
            columns        = ["ANTENNA1", "ANTENNA2", "UVW", "DATA_DESC_ID", "FIELD_ID", "WEIGHT", datacol]
            self.actual_fn = self.withWeightThresholding
        if self.flags:
            columns.append( "FLAGCOL" )
        pts =  ms2util.reducems2(self, self.table, {}, columns, verbose=True, slicers=slicers, chunksize=self.chunksize)

        if self.nreject:
            print "Rejected ",self.nreject," points because of weight criterion"

        rv  = {}
        for (label, dataset) in pts.iteritems():
            rv[ self.MKLAB(fields, label) ] = dataset
        #for k in rv.keys():
        #    print "Plot:",str(k),"/",map(str, rv[k].keys())
        return rv

    ## Here we make the plots
    def __call__(self, *args):
        return self.actual_fn(*args)

    #### This is the version WITHOUT WEIGHT THRESHOLDING
    def withoutWeightThresholding(self, acc, a1, a2, uvw, dd, fld, data, *flag):
        #print "__call__: ",a1,a2,tm,dd,fld,data.shape
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape
        flg  = unflagged() if not flag else flag[0]
        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking + vector averaging
        #         'vamd' = vector averaged masked data
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])
        vamd = self.vectorAvg( mfn(d3d) )

        # Now create the quantity data - map the quantity functions over the
        # (potentially) vector averaged data and (potentially) scalar
        # average them
        qd   = map(lambda (qnm, qfn): (qnm, self.scalarAvg(qfn(vamd))), self.quantities)

        # we can compute the uv distances of all spectral points in units of lambda
        # because we have the UVW's now and the nu/speed-of-lite for all spectral points
        uvd  = numpy.atleast_2d( self.factors[dd].T * self.uvdist_f(uvw) )

        # Now we can loop over all the rows in the data

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(shp[0]):
            (fq, sb, plist) = self.ddSelection[ dd[row] ]
            for (chi, chn) in self.chanidx:
                for (pidx, pname) in plist:
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        acc.setdefault(tuple(l), dataset()).append(uvd[chi, row], qval[row, chi, pidx], flg[row, chi, pidx])
        return acc

    #### This is the version WITH WEIGHT THRESHOLDING
    def withWeightThresholding(self, acc, a1, a2, uvw, dd, fld, weight, data, *flag):
        #print "__call__: ",a1,a2,tm,dd,fld,data.shape
        # Make really sure we have a 3-D array of data ...
        d3d  = m3d(data)
        shp  = data.shape
        flg  = unflagged() if not flag else flag[0]
        # compute weight mask
        w3d  = numpy.zeros(shp, dtype=numpy.float)
        for i in xrange(shp[0]):
            # we have weights per polzarization but we must
            # expand them to per channel ...
            cw = numpy.vstack( shp[1]*[weight[i]] )
            w3d[i] = cw
        w3m =  w3d<self.threshold
        wfn = lambda a: numpy.ma.MaskedArray(a.data, numpy.logical_and(a.mask, w3m))
        # Good. We have a block of data, shape (nrow, nchan, npol)
        # Step 1: apply the masking + vector averaging
        #         'vamd' = vector averaged masked data
        #         Try to use the pre-computed channel mask, if it fits,
        #         otherwise create one for this odd-sized block
        #         (typically the last block)
        mfn  = self.maskfn if shp[0]==self.chunksize else mk3dmask_fn_mask(shp[0], self.chansel, shp[2])
        vamd = self.vectorAvg( wfn(mfn(d3d)) )

        # Now create the quantity data - map the quantity functions over the
        # (potentially) vector averaged data and (potentially) scalar
        # average them
        qd   = map(lambda (qnm, qfn): (qnm, self.scalarAvg(qfn(vamd))), self.quantities)

        # compute uv distances
        uvd  = self.uvdist_f(uvw)
        #for (qn, qv) in qd:
        #    print qn,": shape=",qv.shape

        # Now we can loop over all the rows in the data

        # We don't have to test *IF* the current data description id is 
        # selected; the fact that we see it here means that it WAS selected!
        # The only interesting bit is selecting the correct products
        for row in range(shp[0]):
            (fq, sb, plist) = self.ddSelection[ dd[row] ]
            for (chi, chn) in self.chanidx:
                for (pidx, pname) in plist:
                    if self.reject_f(w3d[row, chi, pidx]):
                        self.nreject = self.nreject + 1
                        continue
                    l = ["", (a1[row], a2[row]), fq, sb, fld[row], pname, chn]
                    for (qnm, qval) in qd:
                        l[0] = qnm
                        #pi       = self.plot_idx(l)
                        #di       = self.ds_idx(l)
                        #print "row #",row,"/l=",l," => pi=",pi," di=",di," qval.shape=",qval.shape
                        acc.setdefault(tuple(l), dataset()).append(tm[row], qval[row, chi, pidx], flag[row, chi, pidx])
        return acc

Iterators = {
    'amptime' : data_quantity_time([(YTypes.amplitude, numpy.abs)]),
    'phatime' : data_quantity_time([(YTypes.phase, lambda x: numpy.angle(x, True))]),
    'anptime' : data_quantity_time([(YTypes.amplitude, numpy.ma.abs), (YTypes.phase, lambda x: numpy.ma.angle(x, True))]),
    'retime'  : data_quantity_time([(YTypes.real, numpy.real)]),
    'imtime'  : data_quantity_time([(YTypes.imag, numpy.imag)]),
    'rnitime' : data_quantity_time([(YTypes.real, numpy.real), (YTypes.imag, numpy.imag)]),
    'ampchan' : data_quantity_chan([(YTypes.amplitude, numpy.abs)]),
    'ampfreq' : data_quantity_chan([(YTypes.amplitude, numpy.abs)], byFrequency=True),
    'phachan' : data_quantity_chan([(YTypes.phase, lambda x: numpy.angle(x, True))]),
    'phafreq' : data_quantity_chan([(YTypes.phase, lambda x: numpy.angle(x, True))], byFrequency=True),
    'anpchan' : data_quantity_chan([(YTypes.amplitude, numpy.abs), (YTypes.phase, lambda x: numpy.angle(x, True))]),
    'anpfreq' : data_quantity_chan([(YTypes.amplitude, numpy.abs), (YTypes.phase, lambda x: numpy.angle(x, True))], byFrequency=True),
    'rechan'  : data_quantity_chan([(YTypes.real, numpy.real)]),
    'imchan'  : data_quantity_chan([(YTypes.imag, numpy.imag)]),
    'rnichan' : data_quantity_chan([(YTypes.real, numpy.real), (YTypes.imag, numpy.imag)]),
    'wt'      : weight_time(),
    'uv'      : uv(),
    'ampuv'   : data_quantity_uvdist([(YTypes.amplitude, numpy.abs)])
        }
