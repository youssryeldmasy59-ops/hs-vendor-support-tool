#!/bin/bash
# Hungerstation Vendor Support Suite - Auto Launcher Daemon
echo "Starting Vendor Support Suite Server on Port 8080..."
pkill -f "http.server 8080" 2>/dev/null
pkill -f "localtunnel.*hs-vendor-support-suite" 2>/dev/null

sleep 1

cd /Users/usefelbedwehy/Downloads/vendor_support_app
python3 -m http.server 8080 --bind 0.0.0.0 > /tmp/hs_server.log 2>&1 &
npx localtunnel --port 8080 --subdomain hs-vendor-support-suite > /tmp/hs_tunnel.log 2>&1 &

echo "Vendor Support Suite is Live on https://hs-vendor-support-suite.loca.lt"
