terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
}

resource "google_compute_network" "vpc_network" {
  project = var.project
  name    = "private-network"
}

resource "google_compute_instance" "vm_api_server" {
  name         = "api-server"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    device_name = "api-server"
    initialize_params {
      # disk optimized for containers
      # image = "cos-cloud/cos-stable"
      image = "debian-cloud/debian-12"
      type  = "pd-balanced"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    # access_config parameter gives the VM an external IP address, making it accessible over
    # the internet
    access_config {}
  }

  metadata = {
    "ssh-keys" = "anthirion: ${var.public_key}"
  }

  tags = ["api-server"]

}

resource "google_compute_instance" "mysql_vm" {
  name         = "db-server"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    device_name = "db-server"
    initialize_params {
      image = "debian-cloud/debian-12"
      type  = "pd-balanced"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    # access_config parameter gives the VM an external IP address, making it accessible over
    # the internet
    access_config {}
  }

  metadata = {
    "ssh-keys" = "anthirion: ${var.public_key}"
  }

  tags = ["db-server"]

}

# Règle de firewall autorisant le protocole ICMP (pour les ping) sur
# toutes les machines du VPC private-network
resource "google_compute_firewall" "allow-icmp" {
  name      = "allow-icmp"
  network   = google_compute_network.vpc_network.name
  direction = "INGRESS"

  allow {
    protocol = "icmp"
  }

  source_ranges = ["0.0.0.0/0"] # Autorise l'accès depuis n'importe quelle adresse IP
}

# Règle de firewall pour autoriser SSH sur toutes les machines du VPC private-network
resource "google_compute_firewall" "allow-ssh" {
  name      = "allow-ssh"
  network   = google_compute_network.vpc_network.name
  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# Règle de firewall pour autoriser les requêtes SQL entrantes
resource "google_compute_firewall" "allow-ingress-sql" {
  name      = "allow-ingress-sql"
  network   = google_compute_network.vpc_network.name
  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["3306"]
  }

  source_ranges = ["0.0.0.0/0"]
  # source_tags = ["db-server"] # Appliquer cette règle uniquement à la VM DB
}

# Règle de firewall pour autoriser les requêtes SQL sortantes
resource "google_compute_firewall" "allow-egress-sql" {
  name      = "allow-egress-sql"
  network   = google_compute_network.vpc_network.name
  direction = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["3306"]
  }
}

# Règle de firewall pour autoriser les requêtes HTTP entrantes
resource "google_compute_firewall" "allow-ingress-http" {
  name      = "allow-ingress-http"
  network   = google_compute_network.vpc_network.name
  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports    = ["80", "8000"]
  }

  source_ranges = ["0.0.0.0/0"]
  # source_tags = ["api-server"]
}

# Règle de firewall pour autoriser les requêtes HTTP sortantes
resource "google_compute_firewall" "allow-egress-http" {
  name      = "allow-egress-http"
  network   = google_compute_network.vpc_network.name
  direction = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["80", "8000"]
  }
}
