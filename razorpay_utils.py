import razorpay

class Razor:
    
    def __init__(self,api_details):
        self.key = api_details['key']
        self.secret = api_details['secret']
        self.client = razorpay.Client(auth=(self.key,self.secret))

    
    def create_customer(self, cust_dict):
        return self.client.customer.create(cust_dict)


