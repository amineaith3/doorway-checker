import streamlit as st
import cv2
import tempfile
import os
from tracker import DoorTracker

st.set_page_config(page_title="Corporate Door Entry", layout="wide")

@st.cache_resource
def get_tracker():
    # Cache the tracker so the model isn't reloaded on every UI interaction
    return DoorTracker()

tracker = get_tracker()

st.title("Corporate Door Entry Simulator")
st.write("Upload a video of a doorway! The app is configured to filter out noise and **only detect and track people (employees)** entering and leaving the frame.")

# File Uploader
uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_video:
    # Save the uploaded video to a temporary file for OpenCV
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    tfile.close()
    
    cap = cv2.VideoCapture(tfile.name)
    
    st.markdown("### Live Surveillance Feed")
    
    # Layout configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_placeholder = st.empty()
        
    with col2:
        st.markdown("#### Access Log")
        metrics_placeholder = st.empty()
        st.divider()
        log_placeholder = st.empty()
        
    prev_tracked_ids = set()
    tracking_logs = []
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # 1. Ask the backend model to process the frame
        annotated_frame_rgb, current_tracked_ids = tracker.process_frame(frame)
        
        # 2. Render the annotated frame
        video_placeholder.image(annotated_frame_rgb, channels="RGB", use_container_width=True)
        
        # --- LOGIC GATE ---
        # Compare current employees to previous frame's employees
        new_objects = current_tracked_ids - prev_tracked_ids
        lost_objects = prev_tracked_ids - current_tracked_ids
        
        # Get video timestamp in seconds for a more realistic log
        current_time = f"{int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)}s"
        
        for obj_id in new_objects:
            tracking_logs.insert(0, f"[ENTRY] **[{current_time}]**: Employee `ID:{obj_id}` entered the building.")
            
        for obj_id in lost_objects:
            tracking_logs.insert(0, f"[EXIT] **[{current_time}]**: Employee `ID:{obj_id}` left the building.")
            
        tracking_logs = tracking_logs[:15] # Keep UI clean
        
        # 3. Render the metrics and logs
        metrics_placeholder.metric("Employees Currently Visible", len(current_tracked_ids))
        
        log_text = "\n\n".join(tracking_logs)
        if not log_text:
            log_text = "_Awaiting entry..._"
        log_placeholder.markdown(log_text)
        
        prev_tracked_ids = current_tracked_ids
        
    cap.release()
    os.remove(tfile.name)
    st.success("Surveillance processing complete!")
