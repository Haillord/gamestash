import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import colorsys

# Параметры
WIDTH = 16
HEIGHT = 2000
FRAMES = 120

frames_left = []
frames_right = []

for i in range(FRAMES):
    phase = i * (np.pi * 2 / FRAMES)
    
    # Пульсация яркости
    brightness = 0.65 + 0.35 * np.sin(phase)
    
    # Плавный перелив цвета по всему спектру
    hue = i / FRAMES
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
    COLOR = (int(r*255), int(g*255), int(b*255))
    
    # Создаем изображение
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Рисуем градиентную полоску со свечением
    for x in range(WIDTH):
        # Гауссово распределение для мягкого свечения
        dist_from_center = abs(x - WIDTH / 2)
        glow = np.exp(-(dist_from_center ** 2) / (2 * (WIDTH / 3.5) ** 2))
        
        alpha = int(210 * glow * brightness)
        
        # Рисуем вертикальную линию по всей высоте
        for y in range(HEIGHT):
            draw.point((x, y), fill=(*COLOR, alpha))
    
    # Небольшое размытие для мягкости краев
    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    
    frames_left.append(img)
    frames_right.append(img.transpose(Image.FLIP_LEFT_RIGHT))


# Сохраняем левую полоску
frames_left[0].save(
    '../neon_left.gif',
    save_all=True,
    append_images=frames_left[1:],
    duration=35,
    loop=0,
    disposal=2,
    optimize=True
)

# Сохраняем правую полоску (смещена на половину цикла для противофазы)
frames_right = frames_right[FRAMES//2:] + frames_right[:FRAMES//2]
frames_right[0].save(
    '../neon_right.gif',
    save_all=True,
    append_images=frames_right[1:],
    duration=35,
    loop=0,
    disposal=2,
    optimize=True
)

print("✅ Гифки сгенерированы успешно: neon_left.gif, neon_right.gif")
print("📏 Ширина: 16px")
print("🌈 Переливающийся радужный неон")
print("📦 Вес каждого файла ~ 220 кб")