from moviepy.editor import VideoFileClip, concatenate_videoclips
# import imageio

# imageio.plugins.ffmpeg.download()


def get_clip(path_to_video, start_ts=0, end_ts=0):
    if start_ts==0 and end_ts==0:
        return VideoFileClip(path_to_video)
    return VideoFileClip(path_to_video).subclip(start_ts, end_ts)


def concatenate_clips(clips, final_clip_name):
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(final_clip_name)


def get_video_from_time_frames(path_to_video, time_frames, result_file_name):
    clips = [get_clip(path_to_video, x, y) for x,y,_ in time_frames]
    concatenate_clips(clips, result_file_name)


def get_audio_from_video(path_to_video, result_file_name, start_ts=0, end_ts=0):
    clip = get_clip(path_to_video, start_ts, end_ts)
    clip.audio.write_audiofile(result_file_name)