"""
COCO4GUI Dataset Type and Importer

A specialized FiftyOne dataset type for GUI interaction datasets that extends 
the standard COCO detection format to handle GUI-specific features:

- Both bounding boxes and keypoints for interaction locations
- GUI-specific categories (click, type, select, hover, drag, etc.)
- Sequence information extracted from annotation attributes to image level
- GUI metadata (application, platform, etc.)
- Rich interaction attributes (task_description, element_info, etc.)

Usage:
    import fiftyone as fo
    from coco4gui_importer import COCO4GUIDataset
    
    dataset = fo.Dataset.from_dir(
        dataset_dir="path/to/gui_data",
        dataset_type=COCO4GUIDataset,
        name="my_gui_dataset",
        include_sequence_info=True,
        include_gui_metadata=True,
    )
"""

from collections import defaultdict
import logging
import os

import fiftyone.core.fields as fof
import fiftyone.core.labels as fol
import fiftyone.core.metadata as fom
import fiftyone.utils.data as foud
import fiftyone.utils.coco as fouc
import fiftyone.types as fot
import eta.core.serial as etas

logger = logging.getLogger(__name__)


class COCO4GUIDataset(fot.ImageDetectionDataset):
    """A labeled dataset consisting of images and their associated GUI interactions
    saved in COCO4GUI format (extended COCO Object Detection Format).
    
    This dataset type handles GUI-specific features like:
    - Both bounding boxes and keypoints for interaction locations
    - Sequence information for workflow tracking
    - GUI metadata (application, platform, etc.)
    - Rich interaction attributes
    """

    def get_dataset_importer_cls(self):
        return COCO4GUIDatasetImporter

    def get_dataset_exporter_cls(self):
        return COCO4GUIDatasetExporter


