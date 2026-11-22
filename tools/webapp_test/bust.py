import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':360,'height':780},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/test/dbg.html');await pg.wait_for_timeout(300)
        await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(1500)
        for i in range(19):
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(120)
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'b_{i:02d}.png')
        await pg.evaluate("o=>{localStorage.setItem('geoji_monyeo_save_v2',JSON.stringify(o))}",{'seenIntro':True,'stars':40,'done':2,'clean':True,'momOut':'rag','kidOut':'rag'});await pg.reload();await pg.wait_for_timeout(400)
        await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(600)
        await pg.evaluate("()=>{document.querySelector('#helpBtn').click()}");await pg.wait_for_timeout(300)
        await pg.evaluate("()=>document.querySelector('#taskBub').click()");await pg.wait_for_timeout(1000)
        for i in range(12):
            await pg.screenshot(path=f'bt_{i:02d}.png')
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(120)
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(500)
        print(errs);await b.close()
asyncio.run(main())
