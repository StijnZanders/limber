import click
from dotenv import load_dotenv
import os
import yaml
import json
from pathlib import Path
from limber.main.limber_terraform_stack import LimberTerraformStack
from cdktf import App
load_dotenv()

TERRAFORM_DIRECTORY = "terraform_plan"
CONFIG_FILE = "limber.yaml"

@click.group()
def cli():
    """
    Just the main cli
    """
    load_environment_variables()


def load_environment_variables():
    absolute_config_file = os.path.abspath(CONFIG_FILE)

    with open(absolute_config_file) as file:
        yaml_config = yaml.safe_load(file.read())

    os.environ["CLOUD_FUNCTIONS_SERVICE_ACCOUNT_EMAIL"] = yaml_config["cloud"]["cloud_functions_service_account"]

    os.environ["TERRAFORM_ORGANIZATION"] = yaml_config["terraform"]["organization"]
    os.environ["TERRAFORM_WORKSPACE"] = yaml_config["terraform"]["workspace"]
    os.environ["TERRAFORM_SECRETS"] = json.dumps(yaml_config["terraform"]["secrets"])


@cli.command("plan")
def init():

    """
    Initializes Limber
    """
    # Create a folder for the output
    Path(TERRAFORM_DIRECTORY).mkdir(exist_ok=True)

    # Create initial terraform config there
    absolute_config_file = os.path.abspath(CONFIG_FILE)

    with open(absolute_config_file) as file:
        yaml_config = yaml.safe_load(file.read())

    namespace = "limber"
    project = yaml_config["cloud"]["project"]
    region = yaml_config["cloud"]["region"]
    cloud_storage_bucket = yaml_config["cloud"]["default_bucket"]
    cloud_storage_bucket_location = yaml_config["cloud"]["default_bucket_location"]

    app = App()
    stack = LimberTerraformStack(app, namespace, project, region, cloud_storage_bucket, cloud_storage_bucket_location, "terraform_plan")
    app.synth()


if __name__ == '__main__':
    cli()
