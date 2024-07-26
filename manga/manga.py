import os
from PIL import Image

def get_image_paths(directory):
    image_paths = []
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            # 使用PIL尝试打开文件，如果成功则认为是图片文件
            with Image.open(filepath) as img:
                image_paths.append(filepath)
        except IOError:
            # 如果打开失败，则不是图片文件，跳过
            pass
    return image_paths

# 使用示例
directory = './manga/stack/'  # 替换为实际的目录路径
image_paths = get_image_paths(directory)

# 打印所有找到的图片路径
for path in image_paths:
    im = Image.open(path)  # 导入图片 fp：图片路径
    im.show()  # 展示图片


