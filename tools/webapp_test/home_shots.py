import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':360,'height':780},device_scale_factor=2)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/test/dbg.html');await pg.wait_for_timeout(300)
        async def st(done,mo,ko,stars,name,edit):
            await pg.evaluate("o=>{localStorage.setItem('geoji_monyeo_save_v2',JSON.stringify(o))}",{'seenIntro':True,'stars':stars,'done':done,'clean':done>=2,'momOut':mo,'kidOut':ko});await pg.reload();await pg.wait_for_timeout(400)
            await pg.evaluate("()=>document.querySelector('.title .big').click()");await pg.wait_for_timeout(700)
            await pg.screenshot(path=name+'_n.png')
            if edit:
                await pg.evaluate("()=>document.querySelector('#helpBtn').click()");await pg.wait_for_timeout(600)
                await pg.screenshot(path=name+'_e.png')
        await st(0,'rag','rag',6,'h0',True)
        await st(4,'rag','rag',6,'h4',True)
        await st(8,'knit','kidrain',6,'h8',True)
        await st(11,'knit','kidrain',6,'h11',True)
        print(errs);await b.close()
asyncio.run(main())
