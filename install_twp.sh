# /bin/bash
cd ~
mkdir Tribal-Wars-Planer || true
cd Tribal-Wars-Planer
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose supervisor
export NEW_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/redeploy.sh
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/webhooks.conf
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/hooks.example.json
mv hooks.example.json hooks.json
sed -i 's/##secret##/$NEW_SECRET/' hooks.json
sudo cp webhooks.conf /etc/supervisor/conf.d/webhooks.conf
sudo rm webhooks.conf
sudo openssl req -newkey rsa:4096 -keyout webhook.key -x509 -days 3650 -out webhook.crt -nodes
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start webhooks:*
echo "Your webhook secret: $NEW_SECRET"