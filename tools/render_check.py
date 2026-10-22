import sys
from playwright.sync_api import sync_playwright
B = sys.argv[1]
IMG = """async () => {
  const m = await (await fetch(document.querySelector('#btnGw').getAttribute('manifest'))).json();
  const bin = new Uint8Array(await (await fetch(m.builds[0].parts[0].path)).arrayBuffer());
  const nvs = new TextDecoder('latin1').decode(bin.subarray(0x9000, 0x9000 + 8192));
  return { len: bin.length, keys: ['wifi_ssid','wifi_pass','Paul iPhone','device_id','mqtt_url'].filter(k => nvs.includes(k)) };
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(B + "/tools/flasher/index.html?cb=91"); pg.wait_for_timeout(2500)
    print("labels:", pg.eval_on_selector_all("label", "els=>els.map(e=>e.childNodes[0].textContent)"), "| fw:", pg.inner_text("#fwVer"))
    print("blank hotspot -> warn shown:", pg.is_visible("#gwWarn"), "| image:", pg.evaluate(IMG))
    pg.fill("#ssid", "Paul iPhone"); pg.fill("#pass", "pw1-12345"); pg.wait_for_timeout(1500)
    print("with hotspot -> image:", pg.evaluate(IMG))
    L = b.new_page(); L.on("pageerror", lambda e: errs.append(str(e)))
    L.goto(B + "/tools/weekend/logger.html?cb=92"); L.wait_for_timeout(800)
    print("role:", L.inner_text("button.role[data-role=logger]").replace("\n", " / "))
    L.click("button.role[data-role=logger]"); L.wait_for_timeout(1500)
    print("steps:", [t[:80] for t in L.eval_on_selector_all(".source ol li", "els=>els.map(e=>e.textContent)")])
    print("ERRS:", errs); b.close()
