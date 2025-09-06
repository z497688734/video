import cv2
import numpy as np
import subprocess
import os


input_video = '1_output_1.mp4'
output_no_audio = '1_output_2.mp4'
final_output = '1_output_3.mp4'

# 区域坐标（你自己已经获取）
x, y, w, h = 141, 114, 348, 106  # 举例

# HSV 颜色范围
lower_color = np.array([80, 0, 203])
upper_color = np.array([100, 86, 255])


cap = cv2.VideoCapture(input_video)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_no_audio, fourcc, fps, (width, height))

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"🎞️ 开始处理视频帧，共 {frame_count} 帧")

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, lower_color, upper_color)

    # 替换目标颜色为白色
    roi[mask > 0] = (255, 255, 255)

    frame[y:y+h, x:x+w] = roi
    out.write(frame)

    frame_idx += 1
    if frame_idx % 30 == 0:
        print(f"✅ 已处理 {frame_idx} 帧")

cap.release()
out.release()
print(f"✅ 视频帧处理完成：{output_no_audio}")

# === Step 2: 使用 FFmpeg 合并音频 ===
print(f"🔊 使用 FFmpeg 将音频合并进视频...")

ffmpeg_cmd = [
    'ffmpeg',
    '-y',  # 自动覆盖输出文件
    '-i', output_no_audio,   # 视频：无音频
    '-i', input_video,       # 音频来源
    '-c:v', 'copy',          # 视频直接复制
    '-map', '0:v:0',         # 视频来自第一个输入
    '-map', '1:a:0',         # 音频来自第二个输入
    '-shortest',
    final_output
]

subprocess.run(ffmpeg_cmd, check=True)

print(f"🎉 合成完成！输出视频：{final_output}")
