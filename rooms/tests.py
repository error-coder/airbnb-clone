from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME="Amenity Test"
    DESC="Amenity Desc"
    URL = "/api/v3/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC,)

    def test_all_amenities(self): # test_로 시작하지 않으면 django는 코드를 실행하지 않음

        response = self.client.get(self.URL) # self.client는 api로 get/post/put/delete request를 보낼 수 있게함
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200",)
        self.assertIsInstance(data, list,)
        self.assertEqual(len(data), 1,)
        self.assertEqual(data[0]["name"], self.NAME,)
        self.assertEqual(data[0]["description"], self.DESC,)
        
        # <작동 원리>
        # 첫번째로 테스트할 것은 누구든 url로 갈 수 있어야 하고 공개되어 있어야 함
        # 테스트 시작 전에 NAME, DESC 값들을 넣어서 Amenity를 하나 생성함
        # 그 다음 URL로 가서 Amenity들을 요청함
        # 응답코드가 200인지 확인, data가 list인지 확인, data의 길이가 1인지 확인함(Amenity를 하나 생성했기 때문)
        # data 첫번째 아이템의 name이 self.NAME이랑 같은지 확인, description도 확인

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(self.URL, {"name" : new_amenity_name, "description" : new_amenity_description,},) 
        data = response.json()

        self.assertEqual(response.status_code, 200, "Not 200 status code.",)
        self.assertEqual(data["name"], new_amenity_name,)
        self.assertEqual(data["description"], new_amenity_description,)
        
        response = self.client.post(self.URL)
        data = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


