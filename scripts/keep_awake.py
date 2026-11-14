"""Open the live app like a visitor, so Streamlit Community Cloud never puts it to sleep.

Community Cloud puts an app to sleep after 12 hours without visitors; the next visitor then sees a
"wake up" page and waits about a minute. GitHub Actions runs this every 6 hours
(.github/workflows/keep-awake.yml). If the app is already asleep, it presses the wake-up button.

  python scripts/keep_awake.py [url]
"""
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://monsoonlens.streamlit.app/"
READY = "What the radar found"


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90_000)
        page.wait_for_timeout(8_000)
        wake = page.get_by_role("button", name="Yes, get this app back up!")
        if wake.count():
            print("App was asleep: waking it up")
            wake.click()
            page.wait_for_timeout(5_000)
        # The app itself runs inside an iframe on streamlit.app.
        for attempt in range(18):  # up to about 3 minutes
            for frame in page.frames:
                try:
                    if frame.get_by_text(READY).count():
                        print("App is awake and showing results")
                        browser.close()
                        return 0
                except Exception:
                    pass
            page.wait_for_timeout(10_000)
        print("App did not show its results within 3 minutes")
        browser.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
