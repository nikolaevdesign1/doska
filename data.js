/* Материалы ленты и соцсети. Чтобы добавить материал – допишите объект в список.
   тип – кейсы | статьи | заметки (по нему работают фильтры), т – заголовок, ист – источник (подпись),
   ссылка – куда ведет плитка, картинка – обложка (файл в assets), видео и постер – для плитки с видео,
   свет:1 – светлая обложка (темный текст), секрет:1 – закрытый кейс (без ссылки),
   награды:[{п:'подпись сверху',т:'главное слово',г:'год',цвет:'сер'|'бронза'|'золото'|'фиолет'}] */
window.ЛЕНТА = [
  {тип:'кейсы',т:'Maryjoy – скоро расскажем',ист:'под NDA',секрет:1,картинка:'/assets/cases/maryjoy.webp'},
  {тип:'статьи',т:'Месяц разборов в «Дизайн будке»: что чаще всего ломает портфолио',ист:'dsgners',ссылка:'https://dsgners.ru/nikolaev_design/166098-mesyats-razborov-v-dizayn-budke-chto-chasche-vsego-lomaet-portfolio',картинка:'/assets/articles/razbory.webp',обложка:1},
  {тип:'кейсы',т:'Chris Williams Art Gallery – сайт и награда на Behance',ист:'Behance',ссылка:'https://www.behance.net/gallery/257145321/Chris-Williams-Art-Gallery',видео:'/assets/cases/chris.mp4',постер:'/assets/cases/chris-poster.webp',награды:[{п:'награда',т:'Behance',цвет:'золото'}]},
  {тип:'статьи',т:'Проекты, от которых я отказываюсь, и как говорю клиенту «нет»',ист:'dsgners',ссылка:'https://dsgners.ru/nikolaev_design/108384-proektyi-ot-kotoryih-ya-otkazyivayus-i-kak-govoryu-klientu-net',картинка:'/assets/articles/otkaz.webp',обложка:1},
  {тип:'кейсы',т:'LITT – интернет-магазин в Дубае',ист:'dprofile',ссылка:'https://dprofile.ru/case/191937/litt-ecommerce',картинка:'/assets/cases/litt.webp'},
  {тип:'статьи',т:'Мидл или сеньор: чем на деле отличается уровень дизайнера',ист:'dsgners',ссылка:'https://dsgners.ru/nikolaev_design/102613-midl-ili-senor-chem-na-dele-otlichaetsya-uroven-dizaynera',картинка:'/assets/articles/midl.webp',обложка:1},
  {тип:'кейсы',т:'Atelier #40 – система для модного журнала в ОАЭ',ист:'dprofile',ссылка:'https://dprofile.ru/case/171057/atelier-40',картинка:'/assets/cases/atelier.webp',свет:1},
  {тип:'статьи',т:'Figma MCP + Claude: как я собираю кейсы и документацию прямо из макетов',ист:'dsgners',ссылка:'https://dsgners.ru/nikolaev_design/94512-figma-mcp-claude-kak-ya-sobirayu-keysyi-i-dokumentatsiyu-pryamo-iz-maketov',картинка:'/assets/articles/figma-mcp.webp',обложка:1},
  {тип:'кейсы',т:'TUD – интернет-магазин',ист:'dprofile',ссылка:'https://dprofile.ru/case/160079/tud-e-commerce',видео:'/assets/cases/tud.mp4',постер:'/assets/cases/tud-poster.webp',награды:[{п:'награда',т:'Behance',цвет:'золото'}]},
  {тип:'кейсы',т:'pyn.ai – мобильное приложение',ист:'dprofile',ссылка:'https://dprofile.ru/case/188243/pynai-app-design',картинка:'/assets/cases/pyn.webp'},
  {тип:'статьи',т:'Grok bot как целая команда: кого он мне заменил',ист:'dsgners',ссылка:'https://dsgners.ru/nikolaev_design/89839-grok-bot-kak-tselaya-komanda-kogo-on-mne-zamenil',картинка:'/assets/articles/grok-bot.webp',обложка:1}
];

window.СОЦСЕТИ = [
  {н:'dprofile',п:'Портфолио',с:'https://dprofile.ru/nikolaev_design1',внешняя:1},
  {н:'Дизайн будка',п:'Телеграм канал',с:'https://t.me/design_budka',внешняя:1},
  {н:'dsgners',п:'Медиа',с:'https://dsgners.ru/nikolaev_design',внешняя:1}
];
