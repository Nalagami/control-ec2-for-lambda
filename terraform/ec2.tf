variable "key_name" {
  default = "terraform-handson-keypair"
}

resource "tls_private_key" "handson_private_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

locals {
  public_key_file  = "C:\\Users\\Public\\aws-resource\\${var.key_name}.id_rsa.pub"
  private_key_file = "C:\\Users\\Public\\aws-resource\\${var.key_name}.id_rsa"
}

resource "local_file" "handson_private_key_pem" {
  filename = local.private_key_file
  content  = tls_private_key.handson_private_key.private_key_pem
}

resource "aws_key_pair" "handson_keypair" {
  key_name   = var.key_name
  public_key = tls_private_key.handson_private_key.public_key_openssh
}

data "aws_ssm_parameter" "amzn2_latest_ami" {
  name = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
}

resource "aws_instance" "handson_ec2" {
  ami                         = data.aws_ssm_parameter.amzn2_latest_ami.value
  instance_type               = "t3a.small"
  availability_zone           = var.az_a
  vpc_security_group_ids      = [aws_security_group.hadson_ec2_sg.id]
  subnet_id                   = aws_subnet.handson_public_1a_sn.id
  associate_public_ip_address = "true"
  key_name                    = var.key_name

  # TODO:minecraft起動スクリプトを修正する
  user_data = <<EOF
  #!/bin/bash
  yum install -y https://corretto.aws/downloads/latest/amazon-corretto-17-x64-al2-jre.rpm
  mkdir /home/ec2-user/minecraft
  cd /home/ec2-user/minecraft
  wget https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar
  java -Xmx1024M -Xms1024M -jar server.jar nogui
  wait
  sed -i.bak -e 's/eula=false/eula=true/g' eula.txt
  java -Xmx1024M -Xms1024M -jar server.jar nogui &
  EOF

  tags = {
    Name = "terraform-handson-ec2"
  }
}
