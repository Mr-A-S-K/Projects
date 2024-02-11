variable "location" {
  description = "The Azure Region in which all resources groups should be created."
  default = "East US"
}

variable "rg-name" {
  description = "The name of the resource group"
  default = "Adi"
}

variable "storage-account-name" {
  description = "The name of the storage account"
}

variable "index_document" {
  description = "The index document of the static website"
  default = "index.html"
}

variable "error_document" {
  description = "The error document of the static website"
  default = "error.html"  
}

variable "source_content" {
  description = "This is the source content for the static website"
    default = "puzzle"
}