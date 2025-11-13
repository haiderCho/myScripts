import cv2
import numpy as np


def add_watermark(input_video_path, output_video_path, watermark_path, position=(10, 10), scale=0.25):
    """Add a watermark to a video and save the output."""
    video_capture = cv2.VideoCapture(input_video_path)
    if not video_capture.isOpened():
        raise IOError(f"Cannot open video file: {input_video_path}")

    watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
    if watermark is None:
        raise IOError(f"Cannot read watermark image: {watermark_path}")

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS) or 30.0

    # Resize watermark once (not every frame)
    target_w = int(frame_width * scale)
    target_h = int(frame_height * scale)
    watermark = cv2.resize(watermark, (target_w, target_h), interpolation=cv2.INTER_AREA)

    has_alpha = watermark.shape[2] == 4
    if has_alpha:
        alpha_mask = watermark[:, :, 3] / 255.0
        watermark_rgb = watermark[:, :, :3]
    else:
        watermark_rgb = watermark

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    wm_h, wm_w = watermark_rgb.shape[:2]
    x, y = position

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if has_alpha:
            # Blend watermark with transparency
            roi = frame[y:y+wm_h, x:x+wm_w]
            if roi.shape[0] != wm_h or roi.shape[1] != wm_w:
                continue  # skip frames where watermark goes out of bounds

            blended = (roi * (1 - alpha_mask[..., None]) + watermark_rgb * alpha_mask[..., None]).astype(np.uint8)
            frame[y:y+wm_h, x:x+wm_w] = blended
        else:
            frame[y:y+wm_h, x:x+wm_w] = watermark_rgb

        output_video.write(frame)

    video_capture.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Watermark added successfully!")


if __name__ == "__main__":
    add_watermark(
        'input_video.mp4',
        'output_video_with_watermark.mp4',
        'watermark.png',
        position=(10, 10),
        scale=0.25
    )
