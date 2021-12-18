terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}
resource "google_compute_address" "static" {
  name = "ipv4-address"
}
resource "google_compute_network" "vpc_network" {
  name                    = "twp-network"
  auto_create_subnetworks = "false"
  routing_mode            = "GLOBAL"
}

resource "google_compute_firewall" "allow-http" {
  name    = "twp-allow-http"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports    = ["80", "443", "22", "9000"]
  }
  allow {
    protocol = "icmp"
  }
}

resource "google_compute_subnetwork" "public_subnet" {
  name          = "public-subnet-twp"
  network       = google_compute_network.vpc_network.name
  region        = var.region
  ip_cidr_range = var.public_subnet_ip
}

resource "google_compute_instance" "default-stage" {
  name         = "twp-instance-stage"
  machine_type = "e2-small"
  tags         = ["web", "dev"]

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-lts"
    }
  }
  labels = {
    webserver = "true"
  }
  network_interface {
    subnetwork = google_compute_subnetwork.public_subnet.name
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }
}
