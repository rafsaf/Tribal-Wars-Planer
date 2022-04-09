# /bin/bash
cd
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y supervisor webhook ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

export NEW_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/redeploy.sh
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/webhooks.conf
wget https://raw.githubusercontent.com/rafsaf/Tribal-Wars-Planer/master/webhook/hooks.example.json
sudo chmod +x redeploy.sh
sed 's/##secret##/'"${NEW_SECRET}"'/' hooks.example.json > hooks.json
rm hooks.example.json
sudo cp webhooks.conf /etc/supervisor/conf.d/webhooks.conf
sudo rm webhooks.conf
sudo openssl req -newkey rsa:4096 -keyout webhook.key -x509 -days 3650 -out webhook.crt -nodes
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start webhooks:*
sudo supervisorctl restart webhooks:*
touch .env
touch docker-compose.yml
echo "Your webhook secret: $NEW_SECRET"
echo "Please fill out .env and docker-compose.yml"