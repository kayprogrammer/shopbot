#!/bin/bash

# Ensure geckodriver has the correct permissions
chmod +x ./geckodriver

# Start the application
gunicorn -b 0.0.0.0:8080 "app:create_app()"
