# 000 – Project Overview

## Product Name
**AI Content Radar**

## Purpose
AI Content Radar is an AI-powered YouTube content discovery engine designed for social media and short-form content teams. It automatically surfaces viral videos, discussion-heavy content, and emerging trends — providing daily ranked lists that editors can act on immediately.

## Background & Problem
Social media teams currently discover content manually, which is time-consuming, inconsistent, and prone to missing early signals. There is no systematic way to identify which YouTube videos are trending before they peak, which ones spark high debate, or which channels are rising.

## Solution
A fully automated backend pipeline that:
- Crawls curated YouTube channels and keyword searches on a daily/weekly schedule
- Computes a **Buzz Score** (virality potential) and **Discussion Score** (debate intensity) for each video
- Detects viral spikes by comparing a video's velocity against its channel average
- Clusters videos into topic groups and tracks trend velocity
- Exposes a clean REST API consumed by a Next.js dashboard

## Target Users
| User | Need |
|---|---|
| Content Editor | Daily ranked list of high-potential videos |
| Social Media Manager | Trend clusters to plan weekly content calendar |
| Channel Scout | Newly discovered channels with high-growth signals |

## MVP Scope (Phase 1)
- Crawl curated channel list
- Compute Buzz Score and Discussion Score
- Detect viral spikes
- Generate daily rankings
- Expose 5 REST API endpoints
- Next.js frontend dashboard

## Phase 2
- AI Trend Detection (TF-IDF + sentence-transformers + HDBSCAN)
- Trend velocity tracking
- Topic cluster UI

## Success Metrics
- Coverage: ≥ 500 videos crawled per day from curated channels
- Freshness: Rankings updated within 1 hour of daily crawl completion
- Accuracy: Buzz Score correlates with actual viral outcomes (manual QA)
- Performance: API response time < 500 ms (cached)

## Constraints
- YouTube Data API quota: must stay within 10,000 units/day
- Comments fetched only for Top 20 videos (200 comments each) to save quota
- Rankings cached in Redis for 24 hours
