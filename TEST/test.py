from PIL import Image, ImageDraw
import os
import math

# Kích thước ảnh
size = 60
center = (size // 2, size // 2)

# Thư mục lưu ảnh
os.makedirs("bullet_splash_topdown", exist_ok=True)

# Màu
bullet_color = (150, 150, 150, 255)
water_color = (0, 200, 255, 255)

# Tổng số frame
frame_count = 10

for frame in range(frame_count):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # === Giai đoạn viên đạn rơi (frame 0-3) ===
    if frame < 4:
        # Vị trí viên đạn dịch dần vào tâm
        y_offset = int((3 - frame) * 6)  # rơi xuống
        draw.ellipse(
            (center[0] - 2, center[1] - 2 - y_offset,
             center[0] + 2, center[1] + 2 - y_offset),
            fill=bullet_color
        )

    # === Giai đoạn splash (frame 3-9) ===
    if frame >= 3:
        # Bán kính gợn sóng tăng dần
        ripple_radius = (frame - 2) * 3
        ripple_alpha = max(50, 255 - (frame - 3) * 30)  # mờ dần
        ripple_color = (0, 200, 255, ripple_alpha)

        # Vẽ 2 vòng gợn sóng
        for i in range(2):
            r = ripple_radius + i * 4
            if r > 0:
                draw.ellipse(
                    (center[0] - r, center[1] - r,
                     center[0] + r, center[1] + r),
                    outline=ripple_color
                )

        # Vẽ giọt nước bắn ra (pixel rời)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = center[0] + math.cos(rad) * (ripple_radius + 2)
            y = center[1] + math.sin(rad) * (ripple_radius + 2)
            draw.rectangle((x, y, x+1, y+1), fill=water_color)

    # Lưu frame
    img.save(f"bullet_splash_topdown/frame_{frame:02d}.png")

print("Đã tạo 10 frame splash nhìn từ trên xuống trong thư mục 'bullet_splash_topdown'.")
