from PIL import Image

# 打开原始图片
img = Image.open('static/images/games/sprunki-lily.png')

# 调整大小为 32x32 像素
favicon = img.resize((32, 32), Image.Resampling.LANCZOS)

# 保存为 favicon
favicon.save('static/images/games/sprunki-lily-favicon.png', 'PNG')
