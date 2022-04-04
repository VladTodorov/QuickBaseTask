
import unittest
import os
import json
import requests
import random

import QuickbaseTask


class TestQuickbaseTask(unittest.TestCase):
    def test_say_hello(self):
        domain = input("Enter domain name: ")
        if domain == "":
            domain = "vlad"
        
        git_token = os.getenv('GITHUB_TOKEN', "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")
        fresh_token = os.getenv('FRESHDESK_TOKEN', "AiZCyFmU7x4N8aHGTVTo")
        password = "x"

        ##tests if github user info is being properly extracted/parsed
        test1 = {'name': 'Chris Wanstrath', 'email': None, 'unique_external_id': '2'}
        test2 = {'name': 'The Octocat', 'email': None, 'unique_external_id': '583231'}
        test3 = {'name': 'VladTodorov', 'email': None, 'unique_external_id': '45175856'}
        self.assertEqual(QuickbaseTask.make_contact("defunkt", git_token, password), test1)
        self.assertEqual(QuickbaseTask.make_contact("octocat", git_token, password), test2)
        self.assertEqual(QuickbaseTask.make_contact("VladTodorov", git_token, password), test3)
        
        '''
        #deletes test_contact if it exists
        cont = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts?unique_external_id="+ "2", auth = (fresh_token, password))
        if cont.content.decode('utf-8') != "[]":
            cont_json = json.loads(cont.text)
            r = requests.delete("https://"+ domain +".freshdesk.com/api/v2/contacts/"+ str(cont_json[0]["id"]), auth = (fresh_token, password))
            r = requests.delete("https://"+ domain +".freshdesk.com/api/v2/contacts/"+ str(cont_json[0]["id"]) +"/hard_delete", auth = (fresh_token, password))
            #print(r.status_code)
        '''

        ##adds contact to freshdesk
        test_contct = QuickbaseTask.make_contact("defunkt", git_token, password)
        test_contct = QuickbaseTask.to_freshdesk(test_contct, domain, git_token, fresh_token, password, "1")
        #print(test_contct)

        ##gets contact from freshdesk
        cont = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts?unique_external_id="+ test_contct["unique_external_id"], auth = (fresh_token, password))
        cont_json = json.loads(cont.text)
        #print(cont_json)
        

        ##checks if contact was added properly
        self.assertEqual(cont_json[0]["name"], "Chris Wanstrath")
        self.assertEqual(cont_json[0]["email"], None)


        ##change test_contact's email in freshdesk
        test_contct["email"] = "etest"+str(random.randint(0,5000000))+"@example.com"
        #print(test_contct["email"]);
        test_contct = QuickbaseTask.to_freshdesk(test_contct, domain, git_token, fresh_token, password, "2", "2")

        ##gets contact from freshdesk and checks if contact email was properly updated
        cont = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts?unique_external_id="+ test_contct["unique_external_id"], auth = (fresh_token, password))
        cont_json = json.loads(cont.text)
        #print(cont_json)

        self.assertEqual(cont_json[0]["email"], test_contct["email"])
        '''
        #resets test_contact's email
        test_contct["email"] = ""
        test_contct = QuickbaseTask.to_freshdesk(test_contct, domain, git_token, fresh_token, password, "2", "2")
        cont = requests.get("https://"+ domain +".freshdesk.com/api/v2/contacts?unique_external_id="+ test_contct["unique_external_id"], auth = (fresh_token, password))
        cont_json = json.loads(cont.text)
        #print(cont_json)

        self.assertEqual(cont_json[0]["email"], None)
        '''
      

if __name__ == '__main__':
    unittest.main()
