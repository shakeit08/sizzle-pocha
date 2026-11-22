# 작업 도구

스크립트 안 경로는 예전 작업 공간 기준(/home/claude/...)이라 쓰기 전에 경로만 바꾸면 됩니다.

- webapp_sprites: 캐릭터 시트 → 포즈 4개 분리(split.py) → 잘린 팔 채우기(cuts.py로 찾고 fill2.py로 채움) → 머리 크기 기준 512x1024 캔버스 배치(build.py, WC=512) → 진한 테두리(outline.py, R=4)
- font: 게임에 쓰인 글자만 뽑아 Jua 폰트 서브셋 만들기 (npm i @fontsource/jua 후 `python3 build_font.py jua jua_sub.woff2`)
- webapp_test: 웹앱 스크린샷 테스트 (dbg.html = index.html에 테스트용 훅을 끼운 사본)
- plugin_test: 플러그인 가짜 Risu 환경(harness.html) + 자동 플레이 테스트 예시(t35.py)
- prompt_panel: 우측 패널 프롬프트 페이지 생성기 (python3 build.py → index.html)
