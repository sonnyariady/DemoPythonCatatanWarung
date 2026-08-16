import time
import os
from playwright.sync_api import sync_playwright

def capture():
    os.makedirs("screenshots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        
        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(3)
        
        # 1. Dashboard Utama
        page.screenshot(path="screenshots/dashboard.png", full_page=True)
        print("Captured dashboard.png")
        
        # 2. Kasir
        try:
            page.locator("text='🛒 Kasir (Penjualan)'").click()
            time.sleep(2)
            page.screenshot(path="screenshots/kasir.png", full_page=True)
            print("Captured kasir.png")
        except Exception as e:
            print("Kasir screenshot error:", e)
            
        # 3. Data Barang & Kategori
        try:
            page.locator("text='📦 Data Barang & Kategori'").click()
            time.sleep(2)
            page.screenshot(path="screenshots/data_barang.png", full_page=True)
            print("Captured data_barang.png")
        except Exception as e:
            print("Data Barang screenshot error:", e)
            
        # 4. Log Barang Dicari
        try:
            page.locator("text='🔍 Log Barang Dicari (Kehabisan)'").click()
            time.sleep(2)
            page.screenshot(path="screenshots/log_dicari.png", full_page=True)
            print("Captured log_dicari.png")
        except Exception as e:
            print("Log Dicari screenshot error:", e)
            
        # 5. Laporan & Analisis Data
        try:
            page.locator("text='📈 Laporan & Analisis Data'").click()
            time.sleep(2)
            page.screenshot(path="screenshots/laporan.png", full_page=True)
            print("Captured laporan.png")
        except Exception as e:
            print("Laporan screenshot error:", e)

        browser.close()

if __name__ == "__main__":
    capture()
