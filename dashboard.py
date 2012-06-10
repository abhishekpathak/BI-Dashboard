import sys
import pymongo
import re
import dashboard_settings
from bson.son import SON
import datetime
import pprint
import pdb

class Dashboard(object):
    def __init__(self,unique_id, mart, metric, aggregation, timeseries, timerange,dimensions):
        self.conn = pymongo.Connection(dashboard_settings.MONGO_HOST,dashboard_settings.MONGO_PORT)
        self.db = self.conn[dashboard_settings.MART_DATABASE]
        self.unique_id = unique_id
        self.mart = __import__("marts."+mart,globals(), locals(), [mart], -1)
        self.metric = self.mart.metrics[metric]
        self.aggregation = aggregation
        self.timeseries = timeseries
        self.timerange = timerange
        self.filter = self.gettimefilter()
        if self.metric.has_key('extra filters'):
            self.apply_extra_filters()
        self.dimensions = dimensions
        self.flag = 0

    def updatefilter(self):
        filter = raw_input('please enter the filter to be used: for example airline,indigo or REMOVE,airline :')
        filter = filter.split(',')
        try:
            filter[1] = int(filter[1]) # if filter contains a number,convert it to an int from string
        except (IndexError,ValueError):
            pass
        if filter[0] == 'REMOVE': # remove an existing filter from the filters
            del self.filter['_id.'+filter[1]]
        else : # update filters to add new filter as well
            self.filter['_id.'+filter[0]] = filter[1]

    def gettimefilter(self):
        timefilter = {
            'date' :{self.timeseries : { '$gte' : self.timerange[1], '$lte': self.timerange[2]}},
            'month' :{self.timeseries : { '$gte' : self.timerange[1], '$lte':self.timerange[2]}},
            'year' :{self.timeseries : { '$gte' : self.timerange[1], '$lte': self.timerange[2]}},
            }
        return timefilter[self.timerange[0]]

    def apply_extra_filters(self):
        for k,v in self.metric['extra filters'].iteritems():
            self.filter[k] = v

    def process(self):
        if self.flag == 0:
            self.parentcollection = getattr(self.db,self.mart.__name__.split('.')[-1])
            self.childcollectionname = 'dashboard_'+str(self.unique_id)
            self.childcollection = getattr(self.conn['dashboard'],self.childcollectionname)
            t1 = datetime.datetime.now()
            self.map_reduce()
            #print str(datetime.datetime.now() - t1)
            self.filter = {}
            self.flag = 1 
        else:
            self.parentcollection = getattr(self.conn['dashboard'],'dashboard_'+str(self.unique_id))
            self.childcollectionname = 'dashboard_'+str(self.unique_id)+'_derived'
            self.childcollection = getattr(self.conn['dashboard'],self.childcollectionname)
            self.map_reduce()

        # check for results having NaN values and remove them
        self.childcollection.remove({'value': float('nan')})

    def render(self):
        self.draw_graph()
        dict = self.summarize()
        pprint.pprint(dict)
        return dict

    def interact(self):
        self.updatefilter()
        self.process()
        self.render()

    def map_reduce(self):
         # construct mapper
        mapper = self.getmapper()
        #print mapper
        # choose reducer
        import standard_reducers
        reducer = getattr(standard_reducers,self.aggregation)
        #print reducer
        #print str(self.filter)
        # do mapreduce
        self.parentcollection.map_reduce(mapper,reducer,out=SON([("replace", self.childcollectionname),("db", "dashboard")]),query = self.filter)

    def getmapper(self):

        keydict = "{"

        if self.flag == 0 :

            for item in self.dimensions:
                keydict += '"'+item+'" : this.'+self.mart.dimensions[item]+','
            value = self.metric['real_name']
            # changing all (dimensionname) to (this.dimensionname) 
            if value[0].isdigit(): 
                pass
            else:
                value = 'this.'+value
            value = re.sub('\-(?=[a-z])','-this.',value)
            value = re.sub('\+(?=[a-z])','+this.',value)
            value = re.sub('\*(?=[a-z])','*this.',value)
            value = re.sub('\/(?=[a-z])','/this.',value)
            #print value
            
            timeseries = str(self.timeseries)

        else: # self.flag = 1 :

            for item in self.dimensions:
                keydict += '"'+item+'" : this._id.'+item+','
            value = 'this.value'
            timeseries = "_id"

        if self.timerange[0] == 'year':
            keydict +=  '"year" : this.'+timeseries+'.year,"month" : this.'+timeseries+'.month,'
        if self.timerange[0] == 'month':
            keydict +=  '"year" : this.'+timeseries+'.year,"month" : this.'+timeseries+'.month,"day" : this.'+timeseries+'.day,'
        if self.timerange[0] == 'day' :
            keydict += '"year" : this.'+timeseries+'.year,"month" : this.'+timeseries+'.month,"day" : this.'+timeseries+'.day,'
        
        keydict += "}" 

        #Override value emitted during map to 1 for COUNT aggregation
        if self.aggregation == 'COUNT':
            mapper = "function map() {emit("+keydict+",1);}"
        else:
            mapper = "function map() {emit("+keydict+","+value+");}"

        return mapper

    def draw_graph(self):
        #childcollection would be used here.
        pass

    def summarize(self):
        dictionary = {}
        for item in self.dimensions:
            dictionary[item] = {}
            # calculating the aggregate based on this key
            results = self.childcollection.group(['_id.'+item],None,{'sum':0},'function(obj, prev) {prev.sum += obj.value}')
            # printing the top 5 values from results
            for element in sorted(results,key=lambda item:item['sum'],reverse=True)[:5]:
                dictionary[item][element['_id.'+item]] = element['sum']
        return dictionary

    def exit(self):
        if self.parentcollection == getattr(self.conn['dashboard'],'dashboard_'+str(self.unique_id)): # drop the
            self.parentcollection.drop() # user-created
        self.childcollection.drop() # tables

