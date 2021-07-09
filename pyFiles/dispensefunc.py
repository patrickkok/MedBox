

    container=json.load(f)
for i in range(1,13):
    ID = container[i]["medicine"]["id"]
    if barcode_input == ID:
        desired_container = i
        
    
