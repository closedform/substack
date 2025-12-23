#!/bin/bash
set -e

# Compile PDF
pdflatex -interaction=nonstopmode network_storage.tex

# Convert to HTML using the shared utility
cd ../utils && uv run tex2substack.py ../20251216_aetherial_network_storage/network_storage.tex --output ../20251216_aetherial_network_storage/network_storage.html

echo "Build complete. Check network_storage.pdf and network_storage.html"
