# Add for searching
* gists
* ~~tldr, cheat~~

# Functionality
* ~~Add "Copy Source"~~
* ~~Add syntax highlighting~~
* Voting system
* Paginate
* Compute hash of content (.strip())


## Use classes for parsing 

* Eg. different parsers for `tldr`, `notes`, etc.
* Probably different `class HighlightRenderer(mt.Renderer) eg:

    ```python
        def codespan(self, code):
            preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
            postCode = '</pre></div>\n'
            code = '<code class="sourceCode">{}</code>'.format(
                mt.escape(code))
            return preCode + code + postCode
    ```

* `tldr` remove '{{', '}}'.



## Show only snippets

```javascript
$('div:not(.sourceCode)').hide();
$('pre.sourceCode').appendTo('body');
```

```javascript
$('body > :not(#myDiv)').hide(); //hide all nodes directly under the body
$('#myDiv').appendTo('body');
```