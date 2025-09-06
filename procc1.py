# This is a sample Python script.
import cv2
import numpy as np
import os
import subprocess

def remove_watermark(input_video, temp_video='temp_video.mp4', final_video='final_output.mp4', watermark_area=(50, 50, 200, 50)):
    # 打开原始视频
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("❌ 无法打开视频。")
        return

    # 视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # 写入临时视频（无水印但无音频）
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    print("🚧 正在处理视频帧...")
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 水印区域 (x, y, w, h)
        x, y, w, h = watermark_area

        # 生成掩码
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        mask[y:y+h, x:x+w] = 255

        # 修补水印区域
        inpainted = cv2.inpaint(frame, mask, 5, cv2.INPAINT_NS)

        out.write(inpainted)
        frame_count += 1
        if frame_count % 50 == 0:
            print(f"✅ 已处理 {frame_count} 帧")

    cap.release()
    out.release()
    print(f"🎉 视频帧处理完成，输出临时文件：{temp_video}")

    # 用 FFmpeg 合并音频
    print("🔊 正在合并音频...")
    cmd = [
        "ffmpeg",
        "-y",  # 覆盖输出文件
        "-i", temp_video,          # 新的视频
        "-i", input_video,         # 原始视频（带音频）
        "-c:v", "copy",            # 视频不重新编码
        "-c:a", "aac",             # 保证音频兼容性
        "-map", "0:v:0",           # 用新视频
        "-map", "1:a:0",           # 用原始音频
        final_video
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 成功输出最终视频文件：{final_video}")
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg 合并音频失败：", e)

    # 可选：删除中间文件
    if os.path.exists(temp_video):
        os.remove(temp_video)


if __name__ == '__main__':
    watermark_area = (556, 333, 90, 30)  # 修改为你水印的实际区域
    remove_watermark(
        input_video='1.mp4',
        final_video='1_output_1.mp4',
        watermark_area=watermark_area
    )




