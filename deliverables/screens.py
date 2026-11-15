"""Screenshots of the running app for the reports and slides.

  streamlit run app/streamlit_app.py --server.port 8501 --server.headless true
  python deliverables/screens.py            # -> deliverables/out/screens/*.png
"""
import asyncio
import os
import sys
from pathlib import Path

from playwright.async_api import async_playwright

BASE = os.environ.get("BASE", "http://localhost:8501")
OUT = Path(__file__).resolve().parent / "out" / "screens"
OUT.mkdir(parents=True, exist_ok=True)
DECK = os.environ.get("DECK_JS")   # optional local copy of deck.gl, for machines without internet GL
ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]


async def page(b, scheme="dark", w=1600, h=900, dsf=2, mobile=False):
    ctx = await b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, device_scale_factor=dsf,
                              is_mobile=mobile, has_touch=mobile)
    if DECK:
        await ctx.route("https://cdn.jsdelivr.net/npm/deck.gl@9.4.1/dist.min.js",
                        lambda r: r.fulfill(path=DECK, content_type="application/javascript"))
    return await ctx.new_page()


async def go(p, path, wait=7000):
    await p.goto(f"{BASE}/{path}", wait_until="networkidle")
    await p.wait_for_timeout(wait)
    await p.add_style_tag(content="[data-testid='stStatusWidget'],[data-testid='stToolbar'] {visibility:hidden !important}")


async def shot_el(p, sel, name, pad=0):
    el = p.locator(sel).first
    await el.evaluate("e => e.scrollIntoView({block: 'center'})")
    await p.wait_for_timeout(2500)
    bb = await el.bounding_box()
    await p.screenshot(path=str(OUT / f"{name}.png"), clip={"x": max(bb["x"] - pad, 0), "y": max(bb["y"] - pad, 0),
                                                            "width": bb["width"] + 2 * pad, "height": bb["height"] + 2 * pad},
                       animations="disabled", timeout=60000)
    print(name)


async def main(only):
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=ARGS)

        async def want(n):
            return not only or n in only

        if await want("hero"):
            p = await page(b)
            await go(p, "?lang=en", 9000)
            await p.screenshot(path=str(OUT / "hero.png"), timeout=60000)
            print("hero")
            await shot_el(p, ".st-key-tour_found", "found")
            await shot_el(p, ".st-key-tour_checks", "checks_band")
            await p.locator(".st-key-tour_3d").first.evaluate("e => e.scrollIntoView({block: 'center'})")
            await p.wait_for_timeout(9000)
            await shot_el(p, ".st-key-tour_3d", "view3d")
            await p.context.close()
        if await want("tour"):
            p = await page(b)
            await go(p, "?lang=en", 6000)
            await p.locator(".st-key-tour_start_hero button").click()
            await p.wait_for_selector("#ml-tour .card")
            for _ in range(3):
                await p.wait_for_timeout(1500)
                await p.locator("#ml-tour .card .n").click()
            await p.wait_for_timeout(9000)
            await p.screenshot(path=str(OUT / "tour.png"), timeout=60000)
            print("tour")
            await p.context.close()
        if await want("story"):
            p = await page(b)
            await go(p, "story?lang=en", 8000)
            await p.screenshot(path=str(OUT / "story.png"), timeout=60000)
            print("story")
            await p.context.close()
        if await want("explore"):
            p = await page(b, scheme="dark", h=1000)
            await go(p, "explore?lang=en", 6000)
            await p.get_by_text("Flat map: what changed", exact=False).first.click()
            await p.wait_for_timeout(9000)
            await p.mouse.wheel(0, 330)
            await p.wait_for_timeout(2500)
            await p.screenshot(path=str(OUT / "explore_flat.png"), timeout=60000)
            print("explore_flat")
            await p.context.close()
        if await want("place"):
            p = await page(b, h=1000)
            await go(p, "place?lang=en&place=517151014&r=5", 9000)
            await p.mouse.wheel(0, 280)
            await p.wait_for_timeout(2500)
            await p.screenshot(path=str(OUT / "place.png"), timeout=60000)
            print("place")
            await p.context.close()
        if await want("field"):
            p = await page(b, h=1000)
            await go(p, "field?lang=en", 8000)
            await p.screenshot(path=str(OUT / "field.png"), timeout=60000)
            print("field")
            await p.mouse.wheel(0, 900)
            await p.wait_for_timeout(2500)
            await p.screenshot(path=str(OUT / "field_evidence.png"), timeout=60000)
            print("field_evidence")
            await p.context.close()
        if await want("method"):
            p = await page(b, scheme="light", h=1000)
            await go(p, "method?lang=en", 8000)
            await p.screenshot(path=str(OUT / "method.png"), timeout=60000)
            print("method")
            await p.context.close()
        if await want("hindi"):
            p = await page(b, scheme="light")
            await go(p, "?lang=hi", 9000)
            await p.screenshot(path=str(OUT / "hindi.png"), timeout=60000)
            print("hindi")
            await p.context.close()
        if await want("phone"):
            for name, path in (("phone_place", "place?lang=mr&place=517151014&r=5"), ("phone_home", "?lang=en"),
                               ("phone_field", "field?lang=hi")):
                p = await page(b, scheme="dark", w=390, h=844, dsf=3, mobile=True)
                await go(p, path, 9000)
                if name == "phone_place":
                    await p.mouse.wheel(0, 900)
                    await p.wait_for_timeout(2000)
                await p.screenshot(path=str(OUT / f"{name}.png"), timeout=60000)
                print(name)
                await p.context.close()
        await b.close()


asyncio.run(main(sys.argv[1:]))
