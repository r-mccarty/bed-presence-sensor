# Website Content Brief: OpticWorks Bed Presence Sensor

**Document Purpose:** To define the brand positioning, narrative arc, and content strategy for the
OpticWorks Bed Presence Sensor landing page and marketing materials. This brief embodies a
**Brand-Led + Product-Led** strategic foundation, where technical excellence serves as proof of an
unwavering commitment to craft, thoughtfulness, and user experience.

---

## 1. Brand Philosophy & Origin Story

### The "Why" Behind OpticWorks

**Every night, millions of people are let down by technology that should just work.**

Lights flicker on when you're trying to sleep. Automations fail when you lie perfectly still. Sensors
trigger falsely when your cat jumps on the bed or a fan turns on. The promise of the "smart home"
feels broken—not because the technology is impossible, but because most products are built to
*ship*, not to *serve*.

**OpticWorks was founded on a different belief: that technology should disappear into your life, not
demand your attention.**

We are a team that obsesses over details most companies ignore. We believe that a sensor isn't just
a component—it's a promise. A promise that your automations will be reliable, that your privacy will
be protected, and that you'll understand *why* things work the way they do. We're building a
company for people who refuse to settle for "good enough."

### Our Craft Philosophy

We approach hardware and software the way a craftsperson approaches their work:

- **Transparency over black boxes** – You deserve to know how decisions are made. Every parameter
  is tunable. Every state change is explained. No magic, just rigorous engineering made accessible.
- **Elegance over complexity** – Sophisticated systems should feel simple. Our firmware runs a
  4-state machine with statistical analysis, but your experience is a single, reliable binary
  sensor.
- **Privacy by design** – We use mmWave radar, not cameras. All processing happens on-device. Your
  home is yours, not ours.
- **Built to last** – Both in durability and in the respect we show you. Comprehensive
  documentation. Open-source code. No planned obsolescence. No forced cloud subscriptions.

---

## 2. The Brand Promise

### What You'll Experience (Not Just What You'll Get)

**From the moment you open the box, you'll feel the difference.**

This isn't just another ESP32 project. This is a product built with the care usually reserved for
luxury goods. Clean packaging. Thoughtfully labeled components. Documentation that reads like it was
written for someone we respect—because it was.

**In your first five minutes, you'll know this works.**

Setup is frictionless. Flash the firmware, power on the device, and Home Assistant auto-discovers
it. No cryptic error messages. No hunting through forums. Within minutes, you'll see live telemetry
and realize: *this is how smart home products should be built*.

**For years to come, you'll trust it.**

This sensor doesn't just *detect* presence—it *understands* it. Using statistical analysis and
temporal filtering, it eliminates the false positives and negatives that plague other solutions.
Your lights won't turn off while you're sleeping. Your automations won't trigger when a fan turns
on. It just works. Every. Single. Time.

**And when you want to go deeper, we're with you.**

Every parameter—from statistical thresholds to debounce timers—is adjustable in real-time. A
calibration wizard guides you through baseline setup. Debug sensors show you exactly what the engine
is thinking. This is a product for people who want to understand their tools, not just use them.

---

## 3. Who This Is For (Aspirational Positioning)

### Primary Audience: The Thoughtful Builder

You're not just a "smart home user." You're someone who:

- **Values craft** – You can tell when something is built with care vs. shipped to hit a deadline.
- **Demands reliability** – You've been burned by "twitchy" PIR sensors and unreliable motion
  detectors. You're done with false positives.
- **Respects transparency** – You want to understand *why* a sensor makes a decision, not just trust
  a black box.
- **Protects privacy** – Cameras in the bedroom feel invasive. You want presence detection without
  surveillance.
- **Appreciates open systems** – You run Home Assistant because you believe in control,
  extensibility, and community.
- **Belongs to a community** – You read documentation. You contribute to forums. You believe that
  sharing knowledge makes everyone better.

### Secondary Audience: The Home Assistant Power User

You've built complex automations. You know what YAML is. You've tried other presence sensors and
been disappointed by their limitations. You're looking for something that:

- Integrates seamlessly with Home Assistant
- Offers runtime tunability without reflashing firmware
- Provides telemetry and transparency for debugging
- Can be adapted and extended for your unique setup

### What Unites Both Groups

**You're tired of "good enough." You want exceptional.**

