import urllib3
import json

from urllib.parse import urlencode


class HTTPClient():

    def __init__(self,target_puzzle_image,target_puzzle_num,target_puzzle_noise,
                  host="localhost",port=8888):
        self.host = host
        self.port = port
        self.http = urllib3.PoolManager()
        self.target_puzzle_noise = target_puzzle_noise
        self.target_puzzle_num = target_puzzle_num
        self.target_puzzle_image = target_puzzle_image

    def send_sanity(self,api_version="v0"):
        target = f"http://{self.host}:{self.port}/{api_version}/sanity"

        response = self.http.request('GET', target)

        if response.status != 200:
            raise response.reason

        return response.data.decode('utf-8')
        

    def send_reconstruct_request(self,body,screenshot_name="", api_version="v0"):

        query_parameters = {
            "noise":self.target_puzzle_noise,
            "num":self.target_puzzle_num,
            "dataset":"ConvexDrawing",
            "image":self.target_puzzle_image
        }

        if screenshot_name !="":
            query_parameters["screenShotName"] = screenshot_name

        encoded_args = urlencode(query_parameters)

        query_parameters = "reconstructions?"+encoded_args
        target = f"http://{self.host}:{self.port}/{api_version}/{query_parameters}"

        response = self.http.request(
                    'POST',
                    target,
                    body=body,
                    headers={'Content-Type': 'text/plain'}
                )
        
        return json.loads(response.data.decode('utf-8'))


    

