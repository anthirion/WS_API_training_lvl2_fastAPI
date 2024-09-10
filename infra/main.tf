terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials =   file(var.credentials_file)
  project     =   var.project
  region      =   var.region
}

resource "google_compute_network" "vpc_network" {
  name = "private-network"
}

# resource "google_compute_instance" "vm_api_server" {
#   name          =  "api-server"
#   machine_type  =  "e2-micro"
#   zone          =  var.zone

#   boot_disk {
#     initialize_params {
#       # disk optimized for containers
#       image = "cos-cloud/cos-stable"
#     }
#   }

#   network_interface {
#     network = google_compute_network.vpc_network.name
#     # access_config parameter gives the VM an external IP address, making it accessible over
#     # the internet
#     # TO REMOVE
#     access_config {
#     }
#   }
# }

resource "google_compute_instance" "vm_mysql" {
  name          =   "db"
  machine_type  =   "e2-micro"
  zone          =   var.zone

  boot_disk {
    # auto_delete = "true"
    initialize_params {
      image = "debian-cloud/debian-11"
      # Taille du disque en Go
      # size  = 20
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    # access_config parameter gives the VM an external IP address, making it accessible over
    # the internet
    access_config {
    }
  }

  # Tags pour identifier les règles de firewall à appliquer
  tags = ["db-server"]
}

# Règle de firewall pour autoriser les connexions externes à MySQL (port 3306)
resource "google_compute_firewall" "allow-sql" {
  name    = "allow-port-3306"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3306"]
  }

  source_ranges = ["0.0.0.0/0"]  # Autorise l'accès depuis toutes les adresses IP (à ajuster pour plus de sécurité)

  target_tags = ["db-server"]  # Appliqué aux instances avec le tag "db-server"
}
