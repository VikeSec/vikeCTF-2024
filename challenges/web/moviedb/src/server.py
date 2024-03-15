from dataclasses import dataclass
import traceback
from flask import Flask, request, render_template_string, Response
import sqlite3
import os

app = Flask(__name__)

index = open("index.html").read()


@dataclass
class Movie:
    title: str
    year: int | None
    runtimeMinutes: int | None
    genres: str | None
    averageRatings: float
    votes: int

    def genresList(self):
        if self.genres:
            return self.genres.split(",")


@app.route("/")
def home():
    try:
        search = request.args.get("search")
        if search is None:
            return render_template_string(index)

        # movie data is from IMDB, thanks! some preprocessing required
        # https://developer.imdb.com/non-commercial-datasets/
        cur = sqlite3.connect("movies.sqlite3").cursor()

        pred = ["WHERE primaryTitle LIKE '%' || ? || '%'"]
        params = [search]

        if min_rating := request.args.get("min-rating"):
            pred.append("averageRating >= ?")
            params.append(float(min_rating))

        if max_rating := request.args.get("max-rating"):
            pred.append("averageRating <= ?")
            params.append(float(max_rating))

        if min_year := request.args.get("min-year"):
            pred.append("startYear >= ?")
            params.append(int(min_year))

        if max_year := request.args.get("max-year"):
            pred.append("startYear <= ?")
            params.append(int(max_year))

        if min_mins := request.args.get("min-mins"):
            pred.append("runtimeMinutes >= ?")
            params.append(int(min_mins))

        if max_mins := request.args.get("max-mins"):
            pred.append("runtimeMinutes <= ?")
            params.append(int(max_mins))

        if min_votes := request.args.get("min-votes"):
            pred.append("numVotes >= ?")
            params.append(int(min_votes))

        if max_votes := request.args.get("max-votes"):
            pred.append("numVotes <= ?")
            params.append(int(max_votes))

        query = ["SELECT * FROM movies"]
        query.append(" AND ".join(pred))
        query.append("LIMIT 100")

        res = cur.execute(" ".join(query), params)
        results = list(map(lambda t: Movie(*t), res.fetchall()))
        return render_template_string(index, results=results, search=search)
    except Exception:
        error_msg = traceback.format_exc()
        print(error_msg)
        return render_template_string(
            """
            <h1>Something went wrong!</h1>
            <pre>{error}</pre>
            """.format(error=error_msg)
        )


@app.route("/robots.txt")
def robots():
    r = Response("/static/flag.txt")
    r.headers["Content-Type"] = "text/plain"
    return r


@app.route("/static")
def static_folder():
    return "<br/>".join(os.listdir("static"))


@app.route("/static/flag.txt")
def flag():
    return "no"

if __name__ != '__main__':
    import logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__": 
    app.run(host="0.0.0.0")
