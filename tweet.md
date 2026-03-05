# TiPToP Twitter Thread Draft

## Tweet 1 (Hook)
State-of-the-art robot policies often need hundreds of hours of data. What if you needed none?

Introducing TiPToP: a modular manipulation system that solves open-world tasks from pixels and language — all without training on a single robot demonstration.

We compose pretrained foundation models with GPU-parallelized planning. Our system can be deployed on supported hardware in under an hour.

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

No task-specific training required! (2/10)

<video controls width="100%">
  <source src="media/overview/pipeline.mp4" type="video/mp4">
</video>

---

## Tweet 3 (Motivating example)
Why does this matter?

Simple task: "Place the peanut butter crackers onto the tray" — in a scene full of different cracker packets.

TiPToP succeeds 5 out of 5 trials.
π₀.₅-DROID (SOTA VLA, 350+ hrs of robot data) fails all 5 trials.

TiPToP does this by *reasoning* at test time about what's in the scene. A pretrained policy on the other hand often has to have seen something similar in training. (3/10)

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
We ran 165 trials across 28 tasks. To ensure broad task coverage and thorough experimentation, most evaluation was performed externally at UPenn by a team not involved in development.

**Results**:
Success rate: TiPToP 59.4% vs π₀.₅-DROID 33.3%
Task progress: TiPToP 74.6% vs π₀.₅-DROID 52.4%
Speed: TiPToP 37% faster when both succeed (5/10)

*(No media, or consider bar chart from website) [njk: I think we should include the bar charts!!!]*

---

## Tweet 6 (Failure analysis + modularity)
A key benefit of modularity: we can trace exactly where failures happen.

30 from grasping
13 from mesh reconstruction
6 from VLM errors
5 from planning

TiPToP improves as components improve: drop in a better grasp model, get a better system. (6/10)

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
TiPToP is far from perfect:

Open-loop execution → no recovery from failed grasps
Single-viewpoint perception → limited visibility
Lacks closed-loop reactivity of VLAs

We generally view TiPToP as a test-time scaling and reasoning method that's ultimately complementary to large robot foundation models like VLAs. We are excited about future research to more tightly combine these paradigms! (9/10)

*(No media)*

---

## Tweet 10 (Closing)
TiPToP was a team effort and wouldn't have been possible without (**TODO: tag everyone, with specific shoutouts to UPenn people**).

🌐 Project: https://tiptop-robot.github.io
📄 Paper: https://tiptop-robot.github.io/tiptop.pdf
💻 Code: https://github.com/tiptop-robot/tiptop

While we're excited by TiPToP's current capabilities, we also feel there's so much more to be done (check out the website for a list of things to be worked on). We hope you'll try it out and consider contributing to the system yourself! (10/10)

---


## Notes for posting:
- Twitter is plain text only (no markdown)
- Links in first and last tweets (X algorithm penalizes mid-thread links)
- Each tweet should be under 280 characters — verify before posting
- Alt text for all videos/images for accessibility
- (N/10) goes at end of tweet per Jesse's style
