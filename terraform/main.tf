provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "voice_analyzer" {
  name     = "voice-analyzer-rg"
  location = "East US"
}

resource "azurerm_app_service_plan" "voice_analyzer_plan" {
  name                = "voice-analyzer-plan"
  location            = azurerm_resource_group.voice_analyzer.location
  resource_group_name = azurerm_resource_group.voice_analyzer.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "voice_analyzer_api" {
  name                = "voice-analyzer-api"
  location            = azurerm_resource_group.voice_analyzer.location
  resource_group_name = azurerm_resource_group.voice_analyzer.name
  app_service_plan_id = azurerm_app_service_plan.voice_analyzer_plan.id

  site_config {
    linux_fx_version = "DOCKER|myregistry.azurecr.io/backend"
  }
}

resource "azurerm_app_service" "voice_analyzer_ui" {
  name                = "voice-analyzer-ui"
  location            = azurerm_resource_group.voice_analyzer.location
  resource_group_name = azurerm_resource_group.voice_analyzer.name
  app_service_plan_id = azurerm_app_service_plan.voice_analyzer_plan.id

  site_config {
    linux_fx_version = "DOCKER|myregistry.azurecr.io/frontend"
  }
}

resource "azurerm_mssql_server" "voice_analyzer_db" {
  name                         = "voice-analyzer-db"
  resource_group_name          = azurerm_resource_group.voice_analyzer.name
  location                     = azurerm_resource_group.voice_analyzer.location
  version                      = "12.0"
  administrator_login          = "adminuser"
  administrator_login_password = "SuperSecurePassword!"
}

resource "azurerm_mssql_database" "voice_analyzer_db" {
  name           = "voice_analyzer"
  server_id      = azurerm_mssql_server.voice_analyzer_db.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  max_size_gb    = 5
}