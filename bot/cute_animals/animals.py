import os
from suport_fl.setting import *
from suport_fl.async_requests import AioRequests



class Animals:
    def __init__(self):
        api_key = str(os.getenv("ACCESS_KEY"))
        self.req = AioRequests(host=KITTY_API_HOST, param={'client_id': api_key})

    async def get_random_animals(self):
        answer = await self.req.get_request(new_param={'query': 'cute animals'},
                                            path=KITTY_API_PATH,
                                            header={'Accept-Version': 'v1'})
        if 'errors' in answer:
            print(answer)
            return False
        return answer['urls']['small']
