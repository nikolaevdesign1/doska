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
    <a href="https://dprofile.ru/nikolaev_design1" target="_blank" rel="noopener">кейсы <span class="sub">(dprofile)</span></a>
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
      <div><h4>связаться</h4><ul><li><a href="mailto:hello@doska.agency">hello@doska.agency</a></li></ul></div>
    </div>
  </div>
  <div class="big" aria-hidden="true">ДОСКА</div>
  <div class="bottom"><span>© ДОСКА, все права защищены</span><span class="links"><a class="u" href="/politika">политика конфиденциальности</a><a class="u" href="#">прочитать договор и условия</a></span></div>
</div></footer>

<div class="modal" id="окно" role="dialog" aria-modal="true" aria-labelledby="окно-заголовок" hidden>
  <div class="modal-shade" data-close></div>
  <div class="modal-box">
    <div class="modal-art" aria-hidden="true"></div>
    <form class="modal-form" id="форма-окна">
      <button class="modal-x" type="button" data-close aria-label="Закрыть">×</button>
      <h3 id="окно-заголовок">расскажите о задаче — вернёмся с расчётом <span class="emo" role="img" aria-label="знак мира" style="--r:8deg">✌️</span></h3>
      <input name="имя" required placeholder="введите ваше имя" autocomplete="name">
      <input name="связь" required placeholder="почта или телеграм">
      <textarea name="задача" rows="2" placeholder="коротко опишите задачу"></textarea>
      <label class="attach"><input type="file" name="файл"><span class="attach-t">прикрепить файл</span></label>
      <div><button class="btn btn-accent" type="submit">отправить</button></div>
      <p class="ok">Спасибо! Мы свяжемся с вами в ближайшее время. <span class="emo" role="img" aria-label="поднятые руки" style="--r:-8deg">🙌</span></p>
    </form>
  </div>
</div>

