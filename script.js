(function(){
  const $=(s,e=document)=>e.querySelector(s), $$=(s,e=document)=>[...e.querySelectorAll(s)];
  const тихо=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- появление при прокрутке ---------- */
  const io='IntersectionObserver' in window&&!тихо?new IntersectionObserver(es=>{
    es.forEach(e=>{
      if(!e.isIntersecting)return;
      e.target.classList.add('in');io.unobserve(e.target);
      setTimeout(()=>{e.target.classList.remove('rv','in');e.target.style.removeProperty('--d')},1200);
    });
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'}):null;
  function появление(корень){
    if(!io){$$('.rv',корень).forEach(e=>e.classList.remove('rv'));return}
    const группы=new Map();
    $$('h1,h2,.sub,.clients,.tile,.more,.cols>div,.lead2,.video,.ai-steps li,.f,.type,.step,.rev,.week,.blk,.fq,.rm-wrap,.cta,.rf,.tabs,.plan,.row,.small,.founder,.menu-list a,.post-cover,.post-h,.post-text,.crumb,.lead,.top>div',корень).forEach(e=>{
      if(e.classList.contains('rv')||e.closest('.modal,.cookie,.head'))return;
      const п=e.parentElement;const i=группы.get(п)||0;группы.set(п,i+1);
      e.classList.add('rv');e.style.setProperty('--d',Math.min(i,6)*.07+'s');io.observe(e);
    });
  }

  /* ---------- шапка: белая подложка только при прокрутке ---------- */
  const шапка=$('.head');
  if(шапка){
    const следить=()=>шапка.classList.toggle('scrolled',scrollY>8);
    следить();addEventListener('scroll',следить,{passive:true});
  }

  /* ---------- меню ---------- */
  const b=$('.burger'),n=$('.nav');
  if(b)b.addEventListener('click',()=>n.classList.toggle('open'));

  /* ---------- плавные переходы между страницами ---------- */
  document.addEventListener('click',e=>{
    const a=e.target.closest('a');
    if(!a||тихо||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||e.button)return;
    const h=a.getAttribute('href');
    if(!h||h[0]==='#'||a.target==='_blank'||a.origin!==location.origin||h.startsWith('mailto:'))return;
    if(a.pathname===location.pathname&&a.hash)return;
    e.preventDefault();document.body.classList.add('leaving');
    setTimeout(()=>{location.href=a.href},220);
  });
  addEventListener('pageshow',e=>{if(e.persisted)document.body.classList.remove('leaving')});

  /* ---------- смена содержимого с анимацией ---------- */
  function сменить(контейнер,вывести){
    if(тихо||!контейнер.children.length){вывести();return}
    контейнер.classList.add('swap-out');
    setTimeout(()=>{контейнер.classList.remove('swap-out');вывести()},150);
  }

  /* ---------- плитки ленты ---------- */
  /* ---------- значки наград у кейсов ---------- */
  function значок(н){
    const n=12,R=44,a=3.2;let p='';
    for(let k=0;k<=240;k++){
      const t=k/240*Math.PI*2,r=R+a*Math.cos(n*t);
      p+=(k?'L':'M')+(50+r*Math.cos(t)).toFixed(2)+' '+(50+r*Math.sin(t)).toFixed(2);
    }
    const b=document.createElement('span');
    b.className='badge c-'+(н.цвет||'сер');
    b.innerHTML='<svg viewBox="0 0 100 100" aria-hidden="true"><path d="'+p+'Z"/><circle cx="19" cy="80" r="2.6" class="hole"/></svg><span class="bt"><small>'+(н.п||'')+'</small><b>'+н.т+'</b>'+(н.г?'<small>'+н.г+'</small>':'')+'</span>';
    return b;
  }
  const РАСКЛАДКА=[8,4,4,4,4,4,8];
  function размеры(n){
    const р=[];let строка=0;
    for(let i=0;i<n;i++){
      let w=РАСКЛАДКА[i%РАСКЛАДКА.length];
      if(строка+w>12)w=12-строка;
      р.push(w);строка=(строка+w)%12;
    }
    if(строка&&р.length)р[р.length-1]+=12-строка;
    return р;
  }
  function плитка(x,анимировать,i,ширина){
    if(x.секрет){
      const d=document.createElement('div');
      d.className='tile secret s'+ширина;d.style.setProperty('--art',x.ф);
      d.innerHTML='<h3>'+x.т+'</h3><div class="mock" aria-hidden="true"><i></i><i></i><i></i><svg viewBox="0 0 300 90" preserveAspectRatio="none"><path d="M0 60 C30 55 50 30 80 38 S130 62 160 40 S210 20 240 34 S280 18 300 10"/><path d="M0 76 C40 70 60 60 90 66 S150 50 190 58 S260 52 300 40"/></svg></div><span class="lock"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10V8a5 5 0 0 1 10 0v2h1a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h1zm2 0h6V8a3 3 0 0 0-6 0v2z"/></svg>пока секрет</span>';
      if(анимировать&&!тихо){d.classList.add('pop');d.style.setProperty('--d',Math.min(i,8)*.05+'s')}
      return d;
    }
    const a=document.createElement('a');
    a.href=x.ссылка;a.target='_blank';a.rel='noopener';
    a.className='tile s'+ширина+(x.свет?' light':'');
    a.style.setProperty('--art',x.ф);
    a.innerHTML='<div class="tags"><span>'+x.тип+'</span><span>'+x.ист+'</span></div><h3>'+x.т+'<i class="go" aria-hidden="true"> ↗</i></h3>';
    if(x.награды){const g=document.createElement('div');g.className='badges';x.награды.forEach(н=>g.appendChild(значок(н)));a.appendChild(g)}
    if(анимировать&&!тихо){a.classList.add('pop');a.style.setProperty('--d',Math.min(i,8)*.05+'s')}
    return a;
  }
  function вывестиПлитки(к,список,анимировать){
    к.innerHTML='';
    const р=размеры(список.length);
    список.forEach((x,i)=>к.appendChild(плитка(x,анимировать,i,р[i])));
    if(!анимировать)появление(к);
  }
  const лента=$('#лента');
  if(лента){
    const всё=лента.dataset.всё==='1';
    вывестиПлитки(лента,всё?window.ЛЕНТА:window.ЛЕНТА.slice(0,6),false);
  }
  const чипы=$('#чипы');
  if(чипы){
    const метки=[...new Set(window.ЛЕНТА.map(x=>x.тип))];
    ['все',...метки].forEach((m,i)=>{
      const t=document.createElement('button');t.className='tab'+(i?'':' on');t.textContent=m;
      t.onclick=()=>{
        $$('.tab',чипы).forEach(e=>e.classList.toggle('on',e===t));
        сменить(лента,()=>вывестиПлитки(лента,window.ЛЕНТА.filter(x=>m==='все'||x.тип===m),true));
      };
      чипы.appendChild(t);
    });
  }

  /* ---------- страница материала ---------- */
  const мат=$('#материал');
  if(мат){
    const слаг=location.pathname.split('/').filter(Boolean).pop();
    const x=window.ЛЕНТА.find(y=>y.с===слаг);
    if(x){
      document.title=x.т+' — ДОСКА';
      $('#обложка').style.setProperty('--art',x.ф);
      $('#метки').innerHTML=x.м.map(t=>'<span>'+t+'</span>').join('');
      $('#заголовок').textContent=x.т;
      const ещё=window.ЛЕНТА.filter(y=>y!==x).slice(0,3).map(y=>({...y,р:'s4'}));
      вывестиПлитки($('#ещё'),ещё,false);
    }else{
      $('#заголовок').textContent='Материал не найден';
      $('#обложка').remove();$('.post-text').innerHTML='<p>Возможно, ссылка устарела. Загляните в <a class="u" href="/lenta">ленту</a>.</p>';
      $('.more-posts').remove();
    }
  }

  /* ---------- соцсети ---------- */
  const соц=$('#соцсети'),пс=$('#подвал-соцсети');
  const ссылка=(s,вид)=>{
    const a=document.createElement(вид==='li'?'li':'a');
    const цель=вид==='li'?document.createElement('a'):a;
    цель.href=s.с;цель.textContent=s.н;
    if(s.внешняя){цель.target='_blank';цель.rel='noopener'}
    if(вид==='li'){a.appendChild(цель)}else{цель.innerHTML=s.н+'<span>'+(s.п||'')+'</span>'}
    return a;
  };
  if(соц)window.СОЦСЕТИ.forEach(s=>соц.appendChild(ссылка(s,'a')));
  if(пс)window.СОЦСЕТИ.forEach(s=>пс.appendChild(ссылка(s,'li')));

  /* ---------- тарифы ---------- */
  /* Тарифы: [название, цена, подпись, состав, популярный]. Цены пока заглушки. */
  const ТАРИФЫ={
    'Логотип / айдентика':[
      ['Базовый','от 30 000 ₽','Логотип и минимальные правила',['Логотип в 2 вариантах (основной + упрощённый)','Цветовая палитра и шрифты','Файлы для печати и экрана (SVG, PNG, PDF)','Минимальные правила: отступы, нельзя / можно','Варианты на светлом и тёмном фоне','1 итерация правок','Передача исходников в удобном пакете'],0],
      ['Стандарт','от 80 000 ₽','Фирменный стиль для старта',['Логотип и фирменный знак','Брендбук-мемо: лого, цвета, шрифты, отступы','Базовые носители: визитка, аватарки, обложки соцсетей','Правила использования на типовых носителях','Файлы для печати, веба и соцсетей','3 итерации правок','Пакет для подрядчиков (что отдавать дальше)'],'оптимальный'],
      ['Кастом','от 250 000 ₽','Айдентика под вашу задачу',['Нейминг и короткая стратегия по запросу','Несколько концепций на старте','Полный брендбук','Система носителей под вашу задачу (упаковка, мерч, презентации)','Гайдлайны для команды и подрядчиков','Сопровождение запуска айдентики','Правки на этапах концепции и финала','Исходники и библиотека файлов «на годы»'],0]],
    'Лендинг':[
      ['Базовый','от 40 000 ₽','Быстрая сборка по готовому мудборду',['Только WordPress','Сборка строго по готовому мудборду, без дизайна с нуля','1–3 экрана под один оффер','Адаптив: десктоп, планшет, мобильный','Форма заявки','SEO-база: заголовок, описание, один чистый адрес','Наполнение вашими текстами и картинками','Базовая проверка скорости и битых ссылок','1 итерация правок до релиза','Релиз на хостинг Beget','Краткая инструкция: как менять тексты и фото'],0],
      ['Стандарт','от 60 000 ₽','Полный лендинг под ключ',['CMS на выбор: WordPress, Tilda, Webflow или аналог','Сборка по мудборду под полную воронку лендинга','Блоки: оффер, преимущества, доверие, вопросы и ответы, призыв к действию','Несколько форм / точек заявки при необходимости','Подключение аналитики (Метрика / Google Аналитика)','Базовая интеграция: почта, мессенджер или CRM','SEO-база, карта сайта, корректные заголовки','Наполнение вашим контентом или создание своего','Проверка на основных устройствах и браузерах','3 итерации правок до релиза','Релиз и финальная сверка с мудбордом','Хостинг Beget на 3 месяца в подарок','Передача доступов + короткая инструкция по правкам'],'оптимальный'],
      ['Кастом','от 180 000 ₽','Индивидуальная разработка по макету',['Бриф: цель, аудитория, оффер, сценарий заявки','Прототип ключевых блоков с согласованием','Дизайн отдельно — утверждаем до разработки','Нестандартные блоки, анимации, микроинтеракции по задаче','Разработка по утверждённому макету (стек под задачу)','Интеграции под воронку: уведомления на почту / мессенджер, CRM, платежи, квиз, чат','Аналитика + цели / события по ключевым кликам','SEO и подготовка к запуску рекламы','Правки на этапах прототипа и дизайна','Разработка без «перерисовок на лету»','Релиз, проверка качества, передача доступов','Хостинг Beget на 3 месяца в подарок','Техническая поддержка на 6 месяцев','Краткая документация по дальнейшим правкам'],0]],
    'Корпоративный сайт':[
      ['Базовый','от 60 000 ₽','Типовой сайт компании',['Только WordPress','Сборка по готовому мудборду','Главная + типовые: о компании, услуги, контакты','Единый шаблон внутренних страниц','Адаптив на все основные разрешения','Формы заявок / обратной связи','Аналитика и SEO-база по страницам','Наполнение вашим контентом','Меню, футер, политики / обязательные страницы','1 итерация правок и релиз','Инструкция по правке текстов и разделов'],0],
      ['Стандарт','от 120 000 ₽','Расширенная структура сайта',['CMS на выбор под задачу','Сборка по мудборду','Расширенная структура: услуги, кейсы, команда, блог / новости','Типовые шаблоны + отдельные ключевые страницы','Формы, аналитика, цели','Базовые интеграции (почта, мессенджер, CRM)','SEO-база, карта сайта, ЧПУ','Наполнение вашим контентом или создание своего','Проверка адаптивности и форм','3 итерации правок и релиз','Хостинг Beget на 3 месяца в подарок','Передача доступов и гайд «что можно трогать»'],'оптимальный'],
      ['Кастом','от 250 000 ₽','Сложный проект под ваши задачи',['Бриф, карта сайта, сценарии ключевых разделов','Прототип главной и важных внутренних','Дизайн с отдельным согласованием по разделам','Сложная структура: фильтры, каталоги услуг, мультиязык','Личный кабинет / интеграции / нестандартные модули по задаче','Разработка после утверждения дизайна','SEO-подготовка, скорость, базовая безопасность','Несколько раундов на прототипе и дизайне','Релиз, проверка качества, документация','Хостинг Beget на 3 месяца в подарок','Техническая поддержка на 6 месяцев','Рекомендации по развитию после запуска'],0]],
    'Интернет-магазин':[
      ['Базовый','от 80 000 ₽','Магазин на WooCommerce',['Только WordPress + WooCommerce','Сборка по готовому мудборду','Каталог, карточка товара, корзина, оформление заказа','Базовые оплата и доставка','Карточки товаров по вашему шаблону данных','Адаптив, аналитика, SEO-база каталога','Уведомления о заказе вам и клиенту','Наполнение номенклатурой до 300 товаров','1 итерация правок и релиз','Инструкция: товары, цены, статусы заказов'],0],
      ['Стандарт','от 150 000 ₽','Магазин с интеграциями',['Платформа / CMS на выбор','Сборка по мудборду','Каталог с фильтрами и сортировкой','Карточка, корзина, оформление заказа','Оплата, доставка, уведомления на почту и в мессенджер','Базовые интеграции: CRM, склад, рассылки','SEO-база, карта сайта, микроразметка товара (базово)','Наполнение вашей номенклатурой до 2000 позиций','Проверка воронки покупки на мобильном','3 итерации правок и релиз','Хостинг Beget на 3 месяца в подарок','Передача доступов + гайд по каталогу и заказам'],'оптимальный'],
      ['Кастом','от 350 000 ₽','Магазин под вашу логику',['Бриф и прототип воронки покупки','Дизайн каталога, карточки и оформления заказа с согласованием','Логика под вас: скидки, продажи для бизнеса, опт, мультивалюта, регионы','Платежи, доставка, ERP / CRM / склад','Личный кабинет покупателя при необходимости','Нагрузка, SEO, подготовка к рекламе','Разработка после утверждения дизайна','Релиз, проверка заказа «от клика до оплаты»','Хостинг Beget на 3 месяца в подарок','Техническая поддержка на 6 месяцев','Документация и рекомендации по масштабированию'],0]],
    'Техническая поддержка':[
      ['Базовый',{p6:45000},'Базовый лимит правок',['Личный кабинет клиента','Базовый лимит правок, обновляется каждый месяц','Правки по заявкам из кабинета, каждую проверяет специалист','Типовые правки: тексты, фото, мелкие блоки','Не входят новые страницы','Выполнение правок до 2 рабочих дней','Короткий ежемесячный отчёт: аптайм и базовые метрики','Не входят уведомления о сбоях','Статус заявки и история в кабинете','Хостинг и доступы оплачиваются отдельно — только правки на уже живом сайте'],0],
      ['Стандарт',{p6:60000},'В 3 раза больше лимита правок',['Личный кабинет клиента','В 3 раза больше лимита правок, чем в Базовом','Правки по заявкам из кабинета, каждую проверяет специалист','Мелкие и средние правки: блоки, формы, простые секции','До 1 новой простой страницы в месяц по готовому визуалу','Выполнение правок на следующий рабочий день','Ежемесячный отчёт: работоспособность и ключевые метрики','Уведомления о сбоях и критичных ошибках','История запросов и статус «в работе / готово» + рекомендации, что лучше править пакетом'],'оптимальный'],
      ['Кастом',{p6:99000,от:1},'Максимальный лимит, пакет под объём',['Личный кабинет с вашим процессом согласования','Максимальный лимит правок: расширенный или безлимитный пул (фиксируем в договоре)','Правки по заявкам из кабинета + ручная доработка сложных задач, каждую проверяет специалист','Любые правки, включая сложные задачи','Новые страницы по готовому визуалу — в согласованном объёме','Реакция в течение часа + гарантии по срокам ответа и закрытия','Регулярные отчёты: аптайм, скорость, метрики, что ломалось','Уведомления о сбоях + сопровождение релизов и крупных обновлений','Статусы и история запросов + слоты на созвоны по развитию','Подходит, если сайт — живой продукт, а не «поставил и забыл»'],0]]
  };
  /* Техподдержка: цена в месяц зависит от периода оплаты. Исходная цена — за полгода;
     помесячно на 15% дороже, за год на 15% дешевле, чем за полгода. */
  const КП='Техническая поддержка';
  const ПЕРИОДЫ={'месяц':'помесячно','полгода':'за полгода','год':'за год'};
  let период='полгода',текущий=null;
  const деньги=n=>n.toLocaleString('ru-RU')+' ₽';
  function цена(ц){
    if(typeof ц==='string')return {главная:ц,доп:''};
    const м=Math.round(ц.p6/.85/100)*100,г=Math.round(ц.p6*.85/100)*100;
    const мес=период==='месяц'?м:период==='год'?г:ц.p6;
    const мн=период==='год'?12:6,итог=период==='месяц'?null:мес*мн;
    return {
      главная:(ц.от?'от ':'')+деньги(мес)+' / мес',
      доп:итог?'Оплата '+ПЕРИОДЫ[период]+': '+(ц.от?'от ':'')+деньги(итог)+' единым платежом':'Оплата помесячно'
    };
  }
  const вкл=$('#вкладки'),пл=$('#тарифы'),пер=$('#период'),перТ=$('#период-табы');
  if(вкл){
    function тарифы(к,анимировать){
      текущий=к;
      const инфо=$('#поддержка-инфо');if(инфо)инфо.hidden=к!==КП;
      if(пер){const показ=к===КП;if(показ&&пер.hidden&&!тихо){пер.classList.remove('show');void пер.offsetWidth;пер.classList.add('show')}пер.hidden=!показ}
      const спис=ТАРИФЫ[к];
      пл.classList.toggle('one',спис.length===1);
      пл.innerHTML=спис.map((t,i)=>
        '<div class="plan'+(t[4]?' hit':'')+(анимировать&&!тихо?' pop':'')+'" style="--d:'+i*.08+'s"><h3>'+t[0]+(t[4]?'<small>'+(t[4]===1?'популярный':t[4])+'</small>':'')+'</h3>'+
        '<div class="price">'+цена(t[1]).главная+'</div>'+(цена(t[1]).доп?'<p class="period">'+цена(t[1]).доп+'</p>':'')+'<p>'+t[2]+'</p><ul>'+t[3].map(y=>'<li'+(/^Не входят/.test(y)?' class="no"':/согласован|утвержд/i.test(y)?' class="key"':'')+'>'+y+'</li>').join('')+'</ul>'+
        '<button type="button" class="btn '+(t[4]?'btn-accent':'')+'" data-к="'+к+'" data-н="'+t[0]+'">выбрать</button></div>').join('');
      $$('.plan .btn',пл).forEach(b=>b.addEventListener('click',()=>{
        const имя=b.dataset.к+' · '+b.dataset.н+(b.dataset.к===КП?' · оплата '+ПЕРИОДЫ[период]:'');
        if(window.открытьЗаказ)window.открытьЗаказ({тариф:имя,тема:b.dataset.к==='Техническая поддержка'?'Техническая поддержка':'Тарифы и стоимость'});
      }));
      if(!анимировать)появление(пл);
    }
    /* табы: общая дорожка со скользящим выбором + отдельная кнопка «Техническая поддержка» */
    const ключи=Object.keys(ТАРИФЫ);
    вкл.classList.add('seg');
    const ползунок=document.createElement('span');ползунок.className='seg-thumb';ползунок.setAttribute('aria-hidden','true');
    вкл.appendChild(ползунок);
    const табы=[];
    const под=$('#поддержка');
    const все=()=>[...табы,под];
    function поставить(){
      const а=табы.find(e=>e.classList.contains('on'));
      ползунок.classList.toggle('off',!а);
      if(!а)return;
      ползунок.style.width=а.offsetWidth+'px';ползунок.style.transform='translateX('+а.offsetLeft+'px)';
    }
    function выбрать(t,к,фокус){
      if(t.classList.contains('on'))return;
      все().forEach(e=>{const on=e===t;e.classList.toggle('on',on);e.setAttribute('aria-selected',on);e.tabIndex=on?0:-1});
      поставить();if(фокус)t.focus();
      if(t!==под)t.scrollIntoView({block:'nearest',inline:'nearest',behavior:тихо?'auto':'smooth'});
      сменить(пл,()=>тарифы(к,true));
    }
    function клавиши(t){
      t.addEventListener('keydown',e=>{
        const d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!d)return;
        e.preventDefault();const л=все();const j=(л.indexOf(t)+d+л.length)%л.length;выбрать(л[j],ключи[j],true);
      });
    }
    ключи.slice(0,-1).forEach((к,i)=>{
      const t=document.createElement('button');t.type='button';t.className='tab'+(i?'':' on');t.innerHTML='<span class="t">'+к+'</span>';
      t.setAttribute('role','tab');t.setAttribute('aria-selected',i===0);t.tabIndex=i?-1:0;
      t.onclick=()=>выбрать(t,к,false);клавиши(t);
      табы.push(t);вкл.appendChild(t);
    });
    под.onclick=()=>выбрать(под,ключи[ключи.length-1],false);клавиши(под);
    пл.setAttribute('role','tabpanel');
    /* переключатель периода оплаты (виден только у техподдержки) */
    if(перТ){
      перТ.classList.add('seg');
      const пт=document.createElement('span');пт.className='seg-thumb';пт.setAttribute('aria-hidden','true');перТ.appendChild(пт);
      const пк=[];
      const пост=()=>{const а=пк.find(e=>e.classList.contains('on'));if(!а||!а.offsetWidth)return;пт.style.width=а.offsetWidth+'px';пт.style.transform='translateX('+а.offsetLeft+'px)'};
      Object.keys(ПЕРИОДЫ).forEach(п=>{
        const t=document.createElement('button');t.type='button';t.className='tab'+(п===период?' on':'');t.innerHTML='<span class="t">'+п+'</span>';
        t.setAttribute('role','tab');t.setAttribute('aria-selected',п===период);
        t.onclick=()=>{
          if(п===период)return;
          период=п;пк.forEach(e=>{const on=e===t;e.classList.toggle('on',on);e.setAttribute('aria-selected',on)});
          пост();сменить(пл,()=>тарифы(текущий,true));
        };
        пк.push(t);перТ.appendChild(t);
      });
      перТ.setAttribute('role','tablist');перТ.setAttribute('aria-label','Период оплаты');
      new MutationObserver(пост).observe(пер,{attributes:true,attributeFilter:['hidden']});
      addEventListener('resize',пост);
      if(document.fonts&&document.fonts.ready)document.fonts.ready.then(пост);
      setTimeout(пост,0);
    }
    тарифы(Object.keys(ТАРИФЫ)[0],false);
    поставить();addEventListener('resize',поставить);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(поставить);
  }

  /* ---------- кастомные выпадающие списки ---------- */
  $$('select.cs').forEach(s=>{
    const w=document.createElement('div');w.className='sel';
    const btn=document.createElement('button');btn.type='button';btn.className='sel-btn';
    btn.setAttribute('aria-haspopup','listbox');btn.setAttribute('aria-expanded','false');
    const ul=document.createElement('ul');ul.setAttribute('role','listbox');
    const t=document.createElement('span');
    btn.append(t,Object.assign(document.createElement('i'),{className:'chev'}));
    const опц=[...s.options].map(o=>{
      const li=document.createElement('li');li.setAttribute('role','option');li.textContent=o.text;li.dataset.v=o.value;
      li.addEventListener('click',()=>{выбрать(li.dataset.v);закрыть();btn.focus()});
      li.addEventListener('mousemove',()=>актив(li));
      ul.appendChild(li);return li;
    });
    let ак=0;
    function актив(li){опц.forEach(o=>o.classList.toggle('act',o===li));ак=опц.indexOf(li)}
    function показать(){t.textContent=s.options[s.selectedIndex].text;опц.forEach(o=>o.setAttribute('aria-selected',o.dataset.v===s.value))}
    function выбрать(v){s.value=v;показать()}
    function открыть(){w.classList.add('open');btn.setAttribute('aria-expanded','true');актив(опц[s.selectedIndex])}
    function закрыть(){w.classList.remove('open');btn.setAttribute('aria-expanded','false')}
    btn.addEventListener('click',()=>w.classList.contains('open')?закрыть():открыть());
    btn.addEventListener('keydown',e=>{
      const o=w.classList.contains('open');
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        e.preventDefault();if(!o)return открыть();
        актив(опц[(ак+(e.key==='ArrowDown'?1:-1)+опц.length)%опц.length]);
      }else if((e.key==='Enter'||e.key===' ')&&o){e.preventDefault();выбрать(опц[ак].dataset.v);закрыть()}
      else if(e.key==='Escape'&&o){e.stopPropagation();закрыть()}
    });
    document.addEventListener('click',e=>{if(!w.contains(e.target))закрыть()});
    s.addEventListener('change',показать);
    s.after(w);w.append(btn,ul);показать();
  });

  /* ---------- формы (отправка на почту подключим в конце) ---------- */
  function спасибо(ф){ф.querySelector('button[type=submit]').disabled=true;ф.querySelector('.ok').classList.add('show')}
  const ф=$('#форма');if(ф)ф.addEventListener('submit',e=>{e.preventDefault();спасибо(ф)});

  /* ---------- окно заказа ---------- */
  const окно=$('#окно');
  if(окно){
    let был;
    const фо=$('#форма-окна'),чип=$('#чип-тарифа'),поле=$('#тариф-окна'),тема=$('#тема-окна');
    const задать=(s,v)=>{s.value=v;s.dispatchEvent(new Event('change'))};
    const сброс=()=>{
      фо.reset();$('button[type=submit]',фо).disabled=false;$('.ok',фо).classList.remove('show');
      $('.attach-t',фо).textContent='прикрепить файл';
    };
    const открыть=(о)=>{
      был=document.activeElement;
      сброс();
      if(о&&о.тариф){чип.hidden=false;чип.textContent='Выбран тариф: '+о.тариф;поле.value=о.тариф;задать(тема,о.тема||'Тарифы и стоимость')}
      else{чип.hidden=true;поле.value='';задать(тема,'Новый проект')}
      окно.hidden=false;
      requestAnimationFrame(()=>окно.classList.add('open'));
      document.body.classList.add('lock');
      setTimeout(()=>$('input[name=имя]',окно).focus(),150);
    };
    window.открытьЗаказ=открыть;
    const закрыть=()=>{
      окно.classList.remove('open');document.body.classList.remove('lock');
      setTimeout(()=>{окно.hidden=true},тихо?0:320);
      if(был&&был.isConnected)был.focus();
    };
    $$('[data-order]').forEach(x=>x.addEventListener('click',()=>открыть()));
    $$('[data-close]',окно).forEach(x=>x.addEventListener('click',закрыть));
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&окно.classList.contains('open'))закрыть()});
    фо.addEventListener('submit',e=>{e.preventDefault();спасибо(фо)});
    const файл=$('input[type=file]',фо),имя=$('.attach-t',фо);
    файл.addEventListener('change',()=>{имя.textContent=файл.files[0]?файл.files[0].name:'прикрепить файл'});
  }

  /* ---------- куки ---------- */
  const к=$('.cookie');
  if(к){
    try{if(localStorage.getItem('куки'))к.remove()}catch(e){}
    $('button',к)&&$('button',к).addEventListener('click',()=>{
      try{localStorage.setItem('куки','1')}catch(e){}
      к.classList.add('gone');setTimeout(()=>к.remove(),300);
    });
  }

  /* ---------- точки-«вода» на фоне ---------- */
  $$('.dots').forEach(блок=>{
    const cv=document.createElement('canvas');cv.className='dots-bg';cv.setAttribute('aria-hidden','true');
    const g=cv.getContext&&cv.getContext('2d');if(!g)return;
    блок.prepend(cv);блок.classList.add('has-canvas');
    const ШАГ=22,R=1.25,УР=14;
    const палитра=[];
    for(let i=0;i<=УР;i++){const k=i/УР;
      palitraPush(k)}
    function palitraPush(k){
      const r=Math.round(20+(123-20)*k),gg=Math.round(18+(92-18)*k),b=Math.round(36+(240-36)*k),a=.13+.27*k;
      палитра.push('rgba('+r+','+gg+','+b+','+a.toFixed(3)+')');
    }
    let W=0,H=0,вид=false,идёт=false,прош=0;
    function размер(){
      const r=cv.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);
      W=r.width;H=r.height;cv.width=Math.round(W*d);cv.height=Math.round(H*d);g.setTransform(d,0,0,d,0,0);
    }
    function рисовать(t){
      g.clearRect(0,0,W,H);
      const T=t/1000,cols=Math.ceil(W/ШАГ)+1,rows=Math.ceil(H/ШАГ),ox=(W%ШАГ)/2;
      for(let j=0;j<rows;j++){
        const y0=j*ШАГ+ШАГ/2,fy=y0/H,кр=Math.min(1,fy/.14,(1-fy)/.14);
        if(кр<=0)continue;
        g.globalAlpha=кр;
        for(let i=0;i<cols;i++){
          const x0=ox+i*ШАГ;
          const h=(Math.sin(x0*.011+T*.9)+Math.sin(y0*.015-T*.7+x0*.004)+Math.sin((x0+y0)*.007+T*.55))/3;
          const k=Math.pow((h+1)/2,1.5);
          g.fillStyle=палитра[Math.round(k*УР)];
          g.beginPath();g.arc(x0+Math.cos(x0*.011+T*.9)*1.6,y0+h*3.4,R*(.7+k*1.1),0,6.2832);g.fill();
        }
      }
      g.globalAlpha=1;
    }
    function цикл(t){
      if(!вид){идёт=false;return}
      if(t-прош>32){прош=t;рисовать(t)}
      requestAnimationFrame(цикл);
    }
    размер();рисовать(2500);
    if(тихо||!('IntersectionObserver' in window))return;
    new IntersectionObserver(es=>{
      вид=es[0].isIntersecting;
      if(вид&&!идёт){идёт=true;requestAnimationFrame(цикл)}
    }).observe(блок);
    let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{размер();рисовать(performance.now())},120)});
  });

  /* ---------- страница «доска.поддержка»: кнопки заявки и тарифы ---------- */
  $$('[data-integr]').forEach(b=>b.addEventListener('click',()=>{
    if(window.открытьЗаказ)window.открытьЗаказ({тариф:'Интеграция доска.поддержки',тема:'Техническая поддержка'});
  }));
  const плП=$('#тарифы-п-список'),перП=$('#период-п-табы');
  if(плП&&перП){
    const вывести=()=>{
      плП.innerHTML=ТАРИФЫ[КП].map(t=>{const ц=цена(t[1]);
        return '<div class="plan'+(t[4]?' hit':'')+'"><h3>'+t[0]+(t[4]?'<small>'+(t[4]===1?'популярный':t[4])+'</small>':'')+'</h3><div class="price">'+ц.главная+'</div><p class="period">'+ц.доп+'</p><p>'+t[2]+'</p><ul>'+t[3].map(y=>'<li'+(/^Не входят/.test(y)?' class="no"':'')+'>'+y+'</li>').join('')+'</ul><button type="button" class="btn '+(t[4]?'btn-accent':'')+'" data-н="'+t[0]+'">оставить заявку на интеграцию</button></div>'}).join('');
      $$('.plan .btn',плП).forEach(b=>b.addEventListener('click',()=>{
        if(window.открытьЗаказ)window.открытьЗаказ({тариф:КП+' · '+b.dataset.н+' · оплата '+ПЕРИОДЫ[период],тема:'Техническая поддержка'});
      }));
    };
    перП.classList.add('seg');
    const пт=document.createElement('span');пт.className='seg-thumb';пт.setAttribute('aria-hidden','true');перП.appendChild(пт);
    const пк=[];
    const пост=()=>{const а=пк.find(e=>e.classList.contains('on'));if(!а||!а.offsetWidth)return;пт.style.width=а.offsetWidth+'px';пт.style.transform='translateX('+а.offsetLeft+'px)'};
    Object.keys(ПЕРИОДЫ).forEach(п=>{
      const t=document.createElement('button');t.type='button';t.className='tab'+(п===период?' on':'');t.innerHTML='<span class="t">'+п+'</span>';
      t.onclick=()=>{
        if(п===период)return;
        период=п;пк.forEach(e=>e.classList.toggle('on',e===t));пост();
        сменить(плП,()=>{вывести();$$('.plan',плП).forEach(e=>{if(!тихо)e.classList.add('pop')})});
      };
      пк.push(t);перП.appendChild(t);
    });
    вывести();пост();addEventListener('resize',пост);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(пост);
  }

  /* ---------- печатающийся фиолетовый текст ---------- */
  const ВАРИАНТЫ=['дизайн-задачи','задачи с сайтами','задачи с презентациями','задачи с айдентикой'];
  function печатать(em,варианты,по_кругу){
    const итог=em.textContent;em.setAttribute('aria-label',итог);
    const h=em.closest('h1,h2');
    if(h){
      const сохр=em.textContent;
      const самый=варианты.reduce((a,b)=>a.length>b.length?a:b);
      em.textContent=самый;h.style.minHeight=h.offsetHeight+'px';em.textContent=сохр;
    }
    let i=0,k=0,стирать=false;
    em.classList.add('tp');em.textContent='';
    const ждать=(мс)=>setTimeout(шаг,мс);
    function шаг(){
      const сл=варианты[k];
      if(!стирать){
        i++;em.textContent=сл.slice(0,i);
        if(i<сл.length)return ждать(55+Math.random()*35);
        if(!по_кругу){em.classList.remove('tp');return}
        стирать=true;return ждать(2300);
      }
      i--;em.textContent=сл.slice(0,i);
      if(i>0)return ждать(28);
      стирать=false;k=(k+1)%варианты.length;ждать(350);
    }
    ждать(250);
  }
  if(!тихо){
    $$('main h1 em, main h2 em').forEach(em=>{
      if(em.closest('.hero')&&em.closest('h1')&&location.pathname==='/'){
        печатать(em,ВАРИАНТЫ,true);return;
      }
      if(!('IntersectionObserver' in window))return;
      const o=new IntersectionObserver(es=>{if(es[0].isIntersecting){o.disconnect();печатать(em,[em.textContent],false)}},{threshold:.6});
      o.observe(em);
    });
  }

  появление(document);
})();
