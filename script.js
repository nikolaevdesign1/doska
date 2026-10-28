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
    if(вид==='li'){a.appendChild(цель)}else{цель.innerHTML=s.н+'<span>'+(s.с==='#'?'скоро':'открыть')+'</span>'}
    return a;
  };
  if(соц)window.СОЦСЕТИ.forEach(s=>соц.appendChild(ссылка(s,'a')));
  if(пс)window.СОЦСЕТИ.filter(s=>s.н!=='почта').forEach(s=>пс.appendChild(ссылка(s,'li')));

  /* ---------- тарифы ---------- */
  const ТАРИФЫ={
    'Логотип / айдентика':[
      ['Базовый','от 30 000 ₽','Логотип и основные правила использования',['Логотип в 2 вариантах','Цвета и шрифты','Файлы для печати и экрана'],0],
      ['Стандарт','от 80 000 ₽','Фирменный стиль для старта бизнеса',['Логотип и знак','Брендбук-памятка','Носители: визитки, соцсети','3 раунда правок'],1],
      ['Кастом','по запросу','Айдентика под вашу задачу',['Нейминг и стратегия','Полный брендбук','Сопровождение запуска'],0]],
    'Лендинг':[
      ['Базовый','от 50 000 ₽','Одностраничный сайт по готовому шаблону',['До 5 блоков','Адаптив под телефон','Форма заявки'],0],
      ['Стандарт','от 120 000 ₽','Авторский дизайн и вёрстка',['Уникальный дизайн','Анимации','Подключение аналитики','3 раунда правок'],1],
      ['Кастом','по запросу','Сложный лендинг с интеграциями',['Прототип и тексты','Интеграции с CRM','Поддержка после запуска'],0]],
    'Корпоративный сайт':[
      ['Базовый','от 150 000 ₽','Сайт-визитка компании',['До 5 страниц','Адаптивный дизайн','Простая система управления'],0],
      ['Стандарт','от 300 000 ₽','Полноценный сайт компании',['До 15 страниц','Уникальный дизайн','Раздел новостей и кейсов','SEO-основа'],1],
      ['Кастом','по запросу','Крупный проект с логикой',['Анализ и прототипирование','Личные кабинеты','Интеграции и поддержка'],0]],
    'Интернет-магазин':[
      ['Базовый','от 150 000 ₽','Магазин на готовой платформе',['Каталог и корзина','Онлайн-оплата','Адаптивный шаблон'],0],
      ['Стандарт','от 350 000 ₽','Магазин с авторским дизайном',['Уникальный дизайн','Фильтры и поиск','Интеграция с учётом','3 раунда правок'],1],
      ['Кастом','по запросу','Магазин с нестандартной логикой',['Индивидуальная разработка','Интеграции с 1С и CRM','Сопровождение'],0]]
  };
  const вкл=$('#вкладки'),пл=$('#тарифы');
  if(вкл){
    function тарифы(к,анимировать){
      пл.innerHTML=ТАРИФЫ[к].map((t,i)=>
        '<div class="plan'+(t[4]?' hit':'')+(анимировать&&!тихо?' pop':'')+'" style="--d:'+i*.08+'s"><h3>'+t[0]+(t[4]?'<small>популярный</small>':'')+'</h3>'+
        '<div class="price">'+t[1]+'</div><p>'+t[2]+'</p><ul>'+t[3].map(y=>'<li>'+y+'</li>').join('')+'</ul>'+
        '<a class="btn '+(t[4]?'btn-accent':'')+'" href="#заявка" data-т="'+к+'">выбрать</a></div>').join('');
      $$('.plan .btn',пл).forEach(a=>a.addEventListener('click',()=>{
        const s=$('#услуга');
        if(s){s.value=a.dataset.т;s.dispatchEvent(new Event('change'))}
      }));
      if(!анимировать)появление(пл);
    }
    Object.keys(ТАРИФЫ).forEach((к,i)=>{
      const t=document.createElement('button');t.className='tab'+(i?'':' on');t.textContent=к;
      t.onclick=()=>{
        if(t.classList.contains('on'))return;
        $$('.tab',вкл).forEach(e=>e.classList.toggle('on',e===t));
        сменить(пл,()=>тарифы(к,true));
      };
      вкл.appendChild(t);
    });
    тарифы(Object.keys(ТАРИФЫ)[0],false);
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
    const открыть=()=>{
      был=document.activeElement;окно.hidden=false;
      requestAnimationFrame(()=>окно.classList.add('open'));
      document.body.classList.add('lock');
      setTimeout(()=>$('input',окно).focus(),150);
    };
    const закрыть=()=>{
      окно.classList.remove('open');document.body.classList.remove('lock');
      setTimeout(()=>{окно.hidden=true},тихо?0:320);
      if(был)был.focus();
    };
    $$('[data-order]').forEach(x=>x.addEventListener('click',открыть));
    $$('[data-close]',окно).forEach(x=>x.addEventListener('click',закрыть));
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&окно.classList.contains('open'))закрыть()});
    const фо=$('#форма-окна');
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

  появление(document);
})();
