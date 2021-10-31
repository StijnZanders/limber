terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "StijnZanders"

    workspaces {
      name = "limber"
    }
  }
}