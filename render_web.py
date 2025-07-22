#!/usr/bin/env python3
"""
Flask app optimized for Render.com deployment
"""
import os
from simple_web import app

# Configuration pour Render.com
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)