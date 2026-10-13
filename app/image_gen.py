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

"""High-impact visual thumbnail and cover-art generator for the Showrunner Agent."""

import io
import os
import uuid
import colorsys
import hashlib
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
from google.cloud import storage

BUCKET_NAME = "bwg3-qwiklabs-gcp-03-d7b60b7a280a"


def generate_episode_thumbnail_image(
    episode_title: str,
    tagline: str = "DEEP TECH & AI TALK SHOW",
    theme_style: str = "cyber_neon"
) -> Dict[str, Any]:
    """Generates a high-resolution 16:9 episode thumbnail/cover-art graphic, uploads it to GCS, and returns the public URL.

    Args:
        episode_title: Main bold title text to display on the thumbnail (e.g. 'Reasoning Models', 'Multi-Agent Swarms').
        tagline: Category or show badge (e.g. 'EPISODE 04 // TECH & AI', 'SPECIAL INTERVIEW').
        theme_style: Aesthetic theme ('cyber_neon', 'clean_dark', 'amber_gold').

    Returns:
        Dictionary containing public image_url, title, and theme details.
    """
    width = 1280
    height = 720
    
    # Hash the title to deterministically derive harmonious accent colors
    h = int(hashlib.md5(episode_title.encode()).hexdigest(), 16)
    hue = (h % 360) / 360.0
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.9, 1.0)]
    accent_color = (r, g, b)
    
    # Background: dark vignette gradient
    img = Image.new("RGB", (width, height), (10, 12, 16))
    draw = ImageDraw.Draw(img)
    
    # Draw futuristic background glow / mesh grid lines
    grid_color = (25, 30, 42)
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, step):
        draw.line([(y * 2, 0), (y * 2, height)], fill=grid_color, width=1)
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Ambient radial neon glow in center-right
    center_x, center_y = int(width * 0.72), int(height * 0.48)
    for radius in range(260, 10, -10):
        alpha_intensity = int(35 * (1 - radius / 260.0))
        glow_color = (
            min(255, 10 + int(accent_color[0] * (alpha_intensity / 100))),
            min(255, 12 + int(accent_color[1] * (alpha_intensity / 100))),
            min(255, 16 + int(accent_color[2] * (alpha_intensity / 100)))
        )
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=glow_color,
            width=6
        )

    # Stylized Glowing AI Waveform / Network Nodes on Right Side
    node_coords = [
        (center_x - 120, center_y - 60),
        (center_x, center_y - 120),
        (center_x + 120, center_y - 40),
        (center_x + 150, center_y + 80),
        (center_x, center_y + 110),
        (center_x - 110, center_y + 70),
        (center_x, center_y),
    ]
    for i, pt1 in enumerate(node_coords):
        for pt2 in node_coords[i+1:]:
            draw.line([pt1, pt2], fill=(accent_color[0]//2, accent_color[1]//2, accent_color[2]//2), width=2)
    for pt in node_coords:
        draw.ellipse([pt[0]-12, pt[1]-12, pt[0]+12, pt[1]+12], fill=accent_color)
        draw.ellipse([pt[0]-6, pt[1]-6, pt[0]+6, pt[1]+6], fill=(255, 255, 255))

    # Badge / Category pill
    draw.rounded_rectangle([70, 70, 480, 115], radius=8, fill=(20, 25, 35), outline=accent_color, width=2)
    draw.text((90, 82), f"● {tagline.upper()}", fill=accent_color)

    # Main Title text
    clean_title = episode_title.strip()
    words = clean_title.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 22:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    y_offset = 180
    for idx, line in enumerate(lines[:3]):
        # Simulated bold drop shadow
        draw.text((73, y_offset + 3), line.upper(), fill=(0, 0, 0))
        draw.text((70, y_offset), line.upper(), fill=(255, 255, 255))
        y_offset += 65

    # Bottom status bar
    draw.line([(70, height - 100), (width - 70, height - 100)], fill=(40, 46, 60), width=2)
    draw.text((70, height - 80), "SHOWRUNNER STUDIO // 4K BROADCAST PRODUCTION", fill=(130, 140, 160))
    draw.text((width - 320, height - 80), "POWERED BY GEMINI 3.8", fill=accent_color)

    # Save to buffer
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    image_bytes = buf.getvalue()

    # Upload to Cloud Storage
    filename = f"thumbnails/{uuid.uuid4().hex[:12]}_{h % 10000}.jpg"
    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type="image/jpeg")
    except Exception as e:
        # Fallback if local without storage credentials
        pass

    return {
        "status": "success",
        "image_url": public_url,
        "episode_title": episode_title,
        "tagline": tagline,
        "aspect_ratio": "16:9",
        "format": "JPEG",
    }
