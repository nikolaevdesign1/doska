#!/usr/bin/env python3
"""Собирает страницы сайта из общих кусков (шапка, подвал, окно заказа, куки).
Запуск: python3 build.py  — результат (html-файлы) коммитится в репозиторий."""
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
<header class="head"><div class="wrap">
  <a class="logo" href="/">ДОСКА</a>
  <nav class="nav">
    <a href="https://dprofile.ru/nikolaev_design1" target="_blank" rel="noopener">кейсы</a>
    <a href="/lenta">лента</a>
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
        <li><a href="/lenta">лента</a></li><li><a href="/kontakty">контакты</a></li><li><a href="/#заявка">заявка</a></li></ul></div>
      <div><h4>связаться</h4><ul><li><a href="mailto:hello@doska.agency">hello@doska.agency</a></li><li>чат в телеграме</li><li>чат в вотсапе</li></ul></div>
    </div>
  </div>
  <div class="big" aria-hidden="true">ДОСКА</div>
  <div class="bottom"><span>© ДОСКА, все права защищены</span><a class="u" href="#">прочитать договор и условия</a></div>
</div></footer>

<div class="modal" id="окно" role="dialog" aria-modal="true" aria-labelledby="окно-заголовок" hidden>
  <div class="modal-shade" data-close></div>
  <div class="modal-box">
    <div class="modal-art" aria-hidden="true"></div>
    <form class="modal-form" id="форма-окна">
      <button class="modal-x" type="button" data-close aria-label="Закрыть">×</button>
      <h3 id="окно-заголовок">расскажите о задаче — вернёмся с расчётом</h3>
      <input name="имя" required placeholder="введите ваше имя" autocomplete="name">
      <input name="связь" required placeholder="почта или телеграм">
      <textarea name="задача" rows="2" placeholder="коротко опишите задачу"></textarea>
      <label class="attach"><input type="file" name="файл"><span class="attach-t">прикрепить файл</span></label>
      <div><button class="btn btn-accent" type="submit">отправить</button></div>
      <p class="ok">Спасибо! Мы свяжемся с вами в ближайшее время.</p>
    </form>
  </div>
</div>

<div class="cookie"><p>Мы используем файлы куки, чтобы улучшить работу сайта. Продолжая использовать этот сайт, вы соглашаетесь с использованием куки-файлов.</p><button class="btn" type="button">согласен(а)</button></div>
<script src="/data.js"></script>
<script src="/script.js"></script>
</body></html>
'''
def page(path,title,desc,body):
    h=HEAD.format(title=title,desc=desc,site=SITE,path=path)
    return h+body+FOOT
D='ДОСКА — агентство: помогаем брендам решать дизайн-задачи. Сайты, презентации, приложения, брендинг.'
INDEX='''
<main>
<div class="wrap">
  <h1>помогаем брендам<br>решать <em>дизайн-задачи</em></h1>
  <div class="clients"><img src="/assets/clients/klient-1.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-2.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-3.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-4.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-5.png" alt="Логотип клиента" loading="eager"></div>

  <section id="кейсы" style="padding-top:0">
    <div class="grid" id="лента"></div>
    <div class="more"><span>Сделаем так же и ещё круче</span><a class="btn btn-accent" href="/lenta">вся лента</a></div>
  </section>

  <section id="возможности" class="services">
    <h2>сайты, презентации,<br>приложения, брендинг<br><em>и многое другое..</em></h2>
    <div class="cols">
      <div>лендинги<br>интернет-магазины<br>мобильные приложения<br>корпоративные сайты<br>дизайн-системы<br>А/Б-тестирование</div>
      <div>презентации<br>годовые отчёты<br>брошюры<br>шаблоны писем<br>руководства по стилю<br>рабочие тетради</div>
      <div>брендинг<br>айдентика<br>нейминг<br>копирайтинг<br>ведение соцсетей<br>креатив</div>
    </div>
  </section>

  <section id="ии" class="ai">
    <h2>работаем через ИИ-интеграции<br><em>и собираем быстрее</em></h2>
    <p class="lead2">Мы построили ИИ-систему, которая берёт на себя рутину: разбирает бриф, собирает черновики и подготавливает материалы. Дизайнеры тратят время на идею и качество, а вы получаете результат заметно быстрее.</p>
    <div class="ai-grid">
      <div class="video" role="img" aria-label="Место под видео о работе ИИ-системы"><span>видео о том, как работает система, появится здесь</span></div>
      <ol class="ai-steps">
        <li><b>Ставим задачу</b><p>Вы описываете задачу, а система помогает разобрать бриф и собрать нужную информацию.</p></li>
        <li><b>Система собирает черновик</b><p>Подключённые ИИ-инструменты готовят варианты и материалы за часы, а не за дни.</p></li>
        <li><b>Дизайнер доводит до результата</b><p>Человек отбирает лучшее, правит и отвечает за качество каждого макета.</p></li>
        <li><b>Передаём готовое</b><p>Отправляем нужные форматы и оставляем время на правки.</p></li>
      </ol>
    </div>
  </section>

  <section id="процесс">
    <h2>не изобретаем колесо.<br>работаем прозрачно<br><em>и без напрягов</em></h2>
    <div class="feat">
      <div class="f"><i>✦</i><div><b>сначала идея</b><p>после понимания задачи переходим к дизайну</p></div></div>
      <div class="f"><i>✦</i><div><b>всегда открыты к диалогу</b><p>внимательно прислушиваемся к вашим комментариям и пожеланиям</p></div></div>
      <div class="f"><i>✦</i><div><b>помним про дедлайн</b><p>высылаем готовый продукт заранее, оставляем время на правки</p></div></div>
      <div class="f"><i>✦</i><div><b>работаем прозрачно</b><p>можем предоставить доступ к проектам</p></div></div>
      <div class="f"><i>✦</i><div><b>всегда на связи</b><p>не пропадаем с радаров, никогда</p></div></div>
      <div class="f"><i>✦</i><div><b>понимаем границы возможностей</b><p>берём столько проектов, сколько осилим, мы ценим качество</p></div></div>
    </div>
    <div class="types">
      <div class="type"><div><span class="pill">не срочно</span><b>Большой проект</b><p>Поможем сформулировать ключевые тезисы и получить на выходе стильный продукт</p></div></div>
      <div class="type"><div><span class="pill g">срочно</span><b>Срочный проект</b><p>Быстро соберём шаблонный вариант в корпоративных цветах за 24 часа</p></div><div class="badge">24</div></div>
    </div>
    <div class="steps" style="margin-top:32px">
      <div class="step"><span>(01)</span>Разбираемся в задаче</div>
      <div class="step"><span>(02)</span>Работаем с информацией</div>
      <div class="step"><span>(03)</span>Выстраиваем логику</div>
      <div class="step"><span>(04)</span>Оформляем проект</div>
      <div class="step"><span>(05)</span>Отправляем нужные форматы</div>
    </div>
  </section>

  <section id="тарифы-блок">
    <h2>тарифы <em>и направления</em></h2>
    <div class="tabs" id="вкладки" role="tablist"></div>
    <div class="plans" id="тарифы"></div>
  </section>
