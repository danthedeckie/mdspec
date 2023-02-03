# mdspec
Looking at defining models / object specification in "plain text" for working w/ designers &amp; clients


This is very much a hacky work-in-progress, / working out loud playground at the moment. 

# The big idea:

Gerkin is decent for describing functional requirements.
Django / Wagtail / CMS based sites often have many objects defined
which automatically implement a tonne of features. (ie, A Page model
with a few fields)

Could we have something similar to gerkin for models / block functional requirements?

## Example:
(syntax subject to change)

```markdown
# HomePage
HomePage is a Page Type.
It has these fields:
 - title
 - banner image
 - banner text
 - contents

The contents fields is a StreamField.
It has these blocks:
 - richtext
 - image
 - raw-html
 - contact-form

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

So for instance, we can find each defined page type, check that it
has all required fields.

We could also have tests that check that the admin page for each page
type actually has all of those fields as form fields in the admin.

Once you get to anywhere where logic is involved (eg, templates, output)
then switching to gerken based cases makes a lot more sense, this
spec type would just be for things which are structurely "defined" rather
than functionally implemented... (if that makes sense?)

# to play:


```sh
python modelspec.py spec/pages.spec
```
and it should output a structured version of the contents.



