emails = ["john.doe@gmail.com", "henryf.ord@ford.org", "OKORO+E766@gmail.com", "john.doe@gmail.com"]
unique_emails = set()
for email in emails:
    #seperate local and domain names for each email address
    email = email.lower()
    index_of_at = email.index("@")
    local = email[0:index_of_at]
    domain = email[(index_of_at + 1): -1] + email[-1]
    #check if there's "." and "+" in the local
    if "." in local:
        #strip out the "." and concatenate the remaining words in the local name
        local = local.replace(".","")
    if "+" in local:
        #strip out everything after the "+" in the local name
        index_of_plus = local.index("+")
        local = local[0: index_of_plus]

    #store the new email and remove duplicates
    processed_email = local+"@"+domain
    unique_emails.add(processed_email)
print(unique_