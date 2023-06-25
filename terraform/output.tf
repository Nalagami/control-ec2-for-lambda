output "ec2_global_ips" {
  value = aws_instance.handson_ec2.*.public_ip
}

output "lambda_function_URLs" {
  value = aws_lambda_function_url.endpoint.function_url
}
