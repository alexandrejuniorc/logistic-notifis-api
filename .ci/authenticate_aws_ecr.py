import os
import sys
import subprocess

def authenticate_aws_ecr(account_id, region):
    try:
        get_login_password_cmd = ['aws', 'ecr', 'get-login-password']

        password = subprocess.check_output(
            get_login_password_cmd, 
            stderr=subprocess.STDOUT, 
            text=True,
        ).strip()

        ecr_url = f'{account_id}.dkr.ecr.{region}.amazonaws.com'

        docker_login_cmd = [
            'docker', 
            'login', 
            '--username', 
            'AWS', 
            '--password-stdin', 
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

authenticate_aws_ecr(
    os.getenv("AWS_ACCOUNT_ID"), 
    os.getenv("AWS_DEFAULT_REGION"),
)
