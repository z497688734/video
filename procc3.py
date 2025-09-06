import cv2
import subprocess

# 输入视频和输出文件路径
input_video = '1_output_3.mp4'  # 输入视频文件
output_no_audio = '1_output_4_no_audio.mp4'  # 裁剪后的视频（无音频）
final_output = '1_output_4.mp4'  # 最终输出的视频（有音频）

# 设置裁剪区域，(x, y, w, h) 为矩形框的起点和宽高
x, y, w, h = 0, 10, 527, 315  # 示例裁剪区域，修改为你需要的区域

# 获取视频信息（帧数、尺寸等）
cap = cv2.VideoCapture(input_video)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_no_audio, fourcc, fps, (w, h))  # 裁剪后的视频大小为 (w, h)

# 读取并处理视频帧
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"🎞️ 开始处理视频帧，共 {frame_count} 帧")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 裁剪帧
    cropped_frame = frame[y:y+h, x:x+w]

    # 写入裁剪后的视频帧
    out.write(cropped_frame)

cap.release()
out.release()
print(f"✅ 视频裁剪完成：{output_no_audio}")

# 使用 FFmpeg 合并音频
print(f"🔊 使用 FFmpeg 将音频合并进视频...")

ffmpeg_cmd = [
    'ffmpeg',
    '-y',  # 自动覆盖输出文件
    '-i', output_no_audio,   # 裁剪后的视频（无音频）
    '-i', input_video,       # 原视频（带音频）
    '-c:v', 'copy',          # 视频直接复制
    '-map', '0:v:0',         # 视频来自第一个输入（裁剪后的视频）
    '-map', '1:a:0',         # 音频来自第二个输入（原视频）
    '-shortest',             # 取最短轨道时长
    final_output
]

subprocess.run(ffmpeg_cmd, check=True)

print(f"🎉 合成完成！输出视频：{final_output}")