<div class="cookie"><p>Мы используем файлы куки, чтобы улучшить работу сайта. Продолжая использовать этот сайт, вы соглашаетесь с использованием куки-файлов. <span class="emo" role="img" aria-label="печенье" style="--r:-12deg">🍪</span></p><button class="btn" type="button">согласен(а)</button></div>
<script src="/data.js"></script>
<script src="/script.js"></script>
</body></html>
'''
def page(path,title,desc,body):
    h=HEAD.format(title=title,desc=desc,site=SITE,path=path)
    foot=FOOT
    if 'class="form"' in body:   # подвал наезжает на белый блок формы
        foot=foot.replace('<footer class="foot">','<footer class="foot lap">',1)
    return h+body+foot
D='ДОСКА — агентство: помогаем брендам решать дизайн-задачи. Сайты, презентации, приложения, брендинг.'
FORM='''<section class="form" id="заявка"><div class="wrap">
  <form id="форма">
    <div class="row"><label>привет! <span class="emo" role="img" aria-label="приветствие" style="--r:-14deg">👋</span> меня зовут</label><input required placeholder="введите ваше имя"></div>
    <div class="row"><label>хотелось бы заказать у вас</label>
      <select class="cs" id="услуга"><option>Логотип / айдентика</option><option>Лендинг</option><option>Корпоративный сайт</option><option>Интернет-магазин</option><option>Техническая поддержка</option><option>Другое</option></select></div>
    <div class="row"><label>планируем заложить на проект</label>
      <select class="cs"><option>до 100 000 ₽</option><option>100 000 – 300 000 ₽</option><option>300 000 – 700 000 ₽</option><option>более 700 000 ₽</option><option>пока не знаем</option></select></div>
    <div class="row"><label>вкратце у нас следующая задача</label><textarea rows="1" placeholder="опишите, что необходимо сделать, на звонке всё обсудим подробнее"></textarea></div>
    <div class="row"><label>ответ можно прислать сюда</label><input required placeholder="тут может быть ваша почта или телеграм / вотсап"></div>
    <div class="form-foot">
      <p class="small">Отправляя форму, вы даёте согласие<br>с <a href="/politika">Политикой обработки персональных данных</a></p>
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
  <div class="hero-cta"><button class="btn btn-accent" type="button" data-order>оставить заявку</button></div>
  <div class="clients"><img src="/assets/clients/klient-1.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-2.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-3.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-4.png" alt="Логотип клиента" loading="eager"><img src="/assets/clients/klient-5.png" alt="Логотип клиента" loading="eager"></div>
  </div>

  <section id="кейсы" style="padding-top:0">
    <div class="grid" id="лента"></div>
    <div class="more"><span>Сделаем так же и ещё круче <span class="emo" role="img" aria-label="очки" style="--r:-6deg">😎</span></span><a class="btn btn-accent" href="/lenta">вся лента</a></div>
  </section>

  <section id="возможности" class="services dots">
    <h2>сайты, презентации,<br>приложения, брендинг<br><em>и многое другое..</em></h2>
    <div class="cols">
      <div>лендинги<br>интернет-магазины<br>мобильные приложения<br>корпоративные сайты<br>дизайн-системы<br>А/Б-тестирование</div>
      <div>презентации<br>годовые отчёты<br>брошюры<br>шаблоны писем<br>руководства по стилю<br>рабочие тетради</div>
      <div>брендинг<br>айдентика<br>нейминг<br>копирайтинг<br>ведение соцсетей<br>креатив</div>
    </div>
  </section>

  <section id="ии" class="ai">
    <h2>работаем через ИИ-интеграции<br><em>и собираем быстрее</em></h2>
    <p class="lead2">Мы построили ИИ-систему, которая берёт на себя рутину: разбирает бриф, собирает черновики и подготавливает материалы. Дизайнеры тратят время на идею и качество, а вы получаете результат заметно быстрее <span class="emo" role="img" aria-label="ракета" style="--r:8deg">🚀</span></p>
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
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg></i><div><b>сначала идея</b><p>после понимания задачи переходим к дизайну</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 4h11a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M19 9h1a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2v3l-4-3h-4a2 2 0 0 1-2-2"/></svg></i><div><b>всегда открыты к диалогу</b><p>внимательно прислушиваемся к вашим комментариям и пожеланиям</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg></i><div><b>помним про дедлайн</b><p>высылаем готовый продукт заранее, оставляем время на правки <span class="emo" role="img" aria-label="будильник" style="--r:10deg">⏰</span></p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg></i><div><b>работаем прозрачно</b><p>можем предоставить доступ к проектам</p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg></i><div><b>всегда на связи</b><p>не пропадаем с радаров, никогда <span class="emo" role="img" aria-label="антенна" style="--r:-10deg">📡</span></p></div></div>
      <div class="f"><i aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 14.5a5 5 0 0 0 8 0M9 9.5h.01M15 9.5h.01"/></svg></i><div><b>понимаем границы возможностей</b><p>берём столько проектов, сколько осилим, мы ценим качество</p></div></div>
    </div>
    <div class="types">
      <div class="type"><div><span class="pill">не срочно</span><b>Большой проект</b><p>Поможем сформулировать ключевые тезисы и получить на выходе стильный продукт</p></div><img src="/assets/illustrations/bolshoy-proekt.png" alt="Календарь большого проекта"></div>
      <div class="type"><div><span class="pill g">срочно</span><b>Срочный проект</b><p>Быстро соберём шаблонный вариант в корпоративных цветах за 24 часа <span class="emo" role="img" aria-label="молния" style="--r:6deg">⚡</span></p></div><img src="/assets/illustrations/srochnyy-proekt.png" alt="Срочный проект: календарь с увеличенной датой"></div>
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
    <div class="tabs-row" role="tablist" aria-label="Направления"><div class="tabs" id="вкладки"></div><button class="tab support" id="поддержка" type="button" role="tab" aria-selected="false" tabindex="-1">Техническая поддержка</button></div>
    <div class="plans" id="тарифы"></div>
  </section>
</div>

