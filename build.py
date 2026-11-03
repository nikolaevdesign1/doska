#!/usr/bin/env python3
"""Собирает страницы сайта из общих кусков (шапка, подвал, окно заказа, куки).
Запуск: python3 build.py  – результат (html-файлы) коммитится в репозиторий."""
import os
SITE='https://doska.agency'
HEAD='''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="ДОСКА">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Manrope:wght@400;500;600;700&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<!-- строка обновлений: правится вручную -->
<div class="ticker"><div class="wrap"><b>обновления</b><span>доска.поддержка версия 1.0.0 запущена в работу.</span></div></div>
<header class="head"><div class="wrap">
  <a class="logo" href="/">ДОСКА</a>
  <nav class="nav">
    <a href="https://dprofile.ru/nikolaev_design1" target="_blank" rel="noopener">кейсы <span class="nav-sub">(dprofile)</span></a>
    <a href="/lenta">лента</a>
    <a href="/podderzhka">поддержка</a>
    <a href="/kontakty">контакты</a>
  </nav>
  <button class="btn" type="button" data-order>заказать дизайн</button>
  <button class="btn burger" type="button" aria-label="Меню">меню</button>
</div></header>
'''
FOOT='''
<footer class="foot"><div class="wrap">
  <div class="top">
    <p class="lead">помогаем брендам<br>решать дизайн-задачи</p>
    <div class="fcols">
      <div><h4>следите за нами</h4><ul class="arrows" id="подвал-соцсети"></ul></div>
      <div><h4>меню</h4><ul>
        <li><a href="https://dprofile.ru/nikolaev_design1" target="_blank" rel="noopener">кейсы</a></li>
        <li><a href="/lenta">лента</a></li><li><a href="/podderzhka">поддержка</a></li><li><a href="/kontakty">контакты</a></li><li><a href="/#заявка">заявка</a></li></ul></div>
      <div><h4>связаться</h4><ul><li><a href="mailto:hello@doska.agency">hello@doska.agency</a></li></ul></div>
    </div>
  </div>
  <div class="big" aria-hidden="true">ДОСКА</div>
  <div class="bottom"><span>© ДОСКА, все права защищены</span><span class="links"><a class="u" href="/politika">политика конфиденциальности</a><a class="u" href="/usloviya">оплата, доставка и возврат</a><a class="u" href="/rekvizity">реквизиты</a></span></div>
</div></footer>

<div class="modal" id="окно" role="dialog" aria-modal="true" aria-labelledby="окно-заголовок" hidden>
  <div class="modal-shade" data-close></div>
  <div class="modal-box">
    <div class="modal-art" aria-hidden="true"><img src="/assets/popup.webp" alt="" width="1100" height="1600"></div>
    <form class="modal-form" id="форма-окна">
      <button class="modal-x" type="button" data-close aria-label="Закрыть">×</button>
      <h3 id="окно-заголовок">оставьте обращение и мы вернемся в ближайшее время</h3>
      <p class="form-contact"><a href="mailto:info@doska.agency">info@doska.agency</a> или напишите в <a href="https://t.me/oleg_nikolaev1" target="_blank" rel="noopener">Телеграм</a></p>
      <p class="modal-sub">Заполните форму – мы ответим и предложим следующий шаг.</p>
      <p class="tariff-chip" id="чип-тарифа" hidden></p>
      <input type="hidden" name="тариф" id="тариф-окна">
      <input name="имя" required placeholder="введите ваше имя" autocomplete="name">
      <input name="связь" required placeholder="почта или телеграм">
      <div class="fld"><span class="fld-l">тема запроса</span><select class="cs" name="тема" id="тема-окна" aria-label="Тема запроса"><option>Новый проект</option><option>Тарифы и стоимость</option><option>Техническая поддержка</option><option>Сотрудничество</option><option>Другое</option></select></div>
      <textarea name="задача" rows="2" placeholder="коротко опишите задачу"></textarea>
      <label class="attach"><input type="file" name="файл"><span class="attach-t">прикрепить файл</span></label>
      <div><button class="btn btn-accent" type="submit">отправить</button></div>
      <p class="ok">Спасибо! Мы свяжемся с вами в ближайшее время. <span class="emo" role="img" aria-label="поднятые руки" style="--r:-8deg">🙌</span></p>
    </form>
  </div>
</div>

<div class="cookie"><p>Мы используем файлы куки, чтобы улучшить работу сайта. Продолжая использовать этот сайт, вы соглашаетесь с использованием куки-файлов. <span class="emo" role="img" aria-label="печенье" style="--r:-12deg">🍪</span></p><button class="btn" type="button">согласен(а)</button></div>
<a class="chat-fab" href="https://t.me/nklvdsgn_bot" target="_blank" rel="noopener" aria-label="Написать в Телеграм"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-8l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg><span>написать в Телеграм</span></a>
<script src="/data.js"></script>
<script src="/script.js"></script>
<script src="https://doskaagency.online/widget/src/support.js" data-project="pk_doska_aXcedvwkiXc" defer></script>
</body></html>
'''
def page(path,title,desc,body):
    h=HEAD.format(title=title,desc=desc,site=SITE,path=path)
    foot=FOOT
    if path=='/podderzhka':
        h=h.replace('<a class="logo" href="/">ДОСКА</a>','<a class="logo logo-long" href="/">ДОСКА.ПОДДЕРЖКА</a>')
    if 'class="form"' in body:   # подвал наезжает на белый блок формы
        foot=foot.replace('<footer class="foot">','<footer class="foot lap">',1)
    return h+body+foot
