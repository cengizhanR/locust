from locust import task, HttpUser, SequentialTaskSet, between
from requests.auth import HTTPBasicAuth
import json

class UserBehaviour(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.token = ""  # Variable to store the token

    def on_start(self):
        # Send login request and extract token
        with self.client.post(
                "/NCTSTraderApi/auth/login",
                json={"userId": "11111111101", "password": "123"},  # JSON request body
                auth=HTTPBasicAuth("NCTSTraderUser", "3vAT.2G98Ar!"),  # Basic Auth credentials
                name="login",
                catch_response=True
        ) as res:
            if res.status_code == 200:
                response_data = res.json()  # Parse the response JSON
                if response_data["data"]["loginResult"]:  # Check if login was successful
                    self.token = response_data["data"]["token"]  # Extract the token
                    res.success()
                    print(f"Login successful, token: {self.token}")  # Print the token
                else:
                    res.failure(f"Login failed, response: {res.text}")
            else:
                res.failure(f"Login failed, response: {res.text}")

    @task
    def submit_declaration(self):
        if self.token:  # Ensure the token is available
            body = {
                "token": self.token,
                "firmId": "testUser",
                "userId": "11111111101",
                "msgType": "CC015C",
                "signFlag": False,
                "msgContent": {
                    "phase5XML": "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ns2:CC015C xmlns:ns2=\"http://ncts.dgtaxud.ec\"><messageSender>TPA.TR</messageSender><messageRecipient>NTA.TR</messageRecipient><preparationDateAndTime>2024-10-01T13:28:36</preparationDateAndTime><messageIdentification>3a940365ff4c4a</messageIdentification><messageType>CC015C</messageType><TransitOperation><LRN>24LR061600000116</LRN><declarationType>T1</declarationType><additionalDeclarationType>D</additionalDeclarationType><security>1</security><reducedDatasetIndicator>0</reducedDatasetIndicator><bindingItinerary>0</bindingItinerary></TransitOperation><CustomsOfficeOfDeparture><referenceNumber>TR061600</referenceNumber></CustomsOfficeOfDeparture><CustomsOfficeOfDestinationDeclared><referenceNumber>AT320300</referenceNumber></CustomsOfficeOfDestinationDeclared><CustomsOfficeOfTransitDeclared><sequenceNumber>1</sequenceNumber><referenceNumber>BG001015</referenceNumber><arrivalDateAndTimeEstimated>2024-10-02T21:00:00</arrivalDateAndTimeEstimated></CustomsOfficeOfTransitDeclared><CustomsOfficeOfTransitDeclared><sequenceNumber>2</sequenceNumber><referenceNumber>RS025011</referenceNumber><arrivalDateAndTimeEstimated>2024-10-05T21:00:00</arrivalDateAndTimeEstimated></CustomsOfficeOfTransitDeclared><CustomsOfficeOfTransitDeclared><sequenceNumber>3</sequenceNumber><referenceNumber>HU515000</referenceNumber><arrivalDateAndTimeEstimated>2024-10-03T21:00:00</arrivalDateAndTimeEstimated></CustomsOfficeOfTransitDeclared><HolderOfTheTransitProcedure><identificationNumber>7810140185</identificationNumber><name>STM Savunma</name><Address><streetAndNumber>Çankaya</streetAndNumber><postcode>065314</postcode><city>Ankara</city><country>TR</country></Address></HolderOfTheTransitProcedure><Guarantee><sequenceNumber>1</sequenceNumber><guaranteeType>1</guaranteeType><GuaranteeReference><sequenceNumber>1</sequenceNumber><GRN>24TR0400010000005</GRN><accessCode>mfy1</accessCode><amountToBeCovered>100000</amountToBeCovered><currency>TRY</currency></GuaranteeReference></Guarantee><Consignment><countryOfDestination>DE</countryOfDestination><modeOfTransportAtTheBorder>3</modeOfTransportAtTheBorder><grossMass>21140.0</grossMass><Carrier><identificationNumber>ITTR0000000000158</identificationNumber></Carrier><Consignor><identificationNumber>6080453907</identificationNumber><name>TNTA</name><Address><streetAndNumber>Çankaya</streetAndNumber><postcode>065314</postcode><city>BEIRUT</city><country>DE</country></Address></Consignor><Consignee><identificationNumber>7080454907</identificationNumber><name>IRMK</name><Address><streetAndNumber>Berne</streetAndNumber><postcode>95448</postcode><city>Byrut</city><country>DE</country></Address></Consignee><DepartureTransportMeans><sequenceNumber>1</sequenceNumber><identificationNumber>06BDR352</identificationNumber><nationality>TR</nationality></DepartureTransportMeans><CountryOfRoutingOfConsignment><sequenceNumber>1</sequenceNumber><country>TR</country></CountryOfRoutingOfConsignment><CountryOfRoutingOfConsignment><sequenceNumber>2</sequenceNumber><country>BG</country></CountryOfRoutingOfConsignment><CountryOfRoutingOfConsignment><sequenceNumber>3</sequenceNumber><country>RS</country></CountryOfRoutingOfConsignment><CountryOfRoutingOfConsignment><sequenceNumber>4</sequenceNumber><country>HU</country></CountryOfRoutingOfConsignment><CountryOfRoutingOfConsignment><sequenceNumber>5</sequenceNumber><country>AT</country></CountryOfRoutingOfConsignment><CountryOfRoutingOfConsignment><sequenceNumber>6</sequenceNumber><country>DE</country></CountryOfRoutingOfConsignment><ActiveBorderTransportMeans><sequenceNumber>1</sequenceNumber><customsOfficeAtBorderReferenceNumber>TR220200</customsOfficeAtBorderReferenceNumber><typeOfIdentification>30</typeOfIdentification><identificationNumber>06BDR352</identificationNumber><nationality>TR</nationality></ActiveBorderTransportMeans><PlaceOfLoading><country>TR</country><location>Ankara</location></PlaceOfLoading><PlaceOfUnloading><country>DE</country><location>Bern</location></PlaceOfUnloading><HouseConsignment><sequenceNumber>1</sequenceNumber><grossMass>21140.0</grossMass><ConsignmentItem><goodsItemNumber>1</goodsItemNumber><declarationGoodsItemNumber>1</declarationGoodsItemNumber><Commodity><descriptionOfGoods>Galvanizli Çelik</descriptionOfGoods><CommodityCode><harmonizedSystemSubHeadingCode>730820</harmonizedSystemSubHeadingCode></CommodityCode><GoodsMeasure><grossMass>21140.0</grossMass><netMass>21140.0</netMass></GoodsMeasure></Commodity><Packaging><sequenceNumber>1</sequenceNumber><typeOfPackages>BI</typeOfPackages><numberOfPackages>13</numberOfPackages><shippingMarks>ASDFE</shippingMarks></Packaging><PreviousDocument><sequenceNumber>1</sequenceNumber><type>N380</type><referenceNumber>MSA202</referenceNumber></PreviousDocument><TransportDocument><sequenceNumber>1</sequenceNumber><type>N703</type><referenceNumber>35345</referenceNumber></TransportDocument></ConsignmentItem></HouseConsignment></Consignment></ns2:CC015C>",
                    "nationXML": "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ns2:CC015National xmlns:ns2=\"http://ncts.dgtaxud.ec\"><messageType>CC015National</messageType><agreedLocationOfGoods></agreedLocationOfGoods><taxStampStatus>1</taxStampStatus><customsOfficeAtBorder>TR161500</customsOfficeAtBorder></ns2:CC015National>"
                }
            }

            with self.client.post(
                "/NCTSTraderApi/trader/submitDeclaration",
                json=body,  # Set the body with token and other data
                auth=HTTPBasicAuth("NCTSTraderUser", "3vAT.2G98Ar!"),  # Basic Auth credentials
                name="submitDeclaration",
                catch_response=True
            ) as res:
                if res.status_code == 200:
                    response_data=res.json()
                    self.guildID=response_data["data"]["guid"]
                    print(self.guildID)
                    res.success()
                    print(f"Declaration submitted successfully: {res.text}")
                else:
                    res.failure(f"Failed to submit declaration, response: {res.text}")

    @task
    def getLrnByGuid(self):
        if not self.token:
            print("Token is missing. Cannot make the request.")
            return

        # Request body
        body = {
            "token": self.token,
            "firmId": "testUser",
            "userId": "11111111101",
            "guid": self.guildID  # Using the guildID from self
        }

        # Debugging: Log the request body
        print(f"Request Body: {json.dumps(body, indent=4)}")

        # Make the POST request
        with self.client.post(
                "/NCTSTraderApi/trader/getLrnByGuid",
                json=body,
                auth=HTTPBasicAuth("NCTSTraderUser", "3vAT.2G98Ar!"),
                name="getLrnByGuid",
                catch_response=True
        ) as res:
            if res.status_code == 200:
                res.success()
            else:
                print(f"Response Code: {res.status_code}, Response Text: {res.text}")
                res.failure(f"Request failed with status {res.status_code}")
    # @task
    # def getUnReadMessageList(self):
    #     if self.token:  # Ensure the token is available
    #         body = {
    #             "token": self.token,
    #             "firmId": "testUser",
    #             "userId": "11111111101"
    #         }
    #
    #         with self.client.post(
    #             "/NCTSTraderApi/trader/getUnReadMessagesList",  # Update the endpoint if needed
    #             json=body,  # Set the request body
    #             auth=HTTPBasicAuth("NCTSTraderUser", "3vAT.2G98Ar!"),  # Basic Auth credentials
    #             name="getUnreadMessageList",
    #             catch_response=True
    #         ) as res:
    #             if res.status_code == 200:
    #                 response_data = res.json()  # Parse the response JSON
    #                 res.success()
    #                 print(f"Unread messages: {json.dumps(response_data, indent=4)}")  # Pretty print the response data
    #             else:
    #                 res.failure(f"Failed to get unread messages, response: {res.text}")


class MyUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1, 2)
    host = "https://ws.gtb.gov.tr:8443"
