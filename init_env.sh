#!/bin/bash

set -e

ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
    read -p ".env file already exists. Overwrite? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

DB_URL="postgresql+psycopg2://username:password@domain"
BUILD_PATH="./builds"
REPO_PATH="./repos"
VERSION_POLL_TIME=60

read -p "Database URL [$DB_URL]: " input
DB_URL=${input:-$DB_URL}

read -p "Build path [$BUILD_PATH]: " input
BUILD_PATH=${input:-$BUILD_PATH}

read -p "Repository path [$REPO_PATH]: " input
REPO_PATH=${input:-$REPO_PATH}

read -p "Version poll time (seconds) [$VERSION_POLL_TIME]: " input
VERSION_POLL_TIME=${input:-$VERSION_POLL_TIME}

mkdir -p "$BUILD_PATH" "$REPO_PATH" 2>/dev/null || true

cat > "$ENV_FILE" << EOF
DB_URL=$DB_URL
BUILD_PATH=$BUILD_PATH
REPO_PATH=$REPO_PATH
VERSION_POLL_TIME=$VERSION_POLL_TIME
EOF

echo ".env file created successfully."
echo ""
echo "Contents:"
cat "$ENV_FILE"