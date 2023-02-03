HomePage is a Page Type.
It is defined in pages.models.
It has these fields:
 - title : CharField (comments are ignored)
 - banner
 - contents

The contents field is a StreamField.
It has these blocks:
 - RichText
 - Banner
 - Three Column Block

RichText is a block.
It has these fields:
- contents : TextField (for holding raw HTML)