You're willing to invest time in tools that reward that investment. You'd rather buy one product
that works perfectly than cycle through five that almost work. You believe that technology should
serve humans, not the other way around.

**If this resonates with you, you've found your people.**

---

## 4. The Product Experience Journey

### Act 1: Unboxing & First Impressions

**The box feels premium.** Simple design. Quality materials. No garish branding or marketing speak.

Inside, you find:
- The sensor unit (M5Stack + LD2410), pre-assembled or with thoughtfully labeled components
- A quick-start card with a QR code to the full documentation
- Cable and mounting hardware
- A handwritten note (in early batches): *"Thank you for believing in what we're building. — The
  OpticWorks Team"*

**First thought:** *This is different.*

### Act 2: The First Five Minutes

You plug in the sensor. Open ESPHome. Flash the firmware.

**No errors. No confusion. It just works.**

Home Assistant auto-discovers the device. You enter the API key (clearly documented). Within 60
seconds, you see:
- `binary_sensor.bed_occupied` (OFF)
- Live graphs of `still_energy` and `z_score`
- A `Presence State Reason` text sensor showing: `"IDLE - Awaiting signal (z=0.2 < k_on=9.0)"`

You sit on the bed. Three seconds later, the sensor switches to ON.

**Second thought:** *This is going to change everything.*

### Act 3: Understanding & Customization

Over the next few days, you explore the documentation. You discover:

- **The 4-state machine** – It doesn't just flip on and off. It *verifies* presence before
  committing to a state change.
- **The Absolute Clear Delay** – A brilliant solution to the "stillness problem." The sensor
  remembers recent high-confidence presence, so it won't turn off if you're lying perfectly still.
- **Z-score statistical analysis** – Instead of fixed energy thresholds, it learns your room's
  baseline and adapts. Works in any environment.
- **The calibration wizard** – A guided Home Assistant interface for baseline collection using
  MAD-based robust statistics. No command-line fumbling.

You realize: **This isn't just a sensor. It's a presence *engine*.**

### Act 4: Long-Term Trust

Weeks pass. Then months. The sensor has never once:
- Turned off your lights while you were sleeping
- Falsely triggered from a fan or pet
- Required you to adjust thresholds because the seasons changed

**You forget it's there. That's the highest compliment.**

When friends ask about your smart home, you tell them: *"The bed sensor? It's from OpticWorks. It
just works. I can't explain how rare that is."*

---

## 5. How Excellence Is Built (Technical Proof Points)

**Our brand makes a promise. Our engineering delivers on that promise.**

These aren't just features—they're the *evidence* that we obsess over craft.

### Proof Point 1: The 4-State Presence Engine

Most sensors are binary: ON or OFF. Ours uses a **state machine with verification stages**:

1. **IDLE** – Waiting for a signal strong enough to matter
2. **DEBOUNCING_ON** – Signal detected! Verifying it's sustained (3s default)
3. **PRESENT** – Confident someone is in bed. Tracking "last high-confidence" timestamp
4. **DEBOUNCING_OFF** – Signal dropped. Waiting to ensure they've actually left (5s default, plus
   30s absolute clear guard)

**Why this matters:** No "twitchy" behavior. No false triggers from momentary noise. The sensor is
*deliberate*, just like your decision to trust it.

### Proof Point 2: Statistical Intelligence

We don't use fixed energy thresholds. We use **z-score normalization**:

```
z_score = (current_energy - baseline_mean) / baseline_stddev
```

The sensor learns what "empty" looks like in *your* room, then only reacts to **statistically
significant changes**.

**Why this matters:** Works in any environment. Different rooms, different hardware, different
seasons—the algorithm adapts. No guesswork. No "tweaking until it works."

### Proof Point 3: The Absolute Clear Delay

The hardest problem in presence detection: **detecting someone who is perfectly still.**

