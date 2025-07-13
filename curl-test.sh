#!/bin/bash

RANDOM_SUFFIX=$(date +%s)
NAME="TestUser$RANDOM_SUFFIX"
EMAIL="test$RANDOM_SUFFIX@example.com"
CONTENT="This is a test post made at $RANDOM_SUFFIX"

echo "🔹 Creating timeline post..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/timeline_post \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "Created:"
echo "$CREATE_RESPONSE"

ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

echo "🔹 Checking if post was added (GET)..."
curl -s http://localhost:5000/api/timeline_post | grep "$CONTENT"

echo "🔹 Deleting test post with id $ID..."
curl -s -X DELETE http://localhost:5000/api/timeline_post/$ID
echo "Deleted test post"
