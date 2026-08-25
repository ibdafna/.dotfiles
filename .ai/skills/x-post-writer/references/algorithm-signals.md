# X Algorithm Ranking Signals Reference

This document contains detailed information about how the X "For You" algorithm ranks posts, based on analysis of the open-source recommendation algorithm.

## Algorithm Architecture

The system uses a two-stage pipeline:

1. **Candidate Retrieval** - Pulls posts from followed accounts (in-network) + similar content via embedding search (out-of-network)
2. **ML Ranking** - A transformer model predicts engagement probabilities for 19 actions per post, ranking primarily by P(favorite/like)

## The 19 Engagement Signals

The model predicts probabilities for these engagement types:

### Positive Signals (Boost Visibility)

| Signal | Description | Impact |
|--------|-------------|--------|
| `favorite_score` | Likes | **PRIMARY ranking signal** - posts sorted by this |
| `reply_score` | Replies/comments | High-intent engagement |
| `repost_score` | Retweets/shares | Viral signal, reaches new audiences |
| `quote_score` | Quote tweets | Higher weight than simple retweets |
| `click_score` | General clicks | Engagement indicator |
| `profile_click_score` | Clicks to view author | Interest in creator |
| `vqv_score` | Video quality view | Video engagement metric |
| `photo_expand_score` | Photo expansion | Image engagement metric |
| `share_score` | Direct sharing | Distribution signal |
| `share_via_dm_score` | DM shares | Private recommendation signal |
| `share_via_copy_link_score` | Link copying | Off-platform sharing |
| `dwell_score` | Time spent viewing | Attention metric |
| `dwell_time` | Duration metric | Scroll-stopping power |
| `follow_author_score` | Following post author | Strong creator interest |

### Negative Signals (Reduce Visibility)

| Signal | Description | Impact |
|--------|-------------|--------|
| `not_interested_score` | "Not interested" clicks | Learned negative weight |
| `block_author_score` | Blocking author | Strong negative signal |
| `mute_author_score` | Muting author | Negative signal |
| `report_score` | Reports/flags | Content quality penalty |

## Hard Filters (Complete Elimination)

Posts are completely removed before ML scoring if:
- From blocked authors
- Contain muted keywords
- Deleted/spam/violence/gore content
- Previously seen
- User's own posts (self-posts)
- Paywalled content user can't access
- Too old (age threshold)

## Soft Penalties

- **Author diversity** - Repeated posts from same author get attenuated
- **Conversation deduplication** - Multiple branches of same thread reduced
- **Negative engagement history** - Past blocks/mutes/reports on similar content

## Out-of-Network Discovery

The Phoenix retrieval system finds similar content via embeddings:
- User's engagement history creates a preference profile
- Two-tower model: user tower (user + history) vs candidate tower (all posts)
- Dot product similarity finds matching content
- Reposts/quotes from different networks expand reach

## What's NOT Explicitly in the Model

These are NOT hard-coded features (may be learned implicitly):
- Hashtags
- Tweet length
- Time of posting
- Follower counts
- Verification status
- Specific keywords
- URL domains

## Key Architectural Insights

1. **Candidate Isolation** - Each post scored independently; no batch effects
2. **ML-First** - No hand-engineered ranking rules; transformer learns everything
3. **Multi-Signal Learning** - 19 engagement types allow nuanced preference learning
4. **User Context is Everything** - Full engagement history used to understand preferences
