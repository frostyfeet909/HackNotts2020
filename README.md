# Tell Me Done - https://devpost.com/software/tell-me-done

My submission for HackNotts2020

How to run (CL windows):

1. Set twilio information in keys.json
2. ngrok http 3000
3. python example_usage.py

# Team

1. Algernon Sampson : WG6B-1 : First time hacker

# Awards

1. [GitHub] Best Beginner Hack 1st. Place
2. [Twilio] Best Use of Twilio

# Main applications

example_usage.py - An example of what the package does and how it works

data_interface.py - Functions for editing data stored sepratly in json and shelves

phone_numbers.py - Holds a template for how the user information is stored

receiver.py - All things receving from twilio

sender.py - All things being sent using twilio

# Additional files

keys.json - All important twilio info: SID, auth_key, twilio phone number as well as a password for admins.

users - All user data in persistant storage

# Requirements

1. python ~= 3.9
   1. twilio
   2. passlib
2. ngrok
