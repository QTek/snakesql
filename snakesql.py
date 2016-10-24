#!/usr/bin/env python
import argparse
import os
import sys
import pypyodbc
import json


version = '2.0'

def get_mod_filter(arg_filter):
    filtertype = ''
    field_name = ''
    field_data = ''

    if len(arg_filter.split("=")) == 2:
        filtertype = 'eq'
        field_name = arg_filter.split("=")[0]
        field_data = arg_filter.split("=")[1]
    elif len(arg_filter.split("~")) == 2:
        filtertype = 'like'
        field_name = arg_filter.split("~")[0]
        field_data = arg_filter.split("~")[1]

    if filtertype == 'eq':
        return "WHERE " + field_name + " = '" + field_data + "'"
    if filtertype == 'like':
        return "WHERE " + field_name + " LIKE '" + field_data + "'"
    return ''

def get_mod_top(arg_top):
    if arg_top == '':
        return ''
    else:
        return 'TOP ' + arg_top

def get_mod_columns(arg_columns):
    if not arg_columns == '':
        return arg_columns

def find_query(queryid):
    path = "queries/"
    plugins = {}
    sys.path.insert(0, path)
    for f in os.listdir(path):
        err = 0
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            try:
                mod = __import__(fname)
                plugins[fname] = mod.SnakeQuery()
                if plugins[fname].plugin_check(queryid) == True:
                    sys.path.pop(0)
                    return plugins[fname]
            except:
                err += 1
    sys.path.pop(0)
    print("No such query was found.")

def list_query():
    path = "queries/"
    plugins = {}
    sys.path.insert(0, path)
    print("[ ID ]: saved query name")
    print("-----------------------------------------")
    for f in os.listdir(path):
        err = 0
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            try:
                mod = __import__(fname)
                plugins[fname] = mod.SnakeQuery()
                if not plugins[fname].get_queryid() == '0':
                    print('[{0:2}]: {1}'.format(plugins[fname].get_queryid(), fname))
            except:
                err += 1
    sys.path.pop(0)

def run_query(conn_str, sql_query):
    connection = pypyodbc.connect(conn_str)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    output = list()
    for item in results:
        output += item
    connection.close()
    return output

def validate_variable_type(input_data):
    if str(input_data.__class__) == "<type \'str\'>":
        return  input_data.strip().encode('utf-8','replace')
    elif str(input_data.__class__) == "<type \'unicode\'>":
        return input_data.strip()
    elif str(input_data.__class__) == "<type \'int\'>":
        return int(input_data)
    elif str(input_data.__class__) == "<type \'float\'>":
        return float(input_data)
    elif str(input_data.__class__) == "<type \'long\'>":
        return long(input_data)
    elif str(input_data.__class__) == "<type \'bool\'>":
        return bool(input_data)
    elif str(input_data.__class__) == "<type \'datetime.datetime\'>":
        return str(input_data)
    elif str(input_data.__class__) == "<type \'NoneType\'>":
        return None
    elif str(input_data.__class__) == "<type \'bytearray\'>":
        return str(input_data).encode('base64').strip()
    else:
        #print ("ERROR_IN_SNAKESQL:" + input_data.__class__)
        return None

#  Collect proper command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', required=False, default='0')
parser.add_argument('-c', '--columns', required=False, default='')
parser.add_argument('-f', '--filter', required=False, default='')
parser.add_argument('-t', '--top', required=False, default='')
parser.add_argument('-i', '--info', required=False, action='store_true')
parser.add_argument('-l', '--list', required=False, action='store_true')
parser.add_argument('-w', '--write', required=False, action='store_true')
parser.add_argument('-7', '--debug', required=False, action='store_true')
cli_args = parser.parse_args()

# Parse out command line arguments
query_id = cli_args.query
query_cols = get_mod_columns(cli_args.columns)
query_fils = get_mod_filter(cli_args.filter)
query_tops = get_mod_top(cli_args.top)
query_info = cli_args.info
query_write = cli_args.write
query_debug =cli_args.debug


query = find_query(query_id)

query.plugin_load(query_cols, query_fils, query_tops)
connection_string = query.get_conn_string()
sql_query_string = query.get_query_string()

if query_info:
    query.info()
    exit(0)

if cli_args.list:
    list_query()
    exit(0)


if query_debug:
    print(query.get_filename())
    exit(0)

result = run_query(connection_string, sql_query_string)
column_result = len(result)
column_count = len(query.get_columns())
column_cycles_complete = 0
x_true = 0
output_results = list()
output_filename = "output/" + query.get_filename()

result_dict = dict()
while x_true < (len(result) - 1):
    sqlrow_dict = dict()
    for x in range(0,column_count,1):
        x_true = x + (column_cycles_complete * column_count)
        if x_true >= column_result:
            sys.exit(0)
        try:
            sqlrow_dict[query.get_columns()[x]] = validate_variable_type(result[x_true])
        except:
            try:
                print("ERROR_IN_SNAKESQL: " + str(result[x_true].__class__) + " with value " + result[x_true])
            except:
                print("ERROR_IN_SNAKESQL: " + str(result[x_true].__class__)) #+ " with value " + result[x_true])
            sqlrow_dict[query.get_columns()[x]] = None
    output_line = json.dumps(sqlrow_dict)
    if query_write:
        f = open(output_filename + ".json",'a')
        f.write(output_line + '\n')
        f.close()
    else:
        print(output_line)
    column_cycles_complete = column_cycles_complete + 1

