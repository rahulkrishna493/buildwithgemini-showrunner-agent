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

"""Showrunner Agent: Executive Producer for Tech & AI Talk Shows and Podcasts."""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from .a2ui_prompt import SHOWRUNNER_A2UI_INSTRUCTION
from .a2ui_utils import a2ui_callback
from .image_gen import generate_episode_thumbnail_image
from .tools import (
    calculate_episode_pacing,
    generate_youtube_seo_pack,
    lookup_trending_ai_topics,
)

MODEL = "gemini-3.8-flash"


# WRITE callback: after each turn, summarize and store durable context into Memory Bank
async def generate_memories_callback(callback_context: CallbackContext):
    """Write session context to Vertex AI Memory Bank for long-term recall if available."""
    try:
        await callback_context.add_session_to_memory()
    except (ValueError, AttributeError):
        # Gracefully pass when runner is using default in-memory session without a Memory Bank service
        pass
    return None


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SHOWRUNNER_A2UI_INSTRUCTION,
    tools=[
        PreloadMemoryTool(),
        calculate_episode_pacing,
        lookup_trending_ai_topics,
        generate_youtube_seo_pack,
        generate_episode_thumbnail_image,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
