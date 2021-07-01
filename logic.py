import os
import datetime
import json
import pprint
from re import I, S
from bson.json_util import default
from bson.objectid import ObjectId
from pymongo import client_options
#from typing_extensions import Required

from tornado import ioloop, web
from tornado.escape import json_decode

from wtforms import validators
from wtforms.fields import TextField
from wtforms.fields.core import BooleanField, DateTimeField
from wtforms.validators import DataRequired
from wtforms_tornado import Form

import dbactions

class MainHandler(web.RequestHandler):
    def get(self):
        title = ['My Todo app']

        self.render(
            template_name='./templates/index.html',
            title='The App', items=title
        )


class TodoForm(Form):
    action = TextField(validators=[DataRequired()])
    date_field = TextField(validators=[DataRequired()])
    status = BooleanField()


class Todos(web.RequestHandler):
        
    def get(self):
        form = TodoForm()
        todo_items = dbactions.db_todo_list(
                        db_name='tasks', table_name='todo'
                    )
        
        self.render(
            template_name='./templates/todolist.html',
            title='Todos', items=todo_items, form=form
        )


class TodoFormHandler(web.RequestHandler):
    # handle form data
    def post(self):
        form = TodoForm(self.request.arguments)
        print(form.data)

        if form.validate():
            dbactions.create_table_items(
                db_name='tasks', table_name='todo',
                date_and_time=form.data['date_field'],
                action_name=form.data['action'],
                status=str(form.data['status'])
            )
            """ self.write(
                str(form.data['action']) +\
                     str(datetime.datetime.strptime(form.data['date_field'], "%Y/%m/%d %H:%M")) +\
                          str(form.data['status'])
            ) """
            self.redirect(r'/todo_list') 
        else:
            self.set_status(400)
            self.write(form.errors)


class StatusUpdater(web.RequestHandler):
    def post(self):
        data = self.request.body
        activity_id = str(data)[2:26]
        print(str(data)[2:26])

        client = dbactions.client
        db = client['tasks']
        table = db['todo']
        result = table.find_one({'_id': ObjectId(activity_id)})
        updated_result = table.update_one(
            {'_id': ObjectId(activity_id)},
            {'$set': {'done': 'False'}}
        )
        table.up
        print(result)
        print(table.find_one({'_id': ObjectId(activity_id)}))



settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'cookie_secret': 'gsN,1=HQ9uu9g?e#Dg-JAb5?*@sdw%0$8DoA3GMT!GLP_eJWeS{J_8-c2r=^4V>',
    'xsrf_cookies': True,
    'login_url': '/login',
}

def make_app():
    return web.Application(
        [
            (r'/', MainHandler),
            (r'/todo_list', Todos),
            (r'/todo_form', TodoFormHandler),
            (r'/update_status', StatusUpdater),
        ], **settings
    )

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()