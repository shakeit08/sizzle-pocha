import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':800},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/test/dbg.html');await pg.wait_for_timeout(600)
        await pg.screenshot(path='sp_title.png')
        await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(1500)
        for i in range(14):
            await pg.screenshot(path=f'sp_pro{i:02d}.png')
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(500)
        # home states
        async def state(o):
            await pg.evaluate("o=>{localStorage.setItem('geoji_monyeo_save_v2',JSON.stringify(o))}",o);await pg.reload();await pg.wait_for_timeout(400)
            await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(700)
        await state({'seenIntro':True,'stars':40,'done':1,'clean':False,'momOut':'rag','kidOut':'rag'})
        await pg.screenshot(path='sp_home1.png')
        await pg.evaluate("()=>document.querySelector('#taskBub').click()");await pg.wait_for_timeout(700)
        for i in range(12):
            if await pg.query_selector('.dirt'): break
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(400)
        await pg.screenshot(path='sp_clean.png')
        await state({'seenIntro':True,'stars':40,'done':2,'clean':True,'momOut':'rag','kidOut':'rag'})
        await pg.evaluate("()=>document.querySelector('#taskBub').click()");await pg.wait_for_timeout(700)
        for i in range(10):
            await pg.screenshot(path=f'sp_t3_{i:02d}.png')
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(450)
        await state({'seenIntro':True,'stars':40,'done':5,'clean':True,'momOut':'rag','kidOut':'rag'})
        await pg.evaluate("()=>document.querySelector('#taskBub').click()");await pg.wait_for_timeout(700)
        for i in range(25):
            if await pg.query_selector('.opt'): break
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(400)
        await pg.screenshot(path='sp_dress.png')
        await pg.evaluate("()=>{document.querySelector('.opt[data-k=\"trench\"]').click()}");await pg.wait_for_timeout(400)
        await pg.evaluate("()=>{document.querySelectorAll('.tabs button')[1].click()}");await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{document.querySelector('.opt[data-k=\"kidrain\"]').click()}");await pg.wait_for_timeout(400)
        await pg.screenshot(path='sp_dress2.png')
        await pg.evaluate("()=>document.querySelector('#done').click()");await pg.wait_for_timeout(1500)
        for i in range(8):
            await pg.screenshot(path=f'sp_after{i}.png')
            await pg.evaluate("()=>{const d=document.querySelector('#sui .dlg');d&&d.click()}");await pg.wait_for_timeout(450)
        await state({'seenIntro':True,'stars':40,'done':8,'clean':True,'momOut':'knit','kidOut':'kidrain'})
        await pg.screenshot(path='sp_home8.png')
        print(errs);await b.close()
asyncio.run(main())
