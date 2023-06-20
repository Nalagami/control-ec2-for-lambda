output "ec2_global_ips" {
    value = "${aws_instance.handson_ec2.*.public_ip}"
}