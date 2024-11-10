# Shablam

Have you ever scrolled on instagram and seen a scene from a movie or show that was not credited. Have you ever wanted to know where the material is from, but had to scroll through the comments to find it from some good samaritan who posted it? Well with Shablam, this will not be a problem any longer!

## Installation

Clone the repository into your folder and then use [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

First we need to use a script to compile a "database" (it's really just a dictionary that's been dumped into a pickle file for later use). Add the movies/scenes to the "movie_scenes" folder and then run compile.py.

```bash
python3 compile.py
```

Then run app.py. This will spawn a locally hosted instance of the website.

```bash
python3 app.py
```

Upload the movie scene to the drop box and press submit. It will take a few moments to generate an answer or tell you there's no match in the database (which for this project is quite small).
