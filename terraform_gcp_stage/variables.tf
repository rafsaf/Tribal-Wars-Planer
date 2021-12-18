variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "europe-central2"
}

variable "zone" {
  default = "europe-central2-a"
}
variable "public_subnet_ip" {
  default = "10.26.2.0/24"
}
