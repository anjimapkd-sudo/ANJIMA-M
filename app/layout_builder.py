def build_comic_layout(panels, image_paths):
    return [
        {
            "panel_number": p.panel_number,
            "title": p.title,
            "scene_description": p.scene_description,
            "image_prompt": p.image_prompt,
            "caption": p.caption,
            "narration": p.narration,
            "image_path": image_paths[i],
        }
        for i, p in enumerate(panels)
    ]
