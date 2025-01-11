set -a
[ -f ../.env ] && . ../.env
set +a

echo "PERMIT_API_KEY=$PERMIT_API_KEY"
echo "PERMIT_PDP_URL=$PERMIT_PDP_URL"

uvicorn main:app --host 0.0.0.0 --port 3000 --reload