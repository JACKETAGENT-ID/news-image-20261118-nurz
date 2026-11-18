# news-image-20261118-nurz

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/JACKETAGENT-ID/news-image-20261118-nurz/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/JACKETAGENT-ID/news-image-20261118-nurz/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image summing up the world news of Wednesday 18 November 2026, drawn
as a newspaper front page: masthead **THE WORLD** with the date, a lead
story on the APEC summit opening in Shenzhen, six illustrated panels
(Gulf drone strikes, Nvidia's $115.84bn quarter, the Gaza ceasefire
warning, Dhoni's IPL retirement, Cyclone Akvan, Voyager 1 nearing one
light-day) and an "In brief" strip (Latvia, Ukraine, Baidu's AI-bubble
warning, Trump's BBC deposition deadline).

The image is drawn entirely in code (`generate.py`, PIL primitives — no
photos, no downloaded art). `main.py` (Python standard library only)
copies the finished `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 generate.py entry.png   # redraw the front page (optional)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
