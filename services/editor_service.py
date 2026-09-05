from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

def merge_video_audio(clip_paths: list, audio_path: str, project_id: int):
    print("\n✂️ BẮT ĐẦU GIAI ĐOẠN EDIT VIDEO...")
    try:
        # 1. Nạp tất cả các clip câm vào bộ nhớ
        video_clips = []
        for path in clip_paths:
            clip = VideoFileClip(path)
            video_clips.append(clip)
            
        # 2. Nối các clip lại với nhau
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # 3. Nạp file âm thanh TTS
        audio = AudioFileClip(audio_path)
        
        # 4. Đồng bộ thời lượng (Dùng cú pháp MỚI: subclipped)
        min_duration = min(final_video.duration, audio.duration)
        final_video = final_video.subclipped(0, min_duration)
        audio = audio.subclipped(0, min_duration)
        
        # 5. Ghép tiếng vào hình (Dùng cú pháp MỚI: with_audio)
        final_video = final_video.with_audio(audio)
        
        # 6. Xuất xưởng file Video
        output_path = f"outputs/final_project_{project_id}.mp4"
        print(f"⚙️ Đang Render video cuối cùng... Quá trình này có thể mất 1-2 phút.")
        
        final_video.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            logger=None
        )
        
        # Giải phóng bộ nhớ
        for clip in video_clips:
            clip.close()
        audio.close()
        final_video.close()
        
        print(f"🎉 ĐÃ RENDER THÀNH CÔNG SIÊU PHẨM TẠI: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Lỗi khi Edit Video: {e}")
        return None