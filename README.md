# TiPToP Website

Website for TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation.
Live at [tiptop-robot.github.io](https://tiptop-robot.github.io).

## Structure

```
index.html          # Main page
results.html        # Results
implementation.html # Implementation details
tiptop.pdf          # Paper
assets/             # CSS, JS, favicon
media/
  overview/         # Teaser and pipeline videos
  implementation/   # Implementation figures, videos, 3D assets (.bin, .glb)
  demos/            # Robot demo videos
  results/
    scenes/         # Environment photos (sim, penn, mit)
    trials/         # Per-task trial videos
  failures/         # Failure analysis figures and videos
```

## Local Development

Requires the `livereload` Python package:

```bash
pip install livereload
python server.py
```

Opens at `http://127.0.0.1:5500` (auto-increments port if busy). Live-reloads on changes to `.html`, `.css`, and `.js` files. Range requests are supported for video seeking.

## Notes

If you fork this repo, please update the Google Analytics measurement ID in the `<head>` of each HTML file.

## License

[CC BY 4.0](LICENSE) — The TiPToP Authors
