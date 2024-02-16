import requests
import os
from threading import Thread
import queue
umls_token = os.getenv('UMLS')

#https://uts-ws.nlm.nih.gov/rest/content/current/source/MSH/D014839/relations?apiKey=

#https://uts-ws.nlm.nih.gov/rest/content/current/source/HPO/HP:0002013/relations?includeRelationLabels=CHD&apiKey=
done = set()

def get_all_id_pages(source_name: str, id: str, umls_token: str):
    url = f"https://uts-ws.nlm.nih.gov/rest/content/current/CUI/{id}/atoms?&sabs={source_name}&apiKey={umls_token}"

    response = requests.get(url).json()

    if "status" in response and str(response["status"]) == "404":
        return ""
    else:
        #print ("response", response)

        page_count = int(response["pageCount"])

        #print ("page_count", page_count)
        
        result = get_id(response, source_name)

        if len(result) > 0:
            return result
        else:
            for i in range(2, page_count+1):
                new_url = url + f"&pageNumber={i}"

                new_response = requests.get(new_url).json()


                result = get_id(new_response, source_name)

                if len(result) > 0:
            
                    return result


def get_id(response: str, source_name: str):

    if "result" not in response:
        return ""

    else:
        for r in response["result"]:
            if r["rootSource"] == source_name:
                return r["code"].split("/")[-1]
  
        return ""


def search(query_name: str, umls_token: str):

    url = f"https://uts-ws.nlm.nih.gov/rest/search/current?string={query_name}&apiKey={umls_token}"

    response = requests.get(url).json()

    #print ("response", response, type(response))

    if "status" in response and str(response["status"]) == "404":
        return ""
    
    else:

        result = ""
        
        if "result" in response and "results" in response["result"]:
            for r in response["result"]["results"]:
                if "ui" in r:
                    result = r["ui"]
                    return result
        else:
                
            return result


def get_all_items(source_name: str, id: str, extra_parameter: str, umls_token: str):
    url = f"https://uts-ws.nlm.nih.gov/rest/content/current/source/{source_name}/{id}/relations?{extra_parameter}&apiKey={umls_token}"

    response = requests.get(url).json()

    if "status" in response and str(response["status"]) == "404":
        return []
    else:
        #print ("response", response)

        page_count = int(response["pageCount"])

        #print ("page_count", page_count)
        
        results = get_item(response)

        for i in range(2, page_count+1):
            new_url = url + f"&pageNumber={i}"

            new_response = requests.get(new_url).json()

            #print ("new_url", new_url)
            #print ("new_response", new_response)

            results += get_item(new_response)
        
        return results



def get_item(response: str):

    result = []
    
    if "result" not in response:
        return result

    else:
        for r in response["result"]:
            if r["classType"] == "AtomClusterRelation" and "relatedId" in r and "relatedIdName" in r:
                item_id = r["relatedId"].split("/")[-1]
                item_name = r["relatedIdName"]


                result.append((item_id, item_name))

        
        return result


if __name__ == "__main__":
    #print(get_parent_HPO("HP:0000001", umls_token))
    #print(recursive_get_parent_HPO("HP:0011458", umls_token))

#### get may_be_prevented_by drugs of a disease
    #result = get_all_items("MSH", "D014839", "includeAdditionalRelationLabels=may_be_prevented_by", umls_token)

    #assert len(result) == 40
    #print (result)
    
#### recursive get all parent HPO
    #print ("\n\n")
    #print(recursive_get_parent_HPO("HP:0011458", umls_token))
###
    #print (get_all_items("MSH", "D015282", "includeAdditionalRelationLabels=isa", umls_token))
    #print (search("Gsk2256098", umls_token))
    #print (get_MSH("C2981865", umls_token))

    #print (get_name("C000604998", umls_token))
    #print (get_all_items("MSH", "C000604998", "includeAdditionalRelationLabels=mapped_to", umls_token))

    id = search("Amitriptyline", umls_token)
    print (id)

    id = get_all_id_pages("RXNORM", id, umls_token)
    print (id)

    print ("may_treat", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=may_treat", umls_token))
    print ("may_prevent", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=may_prevent", umls_token))
    print ("has_structural_class", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=has_structural_class", umls_token))
    print ("has_therapeutic_class", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=has_therapeutic_class", umls_token))
    print ("contraindicated_with_disease", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=contraindicated_with_disease", umls_token))
    print ("has_mechanism_of_action", get_all_items("RXNORM", id, "includeAdditionalRelationLabels=has_mechanism_of_action", umls_token))
    