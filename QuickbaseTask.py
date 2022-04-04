#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import requests

def make_contact(user, git_token, password):
    
    raw_contact = requests.get("https://api.github.com/users/" + user, auth = (git_token, password))
    raw_contact_json = json.loads(raw_contact.text)

    #print(raw_contact_json)

    contact = {
        "name": raw_contact_json["name"],
        "email": raw_contact_json["email"],
        "unique_external_id": str(raw_contact_json["id"])
    }
    if contact["name"] == None:
        contact["name"] = raw_contact_json["login"]
    
    #contact["name"] = "dan"

    #print(contact)

    return contact


def to_freshdesk(contact, domain, git_token, fresh_token, password, action, update = "0"):
    headers = { "Content-Type" : "application/json" }

    
    if action == "1":
        r = requests.post("https://"+ domain +".freshdesk.com/api/v2/contacts", auth = (fresh_token, password), data = json.dumps(contact), headers = headers)
        print(contact["name"] + " added to contacts")
        #print(r.content)
    elif action == "2":
        cont = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts?unique_external_id="+ contact["unique_external_id"], auth = (fresh_token, password), data = json.dumps(contact), headers = headers)
        cont_json = json.loads(cont.text)
        cont_id = str(cont_json[0]["id"])

        if update == "1":
            r = requests.put("https://"+ domain +".freshdesk.com/api/v2/contacts/"+ cont_id, auth = (fresh_token, password), data = json.dumps({"name": contact["name"]}), headers = headers)
            #r = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts/"+ cont_id, auth = (fresh_token, password))
            print(contact["name"] + "'s name updated")
            #print(r.content)
        elif update == "2":
            #contact["email"] = ""
            r = requests.put("https://"+ domain +".freshdesk.com/api/v2/contacts/"+ cont_id, auth = (fresh_token, password), data = json.dumps({"email": contact["email"]}), headers = headers)
            print(contact["email"] + "'s email updated")
            #print(r.content)
            #print(r.content)

    return contact

    
    

def main():
    git_token = os.getenv('GITHUB_TOKEN', "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")
    fresh_token = os.getenv('FRESHDESK_TOKEN', "AiZCyFmU7x4N8aHGTVTo")
    password = "x"

    domain = input("Enter domain name: ")
    if domain == "":
        domain = "vlad"

    action = input("Would you like to Create(1) or Update(2) a contact? ")
    user = input("Enter GitHub User's username: ")
    update = "0"
    if action == "2":
        update = input("Would you like to update contacts name(1) or email(2)? ")

    contact = make_contact(user, git_token, password)
    #print(type(contact))

    to_freshdesk(contact, domain, git_token, fresh_token, password, action, update)

        

if __name__ == '__main__':
    main()



    
