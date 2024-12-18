from PIL import Image
import os

def create_favicon(input_path, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开原始图片
    with Image.open(input_path) as img:
        # 转换为 RGBA 模式（如果不是的话）
        img = img.convert('RGBA')
        
        # 创建标准 favicon 尺寸 (32x32)
        favicon = img.resize((32, 32), Image.Resampling.LANCZOS)
        favicon.save(os.path.join(output_dir, 'favicon.png'), 'PNG')
        
        # 创建 Apple Touch Icon 尺寸 (180x180)
        apple_touch = img.resize((180, 180), Image.Resampling.LANCZOS)
        apple_touch.save(os.path.join(output_dir, 'apple-touch-icon.png'), 'PNG')

if __name__ == '__main__':
    input_path = '/Users/dahuang/Downloads/网站favicon/spranki.png'  # 原始图片路径
    output_dir = 'static/img'  # 输出目录
    create_favicon(input_path, output_dir)