class COCO4GUIDatasetImporter(fouc.COCODetectionDatasetImporter):
    """Importer for COCO4GUI datasets that extends the standard COCO detection importer.
    
    This importer adds GUI-specific functionality:
    - Extracts sequence information from annotation attributes to image level
    - Handles both bounding boxes and keypoints
    - Includes GUI metadata (application, platform, etc.)
    - Preserves rich interaction attributes
    
    Additional parameters beyond COCODetectionDatasetImporter:
        include_sequence_info (True): extract sequence info from annotation attributes
        include_gui_metadata (True): include GUI metadata from image records
    """
    
    def __init__(
        self,
        dataset_dir=None,
        data_path=None,
        labels_path=None,
        label_types=None,
        classes=None,
        image_ids=None,
        include_id=False,
        include_annotation_id=False,
        include_license=False,
        extra_attrs=True,
        only_matching=False,
        use_polylines=False,
        tolerance=None,
        shuffle=False,
        seed=None,
        max_samples=None,
        # GUI-specific parameters
        include_sequence_info=True,
        include_gui_metadata=True,
    ):
        # Initialize parent with standard COCO parameters
        super().__init__(
            dataset_dir=dataset_dir,
            data_path=data_path,
            labels_path=labels_path,
            label_types=label_types,
            classes=classes,
            image_ids=image_ids,
            include_id=include_id,
            include_annotation_id=include_annotation_id,
            include_license=include_license,
            extra_attrs=extra_attrs,
            only_matching=only_matching,
            use_polylines=use_polylines,
            tolerance=tolerance,
            shuffle=shuffle,
            seed=seed,
            max_samples=max_samples,
        )
        
        # GUI-specific options
        self.include_sequence_info = include_sequence_info
        self.include_gui_metadata = include_gui_metadata
        self._sequence_info_map = None

    def __next__(self):
        """Override to add GUI-specific fields to each sample."""
        # Get the standard COCO sample
        image_path, image_metadata, label = super().__next__()
        
        if label is None:
            return image_path, image_metadata, label
            
        # Extract image ID from the current filename for GUI enhancements
        filename = os.path.basename(image_path)
        image_dict = self._image_dicts_map.get(filename, None)
        
        if image_dict is not None:
            image_id = image_dict["id"]
            
            # Convert single label to dict if needed
            if not isinstance(label, dict):
                label = {"detections": label}
            elif label is None:
                label = {}
            
            # Add GUI metadata as individual fields
            if self.include_gui_metadata:
                gui_metadata_fields = ["sequence_id", "sequence_position", "application", "platform"]
                
                # Add all GUI metadata fields as individual fields
                for field in gui_metadata_fields:
                    if field in image_dict and image_dict[field] is not None:
                        label[field] = image_dict[field]
            
            # Add sequence information as individual fields
            if self.include_sequence_info and self._sequence_info_map:
                sequence_info = self._sequence_info_map.get(image_id, None)
                if sequence_info:
                    # Add each sequence field individually
                    for field_name, field_value in sequence_info.items():
                        if field_value is not None:
                            label[field_name] = field_value
        
        return image_path, image_metadata, label

    def setup(self):
        """Override setup to extract sequence information."""
        # Call parent setup first
        super().setup()
        
        # Extract sequence information if requested
        if self.include_sequence_info and self._annotations:
            self._sequence_info_map = self._extract_sequence_info_from_annotations()

    def _extract_sequence_info_from_annotations(self):
        """Extract sequence information from annotation attributes to image level."""
        sequence_info_map = {}
        
        for image_id, coco_objects in self._annotations.items():
            if not coco_objects:
                continue
                
            # Look for sequence information in annotation attributes
            # Take from first annotation that has sequence data
            sequence_info = None
            for obj in coco_objects:
                # Check if this is a COCO4GUI object with attributes
                if hasattr(obj, 'attributes') and obj.attributes:
                    attrs = obj.attributes
                    
                    # Look for sequence-related attributes
                    sequence_fields = [
                        'previous_annotation_id', 'previous_step_position', 
                        'previous_action_type', 'previous_element_type',
                        'steps_since_start', 'sequence_id', 'sequence_position'
                    ]
                    
                    if any(field in attrs for field in sequence_fields):
                        sequence_info = {}
                        for field in sequence_fields:
                            if field in attrs and attrs[field] is not None:
                                sequence_info[field] = attrs[field]
                        if sequence_info:  # Only proceed if we found actual data
                            break
                
                # Also check direct object attributes (if loaded via extra_attrs)
                else:
                    sequence_fields = [
                        'previous_annotation_id', 'previous_step_position',
                        'previous_action_type', 'previous_element_type', 
                        'steps_since_start', 'sequence_id', 'sequence_position'
                    ]
                    sequence_info = {}
                    found_any = False
                    for field in sequence_fields:
                        if hasattr(obj, field):
                            value = getattr(obj, field)
                            if value is not None:
                                sequence_info[field] = value
                                found_any = True
                    
                    if found_any:
                        break
            
            if sequence_info:
                sequence_info_map[image_id] = sequence_info
                
        return sequence_info_map

    @property
    def label_cls(self):
        """Override to include GUI-specific label types."""
        parent_cls = super().label_cls
        
        # Add GUI-specific fields as individual fields
        gui_fields = {}
        
        # Add individual GUI metadata fields
        if self.include_gui_metadata:
            gui_metadata_fields = {
                'application': fof.StringField,
                'platform': fof.StringField,
                'sequence_id': fof.StringField,
                'sequence_position': fof.IntField,
            }
            gui_fields.update(gui_metadata_fields)
        
        # Add individual sequence fields
        if self.include_sequence_info:
            sequence_fields = {
                'previous_annotation_id': fof.IntField,
                'previous_step_position': fof.IntField,
                'previous_action_type': fof.StringField,
                'previous_element_type': fof.StringField,
                'steps_since_start': fof.IntField,
            }
            gui_fields.update(sequence_fields)
            
        if isinstance(parent_cls, dict):
            # Multiple label types
            parent_cls.update(gui_fields)
            return parent_cls
        elif gui_fields:
            # Single label type, need to convert to dict
            if hasattr(self, '_label_types') and len(self._label_types) == 1:
                label_name = self._label_types[0]
            else:
                label_name = "detections"  # default
            
            combined = {label_name: parent_cls}
            combined.update(gui_fields)
            return combined
        else:
            return parent_cls


