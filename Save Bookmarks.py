import time
import csv
import getpass  # For secure password input
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Import Keys class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_credentials():
    """Get username and password from the user in the terminal."""
    username = input("Enter your X (Twitter) username or email: ")
    password = getpass.getpass("Enter your X (Twitter) password: ")  # Securely input password
    return username, password

def login(driver, username, password):
    """Automate the login process."""
    try:
        # Open X (Twitter) login page
        driver.get("https://x.com/login")
        print("Logging in...")

        # Wait for the username/email field to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))
        )

        # Enter username/email
        username_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)  # Press Enter

        # Wait for the password field to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']"))
        )

        # Enter password
        password_field = driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Press Enter

        # Wait for login to complete (check for home page)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/home']"))
        )
        print("Login successful!")

    except Exception as e:
        print(f"Login failed: {e}")
        raise

def get_bookmarks():
    """Collect all bookmarks."""
    driver = webdriver.Chrome()
    try:
        # Get credentials from user
        username, password = get_credentials()

        # Log in
        login(driver, username, password)

        # Access bookmarks
        driver.get("https://x.com/i/bookmarks")
        print("Loading bookmarks...")
        
        # Wait for initial content
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//article"))
        )

        # Bookmark collection parameters
        seen_links = set()
        scroll_attempts = 0
        max_attempts = 15  # Allow sufficient retries for slow loading
        cooldown = 0.3  # Base wait time between scrolls
        scroll_factor = 0.8  # Scroll distance factor
        retry_scroll_factor = 1.5  # Scroll distance when stuck
        dynamic_wait_multiplier = 1.5  # Extra wait multiplier

        # Continuous scroll-collect loop
        while scroll_attempts < max_attempts:
            # Get current page state
            articles = driver.find_elements(By.XPATH, "//article")
            new_links = []

            # Collect links from visible articles
            for article in articles:
                try:
                    link_element = article.find_element(
                        By.XPATH, ".//a[.//time][contains(@href, '/status/')]"
                    )
                    url = link_element.get_attribute("href")
                    if url and url not in seen_links:
                        seen_links.add(url)
                        new_links.append(url)
                except Exception as e:
                    continue

            # Progress reporting
            print(f"Collected {len(new_links)} new links (Total: {len(seen_links)})")

            # Scroll logic
            if new_links:
                scroll_attempts = 0  # Reset counter if found new links
                # Gradual scroll to trigger loading
                driver.execute_script(f"window.scrollBy(0, window.innerHeight * {scroll_factor});")
            else:
                scroll_attempts += 1
                # Increase scroll distance if stuck
                driver.execute_script(f"window.scrollBy(0, window.innerHeight * {retry_scroll_factor});")

            # Dynamic waiting based on content changes
            time.sleep(cooldown)
            if len(new_links) < 3:  # If loading slows
                time.sleep(cooldown * dynamic_wait_multiplier)  # Extra patience for slow networks

        # Final collection pass
        final_articles = driver.find_elements(By.XPATH, "//article")
        for article in final_articles:
            try:
                link = article.find_element(
                    By.XPATH, ".//a[.//time][contains(@href, '/status/')]"
                ).get_attribute("href")
                if link and link not in seen_links:
                    seen_links.add(link)
            except:
                continue

        # Save results
        with open("bookmarks.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Bookmark Links"])
            writer.writerows([[link] for link in seen_links])

        print(f"\nSuccess! Saved {len(seen_links)} bookmarks to 'bookmarks.csv'")

    finally:
        driver.quit()

if __name__ == "__main__":
    get_bookmarks()