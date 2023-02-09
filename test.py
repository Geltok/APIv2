from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_age
import os

pf = PetFriends()


def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    status = pf.get_api_key(email, password)
    assert status != 200


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=''):
    _, auth_key = pf.get_api_key(invalid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200


def test_add_new_pet_with_valid_data(name='Bobby', animal_type='dog', age='2', pet_photo='images/Корги.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_age(name='Dasha', animal_type='cat', age=invalid_age, pet_photo='images/Кот.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result[age] is int


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Бобби", "пес", '1', "images/Корги.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Фрося', animal_type='тигр', age='11'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    else:
        raise Exception("There is no my pets")


def test_add_new_pet_no_photo_with_valid_data(name='Cat_no_photo', animal_type='cat', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''


def test_successful_update_self_pet_photo(pet_photo='images/Корги.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] is not '' 

    else:
        raise Exception("There is no my pets")
