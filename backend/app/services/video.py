import os
import subprocess
import asyncio
from typing import List

class VideoComposer:
    def __init__(self):
        pass

    async def create_clip(self, image_path: str, audio_path: str, output_path: str, duration: float):
        """
        Creates a single video clip from an image and audio, applying a simple zoom effect.
        """
        # FFmpeg command for Ken Burns effect (Zoom in)
        # z='min(zoom+0.0015,1.5)': Zoom speed
        # s=1080x1920: Output resolution (9:16)
        
        # We need to ensure the image is scaled to something larger first to avoid upscaling artifacts, 
        # or just start with high res.
        
        # Using subprocess for fine control
        # cmd = [
        #     "ffmpeg", "-y",
        #     "-loop", "1", "-i", image_path,
        #     "-i", audio_path,
        #     "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':d=700:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
        #     "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
        #     "-shortest",
        #     output_path
        # ]
        
        # Simpler approach: fixed scale and crop, then zoom.
        # Note: input images might not be 9:16.
        cmd = f'''
        ffmpeg -y -loop 1 -i "{image_path}" -i "{audio_path}" \
        -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':d={int(duration*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920" \
        -c:v libx264 -t {duration} -pix_fmt yuv420p -shortest "{output_path}"
        '''
        
        # We use shell=True for easier command construction here, but be careful with inputs.
        # For windows compatibility, we might need list format.
        
        # duration * 25 fps = frames (d parameter)
        frames = int(duration * 25)
        
        command = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', image_path,
            '-i', audio_path,
            '-vf', f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            '-t', str(duration),
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"FFmpeg Error: {stderr.decode()}")
            raise Exception("FFmpeg failed to create clip")
        
        return output_path

    async def stitch_videos(self, clip_paths: List[str], final_output_path: str):
        """
        Concatenates multiple video clips into one.
        """
        # Create a text file with file paths for ffmpeg concat
        list_file = "concat_list.txt"
        with open(list_file, "w") as f:
            for path in clip_paths:
                # FFmpeg requires absolute paths or relative with precautions. 
                # Escape backslashes for Windows.
                safe_path = path.replace('\\', '/')
                f.write(f"file '{safe_path}'\n")
        
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            final_output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        # Cleanup list file
        if os.path.exists(list_file):
            os.remove(list_file)
            
        if process.returncode != 0:
             print(f"FFmpeg Stitch Error: {stderr.decode()}")
             raise Exception("FFmpeg failed to stitch videos")
        
        return final_output_path

video_composer = VideoComposer()
