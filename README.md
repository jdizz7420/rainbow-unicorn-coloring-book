# 🦄 Rosie & the Rainbow Unicorn

A tap-to-fill interactive coloring book for a five-year-old, built as
`index.html` plus a small `audio/` folder of narration clips, with **no
dependencies and no build step** — it runs offline in any modern browser,
including the Silk browser on Amazon Fire tablets, opened directly from a
file with no server required.

## How to play

- Each chapter opens with a **story card** — read it or tap **🔊 Read to Me**
  — then tap **Start Coloring** to open that chapter's page.
- **Tap a color** on the palette at the bottom.
- **Tap a part of the picture** to fill it with that color — the sky, the
  unicorn's mane, a flower, anything outlined in black.
- **Pinch to zoom** in on the picture to color small details more precisely
  (a tiny star, a dress pattern); drag with one finger to pan around while
  zoomed in, and double-tap to snap back to the full page.
- Keep coloring until the page sparkles and celebrates, then tap **Next
  Chapter** to move on to the next story card.
- Progress is saved automatically, so closing the tablet never loses her
  place. The **🧽 button** clears just the current page if she wants a redo,
  and the **🏠 button** returns to the title screen without losing progress.

## The story

Princess Rosie meets a unicorn named Buttercup in a meadow that has lost all
its color. Six chapters later — after painting Buttercup's rainbow mane, a
real rainbow bridge, a sky garden, a flower garden, and the Crystal Castle —
Rosie becomes the kingdom's first Rainbow Princess.

Each chapter opens with a story card and a **🔊 Read to Me** button (natural
pre-recorded narration, browser text-to-speech as a fallback) for pre-readers,
plus a quick spoken color name whenever a new color is picked.

## Run it

Just open `index.html` in a browser. That's it.

Or serve it locally:

```bash
node server.js
# then visit http://localhost:4600/
```

### Playing on a Kindle Fire tablet

1. Copy `index.html` **and the `audio/` folder** to the tablet (USB, email,
   or a shared folder) — keep them in the same directory. (The scene
   illustrations are embedded in `index.html` itself, so only `audio/` needs
   to travel alongside it.)
2. Open the Silk browser and go to `file:///sdcard/Download/index.html`.
3. Use the browser menu to **Add to Home screen** for an app-like icon that
   works offline.

## Notes

- Each scene is a real illustration, not hand-drawn shapes. On first visit to
  a page, the game flood-fills the illustration's enclosed light areas into
  numbered regions bounded by its black outlines — the same idea as tracing
  shapes by hand, done automatically from the artwork. Tapping a region fills
  it; a page "completes" once every medium-or-larger region has been colored
  (tiny detail specks are still fillable for fun, just not required).
- The 6 scene illustrations are embedded directly in `index.html` as base64
  data (source PNGs kept in `assets/scenes/` for reference/re-editing). **Why
  not load them as separate files:** opening `index.html` directly (double-
  click, or `file://` on the tablet) makes the browser treat a same-folder
  image as cross-origin, which blocks the canvas from reading its pixels —
  embedding avoids that restriction entirely and keeps the game a true
  single file.
- To swap in different illustrations: replace the PNG in `assets/scenes/`,
  then re-run `python3 -c "import base64; print(base64.b64encode(open('assets/scenes/NAME.png','rb').read()).decode())"`
  and paste the result into the matching `IMG_*` constant near the top of
  the `<script>` block in `index.html`. Clean black-outline line art on a
  light background works best.
- Sound effects use the Web Audio API. Narration ("Read to Me" and each
  spoken color name) plays pre-recorded MP3 clips generated offline with the
  free, open-source [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) TTS
  model (voice `af_heart`, the same voice used in Dragon's Pearl Chase),
  falling back to the browser's built-in speech synthesis only if a clip
  fails to load. To regenerate or add narration, see
  `audio/generate_audio.py` (kept alongside the clips for reference).
- `server.js` is only a tiny local static-file server for previewing during
  development — it isn't needed to actually play the game.

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
