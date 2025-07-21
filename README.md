# GUI Dataset Collector

A comprehensive tool for collecting and building datasets for GUI agents. This tool allows you to capture screenshots of user interfaces, annotate interactions with bounding boxes and click points, and export structured datasets in COCO format.

![GUI Dataset Collector](https://img.shields.io/badge/License-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)
![Browser](https://img.shields.io/badge/Browser-Chrome%2FFirefox%2FEdge-orange.svg)

<img src="gui_capture_app.gif">

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

### 📝 Rich Metadata Support
- **Image-level metadata**: Application name and platform
- **Annotation-level descriptions**: Task descriptions per interaction
- **Action types**: Click, type, select, hover, drag, right-click, double-click
- **Custom metadata fields**: Add unlimited key-value pairs per annotation
- **Element identification**: CSS selectors, IDs, or custom identifiers

### 💾 Data Management
- **COCO dataset format** export for ML compatibility
- **Automatic file naming** with matching image/annotation basenames
- **Persistent storage** with server-side file handling
- **Dataset statistics** tracking (images, annotations count)
- **Resume capability** - load existing datasets and continue

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
- Click "Export Full Dataset" to save the complete COCO dataset
- All data is automatically saved as you work

## 📁 Output Format

### File Structure
```
data/
├── annotations_coco.json    # Complete COCO dataset
├── frame_1.png             # Screenshot images
├── frame_2.png
└── ...
```

### COCO Dataset Format
The tool exports data in standard COCO format:

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
      "platform": "Windows"
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
        }
      }
    }
  ],
  "categories": [
    {"id": 1, "name": "click", "supercategory": "interaction"},
    {"id": 2, "name": "type", "supercategory": "interaction"}
  ]
}
```

## ⌨️ Keyboard Shortcuts

- **Delete**: Remove selected annotation
- **Esc**: Cancel current drawing operation
- **Click**: Select annotations for editing

## 🎛️ UI Components

### Main Panel
- **Live video stream** for real-time capture
- **Screenshot display** with interactive annotations
- **Toolbar** with capture and annotation controls

### Side Panel
- **Dataset statistics** (image/annotation counts)
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

**Files not saving:**
- Check that the server is running
- Ensure you have write permissions in the project directory
- Look for error messages in the browser console
