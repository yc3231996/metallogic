更新DIFY版本的时候，docker目录下的所有内容都要从dify拷贝过来，同时手动生成.env文件并更新该文件，用dify的docker-compose.yaml文件替换docker-compose-dify.yaml文件.
注意volume文件夹的东西不需要全部copy，只copy github上有的子文件夹。
部署的时候，手动添加openai.env文件（在docker-compose.yaml中指定了），包含OPENAI_API_KEY=XXXX


如果没有网络的情况可以把所有需要的镜像打包，然后传送到目标服务器，再load
sshpass -p '密码' rsync -avz -e "ssh -o StrictHostKeyChecking=no" ubuntu@remote:/data/metallogic_images.tar /home/ec2-user
rsync -avz --progress ubuntu@remote:/data/metallogic_images.tar /home/ec2-user

使用如下命令load：
docker load -i my_image.tar


UCloud - Ubuntu内磁盘扩容：https://docs.ucloud.cn/uhost/guide/disk
sudo apt-get install cloud-initramfs-growroot
LANG=en_US.UTF-8
growpart /dev/vda 1
resize2fs /dev/vda1 (ext4文件系统)
df -TH