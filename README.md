Vid64
=====
Playground for video playback on the C64 inspired by Trixster's [8088 Domination](http://trixter.oldskool.org/2014/06/19/8088-domination-post-mortem-part-1/).
Currently, the compression algorithm is fairly basic. It fits one initial frame
with 15 delta compressed additional frames into memory, all in black and white.
Deltas in turn are run-length encoded.

Uses the ACME crossassembler and pucrunch (both come with [Dustlayer](http://www.dustlayer.com))
and Python's numpy, scipy, and ffvideo packages (for image/video processing).

See it [here in action](http://preview.tinyurl.com/mnqv66o).
