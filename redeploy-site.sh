#!/bin/bash
cd /root/pe-portfolio

echo "Fetching latest changes..."
git fetch && git reset origin/main --hard

echo "Stopping containers..."
docker compose -f docker-compose.prod.yml down

echo "Rebuilding and starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment complete!"
