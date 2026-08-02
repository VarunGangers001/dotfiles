# Daedalus Observation Renderers

This document records the intended visual style of each Observation renderer.

## Engraved

Current preferred renderer and likely default.

Visual goals:

- bronze etching on a deep navy background
- detailed enough to preserve the subject
- controlled texture rather than visual noise
- resembles an engraved scientific illustration
- suitable for planets, galaxies, spacecraft, eclipses and nebulae
- should feel elegant and archival rather than photographic

Current settings:

- width: 72
- height: 30
- resize width: 900 px
- blur: 1.8
- contrast: 6%
- edge strength: 1.2
- threshold: 33%

Possible future improvements:

- cross-hatching or stippling
- multiple bronze brightness levels
- cleaner background removal
- automatic simplification for noisy images
- separate settings based on image type

## Technical

Visual goals:

- sparse and readable
- strong major contours only
- resembles an engineering or mission-document sketch
- avoids unnecessary texture

Best suited to:

- spacecraft
- planets
- sharply defined objects
- diagrams and observatories

## Classic

Visual goals:

- balanced compromise between detail and readability
- dependable fallback renderer
- suitable for a broad range of images

This is currently the safest general-purpose preset.

## Blueprint

Visual goals:

- deep navy background
- cyan or pale technical lines
- resembles CAD, schematics or mission-control graphics
- clean and structured rather than decorative

The Blueprint preset currently changes only the processing settings. Its own colour palette still needs to be implemented.

## Default Renderer

Engraved is currently the preferred default.

The final application may automatically fall back to Classic or Technical when an image becomes too noisy in Engraved mode.
