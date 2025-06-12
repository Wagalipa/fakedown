#!/usr/bin/python3

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import flask
from flask import request, jsonify, make_response
import random
from MarkovJekyll import MarkdownGenerator

markdownGenerator = MarkdownGenerator("word_cache.json")


def make_text(txt):
    response = make_response(txt, 200)
    response.mimetype = "text/plain"
    return response


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index():
    return "<h1>What? Me, worry?</h1>"


@app.route("/words", methods=["GET"])
def home():
    return make_text(markdownGenerator.markov.generate_markov_text(4))


@app.route("/phrase", methods=["GET"])
def phrase():
    return make_text(markdownGenerator.markov.generate_markov_text(25))


@app.route("/paragraph", methods=["GET"])
def paragraph():
    return make_text(markdownGenerator.markov.generate_markov_para(1))


@app.route("/paragraphs", methods=["GET"])
def paragraphs():
    return make_text(markdownGenerator.markov.generate_markov_para(5))


@app.route("/markdown", methods=["GET"])
def markdown():
    return make_text(markdownGenerator.get_markdown())


@app.route("/eleventy-post", methods=["GET"])
@app.route("/markdown-post", methods=["GET"])
def eleventy_post():
    (coso, slug) = markdownGenerator.get_doc()
    return make_text(coso)


# app.run(host='0.0.0.0', port=5201)
