# Add `Webcam` widget

Adds a new `Webcam` widget that shows a live camera preview and lets the user capture photos or record video, with configurable control rendering based on the selected mode.

## New files/changes

- `webcam.py`: new webcam widget behavior, including conditional mode rendering, photo capture, and video recording
- `event.py`: webcam actions now publish using the new event-object pattern
- `theme.css`: webcam styles updated to use the shared Invent design tokens more closely

## Behavior

A `Webcam` renders a live camera preview, a shutter button, and a status area. The widget can be configured in one of three ways:

```python
# Photo-only webcam
Webcam(mode="photo")

# Video-only webcam
Webcam(mode="video")

# Switchable webcam with both controls
Webcam(mode="both")
```

When `mode="photo"`, only the photo control is rendered and the shutter captures a still image.
When `mode="video"`, only the video control is rendered and the shutter starts/stops recording.
When `mode="both"`, the widget renders both mode buttons so the user can switch between photo and video behavior.

The widget also publishes events when media is captured or recorded:

```python
self.publish(self.photo_captured, webcam=self)
self.publish(self.video_recorded, webcam=self)
```

The webcam UI uses the shared Invent theme variables for spacing, borders, typography, and colors so it stays visually consistent with the rest of the framework.
