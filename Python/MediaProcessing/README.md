## 🎞️videoWatermarkAdder.py  
This script adds a watermark image to a video using OpenCV.

### Usage  
```bash
python videoWatermarkAdder.py
```

### Configuration  
* **input_video.mp4** — source video
* **output_video_with_watermark.mp4** — output file
* **watermark.png** — watermark image (supports transparency)
* **position** — `(x, y)` placement of watermark
* **scale** — relative size of watermark (default `0.25`)

### Requirements  
* Python 3.8+
* OpenCV (`pip install opencv-python`)
* NumPy (`pip install numpy`)



## 🖼️imageUpscaler.py  
This script provides a Gradio-based interface for image upscaling using pre-trained PyTorch models.

### Features  
* Supports multiple upscaling models (`4xFFHQDAT`, `4xNomos8k_atd_jpg`)
* Automatic device detection (GPU/CPU)
* Real-time progress and statistics
* Outputs both original and upscaled images

### Usage  
```bash
python imageUpscaler.py
```

Then open the Gradio link in your browser to upload and upscale images.

### Requirements  
* Python 3.9+
* PyTorch (`pip install torch`)
* Gradio (`pip install gradio`)
* NumPy (`pip install numpy`)
* Pillow (`pip install pillow`)
* image_gen_aux package and model weights in correct paths

### Model Paths 
Edit the `MODEL_OPTIONS` dictionary in the script to point to your model `.pth` files.