import json


   # show all medicines 

    # [ (iterate for each medicine) state machine 
    # GUI prompt  to scan 
    # turn on scanner 
    # wait here untill scanner is pressed or back is pressed 
    # if scanner returns a value 
        # get medicine ID 
        # if container exists get id, else allocate and return id 
        # rotate the slot to the area 
        # prompt UI to enter number of pill and click next 
    # ]


def refillProcess() : 
    # pull updated prescription 
    container = Containers() 
    stateMachine = True ; 
    state = 'barcode'
    while(stateMachine) : 
        if (state=="barcode") : 
            #display the relevant details on the front end - Wentao
            # information on what medicine are to be filled up 
            medicine_id = checkBarcode() ; 
            if medicine_id!=None : 
                state = "rotate"

            # add GUI interrupt 
        elif (state=="rotate") : 
            container_id = container.getContainer(medicine_id)
            if container.rotateContainerToRefillArea() : 
                state="wait"
            else : 
                state = "error"
                message = "couldn't rotate container"
        elif (state=="wait") : 
            # wait for a button push on gui and number of pills form input 
            # update infromation i.e container.json
            if refillComplete() : 
                state = "finish"
            else : 
                state = "barcode" 
        elif (state=="finish"): 
            container.writeToFile() 
            stateMachine = False 
        elif  (state=="error") : 
            error = "there was some error" 
            stateMachine = False 
        else : 
            state = "error" 
            error = "invalid sate" 

    return  True     



def refillComplete() : 
    # return true if all the medicines have been refilled 
    # return false if more medicines have to be filled
    return 


def checkBarcode() : 
    # returns the medicine id from the scanned barcode 
    # checks if the id is valid 
    # if not scanned returns None 
    # fill by patrick 
    pass 


def pullPrescription() : 
    # if prescription is updated 
        # update the prescription 
    return True 


class Containers() : 
    def __init__(self) : 
        self.data = None 
        self.filled_containers = {}
        self.unfilled_containers = [] 
        self.current_pos = None 
        self.extractContainerData() 
    
    def extractContainerData(self) : 
        f  = open('container.json')
        self.data = json.load(f)
        self.current_pos = data["current_pos"]
        for i in self.data:
            if i!="current_pos" : 
                if self.data[i]["filled"]==1 : 
                    self.filled_containers[self.data[i]["medicine"]["id"]] = i
                else : 
                    self.unfilled_containers.append(i) 
        f.close() 

    def getContainer(self, medicineID ) : 
        # if container exists get id, else allocate and return id 
        # if no free container return None 
        if medicineID in self.filled_containers : 
            return self.filled_containers[medicineID]
        else : 
            if len(self.unfilled_containers)==0 : 
                return None 
            else : 
                container_id  = self.unfilled_containers.pop(0) 
                self.data[container_id]["filled"] = 1 
                self.data[container_id]["quantity_left"] = 0 
                self.data[container_id]["medicine"] = {
                    "id": medicineID,
                    "name": None, # need to retrive somehow from db ? 
                    "message": None # need to retrive from db ? 
                }
                self.filled_containers[medicineID] = container_id
                return container_id
    
    def updateContainerInformation(self, container_id, number_of_pills) : 
        # update infromation in the container.json file
        self.data[container_id]["quantity_left"] += number_of_pills 

    def rotateContainerToRefillArea(self,container_id) : 
        # given a container id , rotate it the the refill area 
        # return true upon success and false upon failure 
        # to be done by patrick
        # update self.current_pos as required
        return True 

    def rotateContainerToDispenseArea(self, container_id) : 

        # given a container id , rotate it the the Dispense area 
        # return true upon success and false upon failure 
        # to be done by patrick
        # update self.current_pos as required
        return True 
    
    
    def writeToFile(self) : 
        with open("container.json", 'w') as outfile:
            json.dump(self.data, outfile)

        