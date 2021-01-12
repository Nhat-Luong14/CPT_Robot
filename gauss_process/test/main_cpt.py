import setup
import driver 
import time

if __name__ == "__main__":   
    setup.gpio_init()

    driver.go_ahead(100)
    time.sleep(1)
    driver.stop_car()

    driver.go_back(100)
    time.sleep(1)
    driver.stop_car()

    driver.turn_left(100)
    time.sleep(1)
    driver.stop_car()

    driver.turn_right(100)
    time.sleep(1)
    driver.stop_car()

    driver.shift_right(100)
    time.sleep(1)
    driver.stop_car()

    driver.shift_left(100)
    time.sleep(1)
    driver.stop_car()

    driver.upper_left(100)
    time.sleep(1)
    driver.stop_car()

    driver.lower_right(100)
    time.sleep(1)
    driver.stop_car()

    driver.upper_right(100)
    time.sleep(1)
    driver.stop_car()

    driver.lower_left(100)
    time.sleep(1)
    driver.stop_car()

    setup.gpio_clean()