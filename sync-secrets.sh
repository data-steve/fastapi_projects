# load .env (but don’t export your real secrets forever!)
bash -c '
set -o allexport
source .env
set +o allexport

# loop through the vars you care about
for var in \
  DATABASE_HOSTNAME \
  DATABASE_PORT \
  DATABASE_USERNAME \
  DATABASE_PASSWORD \
  DATABASE_NAME \
  SECRET_KEY \
  ALGORITHM \
  ACCESS_TOKEN_EXPIRE_MINUTES
do
  # push each one into your GitHub repo’s secrets
  gh secret set $var \
    --body "${!var}" \
    --repo data-steve/fastapi_social_media_app
done
'