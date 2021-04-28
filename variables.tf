variable "prefix" {
  description = "The prefix used for all resources in this environment"
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default = "uksouth"
}
variable "github_auth_client_id" {
  description = "The GitHub Auth Client Id for this environment"
}
variable "github_auth_client_secret" {
  description = "The GitHub Auth Client Secret for this environment"
}
