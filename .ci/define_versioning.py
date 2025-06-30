import os
import sys
import requests
import json

REPO_SLUG = os.getenv('BITBUCKET_REPO_SLUG')
REPO_OWNER = os.getenv('BITBUCKET_REPO_OWNER')
BRANCH_NAME = os.getenv('BITBUCKET_BRANCH')
COMMIT_HASH = os.getenv('BITBUCKET_COMMIT')
AUTH_TOKEN = os.getenv('BITBUCKET_AUTH_TOKEN')
API_BASE_URL = "https://api.bitbucket.org/2.0/repositories"

common_headers = {
  "Authorization": f"Bearer {AUTH_TOKEN}",
  "Content-Type": "application/json"
}

def get_repository_variable(variable_name: str):
    """it gets a repository variable"""
    get_variables_url = f"{API_BASE_URL}/{REPO_OWNER}/{REPO_SLUG}/pipelines_config/variables/"

    get_variables_response = requests.get(
      get_variables_url,
      headers=common_headers,
      timeout=10,
    )

    if get_variables_response.status_code != 200:
      print(json.dumps(
         {
          "type": "error",
          "action": "get repository variables",
          "url": get_variables_url,
          "error": get_variables_response.text,
        },
        indent=2,
      ))
      sys.exit(1)

    repository_variable = next(
      (
        variable for variable in get_variables_response.json()["values"]
        if variable["key"] == variable_name
      ),
      None,
    )

    if repository_variable is None:
      print(json.dumps(
         {
          "type": "error",
          "action": "find repository variable",
          "error": f"repository variable {variable_name} not found",
        },
        indent=2,
      ))
      sys.exit(1)

    return repository_variable

def update_repository_variable(variable_id: str, new_value: str):
    """it updates a repository variable"""

    update_variable_payload = {
      "value": new_value
    }

    update_variable_url = f"https://api.bitbucket.org/2.0/repositories/{REPO_OWNER}/{REPO_SLUG}/pipelines_config/variables/{variable_id}"

    update_variable_response = requests.put(
      update_variable_url,
      headers=common_headers,
      data=json.dumps(update_variable_payload),
      timeout=10
    )

    if update_variable_response.status_code != 200:
      print(json.dumps(
         {
          "type": "error",
          "action": "update repository variable",
          "url": update_variable_url,
          "error": update_variable_response.text,
        },
        indent=2,
      ))
      sys.exit(1)

def define_app_versioning():
  app_version_variable_name = "APP_VERSION"

  app_version_variable = get_repository_variable(app_version_variable_name)

  major, minor, patch = app_version_variable["value"].split(".")

  if BRANCH_NAME == "main":
    patch = int(patch) + 1

  new_app_version = f"{major}.{minor}.{patch}"

  if new_app_version != app_version_variable["value"]:
    update_repository_variable(app_version_variable["uuid"], new_app_version)

  main_artifact_tag = new_app_version

  if BRANCH_NAME == "develop":
    main_artifact_tag = f"{main_artifact_tag}-dev.{COMMIT_HASH[:7]}"
  elif BRANCH_NAME == "homolog":
    main_artifact_tag = f"{main_artifact_tag}-rc.{COMMIT_HASH[:7]}"
  else:
    main_artifact_tag = f"{main_artifact_tag}.{COMMIT_HASH[:7]}"

  artifact_tags = [main_artifact_tag]

  if not BRANCH_NAME in ["develop", "homolog"] and main_artifact_tag != new_app_version:
    artifact_tags.append(new_app_version)

  env_vars = {
    "APP_ARTIFACT_TAGS": " ".join(artifact_tags),
    "APP_MAIN_ARTIFACT_TAG": main_artifact_tag,
  }

  set_env_content = ""

  for env_var in env_vars.items():
    os.environ[env_var[0]] = env_var[1]
    set_env_content += f'export {env_var[0]}="{env_var[1]}"\n'

  print("exported variables:")
  print(json.dumps(
    env_vars, 
    indent=2,
  ))

  with open('set_env.sh', 'w', encoding='utf-8') as f:
    f.write(set_env_content)

define_app_versioning()
