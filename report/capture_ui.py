# -*- coding: utf-8 -*-
"""
Automatically launches each app's API + static web/mobile client, fills in the
form with a realistic example, submits it, and screenshots the real rendered
result with Playwright (headless Chromium). Produces genuine (not mock)
evidence of the working Web/Mobile deployment for the report, so the user
does not have to take these particular screenshots by hand.

Run:  python capture_ui.py
"""
import functools
import http.server
import os
import socketserver
import subprocess
import sys
import threading
import time

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
A02 = os.path.dirname(ROOT)
IMG_DIR = os.path.join(ROOT, "images")

APPS = [
    {
        "name": "diabetes",
        "api_dir": os.path.join(A02, "diabetes", "api"),
        "api_port": 8000,
        "web_dir": os.path.join(A02, "diabetes", "web"),
        "web_port": 9100,
        "mobile_dir": os.path.join(A02, "diabetes", "mobile"),
        "mobile_port": 9101,
        "fields": {
            "#gender": ("select_label", "Female"),
            "#age": ("fill", "45"),
            "#hypertension": ("select_value", "0"),
            "#heart_disease": ("select_value", "0"),
            "#smoking_history": ("select_label", "never"),
            "#bmi": ("fill", "24.5"),
            "#HbA1c_level": ("fill", "5.7"),
            "#blood_glucose_level": ("fill", "120"),
        },
        "submit": "button[type=submit]",
        "submit_mobile": "#btn",
        "wait_selector": "#result",
    },
    {
        "name": "house_price",
        "api_dir": os.path.join(A02, "house_price", "api"),
        "api_port": 8001,
        "web_dir": os.path.join(A02, "house_price", "web"),
        "web_port": 9110,
        "mobile_dir": os.path.join(A02, "house_price", "mobile"),
        "mobile_port": 9111,
        "fields": {
            "#Area": ("fill", "60"),
            "#Frontage": ("fill", "4.5"),
            "#AccessRoad": ("fill", "6"),
            "#Floors": ("fill", "3"),
            "#Bedrooms": ("fill", "3"),
            "#Bathrooms": ("fill", "2"),
            "#LegalStatus": ("select_label", "Have certificate"),
            "#FurnitureState": ("select_label", "Full"),
            "#HouseDirection": ("select_label", "Đông - Nam"),
            "#BalconyDirection": ("select_label", "Đông - Nam"),
            "#ProvinceGroup": ("select_label", "Hà Nội"),
        },
        "submit": "button[type=submit]",
        "submit_mobile": "#btn",
        "wait_selector": "#result",
    },
    {
        "name": "ecommerce",
        "api_dir": os.path.join(A02, "ecommerce", "api"),
        "api_port": 8002,
        "web_dir": os.path.join(A02, "ecommerce", "web"),
        "web_port": 9120,
        "mobile_dir": os.path.join(A02, "ecommerce", "mobile"),
        "mobile_port": 9121,
        "fields": {
            "#Age": ("fill", "35"),
            "#Rating": ("fill", "5"),
            "#PositiveFeedbackCount": ("fill", "2"),
            "#Title": ("fill", "Great fit"),
            "#ReviewText": ("fill", "Absolutely love this dress, fits perfectly and so comfortable!"),
            "#DivisionName": ("select_label", "General"),
            "#DepartmentName": ("select_label", "Dresses"),
            "#ClassName": ("select_label", "Dresses"),
        },
        "submit": "#form button[type=submit]",
        "submit_mobile": "#btn",
        "wait_selector": "#result",
    },
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def serve_dir(directory, port):
    handler = functools.partial(QuietHandler, directory=directory)
    httpd = ReusableTCPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def fill_and_submit(page, cfg, submit_sel):
    for sel, (kind, value) in cfg["fields"].items():
        if kind == "fill":
            page.fill(sel, value)
        elif kind == "select_label":
            page.select_option(sel, label=value)
        elif kind == "select_value":
            page.select_option(sel, value=value)
    page.click(submit_sel)
    page.wait_for_timeout(1200)


def main():
    procs = []
    httpds = []
    try:
        for cfg in APPS:
            proc = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1",
                 "--port", str(cfg["api_port"])],
                cwd=cfg["api_dir"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            procs.append(proc)
        time.sleep(6)

        for cfg in APPS:
            httpds.append(serve_dir(cfg["web_dir"], cfg["web_port"]))
            httpds.append(serve_dir(cfg["mobile_dir"], cfg["mobile_port"]))
        time.sleep(1)

        with sync_playwright() as p:
            browser = p.chromium.launch()

            for cfg in APPS:
                out_dir = os.path.join(IMG_DIR, cfg["name"])
                os.makedirs(out_dir, exist_ok=True)

                # --- Web (desktop viewport) ---
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(f"http://127.0.0.1:{cfg['web_port']}/index.html")
                page.wait_for_timeout(400)
                fill_and_submit(page, cfg, cfg["submit"])
                page.screenshot(path=os.path.join(out_dir, f"{cfg['name']}_web_ui.png"), full_page=True)
                page.close()
                print(f"[{cfg['name']}] web screenshot saved.")

                # --- Mobile (phone viewport) ---
                page = browser.new_page(viewport={"width": 390, "height": 844})
                page.goto(f"http://127.0.0.1:{cfg['mobile_port']}/index.html")
                page.wait_for_timeout(400)
                fill_and_submit(page, cfg, cfg["submit_mobile"])
                page.screenshot(path=os.path.join(out_dir, f"{cfg['name']}_mobile_ui.png"), full_page=True)
                page.close()
                print(f"[{cfg['name']}] mobile screenshot saved.")

            browser.close()
    finally:
        for h in httpds:
            h.shutdown()
        for proc in procs:
            proc.terminate()
    print("DONE.")


if __name__ == "__main__":
    main()
