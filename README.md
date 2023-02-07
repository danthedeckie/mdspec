# mdspec
"Declarative Model Specifications, from markdown-ish plain text files"

Looking at defining models / object specification in "plain text"
for working w/ designers &amp; clients. 

This is very much a hacky work-in-progress, / working out loud playground at the moment. 

# The big idea:
Tests in Python or JS are great, but not accessible to non-coders.
Features need to be defined somehow, and agreed between parties.

Gerkin is alright for describing functional requirements - but the whole
idea of "given/when/then" is very process oriented - whereas on 
Django / Wagtail / CMS based sites often have many objects defined
which automatically implement a tonne of features. (ie, A Page model
with a few fields).

They're implemented declaratively, not functionally.

Could we have something similar to gerkin for models / blocks that are declarative
not functional?

And could we use a declarative style of specification, but in a plain-english type
of format to facilitate that in a way that's easy to understand & share betweeen
techies & non-techies?

## Example:
(syntax subject to change)

```markdown
# HomePage
HomePage is a Page Type.
It has these fields:
 - title: required, text, maximum 100 characters
 - banner: image, optional
 - banner: text, optional
 - contents (the main contents of the page...)

The contents field is a StreamField.
It has these blocks:
 - richtext
 - image
 - raw-html
 - contact-form

## Block definitions...

richtext is a Wagtail Block.
It has these fields:
 - contents
 - style

image is a Wagtail Block.
It has these fields:
 - image (the link to the image itself...)
 - caption
 - link

...
```

Which, in theory, is relatively easy to understand for non-techies,
and renders nicely as markdown.  It can be rendered out, signed off,
etc.

It's structured though, so it can be parsed (by this project) into
something we can then travese / execute as part of CI / tests.

it results in something like:
```json
{
    "_name": "HomePage",
    "_type": "Page",
    "fields": [
        ["title", "required", "text", "maximum 100 characters"],
        ["banner", "image", "optional"],
        ["contents"]
    ]
},

{
    "_name": "contents",
    "_type": "StreamField",
    "blocks": [
        ["richtext"]
        ["image"]
        ["raw-html"]
        ...
    ]
},

...
```
etc.  (Example, not actual format.  But structured something like that...)

Now we have that specification as (dict / JSON / structured) objects,
it's pretty easy to write tests that automatically find each defined page type,
check that it has all required fields, or whatever.

We could also have tests that check that the admin page for each page
type actually has all of those fields as form fields in the admin.

Once you get to anywhere where logic is involved (eg, templates, output)
then switching to gerken based cases makes a lot more sense, this
spec type would just be for things which are structurely "defined" rather
than functionally implemented... (if that makes sense?)

## Thoughts:

- anything in brakets (like this) is considered a comment, and ignored?
- markdown titles are ignored too.
- how can we have nice sections for random implementaion notes?
  maybe use markdown quotation `> text` blocks?  Should those be
  stored to use as docstrings in generation? or better not?

# to play:


```sh
python3 mdspec/parser.py examples/pages.md
```
and it should output a structured version of the contents.
(There will be tests run with `make test` too - WIP...)

# What could we do with this?

- Use it just as a structured way to define models / pages / etc.
- Get sign off from different teams (BE / FE / Design / client...)
- Run acceptance tests automatically off the structured data.
- Generate initial model python code / tests / templates / etc?

# Example thoughts:

```markdown
TeamPage is a Page Type
it has these fields:
 - title
 - top_contents
 - below_contents
it has these connections:
 - team: Person, many via "TeamPerson"
```

How much worse is this in gerkin?

```gerkin
Scenario:
  Given an Index Page
   When I add a child page
   Then I should be able to add a TeamPage
```
and
```gerkin
Given a TeamPage
 When I edit it in wagtail
 Then I should be able to edit the title field
  And I should be able to edit the top_contents field
  ...
```
hm... it's so verbose.  But functional spec.

I guess with this kind of declarative spec, we can pass that into other tests?
```gerkin
 Given <pagetype>
  When I edit it in wagtail
  Then I should be able to edit all defined fields
```

