from app.ladders.local_wiki_ladder_finder import LocalWikiLadderFinder
from flask import redirect, render_template, url_for, request
from app.utils import parse_requirements, get_random_article
from duckduckgo_search import ddg_images
from aiohttp import ClientSession
from app import app

import mysql.connector
from mysql.connector import errorcode


@app.route("/")
def index():
    return render_template("index.html.jinja", packages=parse_requirements())


@app.route("/find_ladder/", methods=["GET", "POST"])
def find_ladder():
    starting_article = request.args.get(
        "starting_article", default="") or request.form.get("starting_article", default="")
    ending_article = request.args.get("ending_article", default="") or request.form.get("ending_article", default="")
    first_time = request.args.get("first_time", default=None)

    if request.method == "GET":
        random = request.args.get("random", default=None)
        if random:
            if random == '1':
                starting_article = get_random_article()
            if random == '2':
                ending_article = get_random_article()

            return redirect(url_for("find_ladder", starting_article=starting_article, ending_article=ending_article))
        return render_template("find_ladder.html.jinja", starting_article=starting_article, ending_article=ending_article)

    # POST
    if not starting_article or not ending_article:
        message = "Please enter the {article} article or click the button next to it to get a random one"

        message1 = message.format(article="starting") if not starting_article and not first_time else None
        message2 = message.format(article="ending") if not ending_article and not first_time else None

        return render_template("find_ladder.html.jinja", starting_article=starting_article, ending_article=ending_article, messages=(message1, message2))

    return redirect(url_for("ladder", starting_article=starting_article, ending_article=ending_article))


@app.route("/found_ladders/")
def found_ladders():
    try:
        cnx = mysql.connector.connect(host='192.168.100.163', user='flask',
                                      database='flask_web', password="very_secure_password")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        query = ("SELECT * FROM test")
        cursor.execute(query)
        for (index) in cursor:
            print(index)
        
        cursor.close()
        cnx.close()
    return render_template("found_ladders.html.jinja")


@app.route("/about_me/")
def about_me():
    return render_template("about_me.html.jinja")


@app.route("/ladder/<starting_article>/<ending_article>")
async def ladder(starting_article, ending_article):
    async with ClientSession() as session:
        ladder_finder = LocalWikiLadderFinder(session, 100)

        infos = dict[str, tuple[str, str, str]]()

        ladder = await ladder_finder.find(starting_article, ending_article)
        if len(ladder) == 1:
            return render_template("find_ladder.html.jinja", starting_article=starting_article, ending_article=ending_article, messages=(ladder[0], ))

        for step in ladder:
            for image in ddg_images(step, region='wt-wt', safesearch='On', max_results=20, size="Medium", layout="Wide"):
                if image['image'][:5] == "https":
                    description = await ladder_finder._get_description(step)
                    infos[step] = (image["image"], description, "active" if step == starting_article else "")
                    break

        return render_template("ladder.html.jinja", infos=infos)
