import settings
from dashboard import Dashboard

class greeter(object):
    def __init__(self):
        self.unique_id = raw_input('Please enter the name of this dashboard: ')

    def main(self):
        print 'Please enter a mart.You have the following options: '
        for item in settings.MARTS:
            print item
        mart = raw_input('your choice: ')
        if mart in settings.MARTS :
            self.mart = __import__(mart)
            self.getmetric() # METRIC : travelamount/refundamount etc.
            self.getaggregation() # based on each metric, we can provide options to sum,count,min,max,avg etc
            self.gettimeseries() # which will be the time used as X-axis : bookingdate/traveldate etc.
            self.gettimerange() # timerange : list : [date/month/year,datevalue,edatevalue(if applicable)]
            self.getparams() # which are the dimensions against which filtering and grouping is required.
            return self.unique_id,self.mart.__name__,self.metricname,self.aggregation,self.timeseries,self.timerange,self.params
        else:
            print 'incorrect choice entered.'
            self.main()

    def getmetric(self):
        print 'Please enter a metric.You have the following options: '
        for item in self.mart.metrics.keys():
            print item
        metric = raw_input('your choice: ')
        if metric in self.mart.metrics.keys():
            self.metricname = metric
            self.metric = self.mart.metrics[metric]
        else:
            print "incorrect choice entered."
            self.getmetric()

    def getaggregation(self):
        print 'Please enter an aggregation logic.You have the following options: '
        for item in self.metric['aggregation_options']:
            print item
        aggregation = raw_input('your choice: ')
        if aggregation in self.metric['aggregation_options']:
            self.aggregation = aggregation
        else:
            print "incorrect choice entered."
            self.getaggregation()

    def gettimeseries(self):
        print "Please enter a time series to use.You have the following options: "
        for item in self.mart.timeseries:
            print item
        timeseries = raw_input('your choice: ')
        if timeseries in self.mart.timeseries:
            self.timeseries = timeseries
        else:
            print "incorrect choice entered."
            self.gettimeseries()

    def gettimerange(self):
        print "Please enter a time range type.You have the following options: "
        for item in settings.TIMERANGETYPE:
            print item
        timerangetype = raw_input('your choice: ')

        if timerangetype not in settings.TIMERANGETYPE:
            print "incorrect choice entered."
            self.gettimerange()

        if timerangetype == "date":
            sdate = raw_input("please enter start date in YYYY-MM-DD format: ")
            edate = raw_input("please enter end date in YYYY-MM-DD format: ")
        if timerangetype == "month":
            sdate = raw_input("please enter start month in YYYY-MM-DD format: ")
            edate = raw_input("please enter end month in YYYY-MM-DD format: ")
        if timerangetype == "year":
            sdate = raw_input("please enter start month in YYYY-MM-DD format: ")
            edate = raw_input("please enter end month in YYYY-MM-DD format: ")

        self.timerange = (timerangetype,sdate,edate)

    def getparams(self):
        print "please enter the dimensions you want.You have the following options: "
        for item in self.mart.dimensions.keys():
            print item
        self.params = self.mart.dimensions.keys()

#mygreeter = greeter()
#unique_id,mart,metric,aggregation,timeseries,timerange,params = mygreeter.main()
unique_id,mart,metric,aggregation,timeseries,timerange,params = 'Abhishek','flight_paymentdetails','Gross Margin','SUM','bookingdate',('date','2012-05-14','2012-05-14'),['airline','source','destination','sector','city','status','bookingflag','typeoftravel']
mydashboard = Dashboard(unique_id,mart,metric,aggregation,timeseries,timerange,params)
def ask():
    choice = raw_input("Press 0 to continue and 1 to exit : ")
    if choice == '1' :
        mydashboard.exit()
    else : 
        mydashboard.interact()
        ask()
mydashboard.process()
mydashboard.render()
ask()

