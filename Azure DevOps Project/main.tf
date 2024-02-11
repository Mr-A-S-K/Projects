resource "azurerm_resource_group" "resource_group" {
  name     = var.rg-name
  location = var.location
}

resource "azurerm_storage_account" "storage_account" {
  name                     = var.storage-account-name
  resource_group_name      = azurerm_resource_group.resource_group.name
  account_tier             = "Standard"
  location                 = var.location
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  static_website {
    index_document = var.index_document
  }
}

resource "azurerm_storage_blob" "index" {
  name                   = "index.html"
  storage_account_name   = azurerm_storage_account.storage_account.name
  storage_container_name = "$web"
  type                   = "Block"
  content_type           = "text/html"
  source_content         = "puzzle.html"
}

resource "azurerm_storage_blob" "index_js" {
  name                   = "index.js"
  storage_account_name   = azurerm_storage_account.storage_account.name
  storage_container_name = "$web"
  type                   = "Block"
  content_type           = "application/javascript"
  source_content         = "index.js"
}

resource "azurerm_storage_blob" "styles_css" {
  name                   = "styles.css"
  storage_account_name   = azurerm_storage_account.storage_account.name
  storage_container_name = "$web"
  type                   = "Block"
  content_type           = "text/css"
  source_content         = "styles.css"
}