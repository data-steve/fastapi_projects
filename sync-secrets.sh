#!/usr/bin/env bash
set -euo pipefail

# 1) the name of the environment you want
ENV_NAME="testing"

# 2) figure out your repo slug (owner/repo)
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

# 3) ensure the environment exists (this is idempotent)
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/environments/${ENV_NAME}"

# 4) load your .env (ignore comments/blank lines)
while IFS='=' read -r name value; do
  # skip empty lines or lines starting with '#'
  [[ -z "$name" || "$name" == \#* ]] && continue

  echo "🔒 Setting $name in '$ENV_NAME'…"
  gh secret set "$name" \
    --env "$ENV_NAME" \
    --body "$value"
done < .env

echo "✅ Done! All .env vars are now secrets in the '$ENV_NAME' environment."



# # load .env (but don’t export your real secrets forever!)
# bash -c '
# set -o allexport
# source .env
# set +o allexport

# # loop through the vars you care about
# for var in \
#   DATABASE_HOSTNAME \
#   DATABASE_PORT \
#   DATABASE_USERNAME \
#   DATABASE_PASSWORD \
#   DATABASE_NAME \
#   SECRET_KEY \
#   ALGORITHM \
#   ACCESS_TOKEN_EXPIRE_MINUTES
# do
#   # push each one into your GitHub repo’s secrets
#   gh secret set $var \
#     --body "${!var}" \
#     --repo data-steve/fastapi_social_media_app
# done
# '