D='ДОСКА – агентство: помогаем брендам решать дизайн-задачи. Сайты, презентации, приложения, брендинг.'
FORM='''<section class="form" id="заявка"><div class="wrap">
  <form id="форма">
    <p class="form-contact"><a href="mailto:info@doska.agency">info@doska.agency</a> или напишите в <a href="https://t.me/oleg_nikolaev1" target="_blank" rel="noopener">Телеграм</a></p>
    <div class="row"><label>привет! <span class="emo" role="img" aria-label="приветствие" style="--r:-14deg">👋</span> меня зовут</label><input required placeholder="введите ваше имя"></div>
    <div class="row"><label>тема нашего разговора</label>
      <select class="cs" name="тема"><option>Новый проект</option><option>Тарифы и стоимость</option><option>Техническая поддержка</option><option>Сотрудничество</option><option>Другое</option></select></div>
    <div class="row"><label>хотелось бы заказать у вас</label>
      <select class="cs" id="услуга"><option>Логотип / айдентика</option><option>Лендинг</option><option>Корпоративный сайт</option><option>Интернет-магазин</option><option>Техническая поддержка</option><option>Другое</option></select></div>
    <div class="row"><label>планируем заложить на проект</label>
      <select class="cs"><option>до 100 000 ₽</option><option>100 000 – 300 000 ₽</option><option>300 000 – 700 000 ₽</option><option>более 700 000 ₽</option><option>пока не знаем</option></select></div>
    <div class="row"><label>вкратце у нас следующая задача</label><textarea rows="1" placeholder="опишите, что необходимо сделать, на звонке все обсудим подробнее"></textarea></div>
    <div class="row"><label>ответ можно прислать сюда</label><input required placeholder="тут может быть ваша почта или телеграм / вотсап"></div>
    <div class="form-foot">
      <p class="small">Отправляя форму, вы даете согласие<br>с <a href="/politika">Политикой обработки персональных данных</a></p>
      <button class="btn btn-accent" type="submit">отправить заявку и узнать стоимость</button>
    </div>
    <p class="ok">Спасибо! Мы свяжемся с вами в ближайшее время. <span class="emo" role="img" aria-label="поднятые руки" style="--r:10deg">🙌</span></p>
  </form>
</div></section>
'''
INDEX='''
<main>
<div class="wrap">
  <div class="hero dots">
  <h1>помогаем брендам<br>решать <em>дизайн-задачи</em></h1>
  <p class="sub">Сайты, презентации, приложения и айдентика – делаем быстро, прозрачно и аккуратно.</p>
  <div class="hero-cta"><button class="btn btn-accent" type="button" data-order>оставить заявку</button></div>
  <div class="clients"><img src="/assets/clients/klient-1.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-2.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-3.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-4.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-5.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-6.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-7.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-8.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-9.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-10.png" alt="Логотип клиента" loading="eager"></div>
  </div>

  <section id="кейсы" style="padding-top:0">
    <div class="grid" id="лента"></div>
    <div class="more"><span>Сделаем так же и еще круче <span class="emo" role="img" aria-label="очки" style="--r:-6deg">😎</span></span><a class="btn btn-accent" href="/lenta">вся лента</a></div>
  </section>

  <section id="возможности" class="services dots">
    <h2>сайты, презентации,<br>приложения, брендинг<br><em>и многое другое..</em></h2>
    <p class="sub">Все, что нужно бренду для запуска и роста: от логотипа и лендинга до дизайн-системы.</p>
    <div class="cols">
      <div>лендинги<br>интернет-магазины<br>мобильные приложения<br>корпоративные сайты<br>дизайн-системы<br>А/Б-тестирование</div>
      <div>презентации<br>годовые отчеты<br>брошюры<br>шаблоны писем<br>руководства по стилю<br>рабочие тетради</div>
      <div>брендинг<br>айдентика<br>нейминг<br>копирайтинг<br>ведение соцсетей<br>креатив</div>
    </div>
    <button class="btn more-btn" type="button" data-more aria-expanded="false">показать больше</button>
  </section>

  <section id="ии" class="ai">
    <h2>работаем через ИИ-интеграции<br><em>и собираем быстрее</em></h2>
    <p class="lead2">Мы построили ИИ-систему, которая берет на себя рутину: разбирает бриф, собирает черновики и подготавливает материалы. Дизайнеры тратят время на идею и качество, а вы получаете результат заметно быстрее <span class="emo" role="img" aria-label="ракета" style="--r:8deg">🚀</span></p>
    <div class="ai-grid">
      <div class="video ai-vid"><svg class="ai-svg" viewBox="0 0 600 440" role="img" aria-label="Как работает система: ставим задачу, система собирает черновик, дизайнер доводит до результата, передаем готовое">
  <defs>
    <pattern id="aiGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#fff" stroke-opacity=".07"/></pattern>
    <filter id="aiSh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#0d0a24" flood-opacity=".45"/></filter>
    <path id="aiPtr" d="M0 0L0 17L4.6 13L7.6 20.2L10.4 19L7.4 12L13.4 12Z"/>
  </defs>
  <rect width="600" height="440" fill="url(#aiGrid)"/>
  <g fill="none" stroke="#fff" stroke-opacity=".16" stroke-dasharray="4 6">
    <path d="M60 396H540"/><path d="M60 396V352"/><path d="M200 396V352"/><path d="M340 396V352"/><path d="M480 396V352"/>
    <path d="M18 120V60M18 60H34" /><path d="M582 330V390M582 390H566"/>
  </g>
  <g class="ai-nodes" font-size="11" font-weight="700" text-anchor="middle">
    <g transform="translate(60,396)"><circle r="12" class="n n1"/><text y="4">01</text></g>
    <g transform="translate(200,396)"><circle r="12" class="n n2"/><text y="4">02</text></g>
    <g transform="translate(340,396)"><circle r="12" class="n n3"/><text y="4">03</text></g>
    <g transform="translate(480,396)"><circle r="12" class="n n4"/><text y="4">04</text></g>
  </g>
  <g filter="url(#aiSh)"><rect x="40" y="36" width="520" height="296" rx="16" fill="#fff"/></g>
  <path d="M40 70H560" stroke="#e7e5ee"/><path d="M170 70V332" stroke="#e7e5ee"/>
  <circle cx="62" cy="53" r="4.5" fill="#e7e5ee"/><circle cx="78" cy="53" r="4.5" fill="#e7e5ee"/><circle cx="94" cy="53" r="4.5" fill="#e7e5ee"/>
  <rect x="190" y="43" width="190" height="20" rx="10" fill="#f2f1f6"/><text x="285" y="57" text-anchor="middle" font-size="10.5" font-weight="600" fill="#8a8794">доска.система / проект</text>
  <g font-size="12" font-weight="700">
    <g class="ai-nav a1"><rect x="52" y="86" width="108" height="32" rx="10" fill="#ece7ff"/></g>
    <g class="ai-nav a2"><rect x="52" y="126" width="108" height="32" rx="10" fill="#ece7ff"/></g>
    <g class="ai-nav a3"><rect x="52" y="166" width="108" height="32" rx="10" fill="#ece7ff"/></g>
    <g class="ai-nav a4"><rect x="52" y="206" width="108" height="32" rx="10" fill="#ece7ff"/></g>
    <text x="66" y="106" fill="#14121c"><tspan fill="#7b5cf0">01</tspan>  Задача</text>
    <text x="66" y="146" fill="#14121c"><tspan fill="#7b5cf0">02</tspan>  Черновик</text>
    <text x="66" y="186" fill="#14121c"><tspan fill="#7b5cf0">03</tspan>  Правки</text>
    <text x="66" y="226" fill="#14121c"><tspan fill="#7b5cf0">04</tspan>  Готово</text>
  </g>
  <rect x="52" y="290" width="108" height="30" rx="10" fill="#f6f6f7"/><rect x="62" y="302" width="60" height="6" rx="3" fill="#e0deea"/>

  <g class="st s1">
    <text x="192" y="98" font-size="13" font-weight="800" fill="#14121c">Новая задача</text>
    <rect x="192" y="110" width="340" height="40" rx="12" fill="#f6f6f7"/><rect class="ty ty1" x="204" y="126" width="200" height="8" rx="4" fill="#14121c"/>
    <rect x="192" y="162" width="160" height="40" rx="12" fill="#f6f6f7"/><rect class="ty ty2" x="204" y="178" width="90" height="8" rx="4" fill="#8a8794"/>
    <rect x="364" y="162" width="168" height="40" rx="12" fill="#f6f6f7"/><rect class="ty ty3" x="376" y="178" width="110" height="8" rx="4" fill="#8a8794"/>
    <g class="btn1"><rect x="192" y="224" width="120" height="36" rx="18" fill="#7b5cf0"/><text x="252" y="246" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">отправить</text></g>
    <g class="ai-chip"><rect x="326" y="224" width="206" height="36" rx="18" fill="#f2efff"/><circle cx="346" cy="242" r="5" fill="#7b5cf0"/><text x="360" y="246" font-size="11" font-weight="700" fill="#5f3fd8">ИИ разбирает бриф…</text></g>
  </g>

  <g class="st s2">
    <text x="192" y="98" font-size="13" font-weight="800" fill="#14121c">Система собирает черновик</text>
    <rect x="192" y="108" width="340" height="6" rx="3" fill="#ece7ff"/><rect class="bar" x="192" y="108" width="340" height="6" rx="3" fill="#7b5cf0"/>
    <g class="cd cd1"><rect x="192" y="130" width="104" height="140" rx="12" fill="#f6f6f7"/><rect x="202" y="140" width="84" height="64" rx="8" fill="#cfc2ff"/><rect x="202" y="214" width="60" height="8" rx="4" fill="#14121c"/><rect x="202" y="230" width="84" height="6" rx="3" fill="#e0deea"/></g>
    <g class="cd cd2"><rect x="308" y="130" width="104" height="140" rx="12" fill="#f6f6f7"/><rect x="318" y="140" width="84" height="64" rx="8" fill="#ece7ff"/><rect x="318" y="214" width="70" height="8" rx="4" fill="#14121c"/><rect x="318" y="230" width="84" height="6" rx="3" fill="#e0deea"/></g>
    <g class="cd cd3"><rect x="424" y="130" width="108" height="140" rx="12" fill="#f6f6f7"/><rect x="434" y="140" width="88" height="64" rx="8" fill="#b9a6ff"/><rect x="434" y="214" width="50" height="8" rx="4" fill="#14121c"/><rect x="434" y="230" width="88" height="6" rx="3" fill="#e0deea"/></g>
    <text x="192" y="296" font-size="11" font-weight="700" fill="#8a8794">3 варианта за несколько минут</text>
  </g>

  <g class="st s3">
    <text x="192" y="98" font-size="13" font-weight="800" fill="#14121c">Дизайнер доводит до результата</text>
    <g><rect x="192" y="130" width="104" height="140" rx="12" fill="#f6f6f7"/><rect x="202" y="140" width="84" height="64" rx="8" fill="#e7e5ee"/><rect x="202" y="214" width="60" height="8" rx="4" fill="#c9c6d6"/><rect x="202" y="230" width="84" height="6" rx="3" fill="#e0deea"/></g>
    <g><rect x="424" y="130" width="108" height="140" rx="12" fill="#f6f6f7"/><rect x="434" y="140" width="88" height="64" rx="8" fill="#e7e5ee"/><rect x="434" y="214" width="50" height="8" rx="4" fill="#c9c6d6"/><rect x="434" y="230" width="88" height="6" rx="3" fill="#e0deea"/></g>
    <rect x="304" y="126" width="112" height="148" rx="14" fill="#7b5cf0" fill-opacity=".08" stroke="#7b5cf0" stroke-width="1.6" stroke-dasharray="5 4" class="sel"/>
    <g><rect x="308" y="130" width="104" height="140" rx="12" fill="#fff" stroke="#e7e5ee"/><rect x="318" y="140" width="84" height="64" rx="8" fill="#ece7ff"/><rect class="grow" x="318" y="214" width="70" height="8" rx="4" fill="#14121c"/><rect x="318" y="230" width="84" height="6" rx="3" fill="#e0deea"/></g>
    <g class="bub"><rect x="392" y="112" width="132" height="34" rx="12" fill="#14121c"/><text x="404" y="133" font-size="11" font-weight="700" fill="#fff">Заголовок крупнее</text></g>
  </g>

  <g class="st s4">
    <circle cx="364" cy="170" r="42" fill="#ece7ff"/><circle cx="364" cy="170" r="30" fill="#7b5cf0"/>
    <path class="tick" d="M350 171l10 10 18-20" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="364" y="244" text-anchor="middle" font-size="15" font-weight="800" fill="#14121c">Передано</text>
    <g font-size="11" font-weight="700" text-anchor="middle"><rect x="262" y="260" width="64" height="26" rx="13" fill="#f2efff"/><text x="294" y="277" fill="#5f3fd8">PNG</text><rect x="334" y="260" width="64" height="26" rx="13" fill="#f2efff"/><text x="366" y="277" fill="#5f3fd8">PDF</text><rect x="406" y="260" width="64" height="26" rx="13" fill="#f2efff"/><text x="438" y="277" fill="#5f3fd8">Figma</text></g>
  </g>

  <g class="cur c1"><use href="#aiPtr" fill="#7b5cf0" stroke="#fff" stroke-width="1.4"/><g transform="translate(14,22)"><rect x="-4" y="-11" width="48" height="22" rx="11" fill="#7b5cf0"/><text x="20" y="4" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">Вы</text></g></g>
  <g class="cur c2"><use href="#aiPtr" fill="#14121c" stroke="#fff" stroke-width="1.4"/><g transform="translate(14,22)"><rect x="-4" y="-11" width="76" height="22" rx="11" fill="#14121c"/><text x="34" y="4" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">Дизайнер</text></g></g>
</svg></div>
      <ol class="ai-steps">
        <li><b>Ставим задачу</b><p>Вы описываете задачу, а система помогает разобрать бриф и собрать нужную информацию.</p></li>
        <li><b>Система собирает черновик</b><p>Подключенные ИИ-инструменты готовят варианты и материалы за часы, а не за дни.</p></li>
        <li><b>Дизайнер доводит до результата</b><p>Человек отбирает лучшее, правит и отвечает за качество каждого макета.</p></li>
        <li><b>Передаем готовое</b><p>Отправляем нужные форматы и оставляем время на правки.</p></li>
      </ol>
    </div>
  </section>

  <section id="процесс">
    <h2>не изобретаем колесо.<br>работаем прозрачно<br><em>и без напрягов</em></h2>
    <p class="sub">Понятные шаги, сроки и общение: вы всегда знаете, на каком мы этапе.</p>
    <div class="feat">
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg></i><div><b>сначала идея</b><p>после понимания задачи переходим к дизайну</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 4h11a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M19 9h1a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2v3l-4-3h-4a2 2 0 0 1-2-2"/></svg></i><div><b>всегда открыты к диалогу</b><p>внимательно прислушиваемся к вашим комментариям и пожеланиям</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg></i><div><b>помним про дедлайн</b><p>высылаем готовый продукт заранее, оставляем время на правки <span class="emo" role="img" aria-label="будильник" style="--r:10deg">⏰</span></p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg></i><div><b>работаем прозрачно</b><p>можем предоставить доступ к проектам</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg></i><div><b>всегда на связи</b><p>не пропадаем с радаров, никогда <span class="emo" role="img" aria-label="антенна" style="--r:-10deg">📡</span></p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 14.5a5 5 0 0 0 8 0M9 9.5h.01M15 9.5h.01"/></svg></i><div><b>понимаем границы возможностей</b><p>берем столько проектов, сколько осилим, мы ценим качество</p></div></div>
    </div>
    <div class="types">
      <div class="type"><div><span class="pill">не срочно</span><b>Большой проект</b><p>Поможем сформулировать ключевые тезисы и получить на выходе стильный продукт</p></div><img src="/assets/illustrations/bolshoy-proekt.png" alt="Календарь большого проекта"></div>
      <div class="type"><div><span class="pill g">срочно</span><b>Срочный проект</b><p>Быстро соберем шаблонный вариант в корпоративных цветах за 24 часа <span class="emo" role="img" aria-label="молния" style="--r:6deg">⚡</span></p></div><img src="/assets/illustrations/srochnyy-proekt.png" alt="Срочный проект: календарь с увеличенной датой"></div>
    </div>
    <div class="steps" style="margin-top:32px">
      <div class="step"><span>01</span>Разбираемся в задаче</div>
      <div class="step"><span>02</span>Работаем с информацией</div>
      <div class="step"><span>03</span>Выстраиваем логику</div>
      <div class="step"><span>04</span>Оформляем проект</div>
      <div class="step"><span>05</span>Отправляем нужные форматы</div>
    </div>
  </section>

  <section id="отзывы">
    <h2>что говорят <em>клиенты</em></h2>
    <p class="sub">Коротко о том, как с нами работается.</p>
    <div class="revs">
      <figure class="rev"><blockquote>Сделали презентацию для инвестора за два дня. Все аккуратно, без правок по десять кругов. Инвестор спросил, кто нам это оформил.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#c9f0d8,#8fd6ae)" aria-hidden="true">🌿</span><span><b>Анна Соколова</b><small>директор по маркетингу</small></span></figcaption></figure>
      <figure class="rev"><blockquote>Пришли с набором мыслей, ушли с логотипом и понятной айдентикой. Ребята сами предложили то, о чем мы не додумались.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#d9d0ff,#a592f5)" aria-hidden="true">🚀</span><span><b>Максим Крылов</b><small>основатель стартапа</small></span></figcaption></figure>
      <figure class="rev"><blockquote>Новый сайт магазина собрали быстро, заявок стало заметно больше. Всегда отвечали в тот же день, это очень подкупает.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#ffd9e6,#f5a3c0)" aria-hidden="true">🌸</span><span><b>Елена Власова</b><small>владелица интернет-магазина</small></span></figcaption></figure>
      <figure class="rev"><blockquote>Брали срочный проект: шаблон в корпоративных цветах за сутки. Успели к встрече с клиентом, выглядело дорого.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#fff0c2,#f5cd5c)" aria-hidden="true">⚡</span><span><b>Дмитрий Орлов</b><small>руководитель отдела продаж</small></span></figcaption></figure>
      <figure class="rev"><blockquote>Работаем по тарифу поддержки. Мелкие задачи по сайту закрывают за день, больше не ищем исполнителей на каждую правку.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#d4f0f7,#8bcfe3)" aria-hidden="true">🍀</span><span><b>Ольга Миронова</b><small>генеральный директор</small></span></figcaption></figure>
      <figure class="rev"><blockquote>Понравилось, что все прозрачно: сроки, этапы, цены. Никаких сюрпризов в конце, результат совпал с ожиданиями.</blockquote><figcaption><span class="ava" style="background:linear-gradient(135deg,#e6e6ee,#b3b1c4)" aria-hidden="true">🎯</span><span><b>Игорь Лебедев</b><small>управляющий партнер</small></span></figcaption></figure>
    </div>
  </section>

  <section id="тарифы-блок">
    <h2>тарифы <em>и направления</em></h2>
    <p class="sub">Выберите направление и тариф: цена, состав работ и сроки – все на одном экране.</p>
    <div class="tabs-row" role="tablist" aria-label="Направления"><div class="tabs" id="вкладки"></div><button class="tab support" id="поддержка" type="button" role="tab" aria-selected="false" tabindex="-1">Техническая поддержка</button></div>
    <div class="period-row" id="период" hidden><span class="period-l">оплата</span><div class="tabs" id="период-табы"></div><span class="period-note">за полгода на 15% дешевле, чем помесячно, а за год – еще на 15% дешевле</span></div>
    <div class="plans" id="тарифы"></div>
    <p class="support-note" id="поддержка-инфо" hidden>Техническая поддержка работает на <b>uixcorp.support</b></p>
    <p class="partner">Являемся партнерами <b>рег.ру</b></p>
  </section>
</div>

{{FORM}}</main>
'''
LENTA='''
<main><div class="wrap">
  <div class="page-title"><h1>лента <em>материалов</em></h1>
    <p class="sub">Кейсы и статьи о том, как мы работаем и что узнаем по пути.</p></div>
  <!-- плашка «на этой неделе»: правится вручную, меняйте цифры и подписи -->
  <div class="week">
    <b class="week-t">на этой неделе будет</b>
    <span class="week-i"><em>1</em> кейс</span>
    <span class="week-p">+</span>
    <span class="week-i"><em>2</em> статьи</span>
    <span class="week-p">+</span>
    <span class="week-i"><em>3</em> анонса</span>
  </div>
  <div class="chips tabs" id="чипы"></div>
  <div class="grid" id="лента" data-все="1"></div>
  <p style="margin:40px 0"><a class="btn" href="/">← на главную</a></p>
</div></main>
'''
KONTAKTY='''
<main><div class="wrap">
  <div class="page-title"><h1>контакты <em>и соцсети</em></h1>
    <p class="sub">Напишите нам или найдите в соцсетях – расскажем, как можем помочь.</p></div>
  <div class="contacts">
    <aside class="founder">
      <div class="avatar"><img src="/assets/founder.webp" alt="Фото основателя" width="900" height="965"></div>
      <p class="role">основатель</p>
      <h2>Олег Николаев</h2>
      <p class="muted">Дизайнил для Третьяковки, Практикума, Делимобиля и Ростелекома. Упаковываю AI-стартапы и веду блог про дизайн. Работы отмечены международными дизайн-наградами, в том числе на Behance. Помогаю брендам сделать сайт, айдентику и презентации, которые быстро понятны и вызывают доверие.</p>
      <button class="btn btn-accent" type="button" data-order>заказать дизайн</button>
    </aside>
    <nav class="menu-list" id="соцсети" aria-label="Соцсети"></nav>
  </div>
</div>
{{FORM}}</main>
'''
POST='''
<main><div class="wrap">
  <p class="crumb"><a href="/lenta">← вся лента</a></p>
  <article id="материал">
    <div class="post-cover" id="обложка"></div>
    <div class="tags dark" id="метки"></div>
    <h1 class="post-h" id="заголовок"></h1>
    <div class="post-text">
      <p>Здесь будет текст материала. Страница уже готова: обложка, метки и заголовок подставляются автоматически из списка материалов.</p>
      <p>Когда появятся тексты и картинки, мы наполним эту страницу.</p>
    </div>
  </article>
  <section class="more-posts"><h2>читайте <em>также</em></h2><p class="sub">Еще материалы из ленты.</p><div class="grid" id="еще"></div></section>
</div></main>
'''

