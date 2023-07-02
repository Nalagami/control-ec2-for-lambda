#!/bin/bash

# openJDK install
yum install -y https://corretto.aws/downloads/latest/amazon-corretto-17-x64-al2-jre.rpm

# 作業用ディレクトリ作成
mkdir /home/ec2-user/minecraft
cd /home/ec2-user/minecraft

# minecraft server取得
wget https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar

# 起動
java -Xmx1024M -Xms1024M -jar server.jar nogui
wait

# 規約同意
sed -i.bak -e 's/eula=false/eula=true/g' eula.txt

# systemd の準備
cat <<EOF >>/home/ec2-user/minecraft/start.sh
java -Xmx1G -Xms1G -jar /home/ec2-user/minecraft/server.jar nogui
EOF
cat <<EOF >>/etc/systemd/system/minecraft.service
[Unit]
#このUnitファイルの説明をDescriptionにて記載。
Description=launch minecraft spigot server
After=network-online.target

[Service]
#実行するユーザーを指定（指定がないとルートユーザーとして実行することになります）
User=root

#作業するディレクトリを指定（これをしないと「EULAに同意してください」と無限にエラーが出ます）
WorkingDirectory=/home/ec2-user/minecraft

#このサービスとして実行するコマンドの内容
ExecStart=/bin/bash /home/ec2-user/minecraft/start.sh

#サービス停止時の動作（always=常に再起動、on-failure=起動失敗時のみ再起動）
Restart=always

#起動に時間がかかることによる失敗を避けるため、タイムアウト値を設定
TimeoutStartSec=180

[Install]
WantedBy = multi-user.target
EOF
chmod 755 /home/ec2-user/minecraft/start.sh

# systemd 再読み込み
systemctl daemon-reload

# 再起動時期同設定有効、minecraft起動
systemctl enable minecraft.service
systemctl start minecraft.service
