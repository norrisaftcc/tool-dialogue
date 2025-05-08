# Image Support in Terminal Dialogue System

This document explains how to use images in the Terminal Dialogue System to display character portraits and enhance the visual experience.

## Overview

The image display feature allows you to:
- Display character portraits next to dialogue text
- Create a more immersive experience while maintaining the retro terminal aesthetic
- Use either direct URLs or reference a central character database

## Implementation

Images are supported in two ways:

1. **Direct Image URLs in Dialogue Nodes**: Add an `image_url` field to individual dialogue nodes
2. **Character Database**: Define characters with associated images in a central `characters` section

## Adding Images to Dialogue Nodes

To add an image directly to a dialogue node, include the `image_url` field:

```json
{
  "id": "commander_intro",
  "npc": "Commander Chen",
  "image_url": "https://example.com/images/commander_chen.jpg",
  "text": "Welcome aboard, recruit. I'm Commander Chen.",
  "responses": [...]
}
```

## Creating a Character Database

For characters that appear multiple times, you can create a character database:

```json
"characters": {
  "chen": {
    "name": "Commander Chen",
    "image_url": "https://example.com/images/commander_chen.jpg",
    "description": "Station Commander, responsible for operations"
  },
  "rivera": {
    "name": "Lt. Rivera",
    "image_url": "https://example.com/images/lt_rivera.jpg",
    "description": "Flight Engineer"
  }
}
```

## Image Lookup Priority

When displaying a dialogue node, the system looks for images in this order:

1. First checks the dialogue node's `image_url` field
2. If not found, looks in the `characters` section for a character with matching name
3. If no image is found, displays text-only dialogue

## Image Format Guidelines

- Use images with 1:1 or 3:4 aspect ratio for best display
- PNG or JPG format is recommended
- Consider using smaller file sizes (under 500KB) for faster loading
- Square portraits work best with the terminal interface
- Images should have clear subjects that are recognizable at small sizes

## Example Dialogue with Images

The `dialogue_with_images.json` file demonstrates a complete example of a dialogue using character portraits. It features:

- Astronauts on a space station with individual portraits
- Both direct image URLs and character database references
- A quest system integrated with the visual dialogue

## Running the Image-Enabled Terminal

To use the terminal with image support:

```bash
streamlit run retro_app/terminal_image_display.py
```

Then load the example dialogue:
1. Click "Upload Dialogue File" in the sidebar
2. Select `retro_app/dialogue_with_images.json`
3. Click "Load Dialogue" to begin

## Technical Notes

- Images are loaded using the requests library and displayed using Streamlit's image component
- The system caches images to improve performance
- If an image URL is invalid or unavailable, the system falls back to text-only display
- The display is responsive and will adapt to different screen sizes

## Future Improvements

Planned enhancements to the image support system:

- Support for animated GIFs or short looping animations
- Image filters to maintain the retro aesthetic (e.g., CRT effect overlay)
- Local file storage option for offline use
- Multiple image poses per character (happy, sad, angry, etc.)
- Background images for different locations