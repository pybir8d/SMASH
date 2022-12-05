
import ffmpeg
file = input("Enter file: ")
input_stream = ffmpeg.input(file, f='mp4')
output_stream = ffmpeg.output(input_stream, 'output.m3u8', format='hls', start_number=0, hls_time=5, hls_list_size=0)
ffmpeg.run(output_stream)
