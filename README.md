Programmatic DNS Updater for Digital Ocean
==========================================

What does it do:
----------------
Provide a programmatic way to update records that are managed by Digital Ocean's DNS servers.

Created for:
------------
Updating DNS records when you have a changing ip address.

Inspired From:
--------------
This is a rewrite from scratch project which was inspired by [bensquire's repository](https://github.com/bensquire/Digital-Ocean-Dynamic-DNS-Updater), with simplified and more readable code.  

Usage:
------
 * Get an API TOKEN from ['Personal Access Token'](https://cloud.digitalocean.com/settings/applications).
 * Copy `.env.example` to `.env`
 * Add values to the following variables in the created `.env`:
    * `DIGITAL_OCEAN_TOKEN`
    * `DOMAIN_NAME`
    * `SUBDOMAIN_NAME`
    * `RTYPE`
    * `TTL`
 * Run `pip install requirements.txt` to install the dependencies
 * Run `python3 app.py` to update the DNS record based on data from `.env`
