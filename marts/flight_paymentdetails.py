metrics = {
    'GMV'  : {
        'real_name' : 'totalfarebeforediscount',
        'aggregation_options' : ['SUM','COUNT'],
        'extra filters' : {'bookingflag' : 'True','status' : {'$ne':'new'},'status' : {'$ne' : 'not ticketed'}},
        },
    'tickets' : {
        'real_name' : 'ticketscount',
        'aggregation_options' : ['SUM'],
        'extra filters' : {'bookingflag' : 'True','status' : {'$ne':'new'},'status' : {'$ne' : 'not ticketed'},'Error' : { '$exists' : False}},
        },
    'Gross Margin' : {
        'real_name' : 'totalcommission-promocodediscount-extradiscount+transactionfee-discount+leadamount+cybercafecommission',
        'aggregation_options' : ['SUM','COUNT'],
        'extra filters' : {'bookingflag' : 'True','status' : {'$ne':'new'},'status' : {'$ne' : 'not ticketed'}},
        },        
    'Promocode' : {
        'real_name' : '0-promocodediscount-extradiscount',
        'aggregation_options' : ['SUM'],
        'extra filters' : {'bookingflag' : 'True','status' : {'$ne':'new'},'status' : {'$ne' : 'not ticketed'}},
        }
    }


dimensions = {
'total' : 'total',
'airline' : 'airline',
'source' : 'src',
'destination' : 'dest',
'sector' : 'sector',
'city' : 'city',
'status' : 'status',
'bookingflag' : 'bookingflag',
'typeoftravel' : 'typeoftravel'
}


timeseries = ['bookingdate','traveldate']
