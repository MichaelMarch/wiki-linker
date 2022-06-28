from app import app
from app.utils import parse_requirements
from flask import redirect, render_template, url_for, request


@app.route("/")
def index():
    return render_template("index.html.jinja", packages=parse_requirements())


@app.route("/find_ladder/", methods=["GET", "POST"])
def find_ladder():
    starting_article = request.args.get(
        "_starting_article", default="") or request.form.get("_starting_article", default="")
    ending_article = request.args.get("_ending_article", default="") or request.form.get("_ending_article", default="")

    if request.method == "GET":
        random = request.args.get("random", default=None)
        if random == '1':
            starting_article = "BCA"
        if random == '2':
            ending_article = "RET"

        return render_template("find_ladder.html.jinja", starting_article=starting_article, ending_article=ending_article, random=random)

    # POST
    if not starting_article or not ending_article:
        message = "Please enter the {article} article or click the button next to it to get a random one"

        message1 = message.format(article="starting") if not starting_article else None
        message2 = message.format(article="ending") if not ending_article else None

        return render_template("find_ladder.html.jinja", starting_article=starting_article, ending_article=ending_article, messages=(message1, message2))
    return redirect(url_for("ladder", starting_article=starting_article, ending_article=ending_article))


@app.route("/found_ladders/")
def found_ladders():
    return render_template("found_ladders.html.jinja")


@app.route("/about_me/")
def about_me():
    return render_template("about_me.html.jinja")


@app.route("/ladder/<starting_article>/<ending_article>")
def ladder(starting_article, ending_article):
    return render_template("ladder.html.jinja", starting_article=starting_article, ending_article=ending_article)
