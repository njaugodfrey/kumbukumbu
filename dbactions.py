from datetime import datetime
import json
import os
import time
import bson
from bson.json_util import dumps
from bson.objectid import ObjectId
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

# load .env
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# assign database
client = MongoClient(MONGODB_URI)

def create_table_items(
    db_name, table_name,
    date_and_time, action_name, status
    ):
    # date_and_time, action_name, status
    db = client[db_name]
    table_name = db[table_name]
    '''table_name.insert_one(
        {
            'name': 'Cash cheque',
            'time': datetime(2021, 6, 6, 9, 15, 0),
            'done': 'no'
        }
    )'''
    # convert date string to time
    date_and_time = datetime.strptime(date_and_time, "%Y/%m/%d %H:%M")

    table_name.insert_one(
        {
            'name': action_name,
            'time': date_and_time,
            'done': status
        }
    )

def db_todo_list(db_name, table_name):
    db = client[db_name]
    table_name = db[table_name]
    # get todo list from database
    db_things_to_do = json.loads(dumps(table_name.find()))
    list_of_things = []
    
    # create a readable list of the items
    for thing in db_things_to_do:
        list_of_things.append(
            dict(
                [
                    ('id', thing['_id']['$oid']),
                    ('action', thing['name']),
                    ('date', time.strftime(
                        '%Y-%m-%d', time.localtime(thing['time']['$date']/1000)
                    )),
                    ('status', thing['done']),
                ]
            )
        )
    #print(list_of_things)
    return list_of_things

def change_todo_item(
    db_name, table_name,
    item_id
    ):
    db = client[db_name]
    table_name = db[table_name]
    # clean item_id
    item_id = str(item_id)[2:26]

    # change the item
    the_item = json.loads(dumps(table_name.find_one({'_id': ObjectId(item_id)})))
    if the_item['done'] == 'False':
        table_name.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {'done': 'True'}}
        )
    else:
        table_name.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {'done': 'False'}}
        )
    
    changed_item = json.loads(dumps(table_name.find_one({'_id': ObjectId(item_id)})))
    response_item = dict(
        [
            ('id', changed_item['_id']['$oid']),
            ('action', changed_item['name']),
            ('date', time.strftime(
                '%Y-%m-%d', time.localtime(changed_item['time']['$date']/1000)
            )),
            ('status', changed_item['done']),
        ]
    )
    return response_item

if __name__ == '__main__':
    db_todo_list(db_name='tasks', table_name='todo')
    