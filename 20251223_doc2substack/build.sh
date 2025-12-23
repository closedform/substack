#!/bin/bash
set -e

# Convert to HTML using the shared utility
cd ../utils && uv run doc2substack.py ../20251223_doc2substack/announcement.md --output ../20251223_doc2substack/announcement.html

echo "Build complete. Check announcement.html"
