# TiPToP Twitter Thread Draft

## Tweet 1 (Hook)
Introducing TiPToP: a modular manipulation system that solves open-world tasks from pixels and language — with zero robot-specific training data.

We compose pretrained foundation models with GPU-parallelized planning. Deploy on supported hardware in under an hour.

📄 Paper: https://tiptop-robot.github.io/tiptop.pdf
💻 Code: https://github.com/tiptop-robot/tiptop

(1/10)

<video controls width="100%">
  <source src="media/overview/teaser.mp4" type="video/mp4">
</video>

---

## Tweet 2 (How it works)
How does it work?

Perception: FoundationStereo (depth) + Gemini (semantic grounding) + SAM-2 (segmentation) → 3D scene representation

Planning: cuTAMP searches thousands of candidate plans in parallel on GPU, checks feasibility, picks the best one

No task-specific training required. (2/10)

<video controls width="100%">
  <source src="media/overview/pipeline.mp4" type="video/mp4">
</video>

---

## Tweet 3 (Motivating example)
Why does this matter?

Task: "Place the peanut butter crackers onto the tray" — in a scene full of different cracker packets.

TiPToP succeeds 5 out of 5 trials.
π₀.₅-DROID (SOTA VLA, 350+ hrs of robot data) fails all 5 trials.

TiPToP reasons at test time about what's in the scene. A pretrained policy has to have seen something similar in training. (3/10)

<video controls width="100%">
  <source src="media/results/edited/cracker-hard.mp4" type="video/mp4">
</video>

---

## Tweet 4 (Long-horizon + multi-step)
This test-time reasoning lets TiPToP scale to novel scenarios with more objects and longer horizons.

On multi-step manipulation (sequential picks, obstacle clearing, constrained packing):

TiPToP: 57.5% vs π₀.₅-DROID: 15%

The planner sequences actions and checks constraints before committing. (4/10)

<video controls width="100%">
  <source src="media/results/edited/coffee-pack-obs.mp4" type="video/mp4">
</video>

---

## Tweet 5 (Overall results)
We ran 165 trials across 28 tasks — most evaluated externally at UPenn by a team not involved in development.

Success rate: TiPToP 59.4% vs π₀.₅-DROID 33.3%
Task progress: TiPToP 74.6% vs π₀.₅-DROID 52.4%
Speed: TiPToP 37% faster when both succeed (5/10)

*(No media, or consider bar chart from website)*

---

## Tweet 6 (Failure analysis + modularity)
A key benefit of modularity: we can trace exactly where failures happen.

30 from grasping
13 from mesh reconstruction
6 from VLM errors
5 from planning

TiPToP improves as components improve — drop in a better grasp model, get a better system. (6/10)

<img src="media/failures/sankey-failures.png" width="100%">

---

## Tweet 7 (Cross-embodiment)
TiPToP isn't tied to one robot.

We deployed it on Franka, UR5e, and Trossen WidowX AI — each time just swapping in a new URDF and camera config.

No retraining. No new demonstrations. Same perception and planning code. (7/10)

<video controls width="100%">
  <source src="media/demos/ur5-demo.mp4" type="video/mp4">
</video>

---

## Tweet 8 (Beyond pick-and-place)
TiPToP also extends beyond pick-and-place.

We added a whiteboard wiping skill in under a day — without modifying existing perception or execution code.

Skills compose: "erase the whiteboard and put everything into the bowl" just works. (8/10)

<video controls width="100%">
  <source src="media/demos/wipe.mp4" type="video/mp4">
</video>

---

## Tweet 9 (Limitations + future)
TiPToP has limitations:

Open-loop execution → no recovery from failed grasps
Single-viewpoint perception → limited visibility
Lacks closed-loop reactivity of VLAs

We see test-time scaling methods like TiPToP as complementary to large robot foundation models. Combining them is an exciting direction. (9/10)

*(No media)*

---

## Tweet 10 (Closing)
TiPToP shows that modular composition of foundation models + structured planning can produce capable manipulation — without robot-specific training data.

🌐 Project: https://tiptop-robot.github.io
📄 Paper: https://tiptop-robot.github.io/tiptop.pdf
💻 Code: https://github.com/tiptop-robot/tiptop

Thanks to our collaborators at UPenn for the external evaluation! (10/10)

---

## Notes for posting:
- Twitter is plain text only (no markdown)
- Links in first and last tweets (X algorithm penalizes mid-thread links)
- Each tweet should be under 280 characters — verify before posting
- Alt text for all videos/images for accessibility
- (N/10) goes at end of tweet per Jesse's style
