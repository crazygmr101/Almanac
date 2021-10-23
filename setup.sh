#!/usr/bin/env bash
echo -n Checking if python3.9 exists...
if ! command -v python3.9 &> /dev/null
then
  echo -e "\e[31mNot found\e[0m"
  exit
fi
echo -e "\e[32mFound\e[0m"

echo Installing venv
python3.9 -m pip install virtualenv
if [ $? -eq 1 ]; then exit; fi

echo Creating venv
python3.9 -m virtualenv venv
source ./venv/bin/activate
echo Installing requirements
python3 -m pip install -r requirements.txt

echo Setting up env file
cp -n .env-example .env

if ! command -v micro --version &> /dev/null
then
  micro .env
else
  nano .env
fi

echo Almanac Set up!
echo -e "To run, do \e[3mpython3 main.py\e[0m"