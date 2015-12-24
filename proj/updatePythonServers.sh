#!/bin/env bash
while [ true ]; do
 python manage.py hello_world
 python manage.py update_python_servers
 sleep 30
done