POLITIKA='''
<main><div class="wrap doc">
  <div class="page-title"><h1>политика <em>конфиденциальности</em></h1>
    <p class="sub">Как мы обрабатываем и защищаем ваши данные.</p></div>
  <p class="date">Редакция от 29.10.2026</p>

  <h2>1. Общие положения</h2>
  <p>Настоящая политика определяет, как индивидуальный предприниматель Николаев Олег Игоревич, ИНН 780248664938 (далее – «оператор», «мы»), обрабатывает и защищает персональные данные посетителей сайта doska.agency (далее – «сайт») и лиц, оставивших заявку.</p>
  <p>Политика составлена в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных». Используя сайт и отправляя форму, вы соглашаетесь с этой политикой.</p>

  <h2>2. Какие данные мы собираем</h2>
  <ul>
    <li>имя, которое вы указываете в форме;</li>
    <li>контакт для связи: адрес электронной почты, имя в телеграме или номер телефона;</li>
    <li>описание задачи, выбранное направление и бюджет проекта;</li>
    <li>файлы, которые вы прикрепляете к заявке;</li>
    <li>технические данные: сведения о браузере и устройстве, адрес страницы, данные куки (подробнее в разделе 7).</li>
  </ul>

  <h2>3. Цели обработки</h2>
  <ul>
    <li>связаться с вами по заявке, обсудить задачу и рассчитать стоимость;</li>
    <li>заключить и исполнить договор на оказание услуг;</li>
    <li>улучшать работу сайта и понимать, чем он полезен посетителям;</li>
    <li>отвечать на ваши обращения.</li>
  </ul>

  <h2>4. Основания обработки</h2>
  <p>Мы обрабатываем данные на основании вашего согласия, которое вы даете, отправляя форму на сайте, а также для заключения и исполнения договора, стороной которого вы являетесь.</p>

  <h2>5. Сроки хранения и передача третьим лицам</h2>
  <p>Данные хранятся не дольше, чем это необходимо для целей обработки, но не более трех лет после последнего контакта, если иное не требуется законом. Мы не продаем ваши данные.</p>
  <p>Данные могут обрабатываться поставщиками, которые помогают нам работать: хостинг сайта и сервисы отправки почты. Передача данных третьим лицам осуществляется только в случаях и в порядке, разрешенных законом.</p>

  <h2>6. Ваши права</h2>
  <p>Вы можете в любой момент: узнать, какие данные о вас мы обрабатываем; потребовать уточнить, заблокировать или удалить их; отозвать согласие на обработку. Для этого напишите нам на <a href="mailto:hello@doska.agency">hello@doska.agency</a>. Мы ответим в сроки, установленные законом.</p>

  <h2>7. Файлы куки</h2>
  <p>Куки – небольшие файлы, которые сохраняются в вашем браузере. Мы используем их, чтобы сайт работал корректно и запоминал ваш выбор, например согласие на куки. Вы можете отключить куки в настройках браузера, но часть функций сайта может работать иначе.</p>

  <h2>8. Защита данных</h2>
  <p>Мы принимаем организационные и технические меры, чтобы защитить данные от неправомерного доступа, изменения, раскрытия и уничтожения: ограничиваем круг лиц с доступом, используем защищенное соединение и не храним лишнего.</p>

  <h2>9. Изменение политики</h2>
  <p>Мы можем обновлять политику. Актуальная редакция всегда доступна на этой странице, дата редакции указана вверху.</p>

  <h2>10. Контакты оператора</h2>
  <p>Индивидуальный предприниматель Николаев Олег Игоревич, ИНН 780248664938.<br>Почта для обращений: <a href="mailto:hello@doska.agency">hello@doska.agency</a>.<br>Остальные данные – на странице <a href="/rekvizity">реквизитов</a>.</p>
</div></main>
'''
REKVIZITY='''
<main><div class="wrap doc">
  <div class="page-title"><h1><em>реквизиты</em></h1>
    <p class="sub">Данные для договоров и оплаты.</p></div>
  <h2>Исполнитель</h2>
  <p>Индивидуальный предприниматель Николаев Олег Игоревич<br>ИНН: 780248664938</p>
  <h2>Банковские реквизиты</h2>
  <p>Расчетный счет: 40802810720000871188<br>Банк: ООО «Банк Точка»<br>БИК: 044525104<br>Корреспондентский счет: 30101810745374525104</p>
  <h2>Связь</h2>
  <p>Почта: <a href="mailto:hello@doska.agency">hello@doska.agency</a><br>Сайт: doska.agency</p>
</div></main>
'''
USLOVIYA='''
<main><div class="wrap doc">
  <div class="page-title"><h1>условия оплаты, <em>доставки и возврата</em></h1>
    <p class="sub">Как мы работаем, как вы платите и как получаете результат.</p></div>
  <p class="date">Редакция от 29.10.2026</p>

  <h2>1. Кто оказывает услуги</h2>
  <p>Услуги дизайна и разработки оказывает индивидуальный предприниматель Николаев Олег Игоревич, ИНН 780248664938. Полные данные – на странице <a href="/rekvizity">реквизитов</a>.</p>

  <h2>2. Что мы продаем</h2>
  <p>Мы оказываем услуги: разработка логотипа и айдентики, лендингов, корпоративных сайтов и интернет-магазинов, а также техническая поддержка. Состав и стоимость работ указаны в тарифах на сайте и уточняются в коммерческом предложении.</p>

  <h2>3. Порядок оплаты</h2>
  <ul>
    <li>оплата в рублях по счету на реквизиты исполнителя или банковской картой через платежную систему;</li>
    <li>работы начинаются после предоплаты, размер которой указан в коммерческом предложении и договоре;</li>
    <li>оставшаяся часть оплачивается по этапам или после согласования результата – как зафиксировано в договоре;</li>
    <li>техническая поддержка оплачивается вперед за выбранный период: месяц, полгода или год.</li>
  </ul>

  <h2>4. «Доставка» – передача результата</h2>
  <p>Услуги нематериальные, физической доставки нет. Результат передается в электронном виде: файлами, ссылкой на облачное хранилище или публикацией сайта на согласованном адресе. Сроки указаны в тарифе и договоре и отсчитываются с момента предоплаты и получения от вас необходимых материалов.</p>

  <h2>5. Приемка</h2>
  <p>После передачи этапа вы проверяете результат и сообщаете о замечаниях в течение пяти рабочих дней. Количество правок – в рамках выбранного тарифа. Если замечаний нет, этап считается принятым.</p>

  <h2>6. Отказ и возврат денег</h2>
  <ul>
    <li>до начала работ вы можете отказаться от услуги и получить предоплату обратно полностью;</li>
    <li>если работа уже началась, мы удерживаем стоимость фактически выполненной части, остаток возвращаем;</li>
    <li>за принятые этапы деньги не возвращаются;</li>
    <li>если мы не выполнили работу в срок или не выполнили то, что обещано в договоре, вы вправе потребовать возврата оплаты за невыполненное;</li>
    <li>по технической поддержке неиспользованный оплаченный период пересчитывается и возвращается за вычетом уже оказанных услуг.</li>
  </ul>
  <p>Возврат осуществляется тем же способом, которым вы платили, в течение 10 рабочих дней после получения заявления на <a href="mailto:hello@doska.agency">hello@doska.agency</a>.</p>

  <h2>7. Права на результат</h2>
  <p>После полной оплаты исключительные права на созданные материалы переходят к вам, если иное не указано в договоре. Мы вправе показывать работу в портфолио, если вы не возражаете.</p>

  <h2>8. Претензии и связь</h2>
  <p>Вопросы и претензии присылайте на <a href="mailto:hello@doska.agency">hello@doska.agency</a>. Мы отвечаем в течение пяти рабочих дней.</p>
</div></main>
'''
PODD='''
<main><div class="wrap">
  <div class="hx sp-hero hero">
    <div class="hx-in">
      <div>
        <span class="rf"><span class="rf-i" aria-hidden="true">●</span> правки прямо на сайте</span>
        <h1>Разработка и поддержка вашего сайта в одной системе</h1>
        <p class="sub">Выделил блок на странице, написал комментарий, нажал «отправить». Задача сразу попадает в работу. Без скриншотов и переписок.</p>
        <div class="hero-cta"><button class="btn btn-accent" type="button" data-integr>подключить поддержку</button><a class="btn" href="#как-работает">как это работает</a></div>
        <div class="hx-stats">
          <div class="hx-st"><span>1</span><b>клик до задачи</b><p>выделили и отправили</p></div>
          <div class="hx-st"><span>3</span><b>экрана</b><p>телефон, планшет, ПК</p></div>
          <div class="hx-st"><span>№</span><b>спринты</b><p>с отчетом по правкам</p></div>
        </div>
      </div>
      <svg class="scene" viewBox="0 0 560 450" role="img" aria-label="Команда оставляет правки на макете сайта">
    <g filter="url(#sh)"><rect x="20" y="16" width="520" height="376" rx="18" fill="#fff"/></g>
    <path d="M20 56H540" stroke="#e7e5ee"/>
    <circle cx="44" cy="36" r="5" fill="#e7e5ee"/><circle cx="62" cy="36" r="5" fill="#e7e5ee"/><circle cx="80" cy="36" r="5" fill="#e7e5ee"/>
    <rect x="150" y="25" width="260" height="22" rx="11" fill="#f2f1f6"/><text x="280" y="40.5" text-anchor="middle" font-size="11" font-weight="600" fill="#8a8794">yoursite.ru/support</text>

    <rect x="44" y="76" width="64" height="10" rx="5" fill="#14121c"/>
    <rect x="360" y="76" width="30" height="8" rx="4" fill="#e7e5ee"/><rect x="402" y="76" width="30" height="8" rx="4" fill="#e7e5ee"/><rect x="444" y="76" width="52" height="14" rx="7" fill="#14121c"/>
    <rect x="44" y="124" width="250" height="18" rx="9" fill="#14121c"/>
    <rect x="44" y="152" width="190" height="18" rx="9" fill="#14121c"/>
    <rect x="44" y="184" width="210" height="8" rx="4" fill="#e7e5ee"/><rect x="44" y="200" width="160" height="8" rx="4" fill="#e7e5ee"/>
    <rect x="44" y="226" width="96" height="30" rx="15" fill="#7b5cf0"/>
    <rect x="330" y="104" width="186" height="152" rx="16" fill="#ece7ff"/>
    <circle cx="423" cy="176" r="34" fill="#cfc2ff"/><path d="M398 256Q398 214 423 214Q448 214 448 256Z" fill="#7b5cf0"/>
    <rect x="44" y="282" width="140" height="72" rx="12" fill="#f6f6f7"/><rect x="198" y="282" width="140" height="72" rx="12" fill="#f6f6f7"/><rect x="352" y="282" width="164" height="72" rx="12" fill="#f6f6f7"/>

    <g class="a-region"><rect x="38" y="116" width="268" height="64" rx="10" fill="#7b5cf0" fill-opacity=".1" stroke="#7b5cf0" stroke-width="1.6" stroke-dasharray="5 4"/></g>
    <g class="a-bubble" filter="url(#sh2)">
      <rect x="150" y="196" width="196" height="62" rx="14" fill="#fff"/>
      <g transform="translate(174,222)"><use href="#avA"/></g>
      <text x="198" y="217" font-size="11" font-weight="800" fill="#14121c">Анна</text>
      <text x="198" y="233" font-size="11" font-weight="600" fill="#5b5868">Заголовок крупнее,</text>
      <text x="198" y="247" font-size="11" font-weight="600" fill="#5b5868">кнопку сдвинуть вправо</text>
    </g>
    <g class="a-pin" transform="translate(438,262)"><g filter="url(#sh2)"><path d="M0 0 C-14 -6 -16 -26 0 -28 C16 -26 14 -6 0 0Z" fill="#7b5cf0" transform="scale(1.1)"/></g><text x="0" y="-17" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">2</text></g>

    <g filter="url(#sh2)"><rect x="104" y="368" width="352" height="52" rx="26" fill="#14121c"/></g>
    <g font-size="12" font-weight="700" fill="#fff"><text x="132" y="399">Область</text><text x="198" y="399" fill="#bdb8cc">Метка</text><text x="252" y="399" fill="#bdb8cc">Элемент</text></g>
    <g class="a-btn"><rect x="336" y="376" width="112" height="36" rx="18" fill="#7b5cf0"/><text x="392" y="399" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">Отправить · 3</text></g>
    <g class="a-done" filter="url(#sh2)"><rect x="318" y="322" width="190" height="34" rx="17" fill="#fff"/><circle cx="338" cy="339" r="9" fill="#7b5cf0"/><path d="M333.6 339.2l3.2 3.2 5.6-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="354" y="343" font-size="12" font-weight="800" fill="#14121c">Спринт №3 отправлен</text></g>

    <g class="cur a-lena"><use href="#ptr" fill="#b9a6ff" stroke="#fff" stroke-width="1.4"/><g transform="translate(16,24)"><rect x="-4" y="-12" width="62" height="24" rx="12" fill="#ece7ff" stroke="#cfc2ff"/><g transform="translate(8,0) scale(.62)"><use href="#avC"/></g><text x="22" y="4" font-size="11" font-weight="700" fill="#5f3fd8">Лена</text></g></g>
    <g class="cur a-max"><use href="#ptr" fill="#14121c" stroke="#fff" stroke-width="1.4"/><g transform="translate(16,24)"><rect x="-4" y="-12" width="60" height="24" rx="12" fill="#14121c"/><g transform="translate(8,0) scale(.62)"><use href="#avD"/></g><text x="22" y="4" font-size="11" font-weight="700" fill="#fff">Макс</text></g></g>
    <g class="cur a-anna"><use href="#ptr" fill="#7b5cf0" stroke="#fff" stroke-width="1.4"/><g transform="translate(16,24)"><rect x="-4" y="-12" width="64" height="24" rx="12" fill="#7b5cf0"/><g transform="translate(8,0) scale(.62)"><use href="#avA"/></g><text x="22" y="4" font-size="11" font-weight="700" fill="#fff">Анна</text></g></g>
  </svg>
    </div>
    <svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <clipPath id="avc"><circle r="16"/></clipPath>
    <g id="avA"><g clip-path="url(#avc)"><circle r="16" fill="#ece7ff"/><path d="M-14 18Q-14 5 0 5Q14 5 14 18Z" fill="#14121c"/><circle cy="-3" r="6.4" fill="#f1c7a3"/><path d="M-7 -5Q-6 -11 0 -11Q7 -11 7 -4Q3 -8 -7 -5Z" fill="#3b2a20"/></g></g>
    <g id="avC"><g clip-path="url(#avc)"><circle r="16" fill="#e1d9ff"/><path d="M-14 18Q-14 5 0 5Q14 5 14 18Z" fill="#fff"/><circle cy="-3" r="6.4" fill="#f6d2b4"/><path d="M-8 0Q-9 -12 0 -12Q9 -12 8 0Q8 -6 0 -7Q-8 -6 -8 0Z" fill="#b5542c"/></g></g>
    <g id="avD"><g clip-path="url(#avc)"><circle r="16" fill="#cfc2ff"/><path d="M-14 18Q-14 5 0 5Q14 5 14 18Z" fill="#14121c"/><circle cy="-3" r="6.4" fill="#d9a07a"/><path d="M-6.5 -5Q-5 -10 0 -10Q6 -10 6.5 -5Q0 -7.5 -6.5 -5Z" fill="#14121c"/></g></g>
    <path id="ptr" d="M0 0 L0 17 L4.6 13 L7.6 20.2 L10.4 19 L7.4 12 L13.4 12 Z"/>
    <filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#281e5a" flood-opacity=".14"/></filter>
    <filter id="sh2" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#281e5a" flood-opacity=".16"/></filter>
  </defs>
</svg>
  </div>
  <section class="sp-sec" id="как-работает">
    <h2>как это <em>работает</em></h2>
    <p class="sub">Пять шагов от подключения до результата.</p>
    <div class="steps"><div class="step"><span>01</span>Подключаем сайт и доступы</div><div class="step"><span>02</span>Заводим личный кабинет</div><div class="step"><span>03</span>Вы оставляете заявку на правку</div><div class="step"><span>04</span>Специалист проверяет и выполняет</div><div class="step"><span>05</span>Вы получаете результат и отчет</div></div>
  </section>
  <section class="sp-sec team">
    <div class="team-text">
      <h2>дизайнер, разработчик, маркетолог и копирайтер <em>в одной подписке</em></h2>
      <p>Оформите одну подписку и закройте сразу 4 позиции в компании. Мы анализируем входящий трафик, дизайним новые блоки, ведем разработку и пишем тексты – быстрее и дешевле, чем нанимать отдельных специалистов.</p>
      <button class="btn btn-accent" type="button" data-integr>оставить заявку на интеграцию</button>
    </div>
    <div class="team-art" aria-hidden="false"><div class="team-role r1"><span class="emo-b" aria-hidden="true">🎨</span><b>Дизайнер</b><p>Рисует новые блоки и страницы по вашему стилю</p></div><div class="team-role r2"><span class="emo-b" aria-hidden="true">💻</span><b>Разработчик</b><p>Вносит правки и собирает страницы на вашей платформе</p></div><div class="team-role r3"><span class="emo-b" aria-hidden="true">📈</span><b>Маркетолог</b><p>Анализирует входящий трафик и подсказывает, что поправить</p></div><div class="team-role r4"><span class="emo-b" aria-hidden="true">✍️</span><b>Копирайтер</b><p>Пишет и правит тексты, заголовки и описания</p></div></div>
  </section>
  <section class="sp-sec">
    <h2>планы <em>на 4 квартал</em></h2>
    <p class="sub">Что запускаем и что интегрируем в ноябре и декабре.</p>
    <div class="rm-wrap"><table class="rm"><thead><tr><th>месяц</th><th>что делаем</th><th>статус</th></tr></thead><tbody><tr><td>Ноябрь</td><td>Защита, резервные копии по расписанию, мониторинг</td><td><span class="stt go">в работе</span></td></tr><tr><td>Ноябрь</td><td>Оплата прямо из личного кабинета, без заявки оператору</td><td><span class="stt go">в работе</span></td></tr><tr><td>Ноябрь</td><td>Автоматизированная аналитика сайта: события, тепловые карты, дашборд</td><td><span class="stt go">в работе</span></td></tr><tr><td>Ноябрь</td><td>Уведомления о выполненных правках на почту и в мессенджер</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Подключение нескольких ролей к личному кабинету</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Подтверждение в один клик, «принять» или «на доработку», затем публикация</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Предпросмотр сайта на каждый спринт</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Создание вариантов изменений блока по одному клику</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Создание промо-лендингов по одному промпту</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Интеграция с Tilda</td><td><span class="stt go">в работе</span></td></tr><tr><td>Декабрь</td><td>Создание дизайн-систем для сторонних AI</td><td><span class="stt go">в работе</span></td></tr></tbody></table></div>
  </section>
  <section class="sp-sec tar" id="тарифы-п">
    <h2>тарифы <em>поддержки</em></h2>
    <div class="period-row"><span class="period-l">оплата</span><div class="tabs" id="период-п-табы"></div><span class="period-note">за полгода на 15% дешевле, чем помесячно, а за год – еще на 15% дешевле</span></div>
    <div class="plans" id="тарифы-п-список"></div>
  </section>
  <section class="sp-sec">
    <h2>частые <em>вопросы</em></h2>
    <p class="sub">Если вашего вопроса нет, напишите нам.</p>
    <div class="faq"><details class="fq"><summary>Где находятся серверы?</summary><p>Все серверы доска.поддержки находятся в Российской Федерации. Данные клиентов хранятся и обрабатываются на территории РФ.</p></details><details class="fq"><summary>Что такое доска.поддержка?</summary><p>Это сервис технической поддержки сайтов: вы оставляете заявку на правку в личном кабинете, а специалист проверяет ее и выполняет в рамках вашего тарифа.</p></details><details class="fq"><summary>Как быстро вы выполняете правки?</summary><p>Срок зависит от тарифа: Базовый – 7 рабочих дней, Стандарт – 2 рабочих дня, Ультима – на следующий день при заявке до 16:00 по Москве. Точные сроки указаны в карточке тарифа и в договоре.</p></details><details class="fq"><summary>Что входит в тариф и что нет?</summary><p>Входят правки в пределах лимита вашего тарифа: тексты, блоки, формы, настройки. Новый дизайн с нуля и разработка новых разделов оцениваются отдельно.</p></details><details class="fq"><summary>Можно ли подключить мой сайт, сделанный не вами?</summary><p>Да. Сначала смотрим сайт, платформу и доступы, затем говорим, что можем поддерживать, и подключаем.</p></details><details class="fq"><summary>Как оплатить и можно ли расторгнуть?</summary><p>Оплата вперед за месяц, полгода или год: чем длиннее период, тем дешевле месяц. Неиспользованный период пересчитывается и возвращается по условиям оплаты и возврата.</p></details><details class="fq"><summary>Как защищены мои данные?</summary><p>Доступы хранятся в зашифрованном виде, действия по сайту записываются, а к данным имеют доступ только специалисты, назначенные на ваш проект.</p></details></div>
  </section>
  <section class="sp-sec">
    <div class="cta" id="итог">
      <i class="orb o1" aria-hidden="true"></i><i class="orb o2" aria-hidden="true"></i><i class="grid-dots" aria-hidden="true"></i>
      <div class="cta-main">
        <h2>подключим вашу поддержку<br><em>за один день</em></h2>
        <button class="btn btn-accent" type="button" data-integr>оставить заявку на интеграцию</button>
      </div>
      <div class="cta-tags" aria-hidden="true"><span class="t1">серверы в РФ</span><span class="t2">ответ в день заявки</span><span class="t3">без долгих договоренностей</span></div>
      <div class="cta-facts">
        <div><em>1</em><span>день на подключение</span></div>
        <div><em>7 / 2 / 1</em><span>срок правки по тарифам</span></div>
        <div><em>4</em><span>роли в одной подписке</span></div>
      </div>
    </div>
  </section>
</div>
{{FORM}}</main>
'''
def w(p,s):
    d=os.path.dirname(p)
    if d: os.makedirs(d,exist_ok=True)
    open(p,'w').write(s)
