metrics = {
    'GMV'  : {
        'real_name' : 'ticketfare',
        'aggregation_options' : ['SUM','COUNT'],
        'extra filters' : {'status' : {'$ne':'new'},'status' : {'$ne' : 'aborted'}}
        },
    'tickets' : {
        'real_name' : 'Seats',
        'aggregation_options' : ['SUM'],
        'extra filters' : {'status' : {'$ne':'new'},'status' : {'$ne' : 'aborted'}}
        },
    'Gross Margin' : {
        'real_name' : '0.06*ticketfare',
        'aggregation_options' : ['SUM','COUNT'],
        'extra filters' : {'status' : {'$ne':'new'},'status' : {'$ne' : 'aborted'}}
        },        
    'Promocode' : {
        'real_name' : 'Promocode',
        'aggregation_options' : ['SUM'],
        'extra filters' : {'status' : {'$ne':'new'},'status' : {'$ne' : 'aborted'}}
        }
    }

dimensions = {
'total' : 'total',
'source' : 'src',
'destination' : 'dest',
'status' : 'transactiontype',
}


timeseries = ['dateoftransaction']
