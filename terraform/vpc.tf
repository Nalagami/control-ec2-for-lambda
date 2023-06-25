variable "az_a" {
  default = "ap-northeast-1a"
}

# VPC
resource "aws_vpc" "handson_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "terraform-hadson-vpc"
  }
}

# Subnet
resource "aws_subnet" "handson_public_1a_sn" {
  vpc_id            = aws_vpc.handson_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.az_a

  tags = {
    Name = "terraform-handson-public-1a-sn"
  }
}

resource "aws_internet_gateway" "handson_igw" {
  vpc_id = aws_vpc.handson_vpc.id
  tags = {
    Name = "terraform-handson-igw"
  }
}

resource "aws_route_table" "handson_public_rt" {
  vpc_id = aws_vpc.handson_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.handson_igw.id
  }
  tags = {
    Name = "terraform-handson-public-rt"
  }
}

resource "aws_route_table_association" "handson_public_rt_associate" {
  subnet_id      = aws_subnet.handson_public_1a_sn.id
  route_table_id = aws_route_table.handson_public_rt.id
}

data "http" "ifconfig" {
  url = "http://ipv4.icanhazip.com"
}

variable "allowed_cidr" {
  default = null
}

locals {
  myip         = chomp(data.http.ifconfig.body)
  allowed_cidr = (var.allowed_cidr == null) ? "${local.myip}/32" : var.allowed_cidr
}

resource "aws_security_group" "hadson_ec2_sg" {
  name        = "terraform-hadson-ec2-sg"
  description = "For EC2 Linux"
  vpc_id      = aws_vpc.handson_vpc.id
  tags = {
    Name = "terraform-handson-ec2-sg"
  }

}

# 25565番ポート許可のインバウンドルール
resource "aws_security_group_rule" "inbound_minecraft" {
  type      = "ingress"
  from_port = 25565
  to_port   = 25565
  protocol  = "tcp"
  cidr_blocks = [
    "0.0.0.0/0"
  ]

  # ここでweb_serverセキュリティグループに紐付け
  security_group_id = aws_security_group.hadson_ec2_sg.id
}

# 22番ポート許可のインバウンドルール
resource "aws_security_group_rule" "inbound_ssh" {
  type      = "ingress"
  from_port = 22
  to_port   = 22
  protocol  = "tcp"
  cidr_blocks = [
    "0.0.0.0/0"
  ]

  # ここでweb_serverセキュリティグループに紐付け
  security_group_id = aws_security_group.hadson_ec2_sg.id
}

# 全ポート許可のアウトバウンドルール
resource "aws_security_group_rule" "outbound" {
  type      = "egress"
  from_port = 0
  to_port   = 0
  protocol  = "-1"
  cidr_blocks = [
    "0.0.0.0/0"
  ]

  # ここでweb_serverセキュリティグループに紐付け
  security_group_id = aws_security_group.hadson_ec2_sg.id
}
