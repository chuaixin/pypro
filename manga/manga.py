import os
from PIL import Image

directory = './manga/stack/'  # 替换为实际的目录路径
#检索目录中的所有文件及目录
image_paths = []
for root, dirs, files in os.walk(directory):
    for file in files:
        image_paths.append(os.path.join(root, file))    


print(image_paths)  

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


