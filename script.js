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
    $$('h1,h2,.clients,.tile,.more,.cols>div,.lead2,.video,.ai-steps li,.f,.type,.step,.tabs,.plan,.row,.small,.founder,.menu-list a,.post-cover,.post-h,.post-text,.crumb,.lead,.top>div',корень).forEach(e=>{
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
  function плитка(x,анимировать,i){
    const a=document.createElement('a');
    a.href='/lenta/'+x.с;a.className='tile '+x.р+(x.свет?' light':'');
    a.style.setProperty('--art',x.ф);
    a.innerHTML='<div class="tags">'+x.м.map(t=>'<span>'+t+'</span>').join('')+'</div><h3>'+x.т+'</h3>';
    if(анимировать&&!тихо){a.classList.add('pop');a.style.setProperty('--d',Math.min(i,8)*.05+'s')}
    return a;
  }
  function вывестиПлитки(к,список,анимировать){
    к.innerHTML='';
    список.forEach((x,i)=>к.appendChild(плитка(x,анимировать,i)));
    if(!анимировать)появление(к);
  }
  const лента=$('#лента');
  if(лента){
    const всё=лента.dataset.всё==='1';
    вывестиПлитки(лента,всё?window.ЛЕНТА:window.ЛЕНТА.slice(0,7),false);
  }
  const чипы=$('#чипы');
  if(чипы){
    const метки=[...new Set(window.ЛЕНТА.flatMap(x=>x.м))];
    ['все',...метки].forEach((m,i)=>{
      const t=document.createElement('button');t.className='tab'+(i?'':' on');t.textContent=m;
      t.onclick=()=>{
        $$('.tab',чипы).forEach(e=>e.classList.toggle('on',e===t));
        сменить(лента,()=>вывестиПлитки(лента,window.ЛЕНТА.filter(x=>m==='все'||x.м.includes(m)),true));
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
      ['Стандарт','от 80 000 ₽','Фирменный стиль для старта',['Логотип и фирменный знак','Брендбук-мемо: лого, цвета, шрифты, отступы','Базовые носители: визитка, аватарки, обложки соцсетей','Правила использования на типовых носителях','Файлы для печати, веба и соцсетей','3 итерации правок','Пакет для подрядчиков (что отдавать дальше)'],1],
      ['Кастом','от 250 000 ₽','Айдентика под вашу задачу',['Нейминг и короткая стратегия по запросу','Несколько концепций на старте','Полный брендбук','Система носителей под вашу задачу (упаковка, мерч, презентации)','Гайдлайны для команды и подрядчиков','Сопровождение запуска айдентики','Правки на этапах концепции и финала','Исходники и библиотека файлов «на годы»'],0]],
    'Лендинг':[
      ['Базовый','от 40 000 ₽','Быстрая сборка по готовому мудборду',['Только WordPress','Сборка строго по готовому мудборду, без дизайна с нуля','1–3 экрана под один оффер','Адаптив: десктоп, планшет, мобильный','Форма заявки + уведомление на почту / мессенджер','Подключение аналитики (Метрика / Google Аналитика)','SEO-база: заголовок, описание, один чистый адрес','Наполнение вашими текстами и картинками','Базовая проверка скорости и битых ссылок','1 итерация правок до релиза','Релиз на выбранный хостинг','Хостинг на выбор на 3 месяца','Краткая инструкция: как менять тексты и фото'],0],
      ['Стандарт','от 60 000 ₽','Полный лендинг под ключ',['CMS на выбор: WordPress, Tilda, Webflow или аналог','Сборка по мудборду под полную воронку лендинга','Блоки: оффер, преимущества, доверие, вопросы и ответы, призыв к действию','Несколько форм / точек заявки при необходимости','Аналитика + цели / события по ключевым кликам','Базовая интеграция: почта, мессенджер или CRM','SEO-база, карта сайта, корректные заголовки','Наполнение вашим контентом','Проверка на основных устройствах и браузерах','3 итерации правок до релиза','Релиз и финальная сверка с мудбордом','Хостинг на выбор на 3 месяца','Передача доступов + короткая инструкция по правкам'],'оптимальный'],
      ['Кастом','от 180 000 ₽','Индивидуальная разработка по макету',['Бриф: цель, аудитория, оффер, сценарий заявки','Прототип ключевых блоков с согласованием','Дизайн отдельно — утверждаем до разработки','Нестандартные блоки, анимации, микроинтеракции по задаче','Разработка по утверждённому макету (стек под задачу)','Интеграции под воронку: CRM, платежи, квиз, чат','SEO и подготовка к запуску рекламы','Правки на этапах прототипа и дизайна','Разработка без «перерисовок на лету»','Релиз, проверка качества, передача доступов','Хостинг на выбор на 3 месяца','Краткая документация по дальнейшим правкам'],0]],
    'Корпоративный сайт':[
      ['Базовый','от 150 000 ₽','Типовой сайт компании',['Только WordPress','Сборка по готовому мудборду','Главная + типовые: о компании, услуги, контакты','Единый шаблон внутренних страниц','Адаптив на все основные разрешения','Формы заявок / обратной связи','Аналитика и SEO-база по страницам','Наполнение вашим контентом','Меню, футер, политики / обязательные страницы','1 итерация правок и релиз','Хостинг на выбор на 3 месяца','Инструкция по правке текстов и разделов'],0],
      ['Стандарт','от 300 000 ₽','Расширенная структура сайта',['CMS на выбор под задачу','Сборка по мудборду','Расширенная структура: услуги, кейсы, команда, блог / новости','Типовые шаблоны + отдельные ключевые страницы','Формы, аналитика, цели','Базовые интеграции (почта, мессенджер, CRM)','SEO-база, карта сайта, ЧПУ','Наполнение контентом от вас','Проверка адаптивности и форм','3 итерации правок и релиз','Хостинг на выбор на 3 месяца','Передача доступов и гайд «что можно трогать»'],'оптимальный'],
      ['Кастом','по запросу','Сложный проект под ваши задачи',['Бриф, карта сайта, сценарии ключевых разделов','Прототип главной и важных внутренних','Дизайн с отдельным согласованием по разделам','Сложная структура: фильтры, каталоги услуг, мультиязык','Личный кабинет / интеграции / нестандартные модули по задаче','Разработка после утверждения дизайна','SEO-подготовка, скорость, базовая безопасность','Несколько раундов на прототипе и дизайне','Релиз, проверка качества, документация','Хостинг на выбор на 3 месяца','Рекомендации по развитию после запуска'],0]],
    'Интернет-магазин':[
      ['Базовый','от 150 000 ₽','Магазин на WooCommerce',['Только WordPress + WooCommerce','Сборка по готовому мудборду','Каталог, карточка товара, корзина, оформление заказа','Базовые оплата и доставка','Карточки товаров по вашему шаблону данных','Адаптив, аналитика, SEO-база каталога','Уведомления о заказе вам и клиенту','Наполнение номенклатурой в разумном объёме','1 итерация правок и релиз','Хостинг на выбор на 3 месяца','Инструкция: товары, цены, статусы заказов'],0],
      ['Стандарт','от 350 000 ₽','Магазин с интеграциями',['Платформа / CMS на выбор','Сборка по мудборду','Каталог с фильтрами и сортировкой','Карточка, корзина, оформление заказа','Оплата, доставка, уведомления на почту и в мессенджер','Базовые интеграции: CRM, склад, рассылки','SEO-база, карта сайта, микроразметка товара (базово)','Наполнение вашей номенклатурой','Проверка воронки покупки на мобильном','3 итерации правок и релиз','Хостинг на выбор на 3 месяца','Передача доступов + гайд по каталогу и заказам'],'оптимальный'],
      ['Кастом','по запросу','Магазин под вашу логику',['Бриф и прототип воронки покупки','Дизайн каталога, карточки и оформления заказа с согласованием','Логика под вас: скидки, продажи для бизнеса, опт, мультивалюта, регионы','Платежи, доставка, ERP / CRM / склад','Личный кабинет покупателя при необходимости','Нагрузка, SEO, подготовка к рекламе','Разработка после утверждения дизайна','Релиз, проверка заказа «от клика до оплаты»','Хостинг на выбор на 3 месяца','Документация и рекомендации по масштабированию'],0]],
    'Техническая поддержка':[
      ['Базовый','от 15 000 ₽ / мес','До 10 запросов в месяц',['Личный кабинет клиента','До 10 запросов в месяц (правки через ИИ)','Типовые правки: тексты, фото, мелкие блоки','Статус заявки и история в кабинете','Ежемесячный короткий отчёт: аптайм и базовые метрики','Ответ в рабочие дни в рамках очереди','Без новых страниц и без крупных переделок','Хостинг и доступы не входят — только правки на уже живом сайте'],0],
      ['Стандарт','от 40 000 ₽ / мес','До 30 запросов в месяц',['Личный кабинет + более приоритетная очередь, чем в Базовом','До 30 запросов в месяц','Правки через ИИ + проверка человеком при спорных местах','Мелкие и средние правки: блоки, формы, простые секции','До 1 новой простой страницы в месяц по готовому визуалу','Отчёт по работоспособности и ключевым метрикам','Уведомления о сбоях / критичных ошибках','История запросов и понятный статус «в работе / готово»','Рекомендации, что лучше править пакетом, а не по одной мелочи'],1],
      ['Кастом','по запросу','Без жёсткого лимита, пакет под объём',['Личный кабинет с вашим процессом согласования','Расширенный или безлимитный пул запросов (фиксируем в договоре)','Правки через ИИ + ручная доработка сложных задач','Новые страницы по готовому визуалу — в согласованном объёме','Регулярные отчёты: аптайм, скорость, метрики, что ломалось','Приоритетная очередь и слоты на созвоны по развитию','Сопровождение релизов и крупных обновлений','Можно зафиксировать гарантии по срокам ответа и закрытия','Подходит, если сайт — живой продукт, а не «поставил и забыл»'],0]]
  };
  const вкл=$('#вкладки'),пл=$('#тарифы');
  if(вкл){
    function тарифы(к,анимировать){
      const спис=ТАРИФЫ[к];
      пл.classList.toggle('one',спис.length===1);
      пл.innerHTML=спис.map((t,i)=>
        '<div class="plan'+(t[4]?' hit':'')+(анимировать&&!тихо?' pop':'')+'" style="--d:'+i*.08+'s"><h3>'+t[0]+(t[4]?'<small>'+(t[4]===1?'популярный':t[4])+'</small>':'')+'</h3>'+
        '<div class="price">'+t[1]+'</div><p>'+t[2]+'</p><ul>'+t[3].map(y=>'<li>'+y+'</li>').join('')+'</ul>'+
        '<button type="button" class="btn '+(t[4]?'btn-accent':'')+'" data-к="'+к+'" data-н="'+t[0]+'">выбрать</button></div>').join('');
      $$('.plan .btn',пл).forEach(b=>b.addEventListener('click',()=>{
        const имя=b.dataset.к===b.dataset.н||b.dataset.к==='Техническая поддержка'?b.dataset.к:b.dataset.к+' · '+b.dataset.н;
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

  появление(document);
})();
