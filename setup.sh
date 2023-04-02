#!/bin/bash

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -rpi) RPI=true ;;
    *) echo "Unknown parameter passed: $1."; exit 1 ;;
  esac
  shift
done

if [[ $RPI == true ]]; then
  echo "RPI setup mode."
else
  echo "Simple setup mode."
fi

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
if [[ $RPI == true ]]; then
  pip install -r rpi_requirements.txt
fi

echo "Setup finished."
