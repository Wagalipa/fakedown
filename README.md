# Fakedown -- A fake markdown post generator for Static Site Generators

This is a small, WSGI Flask-based web app that can be used as a text-based web service to generate fake markdown posts using Markov chains using two-word tuples as key. 

The corpus has been created using text from various Project Gutenberg sites. 

I made this app to quickly generate a huge amount of fake blog posts and test Static Site Genrators' performance.

It is geared towards [Jekyll](https://jekyllrb.com) and [Eleventy](https://11ty.dev), but I guess it can be adapted to generate posts that can be read by other SSGs.

## Usage

The services exposes the following `GET` endpoints

- `/words` -- generates some words
- `/phrase` -- like `/words`, but longer
- `/paragraph` -- some phrases combined in a single paragraph
- `/paragraphs` -- some markdown paragraphs
- `/markdown` -- a complete markdown post, _sans_ front matter
- `/markdown-post` -- as above, with a complete fake fron matter
- `/eleventy-post` -- as above.

There's a live instance of an early version of this package running here:

https://fakedown.xoxarle.com/eleventy-post

You can use cUrl to generate and save a post this way:

``` bash
$ curl https://localhost:5000/eleventy-post --output the-post.md
```

## Offline usage

The module `MarkovJekyll.py` can also be executed as a standalone program. It will generate 10 markdown posts on 10 different files. 

## Using and creating a different corpus

If you want to generate post using different reference text, you can proceed this way.

1. Create a huge, UTF8-text file containing the text you want to "markov"-ize. Again, Project Gutenberg is your friend.

2. Change the following line in the file `MarkovJekyll.py`

``` python
markdownGenerator = MarkdownGenerator("word_cache.json")
```
to

``` python
markdownGenerator = MarkdownGenerator("my-text-reference.txt")
```

and run the program. 

A new frequency map will be created and stored into `word_cache.json` and will serve as a reference for your fake markdown posts.

## License

This app is licensed under LGPL 2.1