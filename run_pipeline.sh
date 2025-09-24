#!/bin/bash
set -e

mkdir -p ./data

docker run --rm -v "$(pwd)/data:/tmp" ingest:py3.13
docker run --rm -v "$(pwd)/data:/tmp" transform:py3.13
docker run --rm -v "$(pwd)/data:/tmp" train:py3.13