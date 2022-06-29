from aiohttp import ClientSession
from app.ladders.local_wiki_ladder_finder import LocalWikiLadderFinder
from flask import redirect, render_template, url_for, request
from app.utils import parse_requirements, get_random_article
from duckduckgo_search import ddg_images
from app import app


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
        for step in ladder:
            image = ddg_images(step, region='wt-wt', safesearch='On', max_results=1, size="Large", layout="Wide")[0]
            description = await ladder_finder._get_description(step)
            infos[step] = (image["image"], description, "active" if step == starting_article else "")
        return render_template("ladder.html.jinja", infos=infos)
