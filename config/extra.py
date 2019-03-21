from datetime import *
from config import app
from flask import request
import os

def is_item_new(created_at):
	time_now = datetime.now()
	duration = time_now - created_at
	print(str(created_at))
	to_hours = round(duration.total_seconds()/3600)
	if to_hours < 72:
		return True
	else:
		return False
		
def get_first_image(images):
    content = images.split(';')
    return content[0]
	
def count_new_price(item, discount):
	return str(round(item*(100-discount)/100))
	
def get_images_array(images):
	return images.split(';')
	
def str_contains(str):
	rule = request.url_rule
	if str in rule.rule:
		return True
	else:
		return False

def getlen(str):
	return len(str)
	
def get_countries():
	path = os.path.abspath(os.path.dirname(__file__)) + '/static/countries.txt'
	f = open(path, "r")
	return f.read().split('\n')

app.jinja_env.globals.update(is_item_new=is_item_new)
app.jinja_env.globals.update(get_first_image=get_first_image)
app.jinja_env.globals.update(count_new_price=count_new_price)
app.jinja_env.globals.update(get_images_array=get_images_array)
app.jinja_env.globals.update(str_contains=str_contains)
app.jinja_env.globals.update(getlen=getlen)
app.jinja_env.globals.update(get_countries=get_countries)
