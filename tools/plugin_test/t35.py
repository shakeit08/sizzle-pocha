import asyncio
from playwright.async_api import async_playwright
T="window.__POCHA_TEST__"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':400,'height':720},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/plugin/harness.html');await pg.wait_for_timeout(300)
        await pg.evaluate("()=>__open()");await pg.wait_for_timeout(200)
        for run in range(2):
            await pg.evaluate(f"()=>{{const t={T};t.D.tips=new Proxy({{}},{{get:()=>1,set:()=>true}});t.D.lvl=2;t.D.hearts=5;t.startLevel()}}");await pg.wait_for_timeout(1500)
            await pg.evaluate("()=>document.querySelectorAll('.mwrap').forEach(e=>e.remove())")
            await pg.evaluate(f"()=>{{const L={T}.L;L.paused=false;L.running=true}}")
            for i in range(200):
                st=await pg.evaluate(f"()=>{{const t={T},L=t.L;if(document.querySelector('.cmbr'))return 'win';if(!L||L.busy||!L.running)return 'w';const m=t.bestMove(L.gs);if(m)t.tryMove(m.a||m[0],m.b||m[1]);return 'm'}}")
                if st=='win':break
                await pg.wait_for_timeout(260)
            await pg.wait_for_timeout(600)
            print(run,await pg.evaluate(f"()=>[{T}.L.maxCombo,{T}.D.bestCombo,document.querySelector('.cmbr')&&document.querySelector('.cmbr').innerText.replace(/\\n/g,' ')]"))
            await pg.screenshot(path=f'cw{run}.png')
            await pg.evaluate("()=>document.querySelectorAll('.mwrap').forEach(e=>e.remove())")
        print(errs);await b.close()
asyncio.run(main())
