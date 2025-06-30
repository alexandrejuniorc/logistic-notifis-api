import os
import sys
import subprocess

APP_VERSION = os.getenv('APP_VERSION')
BITBUCKET_BRANCH = os.getenv('BITBUCKET_BRANCH')
BITBUCKET_COMMIT = os.getenv('BITBUCKET_COMMIT')

def create_new_tag():
    """it creates a new tag based on APP_VERSION variable"""
    try:
        if BITBUCKET_BRANCH != "main":
            print("Promote can only be executed from the main branch.")
            exit(1)

        subprocess.run(["apk", "add", "git"], check=True)

        subprocess.run(["git", "fetch", "--tags"], check=True)

        NEW_TAG = f"v{APP_VERSION}"

        subprocess.run(
          [
            "git",
            "tag",
            "-a",
            NEW_TAG,
            BITBUCKET_COMMIT,
            "-m",
            f"chore: tagging {BITBUCKET_COMMIT} as {NEW_TAG}",
          ],
          check=True,
        )

        subprocess.run(["git", "push", "origin", NEW_TAG])
    except Exception as ex:
        print(f"An error occurred: {ex}")
        sys.exit(1)

create_new_tag()
