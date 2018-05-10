from moviepy import editor

clip = editor.AudioFileClip("LeCLASICO.wav").subclip(0,60)
clip.audio.write_audiofile("LeCLASICO_60.wav")