import sys
sys.path.append('./')

import unittest
#from src.my_http_client import HTTPClient
from src.my_http_client import HTTPClient 



class TestHTTPClient(unittest.TestCase):
    
    def test_sanity(self):
        http = HTTPClient("Pseudo-Sappho_MAN_Napoli_Inv9084",1,0)
        print(http.send_sanity())

    def test_reconstruct_Inv9084_num1_noise0(self):
        http = HTTPClient("Pseudo-Sappho_MAN_Napoli_Inv9084",1,0)
        encoded_data = "0,0,1,0\r\n0,0,1,0\r\n0,1,1,2\r\n1,1,2,0\r\n1,2,2,2\r\n2,1,5,1\r\n2,2,5,0\r\n"
        
        print(http.send_reconstruct_request(encoded_data))



if __name__ == "__main__":
    unittest.main()