import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':360,'height':780})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/test/dbg.html');await pg.wait_for_timeout(300)
        await pg.evaluate("o=>{localStorage.setItem('geoji_monyeo_save_v2',JSON.stringify(o))}",{'seenIntro':True,'stars':3,'done':3,'clean':True,'lvl':6,'coins':3000});await pg.reload();await pg.wait_for_timeout(400)
        await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(600)
        await pg.evaluate("()=>__d.startLevel()");await pg.wait_for_timeout(1800)
        for _ in range(6):
            await pg.evaluate("()=>{const b=document.querySelector('.mwrap button');b&&b.click()}");await pg.wait_for_timeout(300)
        for r in range(4):
            await pg.evaluate("()=>{const L=__d.L;L.paused=false;L.running=true;L.order=null;L.elapsed=999;L.nextOrder=0}");await pg.wait_for_timeout(700)
            await pg.evaluate("()=>{__d.L.order&&(__d.L.order.left=0.05)}");await pg.wait_for_timeout(1500)
            txt=await pg.evaluate("()=>document.querySelector('.mwrap')?.innerText.replace(/\\n+/g,' | ')")
            print(r,txt)
            has=await pg.evaluate("()=>!!document.querySelector('.mwrap [data-c]')")
            if has: await pg.evaluate("()=>document.querySelector('.mwrap [data-c]').click()")
            else: break
            await pg.wait_for_timeout(400)
        print('coins',await pg.evaluate("()=>__d.G.coins"),errs);await b.close()
asyncio.run(main())
