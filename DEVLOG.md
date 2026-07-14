# Dev Log

A running history of Rosie & the Rainbow Unicorn — what changed in each
version and why.

## Format

Each entry: version, date, what changed, and the decision(s) behind it.
Newest at the top.

---

## v0.4 — 2026-07-13

- Replaced browser speech synthesis with pre-recorded narration for the
  "Read to Me" story text and each spoken color name, generated offline with
  the Kokoro TTS model using voice `af_heart` — the same voice and
  generation approach used in Dragon's Pearl Chase, so the two games sound
  consistent. `speak(text, rate, audioSrc)` now plays the matching MP3 from
  `audio/` via a shared `<audio>` element, falling back to
  `speechSynthesis` only if a clip fails to load (mirrors
  `dragon-pearl-game`'s `playFact()`/`speakFallback()` pattern exactly).
  Added `audio/generate_audio.py` so the clips can be regenerated or
  extended later.
  - Debugging note: the prebuilt `espeakng-loader` wheel Kokoro depends on
    for phonemization ships a espeak-ng build with a hardcoded CI-runner
    data path baked in, which doesn't exist on a real machine and made
    every render fail with `Error processing file
    '.../espeak-ng-data/phontab': No such file or directory` regardless of
    what data path was passed in — confirmed with an isolated repro, then
    fixed by pointing Kokoro's `EspeakConfig` at the Homebrew-installed
    `espeak-ng` (`brew install espeak-ng`) instead of the bundled one.
- `server.js` now serves `.mp3` with the correct `audio/mpeg` content type.

## v0.3 — 2026-07-13

- Reordered each chapter to show its story card *before* the coloring page
  instead of after. `showStoryIntro(index)` now sets `save.sceneIndex`,
  updates the top bar/progress dots, and opens the story panel with a
  "Start Coloring ➜" button; dismissing it is what actually renders the
  canvas. Finishing a page (or tapping the "Next Chapter ➜" pill) now calls
  `showStoryIntro(save.sceneIndex + 1)` instead of recapping the page just
  colored. **Why:** the story sets up *why* she's painting each scene, so it
  reads better read first; resuming an in-progress page still skips straight
  to the canvas since she's already heard that chapter's intro.
- Added pinch-to-zoom and pan on the coloring canvas so small details (a
  tiny star, a dress pattern) are easier to tap precisely: the canvas is
  scaled/panned with a CSS transform (tracked via the Pointer Events API,
  since it uniformly covers touch and mouse), clamped so it can't be panned
  fully off-screen, with double-tap and per-page reset back to fit. **Why
  no changes were needed to tap-to-color:** `regionAtPoint()` already reads
  `canvas.getBoundingClientRect()`, which reflects the live CSS transform,
  so coloring keeps working unchanged at any zoom level.
  - Debugging note: `canvas.setPointerCapture()` needed a try/catch — a
    synthetic (non-OS) pointer down can make it throw, which without the
    catch silently aborted the rest of the handler and looked like the
    gesture wasn't registering at all.

## v0.2 — 2026-07-13

- Replaced the hand-built inline-SVG scenes with real illustrations
  (`assets/scenes/*.png`, sourced from a princess/unicorn coloring book PDF)
  and a canvas flood-fill engine: on first visit to a scene, the game draws
  the PNG to an offscreen canvas, flags dark pixels as "ink," and flood-fills
  the connected light-colored areas into numbered regions — the raster
  equivalent of the old hand-tagged `data-region` shapes. A transparent-
  background stencil of just the outlines is drawn on top so lines stay
  crisp regardless of fill color. **Why:** the new artwork is far more
  detailed than shapes we could reasonably hand-draw in SVG, and this keeps
  the rest of the game (progress tracking, save/resume, sound, story panels)
  working unchanged against auto-detected regions instead of authored ones.
- Regions smaller than ~1200px (at the 700×700 working resolution) are still
  tappable but don't count toward "page complete," so completion tracks the
  ~15-60 big/medium shapes per page instead of the 200-400+ total enclosed
  areas these detailed illustrations actually contain. **Why:** without this,
  a five-year-old would need hundreds of taps to finish a single page.
- `index.html`'s `<svg>` scene container became a `<canvas>`; removed all the
  `T_*` SVG template functions and per-scene `build*()` functions now that
  scenes reference an `image` path instead of a shape-building function.

## v0.2.1 — 2026-07-13

- Fixed the new illustrations rendering as a blank page when `index.html`
  was opened directly as a file (as opposed to through `server.js`).
  **Root cause:** loading a scene PNG from a separate file makes Chrome
  treat it as cross-origin under the `file://` scheme (every local file
  gets its own opaque origin), which throws a `SecurityError` from
  `getImageData()` inside the flood-fill setup -- confirmed with a minimal
  repro in headless Chrome. **Fix:** the 6 scene PNGs are now embedded
  directly in `index.html` as base64 data URIs (`IMG_MEADOW`, `IMG_MANE`,
  etc.), so there's no separate file for the browser to flag as cross-
  origin; verified the same repro succeeds once the image is inlined.
  Restores the "just open `index.html`" / Kindle Fire `file://` workflow
  the README always promised. Source PNGs stay in `assets/scenes/` for
  future re-editing.

## v0.1 — 2026-07-11

- Initial build: single self-contained `index.html`, no dependencies, no
  build step. **Why:** needs to run offline in the Silk browser on a Kindle
  Fire tablet with zero setup, matching the pattern from Dragon's Pearl
  Chase.
- Six-chapter tap-to-fill coloring story (meadow → unicorn's mane → rainbow
  bridge → sky garden → flower garden → Crystal Castle), each scene built
  from reusable SVG part templates (unicorn, princess, castle, rainbow,
  flowers, clouds) positioned per scene. **Why:** keeps ~100 colorable
  regions across the game maintainable from one set of hand-authored shapes
  instead of one-off art per page.
- Unicorn redrawn mid-build with a proper neck connector, flowing multi-lock
  mane/tail (each lock its own tappable region so she can paint an actual
  rainbow mane), hooves, eyelashes, and a spiral horn, after an early
  rotated-ellipse-neck version read as a blob rather than a unicorn.
  Flowers upgraded to six layered petals with leaves, and the castle got
  brick dots, roof stripes, and window mullions, to move the art closer to
  a real printable-coloring-book style.
- Story panel with a "Read to Me" button (browser text-to-speech) and a
  spoken color name on each palette pick. **Why:** the primary player is a
  pre-reader.
- Progress (per-region fills + current chapter) saved to `localStorage` so
  the story resumes exactly where she left off, including mid-page
  coloring.
- Sound effects via Web Audio API (tap blip, completion chime), no external
  audio files. **Why:** keeps the game fully offline with zero assets to
  ship to the tablet.
