# COCO4GUI - A COCO-based GUI Dataset Collector

A comprehensive tool for collecting and building datasets for GUI agents. This tool allows you to capture screenshots of user interfaces, annotate interactions with bounding boxes and click points, navigate and edit existing samples, and export structured datasets in COCO4GUI format.

![Vibe](https://img.shields.io/badge/Vibe_coded_with-Claude_4_Opus-blueviolet)
![GUI Dataset Collector](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)
![Browser](https://img.shields.io/badge/Browser-Chrome%2FFirefox%2FEdge-orange.svg)

<img src="gui_capture_app.gif" alt="GUI Dataset Collector Demo">

## ✨ Features

### 📸 Screen Capture

- **Live screen streaming** with browser's native display picker

- **Real-time video preview** of selected window/screen

- **High-quality screenshot capture** at original resolution

- **Multiple capture modes**: Full desktop, specific window, or partial screen

### 🎯 Interactive Annotations

- **Bounding box drawing** for UI elements

- **Click point markers** for precise interaction points

- **Visual feedback** with color-coded overlays

- **Clickable annotations** for easy editing and management

- **Live annotation editing** with real-time updates

### 📝 Rich Metadata Support

- **Image-level metadata**: Application name and platform

- **Annotation-level descriptions**: Task descriptions per interaction

- **Action types**: Click, type, select, hover, drag, right-click, double-click

- **Custom metadata fields**: Add unlimited key-value pairs per annotation

- **Element identification**: CSS selectors, IDs, or custom identifiers

### 💾 Data Management

- **COCO4GUI dataset format** export for ML compatibility

- **Automatic file naming** with matching image/annotation basenames

- **Persistent storage** with server-side file handling

- **Dataset statistics** tracking (images, annotations count)

- **Resume capability** - load existing datasets and continue

### 🔍 Sample Navigation & Editing

- **Dual-mode interface**: Switch between Live Capture and Review/Edit modes

- **Sample navigation**: Browse through captured frames with Previous/Next controls

- **Real-time editing**: Modify annotations on any previously captured sample

- **Auto-sync**: Changes automatically save to dataset and server

- **Keyboard navigation**: Use arrow keys for quick sample browsing

## 🛠 Installation

### Prerequisites

- Node.js 18+

- Modern web browser (Chrome, Firefox, Edge)

- npm or yarn package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/harpreetsahota204/gui_dataset_creator.git
   cd gui_dataset_creator
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

## 🚀 Usage

### Starting the Application

1. **Start the server**

   ```bash
   npm start
   ```

2. **Open the application**

   Navigate to `http://localhost:3000` in your browser

## 📋 Application Modes

The GUI Dataset Collector operates in two distinct modes:

### 🎥 Live Capture Mode

For capturing new screenshots and creating annotations in real-time.

### ✏️ Review/Edit Mode

For navigating through existing samples and editing their annotations.

Use the mode toggle buttons at the top of the side panel to switch between modes.

---

## 📸 Live Capture Workflow

### Capturing Data

#### 1. **Initialize Capture Session**

- Click "Start Live Capture"

- Select the window/screen you want to capture

- The live video stream will appear in the main panel

#### 2. **Add Image Metadata**

- Fill in the **Application** field (e.g., "Chrome", "Photoshop", "VSCode")

- Select the **Platform** from the dropdown (Windows, macOS, Linux, etc.)

#### 3. **Capture Screenshots**

- Interact with your target application as needed

- Click "Capture Frame" when you want to annotate a specific state

- The screenshot will replace the live stream

#### 4. **Create Annotations**

**Bounding Boxes:**

- Click "Draw Bounding Box"

- Click and drag on the screenshot to create a box around UI elements

- The box will appear with a red border and ID number

**Click Points:**

- Click "Add Click Point"

- Click on specific locations where interactions occur

- Blue circular markers will appear at click coordinates

#### 5. **Edit Annotations**

- **Click on any bounding box or point** to select it
  - The annotation form will appear on the right panel

- Fill in the details:

  - **Task Description**: What this annotation represents

  - **Action Type**: Click, type, select, hover, etc.

  - **Element Info**: CSS selector, ID, or description

  - **Custom Metadata**: Add any additional key-value pairs

#### 6. **Save Data**

- Click "Save Current Frame" to save the screenshot and annotations

- Files are automatically saved to the `data/` folder

- The live stream resumes for the next capture

### Managing Datasets

#### Loading Existing Data

- Click "Load Existing Dataset" to continue from where you left off

- The tool will load your existing `annotations_coco.json` file

- Image and annotation counters will update accordingly

#### Exporting Data

- Click "Export Full Dataset" to save the complete COCO4GUI dataset

- All data is automatically saved as you work

---

## ✏️ Review/Edit Workflow

### Navigating Existing Samples

#### 1. **Switch to Review Mode**

- Click the "Review/Edit" button in the mode toggle
- The application automatically loads your most recent captured frame
- Live capture controls are disabled, navigation controls appear

#### 2. **Browse Through Samples**

- Use **"Previous Sample"** and **"Next Sample"** buttons to navigate
- Or use **arrow keys** (←/→ or ↑/↓) for keyboard navigation
- Current position indicator shows "X of Y samples"

#### 3. **Edit Annotations**

- Click on any annotation (bounding box or point) to select it
- The annotation form appears with current values pre-filled
- Modify any fields:
  - Task Description
  - Action Type
  - Element Info
  - Custom Metadata
- Changes are automatically saved to the dataset

#### 4. **Add New Annotations**

- Use "Draw Bounding Box" or "Add Click Point" tools
- New annotations are immediately added to the dataset
- All existing annotation functionality works in review mode

#### 5. **Delete Annotations**

- Select an annotation and click "Delete" or press the Delete key
- Annotations are immediately removed from the dataset

## 📁 Output Format

### File Structure

```shell
data/
├── annotations_coco.json    # Complete COCO4GUI dataset
├── frame_1.png             # Screenshot images
├── frame_2.png
└── ...

sequence_data/               # For sequence captures
├── sequence_annotations_coco.json
├── 2024-01-15_14-30-45.png
└── ...
```

### COCO4GUI Dataset Format

The tool exports data in COCO4GUI format, an extension of COCO optimized for GUI interactions:

```json
{
  "info": {
    "description": "GUI Interaction Dataset",
    "version": "1.0",
    "year": 2024,
    "date_created": "2024-01-01T00:00:00.000Z"
  },
  "images": [
    {
      "id": 1,
      "file_name": "frame_1.png",
      "width": 1920,
      "height": 1080,
      "date_captured": "2024-01-01T00:00:00.000Z",
      "application": "Chrome",
      "platform": "Windows",
      "sequence_id": "login_flow_001",
      "sequence_position": 1,
      "sequence_description": "User login workflow"
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "bbox": [100, 200, 150, 50],
      "keypoints": [175, 225, 2],
      "category_id": 1,
      "area": 7500,
      "iscrowd": 0,
      "attributes": {
        "task_description": "Click the submit button",
        "action_type": "click",
        "element_info": "button#submit",
        "custom_metadata": {
          "confidence": "high",
          "difficulty": "easy"
        },
        "previous_annotation_id": null,
        "previous_step_position": null,
        "previous_action_type": null,
        "previous_element_type": null,
        "steps_since_start": 1
      }
    }
  ],
  "categories": [
    {"id": 1, "name": "click", "supercategory": "interaction"},
    {"id": 2, "name": "type", "supercategory": "interaction"}
  ]
}
```

#### COCO4GUI Extensions

COCO4GUI extends the standard COCO format with GUI-specific features:

- **Sequence Support**: `sequence_id`, `sequence_position`, `sequence_description` for multi-step workflows
- **Platform Metadata**: `application` and `platform` fields for environment context
- **Step Relationships**: `previous_annotation_id`, `steps_since_start` for workflow dependencies
- **Rich Attributes**: Detailed `task_description`, `action_type`, and custom metadata per annotation

## 🔗 FiftyOne Integration

COCO4GUI datasets can be seamlessly imported into [FiftyOne](https://voxel51.com/docs/fiftyone/) for advanced dataset visualization, analysis, and management.

### Features

- **Specialized COCO4GUI Importer**: Custom importer that understands GUI-specific annotations and metadata
- **Dual Annotation Support**: Handles both bounding boxes and keypoints in the same dataset
- **Sequence Analysis**: Visualize and analyze multi-step GUI workflows
- **Rich Metadata Fields**: All GUI metadata becomes queryable fields in FiftyOne
- **Interactive Exploration**: Browse samples, filter by sequences, and analyze interaction patterns

### Quick Start

```python
import fiftyone as fo
from coco4gui import COCO4GUIDatasetImporter

# Import your COCO4GUI dataset
dataset = fo.Dataset.from_importer(
    COCO4GUIDatasetImporter,
    dataset_dir="path/to/your/data",
    data_path="path/to/images",
    labels_path="annotations_coco.json"
)

# Launch FiftyOne App for interactive exploration
session = fo.launch_app(dataset)
```

### Advanced Analysis

- **Sequence Filtering**: Filter samples by sequence ID or position
- **Action Analysis**: Analyze distribution of interaction types
- **Workflow Visualization**: Track user paths through sequences
- **Performance Metrics**: Measure annotation quality and consistency

For detailed setup instructions, advanced features, and examples, see the [COCO4GUI FiftyOne Integration Guide](COCO4GUI_FIFTYONE_INTEGRATION.md).

## ⌨️ Keyboard Shortcuts

### Live Capture Mode

- **Ctrl+R / Cmd+R**: Refresh stream
- **Delete**: Remove selected annotation
- **Esc**: Cancel current drawing operation

### Review/Edit Mode

- **Arrow Keys**: Navigate between samples (←/→ or ↑/↓)
- **Delete**: Remove selected annotation
- **Click**: Select annotations for editing

## 🎛️ UI Components

### Main Panel

- **Live video stream** for real-time capture

- **Screenshot display** with interactive annotations

- **Toolbar** with capture and annotation controls

### Side Panel

- **Mode toggle** (Live Capture / Review/Edit)

- **Dataset statistics** (image/annotation counts)

- **Sample navigation** (Previous/Next controls with position indicator)

- **Image metadata** fields (application, platform)

- **Annotation list** with visual indicators

- **Annotation editor** with custom metadata support

### Status Bar

- **Current mode** indicator (Streaming, Drawing, etc.)

- **Status messages** for user feedback

## 🔧 Configuration

### Supported Action Types

- `click` - Standard mouse click

- `type` - Text input

- `select` - Dropdown/option selection

- `hover` - Mouse hover actions

- `drag` - Drag and drop operations

- `right_click` - Context menu actions

- `double_click` - Double-click actions

### Supported Platforms

- Windows

- macOS  

- Linux

- Web Browser

- Mobile

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**"Server not running" error:**

- Make sure you ran `npm start`
- Check that port 3000 is not in use by another application
- Ensure all dependencies are installed

**Screen capture not working:**

- Use a modern browser (Chrome, Firefox, Edge)
- Grant screen capture permissions when prompted
- Try refreshing the page if capture fails

**Annotations not clickable:**

- Make sure you're not in drawing mode
- Click directly on the bounding box or marker
- Try refreshing if annotations become unresponsive

**Annotations appear in wrong positions:**

- This typically happens when navigating between samples quickly
- The issue resolves automatically when the image fully loads
- If persistent, navigate away and back to the sample

**Files not saving:**

- Check that the server is running
- Ensure you have write permissions in the project directory
- Look for error messages in the browser console

## 📚 Citation

If you use this tool in your research or project, please cite it as:

```bibtex
@software{sahota2025coco4gui,
  author = {Sahota, Harpreet},
  title = {COCO4GUI - A COCO-based GUI Dataset Collector},
  year = {2025},
  url = {https://github.com/harpreetsahota204/gui_dataset_creator},
}
```

Or in text:

Sahota, H. (2025). GUI Dataset Collector: A Tool for Capturing and Annotating GUI Interactions [Computer software]. <https://github.com/harpreetsahota204/gui_dataset_creator>