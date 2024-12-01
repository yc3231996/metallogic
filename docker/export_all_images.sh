#!/bin/bash

# 文件名设置
OUTPUT_FILE="${1:-/data/metallogic_images.tar}"  # 从参数读取文件路径，默认值为 /data/metallogic_images.tar

# 提取镜像列表
IMAGES=$(docker compose config | grep 'image:' | awk '{print $2}')

# 检查是否有镜像
if [ -z "$IMAGES" ]; then
    echo "No images found in docker-compose.yml"
    exit 1
fi

# 打印镜像列表
echo "Images to be exported:"
for IMAGE in $IMAGES; do
    echo "$IMAGE"
    IMAGE_LIST+="$IMAGE "
done

# 导出镜像
docker save -o "$OUTPUT_FILE" $IMAGE_LIST

if [ $? -eq 0 ]; then
    echo "All images have been exported to $OUTPUT_FILE"
else
    echo "Failed to export images."
    exit 1
fi
