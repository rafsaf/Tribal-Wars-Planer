# /bin/bash
curl -k -X POST https://$1:9000/hooks/redeploy -H "Content-Type: application/json" -d "{\"secret\": \"${2}\"}"