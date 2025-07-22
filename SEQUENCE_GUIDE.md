# Sequential Annotation Guide

## Overview

The GUI Annotation Tool now supports capturing sequences of actions. This allows you to:
- Group related frames into sequences
- Maintain a history of actions within a sequence
- Track the order and relationship between frames
- Identify which frames belong to which sequences

## Key Changes

- **Sequence ID**: Automatically set from the first frame's filename (without extension)
- **Storage**: All sequence information is stored at the frame level in the "images" array
- **Previous Action**: Stores the complete annotation object from the previous frame

## How to Use Sequence Capture

### 1. Starting a Sequence

1. Click the **"Start Sequence"** button in the toolbar
2. The sequence indicator will show "Pending..." until the first frame is saved
3. The sequence ID will be automatically set from the first frame's filename

### 2. Capturing Frames in a Sequence

1. Start live capture as usual
2. Capture frames - each frame will automatically be tagged with:
   - `sequence_id`: Set from the first frame's filename (e.g., "2024-01-15_10-30-45")
   - `sequence_position`: The position in the sequence (1, 2, 3, etc.)
   - `previous_annotation`: Complete annotation object from the previous action

3. Add annotations to each frame as normal
4. When you save a frame, its actions are added to the sequence history

### 3. Action History

- The **Action History** panel shows all actions performed in the current sequence
- Each action displays:
  - Action number
  - Description (from task_description or auto-generated)
  - Timestamp
- The complete annotation object is stored for reference

### 4. Ending a Sequence

1. Click the **"End Sequence"** button
2. Enter a description for the sequence (e.g., "User login workflow")
3. The sequence information is preserved in the frame metadata

## Data Structure

### Frame-Level Sequence Data

All sequence information is stored in the "images" array. Each image captured during a sequence includes:

```json
{
  "id": 1,
  "file_name": "2024-01-15_10-30-45.png",
  "width": 1920,
  "height": 1080,
  "date_captured": "2024-01-15T10:30:45.123Z",
  "application": "Chrome",
  "platform": "macOS",
  "sequence_id": "2024-01-15_10-30-45",  // Based on first frame's filename
  "sequence_position": 2,
  "previous_annotation": {  // Complete annotation object
    "id": 1,
    "bbox": [100, 200, 150, 50],
    "category_id": 1,
    "area": 7500,
    "iscrowd": 0,
    "attributes": {
      "task_description": "Click on username field",
      "action_type": "click",
      "element_info": "input#username",
      "custom_metadata": {}
    }
  }
}
```

### Why This Structure?

1. **Self-contained frames**: Each frame contains all the information needed to understand its context
2. **No separate sequence tracking**: Simplifies the data structure
3. **Complete action history**: The full annotation object provides all details about the previous action
4. **Consistent naming**: Using the first frame's filename ensures all frames in a sequence share the same ID

## Use Cases

### 1. Multi-Step Workflows
Capture complete workflows like:
- User registration (multiple form fields)
- Shopping cart checkout
- File upload process
- Settings configuration

### 2. Tutorial Creation
Document step-by-step procedures:
- Software tutorials
- Training materials
- Bug reproduction steps

### 3. UI Testing
Create test sequences:
- Regression test scenarios
- User journey mapping
- A/B testing documentation

## Tips

1. **Let the system handle IDs**: Don't worry about sequence IDs - they're automatically set from the first frame
2. **Complete each frame**: Add all annotations before saving to ensure proper action history
3. **Review previous actions**: Check the "Previous Action" field to see context
4. **Consistent timing**: All frames in a sequence will have the same sequence_id based on the first frame

## Example Workflow

1. Click "Start Sequence"
2. Start live capture and select window
3. Capture frame 1: Login page
   - Add click annotation on username field
   - Save frame (sequence_id is set to "2024-01-15_10-30-45")
4. Capture frame 2: Username entered
   - Previous annotation shows the complete click action from frame 1
   - Add type annotation showing text entry
5. Continue capturing frames...
6. End sequence with description "Complete login workflow"

All frames will share the same sequence_id and maintain the complete action history through the previous_annotation field. 