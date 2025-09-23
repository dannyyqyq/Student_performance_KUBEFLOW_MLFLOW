# Security Guide
To securely pass DagsHub credentials:
1. Obtain your DagsHub username and token from https://dagshub.com/user/settings/tokens.
2. Pass these as runtime parameters when running the Kubeflow pipeline:
   - `dagshub_username`: Your DagsHub username.
   - `dagshub_token`: Your DagsHub token.
   - `repo_owner`: Your DagsHub username.
   - `repo_name`: Your DagsHub repository name.
3. Avoid hardcoding credentials in scripts or Dockerfiles.