w('index.html',page('/','ДОСКА – помогаем брендам решать дизайн-задачи',D,INDEX.replace('{{FORM}}',FORM)))
w('lenta/index.html',page('/lenta','Лента – ДОСКА','Материалы и проекты агентства ДОСКА.',LENTA))
w('kontakty/index.html',page('/kontakty','Контакты – ДОСКА','Контакты и соцсети агентства ДОСКА.',KONTAKTY.replace('{{FORM}}',FORM)))
w('post.html',page('/lenta','Материал – ДОСКА','Материалы и проекты агентства ДОСКА.',POST))
w('rekvizity/index.html',page('/rekvizity','Реквизиты – ДОСКА','Реквизиты индивидуального предпринимателя.',REKVIZITY))
w('usloviya/index.html',page('/usloviya','Условия оплаты, доставки и возврата – ДОСКА','Как оплатить услуги, получить результат и вернуть деньги.',USLOVIYA))
w('podderzhka/index.html',page('/podderzhka','Поддержка – ДОСКА','доска.поддержка: сервис технической поддержки сайтов, серверы в России.',PODD.replace('{{FORM}}',FORM)))
w('404.html',page('/404','Страница не найдена – ДОСКА','Такой страницы нет.','<main><div class="wrap"><div class="page-title"><h1>страница <em>не найдена</em></h1><p class="sub">Возможно, ссылка устарела. Вернитесь на <a class="u" href="/">главную</a> или загляните в <a class="u" href="/lenta">ленту</a>.</p></div></div></main>'))
w('politika/index.html',page('/politika','Политика конфиденциальности – ДОСКА','Как мы обрабатываем и защищаем персональные данные.',POLITIKA))
