import time

from selenium import webdriver

from selenium.webdriver.common.by import By





def revise(index, iport="localhost:9999", usr="axin1314", pas="axin1314"):

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    driver.get(f"http://{iport}/xui/inbounds/")



    class ServiceError(Exception):

        pass



    try:

        if not "inbounds" in driver.current_url:

            if "Login" in driver.page_source:

                driver.find_elements("tag name", "input")[0].send_keys(usr)

                driver.find_elements("tag name", "input")[1].send_keys(pas)

                driver.find_elements("tag name", "button")[0].click()

                time.sleep(.1)

                driver.get(f"http://{iport}/xui/inbounds/")

            else:

                print("servise ERROR REVISE")

                raise ServiceError

        # page = driver.page_source

        print(f"INDEX:{index}")

        if not "inbounds" in driver.current_url:
            raise RuntimeError("Username Or Password of the xui panel is wrong!!")
        driver.execute_script(f"inbound = app.dbInbounds[{index}].toInbound();")

        driver.execute_script(f"dbInbound = app.dbInbounds[{index}];")

        data = "data = { " \

               "    up: dbInbound.up," \

               "    down: dbInbound.down," \

               "    total: dbInbound.total," \

               "    remark: dbInbound.remark," \

               "    enable: dbInbound.enable," \

               "    expiryTime: dbInbound.expiryTime," \

               "    listen: inbound.listen," \

               "    port: inbound.port," \

               "    protocol: inbound.protocol," \

               "    settings: inbound.settings.toString()," \

               "    streamSettings: inbound.stream.toString()," \

               "    sniffing: inbound.canSniffing() ? inbound.sniffing.toString(): '{}'," \

               "};"

        driver.execute_script(data)

        driver.execute_script(f"app.submit(`/xui/inbound/update/{index + 1}`, data, inModal);")

        print("Revise Sucssusfull!")

    except ServiceError:

        print("Error Try again!!")

    driver.close()
