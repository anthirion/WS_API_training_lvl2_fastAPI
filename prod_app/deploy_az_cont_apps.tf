locals {
  rg_name = "antoine-thirion21378"
  region = "West Europe"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.27.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  subscription_id = "92c9bea0-3c7c-4dda-b314-2c97e654fb1b"
}

resource "azurerm_container_app_environment" "ws-api-training" {
  name                       = "ws-api-training-env"
  location                   = local.region
  resource_group_name        = local.rg_name
}

resource "azurerm_container_app" "apiserver" {
  name                         = "online-shop-api"
  container_app_environment_id = azurerm_container_app_environment.ws-api-training.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"

  template {
    
    container {
      name   = "apiserver"
      image  = "anthirion/apiserver:v2"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    traffic_weight {
      latest_revision = true
      percentage = 100
    }
    allow_insecure_connections = true
    external_enabled = true
    transport = "http"
    target_port = 8000
  }
}