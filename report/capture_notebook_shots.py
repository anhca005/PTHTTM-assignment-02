# -*- coding: utf-8 -*-
"""
Automatically opens each of the three real Jupyter notebooks (Anaconda's
`notebook` server) with Playwright and screenshots the exact cells (code +
rendered output) needed for the report, per SHOT_LIST.md. When a target
needs more than one cell, each cell is captured individually and the images
are stacked vertically (so non-adjacent cells, e.g. skipping a markdown
paragraph in between, can still be combined into one figure).

Run:  python capture_notebook_shots.py
"""
import os
import subprocess
import time

from PIL import Image
from playwright.sync_api import sync_playwright

ANACONDA_PY = r"C:\Users\ADMIN\anaconda3\python.exe"
A02 = r"D:\HOCTAP\PTHTTM\A02"
REPORT_DIR = os.path.join(A02, "report")
IMG_DIR = os.path.join(REPORT_DIR, "images")
TMP_DIR = os.path.join(REPORT_DIR, "_tmp_cells")
os.makedirs(TMP_DIR, exist_ok=True)

NOTEBOOKS = {
    "diabetes": {"dir": os.path.join(A02, "diabetes", "notebook"), "file": "diabetes.ipynb", "port": 8901},
    "house_price": {"dir": os.path.join(A02, "house_price", "notebook"), "file": "house_price.ipynb", "port": 8902},
    "ecommerce": {"dir": os.path.join(A02, "ecommerce", "notebook"), "file": "ecommerce.ipynb", "port": 8903},
}

# (output filename, [0-based cell indices to stack, top to bottom])
SHOTS = {
    "diabetes": [
        ("diabetes_01_overview.png", [6, 7, 8]),
        ("diabetes_02_missing_duplicates.png", [12, 15]),
        ("diabetes_03_representation.png", [38]),
        ("diabetes_04_split.png", [42]),
        ("diabetes_05_training.png", [48]),
        ("diabetes_06_inference.png", [63]),
        ("01_target_distribution.png", [26]),
        ("02_bmi_by_target.png", [28]),
        ("03_hba1c_by_target.png", [30]),
        ("04_glucose_by_target.png", [32]),
        ("05_correlation_matrix.png", [34]),
        ("06_model_comparison.png", [51]),
        ("07_confusion_matrix_test.png", [54]),
    ],
    "house_price": [
        ("house_01_overview.png", [3, 4]),
        ("house_02_missing.png", [5]),
        ("house_03_cleaning.png", [8, 9]),
        ("house_04_representation_split.png", [11, 22]),
        ("house_05_training.png", [28]),
        ("house_06_inference.png", [39]),
        ("01_price_distribution.png", [13]),
        ("02_area_vs_price.png", [15]),
        ("03_price_by_legal_status.png", [17]),
        ("04_price_by_province.png", [18]),
        ("05_correlation_matrix.png", [20]),
        ("06_model_comparison.png", [29]),
        ("07_actual_vs_predicted_test.png", [32]),
    ],
    "ecommerce": [
        ("ecom_01_overview.png", [3, 4]),
        ("ecom_02_missing.png", [5]),
        ("ecom_03_cleaning.png", [8]),
        ("ecom_04_representation_split.png", [10, 20]),
        ("ecom_05_training.png", [25, 26]),
        ("ecom_06_inference.png", [40]),
        ("01_target_distribution.png", [12]),
        ("02_recommend_by_rating.png", [14]),
        ("03_review_length_distribution.png", [16]),
        ("04_reviews_per_department.png", [17]),
        ("05_correlation_matrix.png", [18]),
        ("06_model_comparison.png", [28]),
        ("07_confusion_matrix_test.png", [32]),
        ("08_roc_curve_test.png", [33]),
    ],
}


def capture_cells(page, cells, indices, out_path):
    if len(indices) == 1:
        cell = cells.nth(indices[0])
        cell.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        cell.screenshot(path=out_path)
        return
    tmp_paths = []
    for j, idx in enumerate(indices):
        tp = os.path.join(TMP_DIR, f"tmp_{j}.png")
        cell = cells.nth(idx)
        cell.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        cell.screenshot(path=tp)
        tmp_paths.append(tp)
    imgs = [Image.open(p) for p in tmp_paths]
    width = max(im.width for im in imgs)
    gap = 10
    total_h = sum(im.height for im in imgs) + gap * (len(imgs) - 1)
    canvas = Image.new("RGB", (width, total_h), "white")
    y = 0
    for im in imgs:
        canvas.paste(im.convert("RGB"), (0, y))
        y += im.height + gap
    canvas.save(out_path)
    for im in imgs:
        im.close()


def process_app(app, cfg, playwright_browser):
    print(f"=== {app} ===")
    proc = subprocess.Popen(
        [ANACONDA_PY, "-m", "notebook", "--no-browser", f"--port={cfg['port']}",
         "--ServerApp.token=", "--ServerApp.password=",
         "--ServerApp.disable_check_xsrf=True"],
        cwd=cfg["dir"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(7)
        page = playwright_browser.new_page(viewport={"width": 1300, "height": 1100})
        page.goto(f"http://127.0.0.1:{cfg['port']}/notebooks/{cfg['file']}", timeout=30000)
        page.wait_for_selector(".jp-Cell", timeout=25000)
        page.wait_for_timeout(3000)
        cells = page.locator(".jp-Cell")
        n = cells.count()
        print(f"  {n} cells found")

        out_dir = os.path.join(IMG_DIR, app)
        os.makedirs(out_dir, exist_ok=True)
        for filename, indices in SHOTS[app]:
            out_path = os.path.join(out_dir, filename)
            capture_cells(page, cells, indices, out_path)
            print(f"  saved {filename}  (cells {indices})")
        page.close()
    finally:
        proc.terminate()
        time.sleep(1)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for app, cfg in NOTEBOOKS.items():
            process_app(app, cfg, browser)
        browser.close()
    print("DONE.")


if __name__ == "__main__":
    main()
