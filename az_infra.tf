resource "azurerm_container_registry" "container_reg" {
  name                = "wsApiTrainingACR"
  resource_group_name = local.rg_name
  location            = local.region
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_container_app_environment" "container_env" {
  name                       = "ws-api-training-env"
  location                   = local.region
  resource_group_name        = local.rg_name
}

resource "azurerm_container_app" "apiserver" {
  name                         = "online-shop-apiserver"
  container_app_environment_id = azurerm_container_app_environment.container_env.id
  resource_group_name          = local.rg_name
  revision_mode                = "Single"

  template {
    container {
      name   = "apiserver"
      image  = "${azurerm_container_registry.container_reg.name}/apiserver:v2"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
    allow_insecure_connections = true
    external_enabled           = true
    transport                  = "http"
    target_port                = 8000
  }
}

# WARNING: the activation of Azure APIM can take from 30 to 40 minutes
# so please wait :)
resource "azurerm_api_management" "apim-dev" {
  name                = "ApiTrainingAPIM"
  location            = local.region
  resource_group_name = local.rg_name
  publisher_name      = "Wavestone"
  publisher_email     = "antoine.thirion@wavestone.com"

  sku_name = "Developer_1"
}

# B1s instances are not available for mysql flexible servers
# resource "azurerm_mysql_flexible_server" "db" {
#   name                   = "ws-api-training-main-db"
#   resource_group_name    = local.rg_name
#   location               = local.region
#   administrator_login    = "user"
#   administrator_password = "WavestoneApiTraining01"
#   backup_retention_days  = 7
#   public_network_access  = "Enabled"
#   sku_name               = "B_Standard_B1ms"
#   version = "8.0.21"

#   storage {
#     size_gb = 20
#   }
# }