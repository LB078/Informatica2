from carparking import CarParkingMachine

def test_check_in_single_parking_machine_only():
    # create new instances with id
    north = CarParkingMachine(id='North')
    south = CarParkingMachine(id='South')
    assert True == north.check_in(license_plate='MyTestPlate001'), "Check in for MyTestPlate001 should work on parking North"
    assert True == ('MyTestPlate001' in north.parked_cars), "MyTestPlate001 should be in parked cars on parking North"
    assert True == north.check_in(license_plate='MyTestPlate002'), "Check in for MyTestPlate002 should work on parking North"
    assert True == ('MyTestPlate002' in north.parked_cars), "MyTestPlate002 should be in parked cars on parking North"
    assert False == south.check_in(license_plate='MyTestPlate001'), "Check in for MyTestPlate001 should fail on parking South, since its already present on North"

def test_restore_state_json():
    north = CarParkingMachine(id='North')
    south = CarParkingMachine(id='South')
    assert True == ('MyTestPlate001' in north.parked_cars), "MyTestPlate001 should be in parked cars on parking North"
    assert True == ('MyTestPlate002' in north.parked_cars), "MyTestPlate002 should be in parked cars on parking North"

    north.check_out(license_plate='MyTestPlate001'), "Check out for MyTestPlate001 should work on parking North"
    assert False == ('MyTestPlate001' in north.parked_cars), "MyTestPlate001 should no longer be present in parked cars on parking North"
    north.check_out(license_plate='MyTestPlate002'), "Check out for MyTestPlate002 should work on parking North"
    assert False == ('MyTestPlate002' in north.parked_cars), "MyTestPlate002 should no longer be present in parked cars on parking North"

    assert True == south.check_in(license_plate='MyTestPlate002'), "Check in for MyTestPlate002 should work on parking South"
    assert True == ('MyTestPlate002' in south.parked_cars), "MyTestPlate002 should not be present in parked cars on parking South"
    assert False == north.check_in(license_plate='MyTestPlate002'), "Check in for MyTestPlate002 should fail on parking North, since its already present on South"

test_check_in_single_parking_machine_only()
# test_restore_state_json()



# print("Getting to checking")
# print("#" * 20)
# find_last_checkin_query = """
# SELECT id 
# FROM parkings
# WHERE license_plate = ? AND check_out IS NULL
# ORDER BY id
# DESC 
# LIMIT 1
# """

# self.cursor.execute(find_last_checkin_query, (license_plate.upper(),))
# result = self.cursor.fetchone()
# print(result)

# print("#" * 20)
# print("Passed check")