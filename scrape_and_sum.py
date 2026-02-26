import asyncio
import re
from playwright.async_api import async_playwright

# Automatically generate the 10 target URLs using the provided format
URLS = [f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}" for seed in range(24, 34)]

async def main():
    total_sum = 0.0
    
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Scraping pages and summing numbers. Please wait...")

        for url in URLS:
            await page.goto(url)
            
            # Wait a brief moment to ensure the JavaScript table fully renders
            await page.wait_for_timeout(1000)
            
            # Extract all text specifically from the rendered table cells
            cells = await page.evaluate("Array.from(document.querySelectorAll('td, th')).map(el => el.innerText)")
            
            for cell in cells:
                # Find all numbers (including negatives and decimals) in the cell
                numbers = re.findall(r'-?\d+\.?\d*', cell)
                for num in numbers:
                    total_sum += float(num)

        await browser.close()
        
        # Print the final total exactly as needed for the GitHub Actions logs
        print(f"\nFINAL_TOTAL_SUM: {total_sum}")

if __name__ == "__main__":
    asyncio.run(main())
