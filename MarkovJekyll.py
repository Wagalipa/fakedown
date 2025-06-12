import sys
import random
import string
import json

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

CODE = """

~~~
for {0} in {1}:
	c = make_collection("{2}")
	c.append(get_gizmo("{4}"))
	yield ("{3}",c)
~~~

"""

validFilenameChars = "_%s%s" % (string.ascii_letters, string.digits)


def removeDisallowedFilenameChars(filename):
    cleanedFilename = filename.replace(" ", "_")
    return "".join(c for c in cleanedFilename if c in validFilenameChars)


def safeprint(s):
    try:
        print(s)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode("utf8").decode(sys.stdout.encoding))
        else:
            print(s.encode("utf8"))


class Markov(object):

    def __init__(self, open_file, isJson=False):
        self.cache = {}
        self.isJson = isJson
        self.open_file = open_file
        if self.isJson:
            print("Reading from json")
            self.database_from_json()
        else:
            print("Parsing corpus")
            self.words = self.file_to_words()
            self.word_size = len(self.words)
            self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words

    def triples(self):
        """Generates triples from the given data string. So if our string were
        "What a lovely day", we'd generate (What, a, lovely) and then
        (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 3):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database_from_json(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        jsonData = json.loads(data)
        print("Json data loaded -- ", len(jsonData))
        self.cache = {}
        for d in jsonData:
            self.cache[(d["c1"], d["c2"])] = d["words"]
        self.keys = list(self.cache.keys())
        self.word_size = len(self.cache)

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1.lower(), w2.lower())
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]
        self.keys = list(self.cache.keys())
        self.word_size = len(self.keys)
        self.serialize_database()

    def serialize_database(self):
        ser = []
        for c in self.cache.keys():
            (c1, c2) = c
            words = self.cache[c]
            ser.append({"c1": c1, "c2": c2, "words": words})
        jsonData = json.dumps(ser)
        with open("./word_cache.json", "w", encoding="utf-8") as cache:
            cache.write(jsonData)

    def generate_markov_text(self, size=25, fullstop=True):
        seed = random.randint(1, self.word_size)
        (sw1, sw2) = self.keys[seed]

        w1, w2 = sw1, sw2
        gen_words = []
        cur_size = 0
        for i in range(size):
            gen_words.append(w1)
            try:
                w1, w2 = w2, random.choice(self.cache[(w1.lower(), w2.lower())])
                cur_size = cur_size + 1
            except:
                pass
        while w2[-1] != "." and fullstop:
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1.lower(), w2.lower())])
        gen_words.append(w2)
        return " ".join(gen_words)

    def generate_markov_para(self, paras=3, size=50):
        r = ""
        for p in range(paras):
            wlen = 20 + random.randint(20, 60)
            r += self.generate_markov_text(wlen) + "\n\n"
            z = random.randint(1, 10)
            if z == 2:
                r += self.generate_markov_quote(wlen) + "\n\n"
            if z == 6:
                r += self.generate_markov_code()

        return r

    def generate_markov_quote(self, size=50):
        return "> {txt}\n\n".format(txt=self.generate_markov_text(size))

    def generate_markov_code(self):
        return CODE.format(
            self.generate_markov_text(1).split()[0],
            self.generate_markov_text(1).split()[0],
            self.generate_markov_text(1).split()[0],
            self.generate_markov_text(1).split()[0],
            self.generate_markov_text(1).split()[0],
        )


categories = [
    "article",
    "essay",
    "note",
    "funny",
    "rant",
    "curiosity",
    "games",
    "sci-fi",
    "speculation",
    "miscellanea",
]


TEMPLATE_FM = """---
title: "%s"
tags: %s
date: %s
slug: %s
---
"""

TEMPLATE = """
%s


## %s

%s


### %s 

%s

"""


class MarkdownGenerator:
    def __init__(self, file_name):
        isJson = file_name[-4:].lower() == "json"
        self.f_ = open(file_name, encoding="utf-8")
        self.markov = Markov(self.f_, isJson)
        self.tags = self.markov.generate_markov_text(50).split()
        self.dir = "posts"

    def get_markdown(self):
        title = (
            self.markov.generate_markov_text(4, False).replace('"', "").replace("&", "")
        )
        title2 = self.markov.generate_markov_text(4, False)
        title3 = self.markov.generate_markov_text(5, False)

        word1 = self.markov.generate_markov_para(2)
        word2 = self.markov.generate_markov_para(2)
        word3 = self.markov.generate_markov_para(4)

        random.shuffle(categories)
        cat = categories[0:3]

        e = TEMPLATE % (word1, title2, word2, title3, word3)

        # print unicode(e,errors='ignore'),'\n'
        return e

    def get_doc(self):
        title = (
            self.markov.generate_markov_text(4, False).replace('"', "").replace("&", "")
        )
        mytags = ""
        random.shuffle(self.tags)
        for h in range(0, 5):
            t = removeDisallowedFilenameChars(self.tags[h])
            if t == "":
                t = "blogs"
            mytags = mytags + "'" + t + "'"
            if h != 4:
                mytags = mytags + ","

        d1 = str(random.randrange(2018, 2022))
        d2 = str(random.randrange(1, 12))
        d3 = str(random.randrange(1, 26))
        if (len(d2)) == 1:
            d2 = "0" + d2
        if (len(d3)) == 1:
            d3 = "0" + d3

        data = "{y}-{m}-{d} 12:00:00".format(y=d1, m=d2, d=d3)

        random.shuffle(categories)
        cat = categories[0:3]

        slug = "%s-%s-%s-%s" % (d1, d2, d3, removeDisallowedFilenameChars(title))
        e = TEMPLATE_FM % (title, cat, data, slug) + self.get_markdown()

        # print unicode(e,errors='ignore'),'\n'
        return (e, slug)

    def make_doc(self, subdir="."):
        (e, slug) = self.get_doc()
        with open(subdir + "/" + slug + ".md", "wt", encoding="utf-8") as ff:
            ff.write(e)

        print(slug + ".md", "written")


if __name__ == "__main__":
    markovizzatore = MarkdownGenerator("word_cache.json")
    for h in range(10):
        markovizzatore.make_doc()
