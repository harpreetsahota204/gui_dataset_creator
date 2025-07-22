#!/usr/bin/env python3
"""
Analyze sequences from the GUI annotation dataset.

This script demonstrates how to work with the new sequence structure where:
- Sequence ID is based on the first frame's filename
- All sequence data is stored at the frame level
- Previous annotations are stored as complete objects
"""

import json
import os
from collections import defaultdict
from datetime import datetime

def load_dataset(filepath='data/annotations_coco.json'):
    """Load the COCO format dataset."""
    if not os.path.exists(filepath):
        print(f"Dataset file not found: {filepath}")
        return None
    
    with open(filepath, 'r') as f:
        return json.load(f)

def analyze_sequences(dataset):
    """Analyze sequences in the dataset."""
    if not dataset or 'images' not in dataset:
        print("No images found in dataset")
        return
    
    # Group images by sequence_id
    sequences = defaultdict(list)
    standalone_frames = []
    
    for image in dataset['images']:
        if 'sequence_id' in image and image['sequence_id']:
            sequences[image['sequence_id']].append(image)
        else:
            standalone_frames.append(image)
    
    print(f"\nDataset Summary:")
    print(f"Total images: {len(dataset['images'])}")
    print(f"Total annotations: {len(dataset.get('annotations', []))}")
    print(f"Sequences found: {len(sequences)}")
    print(f"Standalone frames: {len(standalone_frames)}")
    
    # Analyze each sequence
    for seq_id, frames in sequences.items():
        print(f"\n{'='*60}")
        print(f"Sequence: {seq_id}")
        print(f"Frames in sequence: {len(frames)}")
        
        # Sort frames by sequence position
        frames.sort(key=lambda x: x.get('sequence_position', 0))
        
        print("\nAction Flow:")
        for i, frame in enumerate(frames):
            print(f"\n  Frame {i+1} (ID: {frame['id']}):")
            print(f"    File: {frame['file_name']}")
            print(f"    Position: {frame.get('sequence_position', 'N/A')}")
            
            # Show previous annotation
            prev_ann = frame.get('previous_annotation')
            if prev_ann and isinstance(prev_ann, dict):
                action_type = prev_ann.get('attributes', {}).get('action_type', 'unknown')
                task_desc = prev_ann.get('attributes', {}).get('task_description', '')
                element = prev_ann.get('attributes', {}).get('element_info', 'element')
                
                print(f"    Previous Action: {action_type} - {task_desc or element}")
                
                # Show bbox or keypoint info
                if 'bbox' in prev_ann:
                    bbox = prev_ann['bbox']
                    print(f"      Location: bbox at ({bbox[0]:.0f}, {bbox[1]:.0f})")
                elif 'keypoints' in prev_ann:
                    kp = prev_ann['keypoints']
                    print(f"      Location: click at ({kp[0]:.0f}, {kp[1]:.0f})")
            else:
                print(f"    Previous Action: None (first frame)")
            
            # Get current frame's annotations
            frame_annotations = [ann for ann in dataset.get('annotations', []) 
                               if ann.get('image_id') == frame['id']]
            
            if frame_annotations:
                print(f"    Current Actions ({len(frame_annotations)}):")
                for ann in frame_annotations:
                    action_type = ann.get('attributes', {}).get('action_type', 'unknown')
                    task_desc = ann.get('attributes', {}).get('task_description', '')
                    element = ann.get('attributes', {}).get('element_info', 'element')
                    print(f"      - {action_type}: {task_desc or element}")

def reconstruct_sequence_timeline(dataset, sequence_id):
    """Reconstruct the complete timeline of a specific sequence."""
    print(f"\nReconstructing timeline for sequence: {sequence_id}")
    
    # Find all frames in the sequence
    sequence_frames = [img for img in dataset['images'] 
                      if img.get('sequence_id') == sequence_id]
    
    if not sequence_frames:
        print(f"No frames found for sequence: {sequence_id}")
        return
    
    # Sort by position
    sequence_frames.sort(key=lambda x: x.get('sequence_position', 0))
    
    print(f"\nSequence Timeline:")
    print(f"{'='*60}")
    
    for frame in sequence_frames:
        timestamp = frame.get('date_captured', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S')
            except:
                time_str = timestamp
        else:
            time_str = 'Unknown'
        
        print(f"\n[{time_str}] Frame {frame.get('sequence_position', '?')} - {frame['file_name']}")
        
        # Previous action
        prev = frame.get('previous_annotation')
        if prev and isinstance(prev, dict):
            attrs = prev.get('attributes', {})
            print(f"  ← Previous: {attrs.get('action_type', 'unknown')} - "
                  f"{attrs.get('task_description') or attrs.get('element_info', 'unknown')}")
        
        # Current actions
        current_anns = [ann for ann in dataset.get('annotations', [])
                       if ann.get('image_id') == frame['id']]
        
        for ann in current_anns:
            attrs = ann.get('attributes', {})
            print(f"  → Current: {attrs.get('action_type', 'unknown')} - "
                  f"{attrs.get('task_description') or attrs.get('element_info', 'unknown')}")

def main():
    """Main function."""
    # Load dataset
    dataset = load_dataset()
    if not dataset:
        return
    
    # Analyze all sequences
    analyze_sequences(dataset)
    
    # If there are sequences, show detailed timeline for the first one
    sequences = defaultdict(list)
    for image in dataset.get('images', []):
        if 'sequence_id' in image and image['sequence_id']:
            sequences[image['sequence_id']].append(image)
    
    if sequences:
        first_seq_id = list(sequences.keys())[0]
        reconstruct_sequence_timeline(dataset, first_seq_id)

if __name__ == '__main__':
    main() 