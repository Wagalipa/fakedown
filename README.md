# Fakedown

A fake markdown post generator for Static Site Generators using Markov chains.

[![License: LGPL v2.1+](https://img.shields.io/badge/License-LGPL_v2.1+-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

This is a WSGI Flask-based web application that generates fake markdown posts using Markov chains with two-word tuples as keys. The corpus has been created using text from various Project Gutenberg sites.

Perfect for quickly generating a large amount of fake blog posts to test Static Site Generators' performance.

It is geared towards [Jekyll](https://jekyllrb.com) and [Eleventy](https://11ty.dev), but can be adapted to generate posts compatible with other Static Site Generators.

## Features

- 🚀 Fast markdown content generation using Markov chains
- 🌐 RESTful API endpoints for different content types
- 📝 Supports various content formats (words, phrases, paragraphs, full posts)
- 🎯 Jekyll and Eleventy frontmatter support
- 📚 Built on Project Gutenberg corpus
- 🔧 Configurable and extensible

## Installation

### Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fakedown
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Usage

### Web Application

Start the Flask development server:

```bash
poetry run python wsgi.py
```

The application will be available at `http://localhost:5000`.

### Production Deployment

For production, use Gunicorn:

```bash
poetry run gunicorn webapp:app
```

### API Endpoints

The service exposes the following `GET` endpoints:

- `/words` -- generates some words
- `/phrase` -- like `/words`, but longer
- `/paragraph` -- some phrases combined in a single paragraph
- `/paragraphs` -- some markdown paragraphs
- `/markdown` -- a complete markdown post, _sans_ front matter
- `/markdown-post` -- as above, with a complete fake front matter
- `/eleventy-post` -- as above

### Example Usage

You can use cURL to generate and save a post:

```bash
# Generate a few words
curl http://localhost:5000/words

# Generate a complete post
curl http://localhost:5000/eleventy-post --output the-post.md
```

There's a live instance of an early version of this package running here: https://fakedown.xoxarle.com/eleventy-post

## Offline Usage

The module `MarkovJekyll.py` can also be executed as a standalone program:

```bash
poetry run python MarkovJekyll.py
```

This will generate 10 markdown posts in 10 different files in the current directory. 

## Using a Custom Corpus

If you want to generate posts using different reference text:

1. Create a large UTF-8 text file containing the text you want to "markov"-ize (Project Gutenberg is a great source).

2. Change the following line in `MarkovJekyll.py`:

```python
markdownGenerator = MarkdownGenerator("word_cache.json")
```

to:

```python
markdownGenerator = MarkdownGenerator("my-text-reference.txt")
```

3. Run the program to generate a new frequency map that will be stored in `word_cache.json`.

## Development

### Code Quality Tools

This project uses several tools to maintain code quality:

```bash
# Format code with Black
poetry run black .

# Lint code with Flake8
poetry run flake8

# Type checking with MyPy
poetry run mypy .

# Run tests
poetry run pytest
```

### Project Structure

```
├── MarkovJekyll.py    # Core Markov chain text generator
├── webapp.py          # Flask web application
├── wsgi.py           # WSGI entry point
├── word_cache.json   # Pre-computed word frequency cache
├── pyproject.toml    # Poetry configuration
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure tests pass: `poetry run pytest`
4. Format your code: `poetry run black .`
5. Check for linting issues: `poetry run flake8`
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## License

This project is licensed under the GNU Lesser General Public License v2.1 or later (LGPL-2.1+). See the [LICENSE](LICENSE) file for details.

## Authors

- **Max Lambertini** - *Initial work* - [m.lambertini@gmail.com](mailto:m.lambertini@gmail.com)
- **Jace Ju** - [jaceju@gmail.com](mailto:jaceju@gmail.com)

## Acknowledgments

- Text corpus from [Project Gutenberg](https://www.gutenberg.org/)
- Built with [Flask](https://flask.palletsprojects.com/)
- Dependency management with [Poetry](https://python-poetry.org/)