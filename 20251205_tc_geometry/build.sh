#!/bin/bash
set -e

# Compile PDF (optional, since the PDF is tracked in git, but good to have the command)
# pdflatex -interaction=nonstopmode tc_geom.tex

# Convert to HTML using the shared utility
cd ../utils && uv run tex2substack.py ../20251205_tc_geometry/tc_geom.tex --output ../20251205_tc_geometry/tc_geom.html

echo "Build complete. Check tc_geom.html"
