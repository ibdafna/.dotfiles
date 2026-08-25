---
name: x-post-writer
description: Write effective X (Twitter) posts optimized for the "For You" algorithm. This skill should be used when the user wants to craft posts, threads, or content for X that maximizes visibility and engagement. Triggers on requests to write tweets, X posts, or social media content for Twitter/X.
---

# X Post Writer

## Overview

This skill transforms prompts into algorithm-optimized X posts. It applies knowledge of the X recommendation algorithm's ranking signals to craft posts that maximize visibility in the "For You" feed.

## Core Principles

The X algorithm ranks posts primarily by **predicted likelihood of getting a like**, with secondary signals from replies, reposts, quotes, and dwell time. To write effective posts:

### 1. Optimize for Engagement Signals

**Primary target: Likes** - The algorithm literally sorts by P(like). Content must be likeable.

**Secondary targets (in order of impact):**
- Replies - Ask questions, invite discussion, make debatable points
- Reposts/Quotes - Create shareable, quotable content
- Dwell time - Make people stop scrolling and read

### 2. Structure for Dwell Time

The algorithm tracks how long users pause on content. To maximize dwell:

- **Strong opening line** - Hook that stops the scroll
- **Line breaks** - White space slows reading, increases dwell
- **Progressive revelation** - Build to a payoff
- **Optimal length** - Long enough to engage, short enough to finish

### 3. Encourage Specific Actions

Each post should have a clear engagement goal:

| Goal | Technique |
|------|-----------|
| Likes | Relatable observations, useful tips, satisfying insights |
| Replies | Questions, controversial takes, "fill in the blank" |
| Quotes | Strong opinions others want to add commentary to |
| Reposts | Universally useful info, humor, "save for later" value |

### 4. Avoid Negative Signals

Posts that trigger these responses get demoted:
- "Not interested" clicks - Avoid irrelevant/off-topic content
- Mutes - Don't be repetitive or spam one topic
- Blocks - Don't be hostile or harassing
- Reports - Stay within guidelines, avoid rage-bait

## Post Writing Process

When asked to write an X post:

1. **Clarify the goal** - What action should readers take? (like, reply, share, click)
2. **Identify the hook** - What stops the scroll?
3. **Structure for dwell** - Use line breaks, build tension
4. **Add engagement trigger** - Question, CTA, or quotable statement
5. **Review for negative signals** - Remove anything that could trigger mute/block/report

## Post Formats

### Single Post (280 chars)

```
[Hook line - stops the scroll]

[Core value/insight]

[Engagement trigger - question or CTA]
```

### Thread Opener

```
[Controversial or curiosity-driving hook]

[Promise of value: "Here's what I learned:" / "Thread:"]
```

### Engagement Post

```
[Relatable observation or question]

[Optional: your take]

[Direct question to audience]
```

### Value Post

```
[Useful tip or insight]

[Brief explanation why it works]

[Invitation to save/share]
```

## Examples

### Prompt: "Write a post about productivity"

**Weak (no optimization):**
> Productivity tip: make a to-do list every morning.

**Strong (algorithm-optimized):**
> The most productive people I know don't use to-do lists.
>
> They use a "done list" instead.
>
> Write down what you accomplished at the end of each day. You'll be shocked how much more motivated you become.
>
> What's your unconventional productivity hack?

**Why it works:**
- Hook contradicts expectations (scroll stop)
- Line breaks increase dwell time
- Provides genuine value (likeable)
- Ends with question (reply trigger)
- "Unconventional" invites quotable responses

### Prompt: "Write a post about learning to code"

**Weak:**
> Learning to code is hard but worth it. Just keep practicing!

**Strong:**
> I learned to code at 35 with two kids and a full-time job.
>
> 6 months later, I built an app that makes $2k/month.
>
> The secret wasn't "10,000 hours." It was 30 minutes a day, every day, no exceptions.
>
> If you're starting late, this is your sign.

**Why it works:**
- Specific, relatable hook
- Concrete results (credibility)
- Counterintuitive insight (quotable)
- Emotional payoff (likeable, shareable)

## Thread Guidelines

For multi-post threads:

1. **First post must stand alone** - Hook + promise of value
2. **Each post should be valuable independently** - People drop off
3. **Use numbers** - "5 things I learned" creates commitment
4. **End with engagement ask** - "Which resonated most?"

## Media Optimization

The algorithm has separate scoring for media engagement:

- **Images**: Use visuals that invite expansion (charts, infographics, before/after)
- **Videos**: Optimize for watch time, not just views; hook in first 3 seconds
- **No media**: Can still perform well if text is compelling

## Reference

For detailed algorithm signal information, see `references/algorithm-signals.md`.
