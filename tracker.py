import cv2
from ultralytics import YOLO

class DoorTracker:
    def __init__(self, model_path="yolo11n.pt"):
        """Initializes the YOLO model for tracking."""
        self.model = YOLO(model_path)
    
    def process_frame(self, frame):
        """
        Runs tracking on a single frame, filters for 'Person' class, 
        and returns the annotated RGB frame and a set of tracked IDs.
        """
        # Run YOLO11 tracking. classes=[0] ensures we only look for "Person"
        results = self.model.track(frame, persist=True, classes=[0], verbose=False)
        
        # Grab annotated frame and convert for web display
        annotated_frame = results[0].plot()
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Extract tracked employee IDs
        tracked_ids = set()
        if results[0].boxes is not None and results[0].boxes.id is not None:
            ids = results[0].boxes.id.int().cpu().tolist()
            for obj_id in ids:
                tracked_ids.add(obj_id)
                
        return annotated_frame_rgb, tracked_ids