Our solution: After entering the PRESENT state, the sensor tracks the last time it saw
high-confidence presence. Even if the signal drops (you're motionless), it won't clear the room
until **30 seconds have passed since the last strong signal**.

**Why this matters:** Your lights won't turn off while you're sleeping. Ever. This is the kind of
thoughtful engineering that separates "shipped" from "crafted."

### Proof Point 4: Hysteresis by Design

We use **two separate thresholds**:
- **k_on = 9.0** (Turn on when signal is 9 standard deviations above baseline)
- **k_off = 4.0** (Turn off when signal drops below 4 standard deviations)

This creates a "stability zone" that prevents the sensor from flapping between states when the
signal hovers near a single threshold.

**Why this matters:** Systems engineering 101. We built this the *right* way, not the fast way.

### Proof Point 5: Privacy by Design

- **No camera.** mmWave radar detects *that* someone is present, not *who* or *what* they're doing.
- **No cloud.** All processing happens on the ESP32. Your data never leaves your home.
- **No telemetry.** We don't track you. We don't sell your data. The firmware is open-source—verify
  it yourself.

**Why this matters:** Privacy isn't a feature. It's a fundamental right. We designed the system so
that respecting your privacy was the *only* option.

### Proof Point 6: Runtime Tunability

Every parameter—thresholds, timers, distance windows—is a **Home Assistant `number` entity**. Adjust
them in real-time. See the effects immediately. No recompiling. No reflashing.

**Why this matters:** You shouldn't need a computer science degree to customize your smart home. We
made the complex accessible.

### Proof Point 7: Transparent Decision-Making

Two text sensors expose the engine's internal reasoning:

- **Presence State Reason** – *"DEBOUNCING_ON: t=1.2s/3.0s, z=12.3 >= k_on=9.0"*
- **Presence Change Reason** – *"Transitioned IDLE → DEBOUNCING_ON: High signal sustained"*

**Why this matters:** You're not debugging a black box. You're partnering with a system that
respects your intelligence.

---

## 6. Tone & Voice Guidelines

### Brand Personality

- **Confident, not arrogant** – We know we've built something exceptional, but we're not dismissive
  of others.
- **Warm, not corporate** – We're real people who care deeply about craft. Write like a founder
  talking to a fellow builder over coffee.
- **Technical, but human** – We embrace complexity in our engineering, but our communication is
  clear and accessible.
- **Aspirational, not elitist** – We're building a community of people who care about quality. The
  barrier to entry is values, not wealth or credentials.

### Language Patterns to Use

- **Story-driven** – Lead with "why," not "what."
- **Sensory** – Help people *feel* the experience. "The box feels premium." "Within 60 seconds, you
  see..."
- **Specific** – Use concrete details. "3 seconds" not "quickly." "z-score normalization" not "smart
  algorithms."
- **Inclusive "you"** – Address the reader directly. Make them the protagonist of the story.

### Language Patterns to Avoid

- **Hype** – No "revolutionary," "groundbreaking," or "game-changing."
- **Marketing superlatives** – No "best," "ultimate," or "perfect."
- **Jargon without context** – If you use a technical term, explain it in human terms.
- **Apologizing** – No "we're just a small team" or "we hope you like it." Confidence without
  arrogance.

---

## 7. Content Blocks for Landing Page

### Hero Section

**Headline:** *Technology That Earns Your Trust*

**Subheadline:** *A bed presence sensor built with the craft and care usually reserved for luxury
goods. No false positives. No privacy invasion. No compromises.*

**Visuals:** Hero image of the sensor unit on a clean, minimalist nightstand. Soft lighting.
Premium feel. (Not a "tech product shot"—an *aspirational lifestyle shot*.)

**CTA:** *Reserve Yours* | *See How It Works*

---

### Section 1: The Story

**Headline:** *Built for People Who Refuse to Settle*

**Body:**

> Every night, millions of people are let down by smart home devices that should just work. Lights
> turn off while you're sleeping. Sensors trigger falsely. Privacy feels compromised.
>
> We founded OpticWorks because we believe you deserve better.
>
> This isn't just another ESP32 project. It's a sensor built with the care of a craftsperson—where
> every detail, from the unboxing experience to the calibration wizard, reflects our commitment to
> excellence.
>
> If you're tired of "good enough," you've found your people.

**Visuals:** Close-up of the product. Hands holding the unit. A sense of craft and care.

---

### Section 2: The Experience

**Headline:** *From Unboxing to Bedtime, You'll Feel the Difference*

**Three-column layout:**

**Column 1: First Five Minutes**
- Icon: Stopwatch
- Text: *Frictionless setup. Auto-discovery in Home Assistant. Live telemetry in under 60 seconds.
  You'll know it works before you finish your coffee.*

**Column 2: First Five Days**
- Icon: Dashboard/Graph
- Text: *Explore the 4-state engine, adjust thresholds in real-time, and run the guided calibration
  wizard. Every parameter is tunable. Every decision is transparent.*

**Column 3: First Five Months**
- Icon: Checkmark/Shield
- Text: *Forget it's there. No false positives. No false negatives. Your lights won't turn off while
  you're sleeping. Ever. That's the OpticWorks promise.*

---

### Section 3: How Excellence Is Built

**Headline:** *Our Engineering Is the Proof of Our Promise*

**Expandable accordion or tabs for each proof point:**

1. **The 4-State Presence Engine** – *(Diagram of state machine)* "Most sensors are binary. Ours
   *verifies* presence before committing to change."
2. **Statistical Intelligence** – *(Graph of z-score over time)* "We don't use fixed thresholds. We
   learn your room's baseline and adapt."
3. **The Absolute Clear Delay** – *(Timeline showing high-confidence tracking)* "Solves the
   'stillness problem' so your lights won't turn off while you sleep."
4. **Privacy by Design** – *(Icon: mmWave radar vs. camera with X)* "No cameras. No cloud. All
   processing on-device."
5. **Runtime Tunability** – *(Screenshot of HA dashboard)* "Every parameter adjustable. No
   reflashing. See changes instantly."
6. **Transparent Reasoning** – *(Screenshot of debug text sensor)* "Understand every decision. No
   black boxes."

---

### Section 4: Who This Is For

**Headline:** *Built for Thoughtful Builders*

**Body:**

> You run Home Assistant because you believe in control, not convenience-theater. You've been burned
> by unreliable motion sensors. You value privacy, transparency, and open systems.
>
> You're willing to invest time in tools that reward that investment. You'd rather buy one product
> that works perfectly than cycle through five that almost work.
>
> If this sounds like you, welcome home.

**Visuals:** Community-focused imagery. People collaborating, tinkering, building. Not "stock photo
users"—real enthusiasts.

---

### Section 5: What You Get

**Headline:** *Everything You Need to Succeed*

**Checklist format:**

- ✅ Pre-assembled sensor unit (M5Stack + LD2410) or DIY kit with labeled components
- ✅ ESPHome firmware (open-source, fully documented)
- ✅ Home Assistant integration with auto-discovery
- ✅ Lovelace dashboard with live graphs, tuning controls, and calibration wizard
- ✅ Comprehensive documentation (quickstart, architecture deep-dive, troubleshooting runbooks)
- ✅ 16 unit tests + E2E integration tests (you can verify the quality yourself)
- ✅ Lifetime access to firmware updates and community support

**No subscriptions. No cloud lock-in. No planned obsolescence.**

---

### Section 6: Social Proof (Once Available)

**Headline:** *Trusted by the Home Assistant Community*

**Format:** Testimonial cards with avatars, names, and quotes

> *"I've tried every presence sensor on the market. This is the first one that just works. The
> documentation alone is worth the price."*
> — Alex M., Home Assistant Forum

> *"The unboxing experience made me feel like I was opening an Apple product. Then the engineering
> made me realize this is even better—because it's open and I can understand every decision it
> makes."*
> — Jordan K., /r/homeassistant

> *"My lights haven't turned off while I'm sleeping in 6 months. I literally forget the sensor is
> there. That's the highest praise I can give."*
> — Sam T., GitHub Contributor

---

### Section 7: Frequently Asked Questions

**Q: Is this just another ESP32 project I could build myself?**

A: Technically, yes—the firmware is open-source. But this is about more than the BOM. It's the
months of engineering that went into the 4-state machine, the statistical analysis, the calibration
wizard, and the documentation. It's the unboxing experience, the pre-flashed firmware, and the
confidence that it will just work. You're not just buying components—you're buying our obsession
with craft.

**Q: Why mmWave radar instead of a camera or pressure mat?**

A: Privacy and reliability. Cameras feel invasive in a bedroom. Pressure mats fail when you shift
position or if your partner gets up first. mmWave radar detects presence without surveillance, and
because we focus on *still energy*, it's immune to false triggers from fans, pets, or motion outside
the bed.

**Q: Can I customize this for a different use case (e.g., desk presence, bathroom occupancy)?**

A: Absolutely. The engine is designed to generalize. The current baseline defaults (μ=6.7%, σ=3.5%,
k_on=9.0, k_off=4.0) are tuned for bed presence, but every parameter is runtime-adjustable. Run the
calibration wizard for your specific zone, tune the thresholds, and you're set. The documentation
includes guidance for different scenarios.

**Q: What if I need help or something goes wrong?**

A: We've built comprehensive troubleshooting runbooks (`docs/troubleshooting.md`) and a detailed
quickstart guide. If you're stuck, the Home Assistant community is incredibly supportive. And
because the firmware is open-source, you can always inspect the code and understand what's
happening. We're also building a community forum for OpticWorks users.

**Q: Do you have a return policy?**

A: [Details TBD based on sales model] Our goal is for you to be delighted, not just satisfied. If
the sensor doesn't meet your expectations in the first 30 days, we'll make it right.

---

### Section 8: Call to Action

**Headline:** *Join the Community of Thoughtful Builders*

**Body:**

> This is more than a product launch. It's an invitation to be part of a movement—a community of
> people who believe that technology should be crafted, not just shipped.
>
> We're starting with a bed presence sensor. But our vision is bigger: a suite of smart home devices
> built with the same care, transparency, and respect for your intelligence.
>
> Be one of the first.

**CTA Buttons:**
1. **Primary:** *Reserve Your Sensor* (Large, prominent)
2. **Secondary:** *Read the Documentation* (Link to GitHub/docs site)
3. **Tertiary:** *See the Code* (Link to GitHub repo)

**Footer:** *"Built with care by the OpticWorks team. Open-source. Privacy-first. No compromises."*

---

## 8. Visual & Design Guidelines

### Photography Style

- **Premium, not clinical** – Think Apple product photography, but warmer. Soft lighting, real
  environments, not white-box sterile.
- **Lifestyle context** – Show the sensor on a nightstand, next to a book and a lamp. Make it
  aspirational but attainable.
- **Close-ups that show craft** – Component details, clean PCB layouts, thoughtful cable management.
- **Avoid "tech bro" aesthetics** – No RGB LEDs, no aggressive fonts, no "gamer" vibes. This is for
  adults who value quality.

### Dashboard & UI Screenshots

- **Home Assistant integration front and center** – Show the Lovelace dashboard with live graphs,
  the calibration wizard, and tuning controls.
- **Annotate key features** – Use subtle arrows or highlights to draw attention to the debug text
  sensor, z-score graph, state machine status.
- **Show state transitions** – A before/after or video showing the sensor moving through IDLE →
  DEBOUNCING_ON → PRESENT states.

### Diagrams

- **The 4-state machine diagram** (already in current brief) is essential. Make it beautiful—clean
  lines, thoughtful typography, consistent with brand aesthetics.
- **Z-score visualization** – A graph showing baseline (μ), standard deviations (σ), and a signal
  crossing the k_on threshold.
- **Timeline of Absolute Clear Delay** – Visual representation of how the sensor tracks
  "last_high_confidence" and waits 30s before clearing.

### Typography & Color Palette

- **Font:** Clean, modern sans-serif (e.g., Inter, SF Pro, or similar). Avoid overly technical
  "monospace everywhere" but use monospace sparingly for code snippets.
- **Colors:**
  - **Primary:** Deep, confident blue (trust, reliability)
  - **Accent:** Warm amber/gold (craft, quality)
  - **Background:** Off-white or light gray (not stark white—softer, more premium)
  - **Text:** Charcoal (not pure black—easier on the eyes)

---

## 9. Acquisition Strategy: PLG + MLG Flywheel

### Product-Led Growth (Primary)

**The product experience is the primary acquisition engine.**

1. **Frictionless onboarding** – Setup in under 5 minutes creates immediate trust.
2. **"Aha moment" velocity** – Users see the sensor work flawlessly within the first hour.
3. **Built-in virality** – Users show off their HA dashboards in forums, Reddit, Discord. The
   transparent debug sensors and beautiful graphs make the product "shareable."
4. **Documentation as marketing** – Our docs are so good that people link to them even if they
   haven't bought the product. This builds brand authority.

### Marketing-Led Growth (Secondary)

**High-quality content amplifies the product experience.**

1. **Launch blog post** – "Why We Built OpticWorks: A Love Letter to Thoughtful Engineering"
   (founder story)
2. **Technical deep-dive** – "How the 4-State Presence Engine Works" (shareable on Hacker News,
   Reddit /r/homeassistant)
3. **Comparison content** – "We Tested 12 Presence Sensors. Here's What We Learned." (Honest,
   respectful of competitors, but showing why we're different)
4. **Community engagement** – Active participation in Home Assistant forums, Discord, Reddit.
   Helping users, answering questions, sharing knowledge.
5. **Video content** – YouTube tutorial: "Setting Up Your First OpticWorks Sensor" + behind-the-
   scenes: "A Day in the Life of Building OpticWorks"

### Flywheel Effect

```
Exceptional Product → User Delight → Community Advocacy → Brand Awareness → New Users → Feedback →
Improved Product → [Repeat]
```

---

## 10. Success Metrics (Post-Launch)

### Product-Led Indicators

- **Time to first successful detection** (Target: <5 minutes)
- **Time to "aha moment"** (User sees reliable presence detection in real-world use)
- **Support ticket volume** (Lower is better—indicates intuitive product)
- **GitHub stars, forks, and community contributions** (Proxy for product love)

### Marketing-Led Indicators

- **Documentation page views** (Indicates content is driving discovery)
- **Referral sources** (Reddit, Home Assistant forums, Hacker News—shows community sharing)
- **Qualitative testimonials** (Unprompted user posts about the product)
- **Net Promoter Score (NPS)** (Target: >50)

### Brand Health

- **"Loved, not just used"** – Track sentiment analysis of community mentions. Are people saying
  "it's reliable" or "I love this thing"?
- **Pricing power** – Can we maintain premium pricing without constant discounting?
- **Repeat purchase intent** – When we launch the next product, do existing customers buy
  immediately?

---

## 11. Competitive Positioning

### We Don't Compete on Price

We compete on **value delivered per unit of trust**. Our customers aren't looking for the cheapest
sensor—they're looking for the *right* sensor. They've already been burned by cheap solutions that
don't work.

### We Don't Compete on Features Alone

Every feature we list is table-stakes in a world of spec-sheet marketing. What differentiates us is
**how those features come together into a coherent experience**—from unboxing to long-term trust.

### We Compete on Brand

- **Patagonia for smart home devices** – You're buying into a philosophy, not just a product.
- **Apple's attention to detail + open-source ethos** – Premium experience without lock-in.
- **The anti-Kickstarter** – We ship quality, not promises. No vaporware. No "coming soon" features.

---

## 12. Post-Purchase Experience

### Onboarding Email Sequence

**Email 1 (Immediately after purchase):** *"Welcome to OpticWorks"*
- Thank you
- What to expect (shipping timeline)
- Link to pre-read the quickstart guide

**Email 2 (When shipped):** *"Your sensor is on the way"*
- Tracking info
- Reminder: firmware is open-source, you can browse the code while you wait

**Email 3 (3 days after delivery):** *"How's your first week going?"*
- Check-in
- Link to calibration wizard guide
- Invitation to share feedback

**Email 4 (30 days after delivery):** *"You're part of the story"*
- Request for testimonial (if they're happy)
- Early access to next product (if/when available)
- Invitation to GitHub community or forum

### Community Building

- **GitHub Discussions** – For technical Q&A, feature requests, and show-and-tell
- **Discord or Slack** (optional) – Real-time community support and sharing
- **Monthly "Build Log"** – Transparent updates from the team on what we're working on (even if it's
  not ready to ship)

---

## 13. Long-Term Brand Extensions

**This sensor is the beginning, not the end.**

Once we've proven the model with bed presence, we expand to:

1. **Desk presence sensor** – For home office automations
2. **Multi-zone presence** – Whole-home coverage with a unified dashboard
3. **"OpticWorks Calibration Hub"** – A premium HA integration that manages multiple sensors,
   provides analytics, and suggests optimizations
4. **Hardware mounting kits** – Beautiful, minimal, 3D-printed mounts that match the product's
   aesthetic

**Each new product reinforces the brand promise:** *Thoughtfully crafted. Privacy-first. Built to
earn your trust.*

---

## 14. Final Note for the Web Team

**This brief is a strategic blueprint, not a pixel-perfect spec.**

The goal is to *feel* the brand in every sentence, every image, every interaction. When in doubt:

- **Lead with story, not specs.**
- **Make the user the hero, not the product.**
- **Use technical excellence as proof, not the pitch.**
- **Write like you're talking to a fellow builder you respect.**

If the landing page makes someone say, *"This is what I've been looking for,"* we've succeeded.

If it makes them say, *"I want to be part of this,"* we've built something that lasts.

---

**Document Version:** 2.0 (Brand-Led Strategic Rework)
**Last Updated:** 2025-11-12
**Author:** OpticWorks Brand & Strategy Team
