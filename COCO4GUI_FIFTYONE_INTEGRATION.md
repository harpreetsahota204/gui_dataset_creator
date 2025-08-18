# COCO4GUI Dataset Importer

A specialized FiftyOne dataset importer for GUI interaction datasets that extends the standard COCO detection format to handle GUI-specific features and workflow sequences.

## Overview

The COCO4GUI importer is designed to work with GUI annotation datasets that contain:

- **Interaction annotations** with both bounding boxes and keypoints
- **GUI-specific categories** like click, type, select, hover, drag, etc.
- **Sequence information** tracking user workflows and interaction chains
- **GUI metadata** including application, platform, and timing information
- **Rich attributes** for task descriptions, element information, and custom metadata

## Key Features

### 1. Dual Annotation Support
- **Bounding boxes**: For UI element regions
- **Keypoints**: For precise interaction points (click locations, etc.)
- Both can exist in the same annotation for comprehensive interaction tracking

### 2. Sequence Information Extraction
The importer automatically extracts sequence information from annotation-level attributes and promotes it to individual image-level fields for easier querying:

```python
# Annotation-level attributes (in COCO JSON):
"attributes": {
    "previous_annotation_id": 123,
    "previous_step_position": 2,
    "previous_action_type": "type",
    "previous_element_type": "Text Input",
    "steps_since_start": 3
}

# Plus image-level metadata:
"sequence_id": "login_flow_001",
"sequence_position": 3

# Becomes individual fields in FiftyOne:
sample.previous_annotation_id = 123
sample.previous_step_position = 2
sample.previous_action_type = "type"
sample.previous_element_type = "Text Input"
sample.steps_since_start = 3
sample.sequence_id = "login_flow_001"
sample.sequence_position = 3
```

### 3. GUI Metadata as Individual Fields
Automatically extracts GUI-specific metadata from image records as individual fields:

```python
# GUI metadata becomes individual fields:
sample.application = "Chrome"
sample.platform = "macOS"
sample.date_captured = "2025-01-15T10:30:00Z"
```

### 4. Rich Attribute Handling
Preserves all custom attributes from your GUI annotations:

```python
detection.task_description = "Click the login button"
detection.element_info = "Button"
detection.action_type = "click"
detection.custom_metadata = {...}
```

## Installation & Setup

1. **Prerequisites**:
   ```bash
   pip install fiftyone
   ```

2. **Add the importer to your project**:
   ```python
   from coco4gui_importer import COCO4GUIDatasetImporter
   ```

## Usage

### Basic Usage

```python
import fiftyone as fo
from coco4gui_importer import COCO4GUIDataset

# Load a GUI dataset using the standard fo.Dataset.from_dir pattern
dataset = fo.Dataset.from_dir(
    dataset_dir="/path/to/your/gui_dataset",
    dataset_type=COCO4GUIDataset,           # Use COCO4GUI dataset type
    name="my_gui_dataset",
    data_path="data",                       # images folder
    labels_path="annotations_coco.json",    # COCO annotations
    include_sequence_info=True,             # Extract sequence info
    include_gui_metadata=True,              # Include GUI metadata
    extra_attrs=True,                       # Include all attributes
    persistent=True,
)

# Launch FiftyOne app
session = fo.launch_app(dataset)
```

### Advanced Configuration

```python
dataset = fo.Dataset.from_dir(
    dataset_dir="/path/to/gui_dataset",
    dataset_type=COCO4GUIDataset,
    name="filtered_gui_dataset",
    
    # Label types to load
    label_types=["detections", "keypoints"],
    
    # Filter by specific interaction types
    classes=["click", "type", "select"],
    
    # Sequence and metadata options
    include_sequence_info=True,
    include_gui_metadata=True,
    include_annotation_id=True,
    
    # Sampling options
    max_samples=1000,
    shuffle=True,
    seed=42,
    
    # Attribute handling
    extra_attrs=True,  # or ["task_description", "element_info"]
    persistent=True,
)
```

## Data Structure

### Expected COCO4GUI Format

Your COCO JSON should follow this structure:

