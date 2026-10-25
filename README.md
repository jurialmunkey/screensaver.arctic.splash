# Arctic Splash screensaver

Install `screensaver.arctic.splash-1.0.0.zip` using Kodi's **Add-ons → Install
from zip file**, then select **Arctic Splash** in **Settings → Interface →
Screensaver**. Requires `resource.images.arctic.splash` 1.1.0 or later.
The active skin does not need to be Arctic Fuse 3.

The four primary settings are spin controls. Each **Specific** mode reveals a
second spin control listing every available state.

| Setting | Modes | Specific choices | Auto step |
| --- | --- | --- | --- |
| Seasons | Auto, Current, Random, Specific | Summer, Autumn, Winter, Spring | 60 seconds |
| Scenes | Auto, Random, Specific | Mount Fuji, Japanese countryside, Tokyo café | 120 seconds |
| Time | Auto, Current, Random, Specific | Every hour, 00:00–23:00 | 10 seconds |
| Weather | Auto, Current, Random, Specific | Clear, Partly cloudy, Cloudy, Windy, Rain, Heavy rain, Snow, Thunderstorm, Severe thunderstorm, Hazy | 30 seconds |

All four default to Auto. Auto starts at the current season, hour and weather
(Mount Fuji for scenes), advances in the listed order, and wraps. Each clock
runs independently. Time cycles forward through all 24 hours. The season order
is Summer → Autumn → Winter → Spring → Summer.

Current updates while the screensaver runs. Seasons use the local date and
Kodi's configured region to choose northern or southern meteorological seasons,
matching the splash. Unknown regions use northern seasons. Weather follows
`Weather.FanartCode` from the configured Kodi weather provider; unavailable or
unknown codes fall back to Clear. Current time uses the local 24-hour clock.
Random makes one independent choice per setting on each screensaver start and
holds it until exit. Specific holds the selected value. No setting alters the
skin's splash, preview state, weather provider, or system clock.

The screensaver closes on user input, screensaver deactivation, display sleep
or Kodi shutdown. It does not play media or request a weather refresh.

## Rendering and maintenance

Artwork and masks remain in the shared resource; no images are duplicated.
Rendering XML is exported from Arctic Fuse 3's existing splash includes,
preserving layer order, animated clouds, reflections, stream frames, lighting,
precipitation, foliage and lightning. Includes are expanded offline, so runtime
rendering needs neither the source skin nor SkinVariables. Window-local
properties provide live state and texture aliases. All Python belongs to this
standalone screensaver add-on.

The startup splash's daytime text-readability dim layer is omitted from all
three screensaver scenes. Keep this exclusion when regenerating the renderer.

`resources/renderer-sources.json` records the source skin version and hashes.
The adjacent offline `export_splash.py` and `build_splash.py` files rebuild the
renderer/settings/package; they are outside the distributable add-on. Run both
with the source skin directory as the first argument; the exporter also takes
the add-on output directory as its second argument. Regenerate the renderer when
the source splash contract changes, then verify state aliases and asset paths.

Derived splash rendering: jurialmunkey / Arctic Fuse 3 contributors.
Licensed under CC BY-NC-SA 4.0; see LICENSE.txt.

Static verification can run without Kodi. Visual output, settings interaction,
GPU performance, and live screensaver exit behavior require in-Kodi testing.
