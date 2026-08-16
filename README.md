# Peripersonal_Reaching

Egocentric annotations for guiding a blind or low-vision user's hand. Each frame is labelled with the user's stated need, a scene description, an ordered chain of touchable landmarks to the target, whether the target and the hand are visible, the head and hand motion to recommend next, nearby hazards and their direction, the surface the hand is being sent to, and a task phase.

| File | What it is |
|---|---|
| `annotation.md` | The schema: every field, every label code, and what the labels look like in practice. |
| `peripersonal_reaching.py` | The loader. Reads the JSON into objects and stops there. |
| `README.md` | How to use the dataset. |
| `LICENSE.md` | CC BY 4.0 License |

## Getting the data

The release archive is in Google Drive: <https://drive.google.com/file/d/1Ir6Wholn47Sv9QnCtLlQmKmg39EyPLQ0/view?usp=sharing>. Download it, unpack it, and point the loader at the directory that contains the `image_*/` folders:

```text
data/annotations/image_71/0.json
data/annotations/image_71/1.json
...
```

## Loading it

```python
from peripersonal_reaching import load_dataset

ds = load_dataset("data/annotations")
print(len(ds.videos), len(ds.frames))   # what your copy actually holds

frame = ds.videos[0].frames[0]
frame.video_id                          # e.g. "image_71" — ids are not zero-based
frame.frame_index                       # a video frame index, not a list position
frame.question                          # e.g. "I want a pair of pliers. "
frame.is_target_in_frame                # "A", "B", or the string "None"
frame.raw                               # the parsed JSON, untouched
```

Run the loader as a script to see what your copy holds, and to count the three defects most likely to change a result quietly:

```bash
python peripersonal_reaching.py data/annotations
```
This file and `annotation.md` describe data version **1.0.0**. 

## licence

The data is released under **CC BY 4.0** — use it for anything, including commercially, with attribution. `peripersonal_reaching.py` has no separate software licence, so CC BY covers it by default; that is a poor fit for code, saying nothing about warranty or patents, so ask before vendoring the loader into a product.

** Citation

A. Zhang, "Safety-aware peripersonal object reaching guidance via vision-language models for people with vision impairments," Applied Artificial Intelligence, vol. XX, no. X, pp. XX–XX, 2026.

@article{zhang2026safety,
  author  = {Zhang, Amy},
  title   = {Safety-Aware Peripersonal Object Reaching Guidance via Vision-Language Models for People with Vision Impairments},
  journal = {Applied Artificial Intelligence},
  year    = {2026}
}