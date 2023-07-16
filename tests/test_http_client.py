import sys
sys.path.append('./')

import unittest
#from src.my_http_client import HTTPClient
from src.my_http_client import HTTPClient 



class TestHTTPClient(unittest.TestCase):
    
    def test_sanity(self):
        http = HTTPClient("Pseudo-Sappho_MAN_Napoli_Inv9084",1,0)
        print(http.send_sanity())



if __name__ == "__main__":
    unittest.main()