{{FORM}}</main>
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
      <div class="avatar"><img src="/assets/founder.webp" alt="Фото основателя" width="900" height="965"></div>
      <p class="role">основатель</p>
      <h2>Имя Фамилия</h2>
      <p class="muted">Основатель агентства ДОСКА. Здесь будет короткий рассказ о себе и о подходе к работе.</p>
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
  <section class="more-posts"><h2>читайте <em>также</em></h2><div class="grid" id="ещё"></div></section>
</div></main>
'''

POLITIKA='''
<main><div class="wrap doc">
  <div class="page-title"><h1>политика <em>конфиденциальности</em></h1></div>
  <p class="note">Это черновик-шаблон. Перед публикацией его должен проверить юрист, а поля в квадратных скобках нужно заполнить реальными данными оператора.</p>
  <p class="date">Редакция от [дата]</p>

  <h2>1. Общие положения</h2>
  <p>Настоящая политика определяет, как [полное наименование оператора или ФИО индивидуального предпринимателя / самозанятого], ИНН [номер] (далее — «оператор», «мы»), обрабатывает и защищает персональные данные посетителей сайта doska.agency (далее — «сайт») и лиц, оставивших заявку.</p>
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
  <p>Мы обрабатываем данные на основании вашего согласия, которое вы даёте, отправляя форму на сайте, а также для заключения и исполнения договора, стороной которого вы являетесь.</p>

  <h2>5. Сроки хранения и передача третьим лицам</h2>
  <p>Данные хранятся не дольше, чем это необходимо для целей обработки, но не более [срок, например 3 года] после последнего контакта, если иное не требуется законом. Мы не продаём ваши данные.</p>
  <p>Данные могут обрабатываться поставщиками, которые помогают нам работать: услуги размещения сайта и почтовой рассылки — [перечень поставщиков и страна, где находятся серверы]. Передача данных за пределы России осуществляется только в случаях и в порядке, разрешённых законом.</p>

  <h2>6. Ваши права</h2>
  <p>Вы можете в любой момент: узнать, какие данные о вас мы обрабатываем; потребовать уточнить, заблокировать или удалить их; отозвать согласие на обработку. Для этого напишите нам на <a href="mailto:hello@doska.agency">hello@doska.agency</a>. Мы ответим в сроки, установленные законом.</p>

  <h2>7. Файлы куки</h2>
  <p>Куки — небольшие файлы, которые сохраняются в вашем браузере. Мы используем их, чтобы сайт работал корректно и запоминал ваш выбор, например согласие на куки. Вы можете отключить куки в настройках браузера, но часть функций сайта может работать иначе.</p>

  <h2>8. Защита данных</h2>
  <p>Мы принимаем организационные и технические меры, чтобы защитить данные от неправомерного доступа, изменения, раскрытия и уничтожения: ограничиваем круг лиц с доступом, используем защищённое соединение и не храним лишнего.</p>

  <h2>9. Изменение политики</h2>
  <p>Мы можем обновлять политику. Актуальная редакция всегда доступна на этой странице, дата редакции указана вверху.</p>

  <h2>10. Контакты оператора</h2>
  <p>[Наименование оператора / ФИО], ИНН [номер], адрес: [адрес].<br>Почта для обращений: <a href="mailto:hello@doska.agency">hello@doska.agency</a>.</p>
</div></main>
'''
def w(p,s):
    d=os.path.dirname(p)
    if d: os.makedirs(d,exist_ok=True)
    open(p,'w').write(s)
w('index.html',page('/','ДОСКА — помогаем брендам решать дизайн-задачи',D,INDEX.replace('{{FORM}}',FORM)))
w('lenta/index.html',page('/lenta','Лента — ДОСКА','Материалы и проекты агентства ДОСКА.',LENTA))
w('kontakty/index.html',page('/kontakty','Контакты — ДОСКА','Контакты и соцсети агентства ДОСКА.',KONTAKTY.replace('{{FORM}}',FORM)))
w('post.html',page('/lenta','Материал — ДОСКА','Материалы и проекты агентства ДОСКА.',POST))
w('politika/index.html',page('/politika','Политика конфиденциальности — ДОСКА','Как мы обрабатываем и защищаем персональные данные.',POLITIKA))
