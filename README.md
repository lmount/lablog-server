Warning: This is a draft documentation file. Follow at your own risk.

# LaBlog Search

> Search your Markdown notes in the browser

## Instructions


At this moment, this project has been tested only with `python2`. Install the dependencies with:

```bash
pip install flask mistune bs4
```

edit the file `config-sample.json` to locate your markdown files and start the server with:

```
python2 lablog_server.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001) in your browser.

## How it works with the markdown files

Each `#` title (`h1` header) is considered a separate entry, e.g.:

```markdown

# This is an entry
<!-- keywords, in, comments -->

I keep code snippets and small workflows in my notes.

This way, the content is easily accessible.

# What is searched?
<!-- comment, section, is, searchable -->

The header and the comment sections are searched for the keywords.

No boolean operations are implemented at the moment and all keywords should be present in either the title (h1 header) or the comment sections.

## Second order titles (h2 headers)

.. are not searchable!

# Tricks
<!-- inside, text -->

* To search only the header, use "title:keyword"
* To search only the comment section, use "tags:keyword"
* To search inside the main text, use "text:keyword" (off by default)

```


