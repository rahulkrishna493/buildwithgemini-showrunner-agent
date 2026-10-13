# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for the Showrunner Agent (Tech & AI Talk Show Producer)."""

from typing import Dict, Any, List


def calculate_episode_pacing(target_duration_minutes: int, segment_types: str = "standard") -> Dict[str, Any]:
    """Calculates ideal timestamp pacing, segment breakdown, and ad-break cue points.

    Args:
        target_duration_minutes: The planned total episode length in minutes (e.g. 30, 45, 60).
        segment_types: Format style ('standard', 'interview_heavy', 'news_roundup').

    Returns:
        A dictionary with segment durations, timestamp cues, and percentage allocations.
    """
    total_sec = max(10, target_duration_minutes) * 60
    
    if segment_types == "interview_heavy":
        cold_open = int(total_sec * 0.05)
        intro = int(total_sec * 0.08)
        sponsor_1 = int(total_sec * 0.03)
        main_interview = int(total_sec * 0.60)
        sponsor_2 = int(total_sec * 0.03)
        audience_qa = int(total_sec * 0.15)
        outro = total_sec - (cold_open + intro + sponsor_1 + main_interview + sponsor_2 + audience_qa)
        
        segments = [
            {"segment": "Hook / Cold Open", "duration_sec": cold_open, "cue": "00:00"},
            {"segment": "Show Intro & Guest Intro", "duration_sec": intro, "cue": f"{cold_open // 60:02d}:{cold_open % 60:02d}"},
            {"segment": "Sponsor Break #1", "duration_sec": sponsor_1, "cue": f"{(cold_open + intro) // 60:02d}:00"},
            {"segment": "Deep Dive Guest Interview", "duration_sec": main_interview, "cue": f"{(cold_open + intro + sponsor_1) // 60:02d}:00"},
            {"segment": "Midroll Sponsor Break #2", "duration_sec": sponsor_2, "cue": f"{(cold_open + intro + sponsor_1 + (main_interview // 2)) // 60:02d}:00"},
            {"segment": "Audience Q&A / Lightning Round", "duration_sec": audience_qa, "cue": f"{(total_sec - outro - audience_qa) // 60:02d}:00"},
            {"segment": "Key Takeaways & Outro Call-To-Action", "duration_sec": outro, "cue": f"{(total_sec - outro) // 60:02d}:00"},
        ]
    else:
        # Standard Tech Talk Show
        cold_open = int(total_sec * 0.05)
        headline_news = int(total_sec * 0.25)
        paper_of_the_week = int(total_sec * 0.35)
        sponsor = int(total_sec * 0.05)
        ai_tool_showcase = int(total_sec * 0.20)
        outro = total_sec - (cold_open + headline_news + paper_of_the_week + sponsor + ai_tool_showcase)
        
        segments = [
            {"segment": "Teaser / Cold Open", "duration_sec": cold_open, "cue": "00:00"},
            {"segment": "AI Headlines & Industry Pulse", "duration_sec": headline_news, "cue": f"{cold_open // 60:02d}:{cold_open % 60:02d}"},
            {"segment": "Deep Dive / Paper of the Week", "duration_sec": paper_of_the_week, "cue": f"{(cold_open + headline_news) // 60:02d}:00"},
            {"segment": "Sponsor Read / Community Shoutout", "duration_sec": sponsor, "cue": f"{(cold_open + headline_news + paper_of_the_week) // 60:02d}:00"},
            {"segment": "Hands-on AI Tool Showcase", "duration_sec": ai_tool_showcase, "cue": f"{(cold_open + headline_news + paper_of_the_week + sponsor) // 60:02d}:00"},
            {"segment": "Wrap-up & Next Episode Tease", "duration_sec": outro, "cue": f"{(total_sec - outro) // 60:02d}:00"},
        ]

    return {
        "target_duration_minutes": target_duration_minutes,
        "format": segment_types,
        "total_seconds": total_sec,
        "segments": segments,
    }


