import os
import sys
import json

def get_scan_variables():
  """Get the necessary pipeline variables to execute engineering scans."""

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
  scan_variables = get_scan_variables()

  scan_variables_as_json = json.dumps(scan_variables)

  scan_pipeline_name = 'execute-scans'

  if os.getenv("BITBUCKET_BRANCH", "") == 'main':
    scan_pipeline_name = 'execute-scans-main'

  env_vars = {
    "IT_ENGINEERING_SCANS_BRANCH": "main",
    "IT_ENGINEERING_SCANS_REPOSITORY": "lar-it-engineering-scans",
    "IT_ENGINEERING_SCANS_VARIABLES": scan_variables_as_json,
    "IT_ENGINEERING_SCANS_PIPELINE_NAME": scan_pipeline_name,
  }

  set_env_content = ""

  for env_var in env_vars.items():
    os.environ[env_var[0]] = env_var[1]
    set_env_content += f"export {env_var[0]}='{env_var[1]}'\n"

  print("exported variables:")
  print(json.dumps(
    env_vars,
    indent=2,
  ))

  with open('set_env.sh', 'w', encoding='utf-8') as f:
    f.write(set_env_content)

define_scan_variables()