</div>

<section class="form" id="заявка"><div class="wrap">
  <form id="форма">
    <div class="row"><label>привет! меня зовут</label><input required placeholder="введите ваше имя"></div>
    <div class="row"><label>хотелось бы заказать у вас</label>
      <select class="cs" id="услуга"><option>Логотип / айдентика</option><option>Лендинг</option><option>Корпоративный сайт</option><option>Интернет-магазин</option><option>Другое</option></select></div>
    <div class="row"><label>планируем заложить на проект</label>
      <select class="cs"><option>до 100 000 ₽</option><option>100 000 – 300 000 ₽</option><option>300 000 – 700 000 ₽</option><option>более 700 000 ₽</option><option>пока не знаем</option></select></div>
    <div class="row"><label>вкратце у нас следующая задача</label><textarea rows="2" placeholder="опишите, что необходимо сделать, на звонке всё обсудим подробнее"></textarea></div>
    <div class="row"><label>ответ можно прислать сюда</label><input required placeholder="тут может быть ваша почта или телеграм / вотсап"></div>
    <p class="small">Отправляя форму, вы даёте согласие с <a href="#">Политикой обработки персональных данных</a></p>
    <div><button class="btn btn-accent" type="submit">отправить заявку и узнать стоимость</button></div>
    <p class="ok">Спасибо! Мы свяжемся с вами в ближайшее время.</p>
  </form>
</div></section>
</main>
'''
LENTA='''
<main><div class="wrap">
  <div class="page-title"><h1>лента <em>материалов</em></h1></div>
  <div class="chips tabs" id="чипы"></div>
  <div class="grid" id="лента" data-всё="1"></div>
  <p style="margin:40px 0"><a class="btn" href="/">← на главную</a></p>
</div></main>
'''
KONTAKTY='''
<main><div class="wrap">
  <div class="page-title"><h1>контакты <em>и соцсети</em></h1></div>
  <div class="contacts">
    <aside class="founder">
      <div class="avatar" aria-label="Место под фото основателя"><span>Д</span></div>
      <p class="role">основатель</p>
      <h2>Имя Фамилия</h2>
      <p class="muted">Основатель агентства ДОСКА. Здесь будет короткий рассказ о себе и о подходе к работе.</p>
      <button class="btn btn-accent" type="button" data-order>заказать дизайн</button>
    </aside>
    <nav class="menu-list" id="соцсети" aria-label="Соцсети"></nav>
  </div>
</div></main>
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
  <section class="more-posts"><h2>читайте <em>также</em></h2><div class="grid" id="ещё"></div></section>
</div></main>
'''
def w(p,s):
    d=os.path.dirname(p)
    if d: os.makedirs(d,exist_ok=True)
    open(p,'w').write(s)
w('index.html',page('/','ДОСКА — помогаем брендам решать дизайн-задачи',D,INDEX))
w('lenta/index.html',page('/lenta','Лента — ДОСКА','Материалы и проекты агентства ДОСКА.',LENTA))
w('kontakty/index.html',page('/kontakty','Контакты — ДОСКА','Контакты и соцсети агентства ДОСКА.',KONTAKTY))
w('post.html',page('/lenta','Материал — ДОСКА','Материалы и проекты агентства ДОСКА.',POST))
