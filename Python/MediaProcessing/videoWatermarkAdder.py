import cv2
import numpy as np
import argparse
import sys
from pathlib import Path


def add_watermark(input_video, output_video, watermark_path, position='bottom-right', 
                 scale=0.2, opacity=1.0, codec='h264', preset='medium', crf=23):
    """
    Add a watermark to a video
    
    Args:
        input_video: Path to input video
        output_video: Path to output video
        watermark_path: Path to watermark image
        position: Position preset or tuple (x, y)
        scale: Watermark scale relative to video (0.0-1.0)
        opacity: Watermark opacity (0.0-1.0)
        codec: Output codec (h264, h265, xvid, copy)
        preset: Encoding preset (ultrafast, fast, medium, slow)
        crf: Constant Rate Factor for quality (0-51, lower=better)
    """
    # Open video
    video_capture = cv2.VideoCapture(str(input_video))
    if not video_capture.isOpened():
        raise IOError(f"Cannot open video  file: {input_video}")
    
    # Load watermark
    watermark = cv2.imread(str(watermark_path), cv2.IMREAD_UNCHANGED)
    if watermark is None:
        raise IOError(f"Cannot read watermark image: {watermark_path}")
    
    # Get video properties
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video: {frame_width}x{frame_height} @ {fps:.2f} FPS, {total_frames} frames")
    
    # Resize watermark
    target_w = int(frame_width * scale)
    target_h = int(frame_height * scale)
    watermark = cv2.resize(watermark, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Prepare watermark with alpha channel
    has_alpha = watermark.shape[2] == 4 if len(watermark.shape) == 3 else False
    if has_alpha:
        alpha_mask = (watermark[:, :, 3] / 255.0) * opacity
        watermark_rgb = watermark[:, :, :3]
    else:
        watermark_rgb = watermark
        alpha_mask = np.ones((watermark_rgb.shape[0], watermark_rgb.shape[1])) * opacity
    
    wm_h, wm_w = watermark_rgb.shape[:2]
    
    # Calculate position
    if isinstance(position, tuple):
        x, y = position
    else:
        padding = 10
        position_map = {
            'top-left': (padding, padding),
            'top-right': (frame_width - wm_w - padding, padding),
            'bottom-left': (padding, frame_height - wm_h - padding),
            'bottom-right': (frame_width - wm_w - padding, frame_height - wm_h - padding),
            'center': ((frame_width - wm_w) // 2, (frame_height - wm_h) // 2),
        }
        x, y = position_map.get(position, (padding, padding))
    
    print(f"Watermark: {wm_w}x{wm_h} at position ({x}, {y})")
    print(f"Opacity: {opacity:.1%}, Has alpha: {has_alpha}")
    
    # Setup video writer
    if codec == 'copy':
        print("Warning: 'copy' codec not supported, using h264")
        codec = 'h264'
    
    codec_map = {
        'h264': 'H264',
        'h265': 'HEVC',
        'hevc': 'HEVC',
        'xvid': 'XVID',
        'mjpeg': 'MJPG',
    }
    
    fourcc_str = codec_map.get(codec.lower(), 'H264')
    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
    
    print(f"Output codec: {fourcc_str}, CRF: {crf}")
    
    output_video = cv2.VideoWriter(str(output_video), fourcc, fps, (frame_width, frame_height))
    
    if not output_video.isOpened():
        raise IOError(f"Cannot create output video: {output_video}")
    
    # Process frames with progress
    frame_count = 0
    print("\nProcessing frames:")
    print_interval = max(1, total_frames // 20)  # Print progress 20 times
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Check bounds
        if y + wm_h > frame_height or x + wm_w > frame_width:
            print(f"Warning: Watermark goes out of bounds at frame {frame_count}, skipping overlay")
        else:
            # Extract region of interest
            roi = frame[y:y+wm_h, x:x+wm_w]
            
            # Blend watermark with alpha
            blended = (roi * (1 - alpha_mask[..., None]) + watermark_rgb * alpha_mask[..., None]).astype(np.uint8)
            frame[y:y+wm_h, x:x+wm_w] = blended
        
        output_video.write(frame)
        frame_count += 1
        
        # Progress update
        if frame_count % print_interval == 0 or frame_count == total_frames:
            progress = (frame_count / total_frames) * 100 if total_frames > 0 else 0
            print(f"  Progress: {frame_count}/{total_frames} frames ({progress:.1f}%)")
    
    # Cleanup
    video_capture.release()
    output_video.release()
    cv2.destroyAllWindows()
    
    print(f"\n✓ Watermark added successfully!")
    print(f"  Output: {output_video}")


def batch_add_watermark(video_files, watermark_path, output_dir=None, **kwargs):
    """Add watermark to multiple videos"""
    output_dir = Path(output_dir) if output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    for video_file in video_files:
        video_path = Path(video_file)
        
        if not video_path.exists():
            print(f"\n⚠️  Skipping {video_file}: File not found")
            continue
        
        # Determine output path
        if output_dir:
            output_path = output_dir / f"{video_path.stem}_watermarked{video_path.suffix}"
        else:
            output_path = video_path.parent / f"{video_path.stem}_watermarked{video_path.suffix}"
        
        try:
            print(f"\n{'='*60}")
            print(f"Processing: {video_path.name}")
            print('='*60)
            add_watermark(video_file, output_path, watermark_path, **kwargs)
        except Exception as e:
            print(f"✗ Error processing {video_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Add watermark to videos with position and opacity control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Position Presets:
  top-left, top-right, bottom-left, bottom-right, center
  Or use custom coordinates: --position 100 200

Examples:
  # Basic watermark
  %(prog)s input.mp4 watermark.png -o output.mp4
  
  # Custom position and opacity
  %(prog)s video.mp4 logo.png -o output.mp4 --position top-left --opacity 0.7
  
  # Larger watermark with custom position
  %(prog)s video.mp4 logo.png -o output.mp4 --scale 0.3 --position 50 50
  
  # High quality H.265 output
  %(prog)s video.mp4 logo.png -o output.mp4 --codec h265 --crf 18
  
  # Batch processing
  %(prog)s video1.mp4 video2.mp4 video3.mp4 --watermark logo.png --batch --output-dir watermarked
        '''
    )
    
    parser.add_argument('input', nargs='*', help='Input video file(s)')
    parser.add_argument('watermark', nargs='?', help='Watermark image file (PNG recommended)')
    parser.add_argument('-o', '--output', help='Output video file')
    parser.add_argument('--position', nargs='+', default='bottom-right',
                       help='Watermark position (preset or x y coordinates)')
    parser.add_argument('--scale', type=float, default=0.2,
                       help='Watermark scale relative to video (default: 0.2)')
    parser.add_argument('--opacity', type=float, default=1.0,
                       help='Watermark opacity 0.0-1.0 (default: 1.0)')
    parser.add_argument('--codec', default='h264',
                       choices=['h264', 'h265', 'hevc', 'xvid', 'mjpeg'],
                       help='Output video codec (default: h264)')
    parser.add_argument('--crf', type=int, default=23,
                       help='Constant Rate Factor 0-51, lower=better (default: 23)')
    parser.add_argument('--batch', action='store_true',
                       help='Batch mode: process multiple videos')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        if not args.input:
            parser.error("At least one input video is required")
        
        if not args.watermark and not args.batch:
            parser.error("Watermark image is required")
        
        # Parse position
        if isinstance(args.position, list):
            if len(args.position) == 2:
                try:
                    position = (int(args.position[0]), int(args.position[1]))
                except ValueError:
                    position = ' '.join(args.position)
            else:
                position = args.position[0]
        else:
            position = args.position
        
        # Validate scale and opacity
        if not 0.0 <= args.scale <= 1.0:
            parser.error("Scale must be between 0.0 and 1.0")
        if not 0.0 <= args.opacity <= 1.0:
            parser.error("Opacity must be between 0.0 and 1.0")
        
        # Batch mode
        if args.batch or len(args.input) > 1:
            # In batch mode, watermark comes from --watermark flag
            if not args.watermark:
                # Try to use second positional arg as watermark
                if len(args.input) > 1:
                    watermark = args.input[1]
                    videos = [args.input[0]]
                else:
                    parser.error("Watermark path required for batch mode")
            else:
                watermark = args.watermark
                videos = args.input
            
            batch_add_watermark(
                videos,
                watermark,
                output_dir=args.output_dir,
                position=position,
                scale=args.scale,
                opacity=args.opacity,
                codec=args.codec,
                crf=args.crf
            )
        
        # Single file mode
        else:
            input_video = args.input[0]
            watermark = args.watermark
            
            if not args.output:
                input_path = Path(input_video)
                output_video = input_path.parent / f"{input_path.stem}_watermarked{input_path.suffix}"
            else:
                output_video = args.output
            
            add_watermark(
                input_video,
                output_video,
                watermark,
                position=position,
                scale=args.scale,
                opacity=args.opacity,
                codec=args.codec,
                crf=args.crf
            )
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
