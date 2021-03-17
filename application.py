from flask import Flask, request, render_template, abort
from flask_pymongo import PyMongo
from story_insert import mongo, StoryInsert
from pagination import Pagination

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
mongo.init_app(app)

PER_PAGE = 1


@app.route('/')
def home_page():
    page = request.args.get("page", type=int, default=1)
    story_list = mongo.db.hindi.find()\
        .sort("story_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    total_story = story_list.count()
    if not total_story:
        abort(404)

    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)
    return render_template('home_page.html', records=story_list, pagination=pagination)


@app.route('/category/<category>/')
@app.route('/category/<category>')
def category_page(category):
    page = request.args.get("page", type=int, default=1)
    story_list = mongo.db.hindi.find({"tags.url": category}) \
        .sort("story_id", -1) \
        .skip(PER_PAGE * (page - 1)) \
        .limit(PER_PAGE)

    total_story = story_list.count()
    if not total_story:
        abort(404)

    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)
    return render_template('home_page.html', records=story_list, pagination=pagination)


@app.route('/story/<title>/')
@app.route('/story/<title>')
def story_page(title=None):
    return render_template('test.html')


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title='404'), 404


@app.cli.command('story_update')
def story_update():
    path = app.config.get("IMPORT_PATH")
    si = StoryInsert(path)
    si.trigger_import()




