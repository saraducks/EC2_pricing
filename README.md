## Why I wrote this?
Developed this library to solve my own problem while using AWS EC2 CLI. I wanted the CLI to give me the price and pause to proceed before provisioning. So, given an aws cli ec2 provision call, it returns the price of my action. Using python, I called the EC2 pricing API to get JSON pricing files and cache/parse them locally. This is exposed as pricing.py library and called from within AWS CLI source code.

## How it works? 
1. Get the index.JSON file for aws pricing using HTTP
1. Compute the EC2 price based on user input {Based on below options, need to compute EC2 pricing}
   1. On-demand instances {Costs based on hours}
   1. Spot-insatnces {Costs varies every 5 mins and hourly basis}
   1. Reserved instances {It's 1 year/3 year duration}
   1. Dedicated Host {Standard/Convertible 1year/3year term with no-upfront, partial-upfront, all-upfront option}