```json
{
  "info": {
    "description": "GUI Interaction Dataset",
    "version": "1.0",
    "year": 2025
  },
  "categories": [
    {"id": 1, "name": "click", "supercategory": "interaction"},
    {"id": 2, "name": "type", "supercategory": "interaction"},
    {"id": 3, "name": "select", "supercategory": "interaction"}
  ],
  "images": [
    {
      "id": 1,
      "file_name": "screenshot_001.png",
      "width": 1920,
      "height": 1080,
      "application": "Chrome",
      "platform": "macOS",
      "date_captured": "2025-01-15T10:30:00Z",
      "sequence_id": "login_flow_001",
      "sequence_position": 1
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [100, 200, 150, 40],        // UI element bounding box
      "keypoints": [175, 220, 2],         // Interaction point [x, y, visibility]
      "area": 6000,
      "iscrowd": 0,
      "attributes": {
        "task_description": "Click login button",
        "action_type": "click",
        "element_info": "Button",
        "previous_annotation_id": null,
        "previous_action_type": null,
        "steps_since_start": 1,
        "custom_metadata": {}
      }
    }
  ]
}
```

### Generated FiftyOne Schema

The importer creates the following fields in your FiftyOne dataset:

```python
{
    "filepath": fiftyone.core.fields.StringField,
    "metadata": fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.metadata.ImageMetadata),
    
    # Annotation fields
    "detections": fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Detections),
    "keypoints": fiftyone.core.fields.EmbeddedDocumentField(fiftyone.core.labels.Keypoints),
    
    # Individual GUI metadata fields
    "application": fiftyone.core.fields.StringField,
    "platform": fiftyone.core.fields.StringField,
    "date_captured": fiftyone.core.fields.StringField,
    "sequence_id": fiftyone.core.fields.StringField,
    "sequence_position": fiftyone.core.fields.IntField,
    
    # Individual sequence fields
    "previous_annotation_id": fiftyone.core.fields.IntField,
    "previous_step_position": fiftyone.core.fields.IntField,
    "previous_action_type": fiftyone.core.fields.StringField,
    "previous_element_type": fiftyone.core.fields.StringField,
    "steps_since_start": fiftyone.core.fields.IntField,
}
```

## Analysis Examples

### Basic Dataset Analysis

```python
from fiftyone import ViewField as F

# Dataset overview
print(f"Total samples: {len(dataset)}")
print(f"Interaction types: {dataset.distinct('detections.detections.label')}")
print(f"Applications: {dataset.distinct('gui_metadata.application')}")

# Sequence analysis
if dataset.has_field("sequence_info"):
    with_sequences = dataset.exists("sequence_info")
    print(f"Samples with sequences: {len(with_sequences)}")
    
    steps = with_sequences.values("sequence_info.steps_since_start")
    steps = [s for s in steps if s is not None]
    print(f"Sequence length range: {min(steps)} - {max(steps)}")
```

## Advanced Queries

```python
# Find all click interactions
clicks = dataset.filter_labels("detections", F("label") == "click")

# Find long interaction sequences
long_sequences = dataset.match(F("steps_since_start") > 5)

# Find interactions that followed typing
after_typing = dataset.match(F("previous_action_type") == "type")

# Find Chrome interactions with task descriptions
chrome_tasks = dataset.match(
    (F("application") == "Chrome") &
    (F("detections.detections.task_description").exists())
)

# Complex sequence analysis
click_after_type_in_chrome = dataset.match(
    (F("application") == "Chrome") &
    (F("previous_action_type") == "type") &
    (F("detections.detections.label") == "click")
)
```


## Export Options

```python
# Export back to COCO format
dataset.export(
    export_dir="/path/to/export",
    dataset_type=fo.types.COCODetectionDataset,
    label_field="detections",
)

# Export only keypoints
dataset.export(
    export_dir="/path/to/keypoints_export",
    dataset_type=fo.types.COCODetectionDataset, 
    label_field="keypoints",
)

# Export filtered subset
clicks_only = dataset.filter_labels("detections", F("label") == "click")
clicks_only.export(
    export_dir="/path/to/clicks_export",
    dataset_type=fo.types.COCODetectionDataset,
)
```