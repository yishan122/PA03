#! /opt/miniconda3/bin/python3
'''
Finance Tracker
'''

import sys
from transaction import Transaction


# here are some helper functions ...

def print_usage():
    ''' print an explanation of how to use this command '''
    print('''usage:
        quit
        show transaction
        add transaction
        delete transaction
        summarize transaction by date
        summarize transaction by month
        summarize transaction by year
        summarize transaction by category
        print this menu
        '''
        )

def print_transactions(transactions, summarize_by=None):
    ''' print the transaction items '''
    if len(transactions)==0:
        print('no transactions to print')
        return
    print('\n')
    if len(transactions[0]) == 6:
        print(f"{'id':<10} {'item #':<10} {'amount':<10}\
              {'category':<20} {'date':<10} {'description':<10}")
    else :
        print(f"{'item #':<10} {summarize_by:<10} {'amount':<10}")
    print('-'*100)
    for item in transactions:
        values = tuple(item.values())
        if len(values) == 6:
            print(f"{values[0]:<10} {values[1]:<10} {values[2]:<10}\
                  {values[3]:<10} {values[4]:<10} {values[5]:<10}")
        else:
            print(f"{values[0]:<10} {values[1]:<10} {values[2]:<20}")

def process_args(arglist):
    ''' examine args and make appropriate calls to transaction'''
    transaction = Transaction('tracker.db')
    if arglist==[] or arglist[0] == "print":
        print_usage()
    elif arglist[0] == "quit":
        sys.exit()
    elif arglist[0]=="show":
        print_transactions(transaction.select_all())
    elif arglist[0]=="summarize":
        if len(arglist) == 4:
            print_transactions(transaction.summarize(arglist[-1]), arglist[-1])
    elif arglist[0]=='add':
        if len(arglist) != 3:
            print_usage()
        else:
            new_data = arglist[2].split(',')
            transaction.add({
                'id': new_data[0], 
                'item #': new_data[1], 
                'amount': new_data[2], 
                'category': new_data[3], 
                'date': new_data[4], 
                'description': new_data[5]})
    elif arglist[0]=='delete':
        if len(arglist)!= 3:
            print_usage()
        else:
            transaction.delete(arglist[2])
    else:
        print(arglist,"is not implemented")
        print_usage()

def toplevel():
    ''' read the command args and process them'''
    if len(sys.argv)==1:
        # they didn't pass any arguments,
        # so prompt for them in a loop
        print_usage()
        args = []
        while args!=['']:
            args = input("command> ").split(' ')
            if args[0]=='add':
                # join everyting after the name as a string
                args = ['add',args[1]," ".join(args[2:])]
            process_args(args)
            print('-'*100+'\n'*3)
    else:
        # read the args and process them
        args = sys.argv[1:]
        process_args(args)
        print('-'*100+'\n'*3)

toplevel()
