import os
import sys
import json
import subprocess

def get_scan_variables():
  """
  Get the necessary pipeline variables to execute engineering scans.
  """
  try:
    variables_map = {
      # "SECURED_VAR": ("ENV_VAR_NAME", True),
      "APP_REPO_SLUG": ("BITBUCKET_REPO_SLUG", False),
      "BITBUCKET_BRANCH": ("BITBUCKET_BRANCH", False),
      "BITBUCKET_COMMIT": ("BITBUCKET_COMMIT", False),
      "BITBUCKET_PROJECT_KEY": ("BITBUCKET_PROJECT_KEY", False),
      "BITBUCKET_STEP_TRIGGERER_UUID": ("BITBUCKET_STEP_TRIGGERER_UUID", False),
    }

    return [
      {
        "key": key,
        "value": os.getenv(env_var, ""),
        "secured": secured
      }
      for key, (env_var, secured) in variables_map.items()
    ]
  except Exception as ex:
    error_info = {
      "type": "error",
      "action": "get scan variables",
      "error": str(ex),
    }
    print(json.dumps(error_info, indent=2))
    sys.exit(1)

def define_scan_variables():
  """
  Define variáveis de ambiente necessárias para o pipeline e grava em set_env.sh
  """
  scan_variables = get_scan_variables()
  scan_variables_as_json = json.dumps(scan_variables)
  scan_pipeline_name = "execute-scans"

  if os.getenv("BITBUCKET_BRANCH", "") == "main":
    scan_pipeline_name = "execute-scans-main"

  env_vars = {
    "IT_ENGINEERING_SCANS_VARIABLES": scan_variables_as_json,
    "IT_ENGINEERING_SCANS_PIPELINE_NAME": scan_pipeline_name,
  }

  set_env_content = ""

  for key, value in env_vars.items():
    os.environ[key] = value  # já exportando no "runtime" do Python
    set_env_content += f"export {key}='{value}'\n"

  print("exported variables:")
  print(json.dumps(env_vars, indent=2))

  # Salva as variáveis no arquivo set_env.sh (caso outro processo precise 'sourcear')
  with open("set_env.sh", "w", encoding="utf-8") as f:
    f.write(set_env_content)

def authenticate_aws_ecr():
  """
  Autentica no ECR usando as variáveis de ambiente passadas.
  """
  try:
    account_id = os.getenv("IT_ENG_SCANS_AWS_ACCOUNT_ID")
    region = os.getenv("IT_ENG_SCANS_AWS_DEFAULT_REGION")

    env = os.environ.copy()
    env["AWS_ACCESS_KEY_ID"] = os.getenv("IT_ENG_SCANS_AWS_ACCESS_KEY_ID")
    env["AWS_SECRET_ACCESS_KEY"] = os.getenv("IT_ENG_SCANS_AWS_SECRET_ACCESS_KEY")

    get_login_password_cmd = ["aws", "ecr", "get-login-password", "--region", region]
    password = subprocess.check_output(
      get_login_password_cmd,
      stderr=subprocess.STDOUT,
      text=True,
      env=env
    ).strip()

    ecr_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com"

    docker_login_cmd = [
      "docker",
      "login",
      "--username",
      "AWS",
      "--password-stdin",
      ecr_url,
    ]
    subprocess.run(
      docker_login_cmd,
      input=password,
      check=True,
      text=True,
    )

    print("Successfully logged in to ECR")
  except subprocess.CalledProcessError as e:
    print(f"Failed to login to ECR: {e}")
    sys.exit(1)
  except Exception as ex:
    print(f"An error occurred: {ex}")
    sys.exit(1)

def main():
  define_scan_variables()
  authenticate_aws_ecr()

if __name__ == "__main__":
  main()
