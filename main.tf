terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
    random = {
        source = "hashicorp/random"
        version = ">=2.3.0"
    }
  }
}
provider "azurerm" {
  features {}
}

resource "random_uuid" "uuid" { }
data "azurerm_resource_group" "main" {
  name = "SoftwirePilot_BeckyCarter_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "beccar-${var.prefix}-cosmosdb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"
  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }
  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "beccar-${var.prefix}-todo-app"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name

  
}

resource "azurerm_app_service_plan" "main" {
  name                = "beccar-${var.prefix}-app-service-plan"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}
resource "azurerm_app_service" "main" {
  name                = "beccar-${var.prefix}-webapp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|beckycarter/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_CONNECTION_STRING"    = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/${azurerm_cosmosdb_mongo_database.main.name}?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "GITHUB_AUTH_CLIENT_ID" = var.github_auth_client_id
    "GITHUB_AUTH_CLIENT_SECRET" = var.github_auth_client_secret
    "FLASK_SECRET_KEY" = random_uuid.uuid.result
    "OAUTHLIB_INSECURE_TRANSPORT" = 1
  }
}
