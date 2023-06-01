from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# create a new Chrome browser instance
driver = webdriver.Chrome()

try:
    # navigate to the desired website
    # ACTUAL
    driver.get("https://rapsodo.com/products/mlm2pro-golf-simulator")
    # TEST
    # driver.get("https://rapsodo.com/products/callaway-rpt-chrome-soft-x-golf-balls")

    # wait for the add to cart button to be clickable, and click it
    add_to_cart_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn--full.R-MlmProBtnCart"))
    )
    add_to_cart_btn.click()

    # wait for the terms checkbox to be clickable, and click it
    terms_checkbox = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart__terms-checkbox"))
    )
    terms_checkbox.click()

    # locate the accept cookies button and click it
    accept_cookies_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc-btn.cc-dismiss"))
    )
    accept_cookies_btn.click()

    # wait for the checkout button to be clickable, and click it
    checkout_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.cart__checkout"))
    )
    checkout_btn.click()
except:
    # if any of the above fails, close the browser
    driver.quit()
    exit(1)

try:
    # fill in the fields
    shipping_fields = {
        "checkout_email": "emaill@address.com",  # replace with your email
        "checkout_shipping_address_first_name": "first",  # replace with your first name
        "checkout_shipping_address_last_name": "last",  # replace with your last name
        "checkout_shipping_address_address1": "address",  # replace with your address
        "checkout_shipping_address_address2": "unit",  # replace with your apartment, suite, etc.
        "checkout_shipping_address_city": "city",  # replace with your city
        "checkout_shipping_address_zip": "12345",  # replace with your zip code
        "checkout_shipping_address_phone": "1234567890",  # replace with your phone number
    }

    for id, input_text in shipping_fields.items():
        field_input_box = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, id))
        )
        field_input_box.send_keys(input_text)

    # wait for the continue to shipping button to be clickable, and click it
    continue_to_shipping_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".step__footer__continue-btn.btn"))
    )
    continue_to_shipping_btn.click()

    continue_to_payment_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".step__footer__continue-btn.btn"))
    )
    continue_to_payment_btn.click()

    # After clicking the continue to payment button, wait for the iframe to load
    # Replace 'iframe_css_selector' with the actual CSS selector for the iframe
    # You will need to inspect the page to find the appropriate selector
    iframes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "iframe.card-fields-iframe")
        )
    )

    credit_card_ids = [
        "number",
        "name",
        "expiry",
        "verification_value",
    ]

    credit_card_input_text = [
        "0123456789101213",
        "name",
        "1234",
        "123",
    ]

    while True:
        pay_now_btn_exists = driver.find_elements(By.CSS_SELECTOR, ".step__footer__continue-btn.btn")
        if pay_now_btn_exists:
            # Switch to the iframe
            for i, iframe in enumerate(iframes):
                driver.switch_to.frame(iframe)

                wait = WebDriverWait(driver, 20)
                input_box = wait.until(EC.element_to_be_clickable((By.ID, credit_card_ids[i])))
                input_box.clear()
                time.sleep(0.1)
                input_box.send_keys(credit_card_input_text[i])

                # Switch back to the main content when finished
                driver.switch_to.default_content()

            pay_now_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".step__footer__continue-btn.btn"))
            )
            pay_now_btn.click()
        else:
            print("Payment successful!")
            break

finally:
    # always close the browser to free up resources
    while True:
        user_input = input("Enter `q` to quit: ")
        if user_input == 'q':
            break
    driver.quit()
