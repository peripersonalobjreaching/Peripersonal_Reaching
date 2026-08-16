# Peripersonal_Reaching — annotation format

Each video is one search-and-reach episode, each annotated frame is one JSON file, and all files for a video live in one `image_<number>/` folder beside the video and a preview still. A frame's annotation records what the user asked for, what the camera sees, an ordered chain of touchable landmarks from a findable reference object to the target, whether the target and the hand are visible, which way the head and hand should move next, what is dangerous nearby and in which direction, which surface the hand is being sent to, and which phase of the task the frame belongs to.

The code to load the data:

```python
from collections import Counter
from peripersonal_reaching import load_dataset
ds = load_dataset("data/annotations")     # the directory holding the image_*/ folders
```

## Directory layout

```text
annotations/
├── image_132/
│   ├── 0.json
│   ├── 1.json
│   ├── 2.json
│   ├── 3.json
│   ├── 4.json
│   ├── 8.json
│   ├── ...
│   ├── image_132_cut.mp4                    # the episode
│   └── image_132_first_frame_preview.jpg    # frame 0 as a still
├── image_133/
│   └── ...
├── image_100_cut/                           # a placeholder, not a sample
│   ├── 0.json
│   └── image_100_cut_cut.mp4
└── ...
```

The number in a JSON filename is the video frame index, not a position in a sequence.

## Frame sampling

The annotation tool ran with `frame_step = 4`. Frames `0, 1, 2, 3, 4` were annotated consecutively, and after frame 4 every fourth frame: `8, 12, 16, 20, …`. Every video in the release follows that grid exactly, so you can rely on the pattern — but not on how far it runs. Some directories stop at frame 0, and those are broken rather than short; see below.

## Fields

Each JSON holds these 11 keys. All of them are present in every frame, no undocumented key appears anywhere, and every value has the type below.

| Field | Type | Description |
|---|---|---|
| `Question` | string | The user's need, e.g. "I want a kettle." Often indirect: "I am thirsty" names no object at all, so the target has to be inferred. |
| `Scene Description` | string | Free text describing the scene and where the important objects are. |
| `Chain-of-landmark` | list[string] | Ordered chain of touchable landmarks from an easy-to-find reference object to the target. |
| `Is target in frame` | string | Whether the target is *fully* visible. `A` yes, `B` no, `"None"` unannotated. |
| `Head movement` | list[string] | Recommended head motion. |
| `Is hand in frame` | string | Whether the user's hand is visible. `A` yes, `B` no, `"None"` unannotated. |
| `Hand movement` | list[string] | Recommended hand motion. |
| `Risk Items` | list[string] | Free-text hazards — in practice a knife, scissors, pliers, a stove, or a table. |
| `Risk direction` | list[string] | Where the hazard is relative to the user. |
| `Reaching Target` | string | The landmark currently being approached, as `reaching to <object>`. |
| `Phase` | integer | Task phase, `1`, `2` or `3`. |

## Label codes

Both visibility fields use the same encoding: `A` yes, `B` no, `"None"` for not annotated.

| Code | `Head movement` | `Hand movement` | `Risk direction` |
|---|---|---|---|
| `A` | left | left | left |
| `B` | right | right | right |
| `C` | up | forward | front |
| `D` | down | backward | back |
| `E` | no movement | no movement | the hand is not visible |

## Phases

As designed, the episode runs Phase I search → Phase II describe → Phase III reach.

| Value | Phase | Rule the tool applied |
|---|---|---|
| `1` | I / search | frame 0 |
| `2` | II / describe | frame 4 |
| `3` | III / reach | every other sampled frame |

## Example

`image_132/0.json`, verbatim:

```json
{
    "Question": "I want a kettle.",
    "Scene Description": "There is a kettle on top of a table in the middle of the table. There is a stove on the right.",
    "Chain-of-landmark": [
        "Table",
        "Kettle",
        "Stove"
    ],
    "Is target in frame": "B",
    "Head movement": [
        "A",
        "C"
    ],
    "Is hand in frame": "B",
    "Hand movement": [
        "E"
    ],
    "Risk Items": [],
    "Risk direction": [
        "E"
    ],
    "Reaching Target": "reaching to Table",
    "Phase": 1
}
```