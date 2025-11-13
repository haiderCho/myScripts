import os
import time
import tempfile
import gradio as gr
import torch
import numpy as np
from PIL import Image
from image_gen_aux import UpscaleWithModel
from image_gen_aux.utils import load_image
from torch.cuda.amp import autocast

# Available models
MODEL_OPTIONS = {
    "4xFFHQDAT": "/teamspace/studios/this_studio/4xFFHQDAT/4xFFHQDAT.pth",
    "4xNomos8k_atd_jpg": "/teamspace/studios/this_studio/4xFFHQDAT/4xNomos8k_atd_jpg.pth",
}

# Device check
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    device = torch.device("cuda")
    print(f"Using device: {device}")
    print(f"GPU memory used: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    print(f"GPU memory reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
    torch.cuda.empty_cache()
else:
    device = torch.device("cpu")
    print(f"CUDA not available. Using device: {device}")


def upscale_image(image_path, selected_model):
    model_path = MODEL_OPTIONS[selected_model]

    original_output_path = None
    upscaled_output_path = None

    try:
        print("\n[INFO] Starting upscaling process...")
        start_time = time.time()

        # Load original image
        original = load_image(image_path)

        if isinstance(original, Image.Image):
            print(f"Original loaded as PIL. Size: {original.size}")
            original_pil = original.convert("RGB")
            original_array = np.array(original_pil)
        else:
            print(f"Original loaded as numpy array. Shape: {original.shape}")
            original_array = original
            original_pil = Image.fromarray(original_array)

        # Save original to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            original_pil.save(temp_file.name, format="PNG")
            original_output_path = temp_file.name

        print(
            f"Original stats: min={original_array.min()}, max={original_array.max()}, mean={original_array.mean():.4f}"
        )

        # Preprocess for model
        if original_array.ndim == 3 and original_array.shape[2] == 3:
            original_array = original_array.transpose((2, 0, 1))

        original_array = original_array.astype(np.float32) / 255.0
        input_tensor = torch.from_numpy(original_array).unsqueeze(0).to(device)

        print(
            f"Input tensor stats: min={input_tensor.min().item()}, "
            f"max={input_tensor.max().item()}, mean={input_tensor.mean().item():.4f}"
        )

        # Load model
        upscaler = UpscaleWithModel.from_pretrained(model_path).to(device)
        print(f"Model loaded: {selected_model}")

        # Run upscaling
        with torch.no_grad():
            upscaled_result = upscaler(
                input_tensor.float(),
                tiling=True,
                tile_width=256,
                tile_height=256,
            )

        # Handle output
        if isinstance(upscaled_result, Image.Image):
            upscaled_pil = upscaled_result
        else:
            upscaled_tensor = upscaled_result
            upscaled_array = upscaled_tensor.squeeze().cpu().numpy()
            if upscaled_array.shape[0] == 3:  # CHW -> HWC
                upscaled_array = upscaled_array.transpose((1, 2, 0))
            upscaled_array = np.clip(upscaled_array * 255, 0, 255).astype(np.uint8)
            upscaled_pil = Image.fromarray(upscaled_array)

        # Save upscaled image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            upscaled_pil.save(temp_file.name, format="PNG")
            upscaled_output_path = temp_file.name

        elapsed = time.time() - start_time
        print(f"[INFO] Upscaling finished in {elapsed:.2f} seconds")
        print(f"Original saved at: {original_output_path}")
        print(f"Upscaled saved at: {upscaled_output_path}")

        return original_output_path, upscaled_output_path

    except Exception as e:
        print(f"[ERROR] During upscaling: {str(e)}")
        raise


# Gradio interface
iface = gr.Interface(
    fn=upscale_image,
    inputs=[
        gr.Image(type="filepath", label="Upload Image"),
        gr.Dropdown(choices=list(MODEL_OPTIONS.keys()), label="Select Model"),
    ],
    outputs=[
        gr.Image(type="filepath", label="Original Image"),
        gr.Image(type="filepath", label="Upscaled Image"),
    ],
    title="Image Upscaler",
    description="Upload an image and upscale it using the selected model.",
)

iface.launch(share=True)