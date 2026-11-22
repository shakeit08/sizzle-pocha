import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':360,'height':780},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/test/dbg.html');await pg.wait_for_timeout(300)
        await pg.evaluate("o=>{localStorage.setItem('geoji_monyeo_save_v2',JSON.stringify(o))}",{'seenIntro':True,'stars':3,'done':3,'clean':True,'lvl':2,'bestCombo':4});await pg.reload();await pg.wait_for_timeout(400)
        await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(600)
        await pg.evaluate("()=>__d.startLevel()");await pg.wait_for_timeout(1500)
        for i in range(200):
            await pg.evaluate("()=>document.querySelectorAll('.mwrap').forEach(e=>{if(!e.querySelector('.cmbr'))e.remove()})")
            st=await pg.evaluate("()=>{const L=__d.L;if(document.querySelector('.cmbr'))return 'win';if(!L)return 'w';L.paused=false;if(L.busy||!L.running)return 'w';const m=__d.bestMove(L.gs);if(m)__d.tryMove(m.a||m[0],m.b||m[1]);return 'm'}")
            if st=='win':break
            await pg.wait_for_timeout(260)
        await pg.wait_for_timeout(700)
        print(await pg.evaluate("()=>[__d.L.maxCombo,__d.G.bestCombo,document.querySelector('.cmbr')&&document.querySelector('.cmbr').innerText.replace(/\\n/g,' ')]"))
        await pg.screenshot(path='wc.png');print(errs);await b.close()
asyncio.run(main())