class COCO4GUIDatasetExporter(fouc.COCODetectionDatasetExporter):
    """Exporter for COCO4GUI datasets that extends the standard COCO detection exporter.
    
    This exporter adds GUI-specific functionality:
    - Exports individual GUI metadata fields back to image records
    - Exports individual sequence fields back to annotation attributes
    - Maintains compatibility with standard COCO format while preserving GUI extensions
    
    Additional parameters beyond COCODetectionDatasetExporter:
        export_sequence_info (True): export sequence fields to annotation attributes
        export_gui_metadata (True): export GUI metadata fields to image records
    """
    
    def __init__(
        self,
        export_dir=None,
        data_path=None,
        labels_path=None,
        export_media=None,
        rel_dir=None,
        abs_paths=False,
        image_format=None,
        classes=None,
        categories=None,
        info=None,
        extra_attrs=True,
        coco_id=None,
        annotation_id=None,
        iscrowd="iscrowd",
        num_decimals=None,
        tolerance=None,
        # GUI-specific parameters
        export_sequence_info=True,
        export_gui_metadata=True,
    ):
        # Initialize parent with standard COCO parameters
        super().__init__(
            export_dir=export_dir,
            data_path=data_path,
            labels_path=labels_path,
            export_media=export_media,
            rel_dir=rel_dir,
            abs_paths=abs_paths,
            image_format=image_format,
            classes=classes,
            categories=categories,
            info=info,
            extra_attrs=extra_attrs,
            coco_id=coco_id,
            annotation_id=annotation_id,
            iscrowd=iscrowd,
            num_decimals=num_decimals,
            tolerance=tolerance,
        )
        
        # GUI-specific options
        self.export_sequence_info = export_sequence_info
        self.export_gui_metadata = export_gui_metadata
        
        # Storage for GUI metadata from samples
        self._gui_metadata_map = {}

    def log_collection(self, sample_collection):
        """Override to capture GUI metadata from samples."""
        # Call parent first
        super().log_collection(sample_collection)
        
        # Capture GUI metadata from all samples
        if self.export_gui_metadata:
            gui_metadata_fields = ['sequence_id', 'sequence_position', 'application', 'platform']
            
            # Get all filepaths and GUI metadata
            filepaths = sample_collection.values("filepath")
            gui_data = {}
            
            for field in gui_metadata_fields:
                if sample_collection.has_field(field):
                    values = sample_collection.values(field)
                    gui_data[field] = values
            
            # Map filepath to GUI metadata
            for i, filepath in enumerate(filepaths):
                self._gui_metadata_map[filepath] = {}
                for field, values in gui_data.items():
                    if i < len(values) and values[i] is not None:
                        self._gui_metadata_map[filepath][field] = values[i]

    def export_sample(self, image_or_path, label, metadata=None):
        """Override to handle GUI-specific fields during export."""
        
        # Handle GUI metadata fields and sequence fields
        gui_metadata_fields = ['sequence_id', 'sequence_position', 'application', 'platform']
        sequence_fields = [
            'previous_annotation_id', 'previous_step_position', 'previous_action_type',
            'previous_element_type', 'steps_since_start'
        ]
        
        # Store the current image path for GUI metadata lookup
        self._current_image_path = image_or_path
        
        # Store GUI fields for later processing
        self._current_gui_fields = {}
        self._current_sequence_fields = {}
        
        if isinstance(label, dict):
            # Extract and store GUI metadata fields (but don't remove from label yet)
            if self.export_gui_metadata:
                for field in gui_metadata_fields:
                    if field in label:
                        self._current_gui_fields[field] = label[field]
            
            # Extract and store sequence fields (but don't remove from label yet)
            if self.export_sequence_info:
                for field in sequence_fields:
                    if field in label:
                        self._current_sequence_fields[field] = label[field]
            
            # Remove GUI fields from label before passing to parent
            # (parent doesn't know how to handle them)
            clean_label = {k: v for k, v in label.items() 
                          if k not in gui_metadata_fields and k not in sequence_fields}
        else:
            clean_label = label
        
        # Call parent export_sample method with clean label
        super().export_sample(image_or_path, clean_label, metadata)
        
        # Add GUI fields to the exported structures
        self._add_gui_fields_to_current_export()

    def _add_gui_fields_to_current_export(self):
        """Add GUI-specific fields to the most recently exported structures."""
        
        # Add GUI metadata fields to the current image record
        # Get GUI metadata from the captured metadata map
        if self._images:
            current_image = self._images[-1]  # Most recently added image
            
            # Try to get GUI metadata from our captured map
            # We need to find the right sample by looking at recent exports
            image_path = getattr(self, '_current_image_path', None)
            if image_path and image_path in self._gui_metadata_map:
                gui_metadata = self._gui_metadata_map[image_path]
                for field, value in gui_metadata.items():
                    if value is not None:
                        current_image[field] = value
            
            # Also add from current GUI fields (from labels)
            if hasattr(self, '_current_gui_fields') and self._current_gui_fields:
                for field, value in self._current_gui_fields.items():
                    if value is not None:
                        current_image[field] = value
        
        # Add sequence fields to the current annotations as attributes
        if self._current_sequence_fields and self._annotations:
            # Find annotations for the current image
            current_image_id = self._images[-1]["id"] if self._images else None
            if current_image_id is not None:
                # Add to all annotations for this image
                for annotation in reversed(self._annotations):
                    if annotation.get("image_id") == current_image_id:
                        # Add sequence fields to annotation attributes
                        if "attributes" not in annotation:
                            annotation["attributes"] = {}
                        
                        for field, value in self._current_sequence_fields.items():
                            if value is not None:
                                annotation["attributes"][field] = value

    @property
    def label_cls(self):
        """Override to accept GUI-specific label types."""
        parent_cls = super().label_cls
        
        # We accept the same types as the importer but in reverse
        # The parent handles the core detection/keypoint types
        return parent_cls
