from random import uniform, randint
from faker import Faker

import requests


class TestGoogleMapApi:
    def __init__(
            self,
            base_url,
            key,
            post_resourse,
            get_resourse,
            delete_resourse
    ):
        self.__base_url = base_url
        self.__key = key
        self.__post_resourse = post_resourse
        self.__get_resourse = get_resourse
        self.__delete_resourse = delete_resourse
        self.__list_place_id = []

    # тело для создания локации
    @staticmethod
    def __body_to_creating_location():
        return {
            "location": {
                "lat": round(uniform(-100, 100), 6),
                "lng": round(uniform(-100, 100), 6)
            },
            "accuracy": randint(10, 100),
            "name": "Frontline house",
            "phone_number": Faker("ru_Ru").phone_number(),
            "address": "29, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "http://google.com",
            "language": "French-IN"
        }

    # тело для удаления локации
    @staticmethod
    def __body_to_remove_location(place_id):
        return {
            "place_id": place_id
        }

    # отправить метод POST
    def __send_post_method(self):
        full_post_url = self.__base_url + self.__post_resourse + self.__key
        return requests.post(full_post_url, json=self.__body_to_creating_location())

    # отправить метод Get
    def __send_get_method(self, place_id):
        full_get_url = self.__base_url + self.__get_resourse + self.__key + "&place_id=" + place_id
        return requests.get(full_get_url)

    # отправить метод Delete
    def __send_delete_method(self, place_id):
        full_delete_url = self.__base_url + self.__delete_resourse + self.__key
        return requests.delete(full_delete_url, json=self.__body_to_remove_location(place_id))

    # добавить в текстовый файл
    @staticmethod
    def __add_to_file(name_file, place_id):
        with open(name_file + ".txt", "a", encoding="utf-8") as file:
            file.write(place_id + "\n")

    # чтение из текстового файла
    @staticmethod
    def __reading_file(name_file):
        with open(name_file + ".txt", "r", encoding="utf-8") as file:
            for place_id in file:
                yield place_id.strip()

    # создать 5 place_id и поместить их в текстовый файл
    def five_place_id_in_file(self, name_file):
        number = 1
        while number <= 5:
            place_id = self.__send_post_method().json()["place_id"]

            self.__add_to_file(name_file, place_id)

            print(f"В файл \"{name_file}.txt\" добавлен {number} place_id - \"{place_id}\"")
            number += 1

    # переместить в переменную place_id из текстового файла
    def place_id_move_to_variable(self, name_file):
        for place_id in self.__reading_file(name_file):
            self.__list_place_id.append(place_id)
        print("Данные из текстового файла помещены в переменную")

    # удалить локацию по place_id
    def delete_location(self, number_to_delete):
        print(f"Локация №{number_to_delete} с place_id - "
              f"{self.__list_place_id[number_to_delete - 1]} удалена.")
        return self.__send_delete_method(
            self.__list_place_id[number_to_delete - 1]
        )

    # сортировка place_id на существующие и несуществующие локации
    def sort_place_id(self):
        for place_id in self.__reading_file("text_file"):

            status_code = self.__send_get_method(place_id).status_code

            if status_code == 404:
                print(f"Локация с place_id - {place_id} не существует!")

            elif status_code == 200:
                self.__add_to_file("new_text_file", place_id)
                print(f"В файл \"new_text_file.txt\" добавлен place_id - \"{place_id}\"")

    # очистить текстовый файл
    @staticmethod
    def clear_text_file(name_file):
        with open(name_file + ".txt", 'w'):
            pass
        print(f"Файл \"{name_file}.txt\" очищен")


if __name__ == "__main__":
    base_url = "https://rahulshettyacademy.com"
    post_resourse = "/maps/api/place/add/json"
    get_resourse = "/maps/api/place/get/json"
    delete_resourse = "/maps/api/place/delete/json"
    key = "?key=qaclick123"

    start_test = TestGoogleMapApi(
        base_url,
        key,
        post_resourse,
        get_resourse,
        delete_resourse
    )

    # создать 5 place_id и поместить их в текстовый файл
    start_test.five_place_id_in_file("text_file")
    # переместить в переменную place_id из текстового файла
    start_test.place_id_move_to_variable("text_file")
    # удалить локации 2 и 4 по place_id
    start_test.delete_location(2)
    start_test.delete_location(4)
    # сортировка place_id на существующие и несуществующие локации
    start_test.sort_place_id()
    # очистить текстовый файл
    start_test.clear_text_file("text_file")
    start_test.clear_text_file("new_text_file")
