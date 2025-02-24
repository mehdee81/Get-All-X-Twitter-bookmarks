# X (Twitter) Bookmark Manager

This Python script automates the process of logging into X (formerly Twitter) and crawling all your bookmarked posts. It uses Selenium to interact with the web browser and collects the URLs of all bookmarked tweets, saving them to a CSV file named `bookmarks.csv`.

## Features
- **Secure Login**: Uses `getpass` to securely input your X (Twitter) password.
- **Dynamic Scrolling**: Automatically scrolls through your bookmarks to load and collect all links.
- **Error Handling**: Retries scrolling and loading to handle slow internet connections or lazy-loaded content.
- **CSV Export**: Saves all collected bookmark links to a CSV file for easy access.

## How It Works
The script logs into X (Twitter) using your credentials, navigates to the bookmarks page, and dynamically scrolls through the content to collect all bookmarked tweet URLs. It uses a combination of scrolling, waiting, and retries to ensure all bookmarks are captured, even on slower internet connections.

### Key Parameters
The following parameters control the scrolling and loading behavior:

```python
seen_links = set()  # Tracks collected links to avoid duplicates
scroll_attempts = 0  # Counts how many times the script has attempted to scroll
max_attempts = 15  # Maximum number of scroll attempts before stopping
cooldown = 0.3  # Base wait time between scrolls (in seconds)
scroll_factor = 0.8  # Fraction of the viewport height to scroll each time
retry_scroll_factor = 1.5  # Increased scroll distance when no new links are found
dynamic_wait_multiplier = 1.5  # Multiplier for wait time when loading slows down
```

### Internet Speed and Script Behavior
The script is designed to handle varying internet speeds by dynamically adjusting its behavior:
1. **Slow Connections**: If the page takes longer to load (e.g., due to a slow internet connection), the script increases the wait time between scrolls using the `dynamic_wait_multiplier`. This ensures that content has enough time to load before the next scroll.
2. **Stuck Detection**: If no new links are found after a scroll, the script increases the scroll distance (`retry_scroll_factor`) and increments the `scroll_attempts` counter. If the maximum number of attempts (`max_attempts`) is reached, the script stops scrolling.
3. **Efficient Scrolling**: The `scroll_factor` ensures that the script scrolls smoothly through the page, triggering lazy-loaded content without overshooting.

These parameters make the script robust and adaptable to different network conditions, ensuring it works reliably even on slower connections.

### Adjusting Parameters Based on Internet Speed

The script's performance can be optimized by adjusting parameters like `cooldown`, `scroll_factor`, `retry_scroll_factor`, and `dynamic_wait_multiplier` based on your internet speed. Here's how you can tailor these settings:

---

#### **1. For Fast Internet Connections**
If your internet connection is fast, the page content will load quickly, and you can reduce waiting times and increase scrolling efficiency:
- **`cooldown`**: Set this to a lower value (e.g., `0.1` to `0.2` seconds). This reduces the wait time between scrolls since content loads almost instantly.
- **`scroll_factor`**: Increase this to `1.0` or higher. A larger scroll distance ensures you cover more content in fewer scrolls.
- **`retry_scroll_factor`**: Keep this moderate (e.g., `1.2` to `1.5`). If the script gets stuck, it will scroll further to load new content.
- **`dynamic_wait_multiplier`**: Set this to `1.0` or lower. Since the internet is fast, you don’t need extra waiting time even if loading slows down temporarily.

**Example for Fast Internet:**
```python
cooldown = 0.1  # Shorter wait time
scroll_factor = 1.0  # Scroll a full viewport height
retry_scroll_factor = 1.2  # Slightly larger scroll when stuck
dynamic_wait_multiplier = 1.0  # No extra waiting needed
```

---

#### **2. For Slow Internet Connections**
If your internet connection is slow, the script needs more time to load content and avoid missing links:
- **`cooldown`**: Increase this to `0.5` or higher. This gives the page enough time to load new content after each scroll.
- **`scroll_factor`**: Reduce this to `0.5` or `0.6`. Smaller scrolls ensure you don’t skip content that hasn’t loaded yet.
- **`retry_scroll_factor`**: Increase this to `1.5` or `2.0`. If the script gets stuck, it will scroll further to trigger loading.
- **`dynamic_wait_multiplier`**: Set this to `2.0` or higher. This adds extra waiting time when loading slows down, ensuring the script doesn’t proceed before content is fully loaded.

**Example for Slow Internet:**
```python
cooldown = 0.5  # Longer wait time
scroll_factor = 0.5  # Scroll half the viewport height
retry_scroll_factor = 1.5  # Larger scroll when stuck
dynamic_wait_multiplier = 2.0  # Extra waiting for slow loading
```

---

#### **3. General Guidelines**
- **Test and Adjust**: Run the script and observe its behavior. If it misses links or scrolls too quickly, increase the `cooldown` or `dynamic_wait_multiplier`. If it’s too slow, reduce these values.
- **Monitor Progress**: The script prints the number of links collected after each scroll. Use this feedback to fine-tune the parameters.
- **Balance Speed and Reliability**: Faster settings may miss some links, while slower settings ensure completeness but take more time. Choose based on your needs.

By adjusting these parameters, you can optimize the script for your specific internet speed and ensure it works efficiently in all conditions.

## Requirements
- Python 3.x
- Selenium (`pip install selenium`)
- This code does not require ChromeDriver. However, if you encounter a ChromeDriver-related error, download and install it before running the code.

## Usage
1. Clone this repository or download the script.
2. Install the required dependencies:
   ```bash
   pip install selenium
   ```
3. Download ChromeDriver and ensure it's in your system's PATH.
4. Run the script:
   ```bash
   python "Get Bookmarks.py"
   ```
5. Enter your X (Twitter) username and password when prompted.
6. The script will collect all your bookmarks and save them to `bookmarks.csv`.

## Output
The script generates a CSV file named `bookmarks.csv` with the following format:
```
Bookmark Links
https://x.com/username/status/1234567890
https://x.com/username/status/0987654321
...
```

## Disclaimer
This script is for educational purposes only. Use it responsibly and in compliance with X (Twitter)'s terms of service. The author is not responsible for any misuse or consequences arising from the use of this script.



---

Feel free to contribute to this project by opening issues or submitting pull requests!