def lookup_trending_ai_topics(category: str = "all") -> Dict[str, Any]:
    """Fetches trending themes, breakthrough papers, and discussion starters in Tech & AI.

    Args:
        category: Filter by area: 'models', 'robotics', 'agents', 'open_source', or 'all'.

    Returns:
        Curated topic summaries, controversy angles, and recommended talking points.
    """
    topics = [
        {
            "topic": "Reasoning Models vs Chain-of-Thought Inference Scaling",
            "category": "models",
            "summary": "How test-time compute is replacing pure pre-training scaling laws, and what that means for developers.",
            "talking_points": [
                "Why spend compute at generation time rather than just parameter count?",
                "Latency vs reasoning depth tradeoffs in user-facing products.",
                "How smaller distilled models compare against giant frontier clusters."
            ],
            "recommended_hook": "Are scaling laws hitting a wall, or did we just look in the wrong place?"
        },
        {
            "topic": "Multi-Agent Systems & A2A (Agent-to-Agent Protocols)",
            "category": "agents",
            "summary": "Autonomous agents coordinating via open standards like Google A2A and MCP protocols.",
            "talking_points": [
                "Single agent with many tools vs orchestrator with specialized subagents.",
                "Handling trust, delegation, and security when agents speak to third-party endpoints.",
                "Real enterprise deployments beyond toy hackathon demos."
            ],
            "recommended_hook": "Why your next API might not be for humans, but for an autonomous agent fleet."
        },
        {
            "topic": "Edge AI & Small Language Models on Device",
            "category": "open_source",
            "summary": "Running high-performance 2B-9B parameter models locally on laptops, phones, and robotics chips.",
            "talking_points": [
                "Privacy and zero-latency local processing.",
                "Quantization techniques (4-bit, 2-bit, speculative decoding).",
                "Developer battery and memory constraints."
            ],
            "recommended_hook": "Could the most impactful AI of 2026 be running entirely offline on your phone?"
        }
    ]
    
    if category != "all":
        filtered = [t for t in topics if t["category"] == category]
        return {"category": category, "topics": filtered or topics}
    return {"category": "all", "topics": topics}


def generate_youtube_seo_pack(topic: str, target_audience: str = "tech professionals") -> Dict[str, Any]:
    """Generates high-CTR YouTube titles, description hooks, chapter structures, and tags.

    Args:
        topic: The primary subject of the episode (e.g. 'Agentic AI Workflows', 'Gemini 3 Flash').
        target_audience: The audience persona (e.g. 'developers', 'founders', 'curious general tech').

    Returns:
        A package of click-worthy title options, thumbnail visual cues, and tags.
    """
    clean_topic = topic.strip().title()
    return {
        "topic": clean_topic,
        "target_audience": target_audience,
        "title_options": [
            f"The Real Truth About {clean_topic} (Deep Dive)",
            f"Why {clean_topic} Changes Everything For Developers in 2026",
            f"I Tested {clean_topic} So You Don't Have To",
            f"{clean_topic}: Genius Architecture or Overhyped Trend?",
            f"How to Actually Build With {clean_topic} (Step-by-Step Breakdown)"
        ],
        "thumbnail_visual_concepts": [
            f"Split screen: Host looking skeptical on left, dramatic neon architectural diagram of {clean_topic} on right. High contrast text: 'IT ACTUALLY WORKS?'.",
            f"Minimalist tech aesthetic: Giant bold text '{clean_topic}' with glowing futuristic hardware/chip motif in dark studio lighting.",
            f"Side-by-side performance speed graph showing massive leap, host pointing with shocked expression."
        ],
        "suggested_tags": [
            "ai", "artificial intelligence", "tech podcast", "machine learning",
            clean_topic.lower(), f"{clean_topic.lower()} tutorial", "deep tech", "google gemini", "developer"
        ],
        "pinned_comment_prompt": f"What's your biggest takeaway on {clean_topic}? Let us know your thoughts below—we're reading every reply!"
    }
