from flask import Flask, render_template, request
import spacy
import re

# all
prefix1_regex = re.compile(r"ber[\w\.-]+|di[\w\.-]+|diper[\w\.-]+|seri[\w\.-]+|me[\w\.-]+|mem[\w\.-]+|men[\w\.-]+|meng[\w\.-]+"
                           r"|menge[\w\.-]+|ter[\w\.-]+|pe[\w\.-]+"
                           r"|pem[\w\.-]+|pen[\w\.-]+|peng[\w\.-]+|penge[\w\.-]+|pende[\w\.-]+|per[\w\.-]+|se[\w\.-]+"
                           r"|ke[\w\.-]+|dwi[\w\.-]+|juru[\w\.-]+|pra[\w\.-]+|\w+-\w+", re.IGNORECASE)

# noun
prefix2_regex = re.compile(r"ke[\w\.-]+|pe[\w\.-]+|pem[\w\.-]+|peng[\w\.-]+|penge[\w\.-]+|per[\w\.-]+", re.IGNORECASE)

# verb
prefix3_regex = re.compile(r"ber[\w\.-]+|di[\w\.-]+|me[\w\.-]+|mem[\w\.-]+|meme[\w\.-]+|men[\w\.-]+"
                           r"|meng[\w\.-]+|menge[\w\.-]+|ter[\w\.-]+", re.IGNORECASE)

# adjective
prefix4_regex = re.compile(r"ter[\w\.-]+|se[\w\.-]+", re.IGNORECASE)

# compound
comp_regex = re.compile(r"|antarabangsa|olahraga|warganegara|tandatangan|jawatankuasa|bumiputera|"
                        r"|kakitangan|beritahu|pesuruhjaya|setiausaha|sukarela|kerjasama|kebolehubahan|"
                        r"|sukacita|dukacita|apabila|apakala|apahal|apalagi|bagaimana|gambar rajah|biru laut|"
                        r"|terima kasih|kuning langsat|perdana menteri|raja muda|menteri besar|profesor madya|"
                        r"|model linear|garis pusat|mata pelajaran|kertas kerja|kanta tangan|walaupun|apakata|"
                        r"|kaki ayam|buah hati|duit kopi|makan angin|pilih kasih|uji bakat|ulang tayang|temu janji|"
                        r"|hak milik|matahari|suruhanjaya|tanggungjawab|peribadi|peribahasa|dinihari|perikemanusiaan|"
                        r"|hari bulan|kadangkala|kepada|daripada|kenapa|manakala|padahal|darihal|barangkali|walhal|"
                        r"|ketidakkeruanan|dwi[\w\.-]+|juru[\w\.-]+|semi[\w\.-]+|pra[\w\.-]+|\w+-\w+",
                        re.IGNORECASE)

t = ['^dia$', '^diabetes', '^diaforesis', '^diafragma', '^diagnosis', '^diagonal', '^diagram', '^diakritik',
     '^diakronik', '^dialek', '^dialektik', '^dialektologi', '^dialisis', '^dialog', '^diam$', '^diameter', '^diarea',
     '^diaspora', '^diat', '^diatonik', '^didaktisisme', '^didih$', '^didik$', '^didikan$', '^diesel', '^diesius',
     '^diet$', '^dietetik', '^diftong', '^difusi', '^digit$', 'digital', '^diglosia', '^digniti', '^digraf', '^dikir',
     '^dikit$', '^dikotiledon', '^diari', '^dikotomi', '^diksi', '^diktat$', '^diktator$', '^diktatorial', '^dikte',
     '^diktum', '^dilema', '^diri$', '^dimensi', '^dimiti', '^dim$', '^dinamik', '^dinamisir', '^dinamisme',
     '^dinamit', '^dinamo', '^dinar$', '^dinas$', '^dinasti', '^dinding$', '^dingin$', '^dingkelik', '^dingkis$', '^dingkit',
     '^dingo', '^dini$', '^dinis', '^dinosaur', '^diod', '^dioksida', '^dipan$', '^diploma$', '^diplomasi', '^diplomat',
     '^diplomatik', '^diplopia', '^dipsomania', '^diraja', '^direksi', '^direktif', '^direktorat', '^direktori',
     '^direktur', '^dirham$', '^diris$', '^dirus', '^disakarida', '^diseksi', '^disember', '^disenteri', '^disertasi',
     '^dirgahayu', '^diuretik', '^diurnal', '^dius', '^diva', '^diversifikasi', '^diversiti', '^dividen', '^divisi',
     '^disfasia', '^disfemisme', '^disfonia', '^disfungsi', '^disgrafia', '^disharmoni', '^disimilasi', '^disinfeksi',
     '^disinfektan', '^disinflasi', '^disiplin', '^diskaun', '^disket', '^disko$', '^diskonto', '^diskriminasi',
     '^diskriminatif', '^disprosium', '^diuresis', '^disional$', '^al$', '^dividu$', '^disulfida', '^disuria', '^dito$',
     '^diskus', '^diskusi', '^dislalia', '^disopia', '^disorientasi', '^dispareunia', '^dispensari', '^dyspepsia',
     '^distaksia', '^distingtif', '^distosia', '^distribusi', '^distrik', '^diestrus', '^divisyen']

u = ['^ketimbir', '^ketimbul$', '^ketimbung', '^keting', '^ketingting', '^ketip$', '^ketipung', '^ketirah', '^ketis$',
     '^ketit', '^ketrok', '^kempuh$', '^keran$', '^ketul$', '^ketereh', '^ketiding', '^kemul', '^kereta$', '^kenari',
     '^ketitir', '^ketola', '^ketombe', '^keton$', '^ketongkeng', '^ketopong', '^ketoprak', '^ketot', '^ketoyong',
     '^ketu', '^ketua$', '^ketual', '^ketuat', '^ketuau', '^ketubah', '^ketuhar', '^ketui', '^ketuir', '^ketuk',
     '^ketum', '^ketumbak', '^ketumbar', '^ketumbe', '^ketumbi', '^ketumbit', '^ketumbu', '^ketumbuk', '^ketumpang',
     '^ketun', '^ketung', '^ketungging', '^ketup', '^ketupat', '^ketupuk', '^ketur', '^ketus', '^ketut$', '^ketutu',
     '^kewalahan', '^keweh', '^kewek', '^ketang', '^ketap$', '^ketapak', '^ketapang', '^ketapi', '^ketapik', '^ketar',
     '^ketara$', '^ketarap', '^ketat$', '^ketaton', '^ketawa$', '^ketaya', '^ketayap', '^ketegar$', '^ketek', '^ketel',
     '^ketela', '^keteng', '^ketengan', '^ketenggah', '^ketenun', '^ketepeng', '^ketepil', '^keteping', '^keter$',
     '^ketering', '^ketes', '^ketetel', '^keteter', '^keti$', '^ketiak', '^ketial', '^ketiap', '^ketiar', '^ketiau',
     '^ketik$', '^ketika', '^ketil', '^ketilang', '^ketimaha', '^kera$', '^kerabat', '^kerabit', '^kerabu', '^keracak',
     '^kempul', '^kempun', '^kempung', '^kemput', '^kemu$', '^kemucing', '^kemudi', '^kemudian', '^kemudu', '^kemuk',
     '^kesiur', '^keskul', '^kesmak', '^kesmaran', '^kesohor', '^kesomplok', '^kesot', '^kesting', '^kestul', '^kesturi',
     '^kesu', '^kesuari', '^kesuh', '^kesuk', '^kesum$', '^kesuma', '^kesumat', '^kesumba', '^kesup', '^kesusu', '^kesut',
     '^ketaban', '^ketai', '^kecai', '^ketak', '^ketakung', '^ketam', '^ketambak', '^ketampi', '^ketan', '^ketom',
     '^kenarus', '^kenas', '^kencana', '^kencang', '^kencar', '^kenceng', '^kencing', '^kensiu', '^kencong', '^kencung',
     '^kencur', '^kendaga', '^kendak', '^kendal', '^kendala', '^kendali', '^kendana', '^kendang', '^kendati', '^kendeka',
     '^kendera', '^kenderaan', '^kenderap', '^kenderi', '^kendi', '^kendik', '^kendil', '^kendiri', '^kendit', '^kendo$',
     '^kendong', '^kenduduk', '^kendung', '^kendur', '^kenduri', '^keneh', '^kenek', '^keneker', '^kenen', '^kenerak',
     '^kenerian', '^kenes', '^keng$', '^kengkalung', '^kengkang', '^kengkatuk', '^kengkeng', '^kengkunang', '^kengwa',
     '^kenik', '^kenikah', '^kening', '^kenini', '^kenit', '^kenjah', '^kenjar', '^kenjing', '^kenkacang', '^kenohong',
     '^kenop', '^kensel', '^kental', '^kentala', '^kentang', '^kentar', '^kentara', '^kentung', '^kentut', '^kenung', '^kenya',
     '^kenyah', '^kenyal', '^kenyam', '^kenyang', '^kenyap', '^kenyat', '^kenyek', '^kenyi', '^kenyir', '^kenyit', '^kenur',
     '^kenyut', '^keok', '^keong', '^kep$', '^kepada', '^kepah', '^kepai', '^kepak', '^kepaksa', '^kepal$', '^kepala',
     '^kepalang', '^kepam', '^kepang', '^kepar', '^keparat', '^kepari', '^kepau', '^kepaya$', '^kepayang', '^kepayat',
     '^kepecong', '^kepek', '^kepencong', '^kepeng', '^kepepet', '^keperancak', '^kepergok', '^kepet$', '^kepetang',
     '^kepiat', '^kepik', '^kepil', '^kepincut', '^kepinding', '^keeping$', '^kepingin', '^kepinis', '^kepinjal', '^kepir$',
     '^kepiran', '^kepis$', '^kepit$', '^kepiting', '^kepleset', '^kepoh', '^kepok', '^kepol', '^kepompong', '^keponakan',
     '^kepong$', '^kepot', '^keprak', '^kepruk', '^kepudang', '^kepuh', '^kepuk', '^kepul$', '^kepulan', '^kepulaga', '^kenidai',
     '^kepundan', '^kepundung', '^kepung$', '^kepur$', '^kepurun', '^kepuyuk', '^keracap', '^keraeng', '^kerah$', '^kerai', '^kerajang',
     '^kerajat', '^kerak$', '^kerakah', '^kerakal', '^kerakap', '^keram$', '^kerama$', '^keramas', '^keramat$', '^kerambil', '^kerambit',
     '^kerampang', '^keramunting', '^keran$', '^kerana', '^kerancang', '^keranda', '^kerandang', '^kerandut', '^kerang$', '^kerangka$',
     '^kerangkai', '^kerangkang', '^kerangkeng', '^kerangking', '^kerana$', '^keranjang', '^keranji', '^keranta$', '^kerantai', '^kerantu$',
     '^kerantung', '^keranyah', '^kerap$', '^kerapah', '^kerapan', '^kerapis', '^kerapu', '^keras$', '^kerat', '^keratabasa',
     '^kertang', '^keratau', '^keratin', '^kerating', '^keraton', '^kerau', '^kerawai', '^kerawak', '^kerawang', '^kerawat',
     '^kerawit', '^kerayung', '^kerbang', '^kerbat', '^kerbau', '^kerbuk', '^kercap', '^kercau', '^kercing', '^kercip',
     '^kercit', '^kercup', '^kercut', '^kerdak', '^kerdam', '^kerdum', '^kerdan', '^kerdil', '^kerdip', '^kerdom',
     '^kerdut', '^kerebok', '^kereceng', '^keredak', '^keredas', '^keredep', '^keredong', '^kerejut', '^kerek', '^kepialu',
     '^kerekau', '^kereket', '^kerekot', '^kerekup', '^keremak', '^keremangka', '^keremi', '^keremot', '^kerempagi', '^kerempung',
     '^keremut', '^keren', '^kerenah', '^kerenam', '^kerenan$', '^kerencang', '^kerencung', '^kereng$', '^kerengga$',
     '^kerengkam', '^kerengkek', '^kerengkiang', '^kerengseng', '^kereniok', '^kerenting', '^kerenyeh', '^kerenyet', '^kerenyot',
     '^kerepeh', '^kerepek', '^kerepes', '^kerepot', '^kerepuh', '^keresek', '^kereseng', '^keresepese', '^keleseh', '^keresoi',
     '^keresot', '^keret$', '^kereta$', '^keretan', '^keretek', '^keretot', '^keretuk', '^keretup', '^keri$', '^keria$',
     '^keriak', '^kerian$', '^keriang', '^keriap', '^keriat', '^keriau', '^kerical', '^kericau', '^kericik', '^keridas',
     '^keridau', '^keridik', '^kerih', '^kerik$', '^kerikal', '^kerikam', '^kerikil', '^kerikit', '^keriling', '^kerinan',
     '^kerincing', '^kering', '^keringat', '^kerinjal', '^kerinjang', '^kerinjing', '^kerintil', '^kerinting', '^kerip$',
     '^keris$', '^kerisi$', '^kerisik', '^kerising', '^keritik', '^keriuk', '^keriut', '^keriang', '^keriut', '^kerja$',
     '^kesateria', '^kesed', '^kesek', '^kesel', '^keselak', '^keseleo', '^kesenai', '^keseng', '^keser', '^keset', '^kesian',
     '^kesiap', '^kesidang', '^kesih', '^kesik', '^kesima', '^kesimbukan', '^kesinan', '^kesing', '^kesinga', '^kesip',
     '^kerjang$', '^kerjantara', '^kerjap', '^kerjasama', '^kerjaya', '^kerjung', '^kerkah', '^kerkak', '^kerkap', '^kerkau',
     '^kerki', '^kerkop', '^kerkuk', '^kerkum', '^kerkup', '^kerlap', '^kerlik', '^kerling', '^kerlip', '^kelip$',
     '^kerluk', '^kerlung', '^kermah', '^kerman$', '^kermanici', '^kermi$', '^kermian', '^kermi$', '^kernai', '^kerenam',
     '^kernap', '^kernet', '^kernu', '^kernyam', '^kernyat', '^kernyau', '^kernyih', '^kernying', '^kernyit', '^kernyut',
     '^kero$', '^kerobak', '^kerobek', '^kerobok', '^kerocok', '^kerodak', '^keroh$', '^keroi', '^kerok$', '^keroket',
     '^kerokot', '^keron$', '^keroncang', '^keroncong', '^keroncor', '^kerongkong', '^kerongsang', '^kerontang', '^kerop$', '^keropak',
     '^keropas', '^keropeh', '^keropeng', '^keropok', '^keropong', '^keropos', '^kerosek', '^kerosin', '^kerosok', '^kerosong',
     '^kempas', '^kempeitai', '^kempek', '^kempelang', '^kempelangan', '^kempen', '^kempening', '^kemperas', '^kempiluh',
     '^kempuh', '^kempul', '^kempun', '^kampung', '^kemput', '^kemu$', '^kemucing', '^kemudi$', '^kemudian', '^kemudu',
     '^kemuk', '^kemul', '^kemumu', '^kemuncup', '^kemung', '^kemungkus', '^kemuning', '^kemunting', '^kemuruk', '^kemut',
     '^kemutul', '^ken$', '^kena$', '^kenal$', '^kenalpot', '^kenan$', '^kenang$', '^kenanga', '^kenap$', '^kenapa',
     '^kebab$', '^kebabal', '^kebah', '^kebal', '^kebam', '^keban$', '^kebarung', '^kebas$', '^kebasi', '^kebat', '^kerit',
     '^kebaya$', '^kebayan', '^kebayang', '^kebek', '^kebel$', '^kebelai', '^kebil', '^keboba', '^kebuk', '^kerenggamunggu',
     '^kebun', '^kebur$', '^keburu', '^kebut', '^kecah', '^kecai', '^kecak', '^kecam$', '^kecambah', '^kecamuk',
     '^kecap$', '^kecapi', '^kecar', '^keceh', '^kecek', '^kecele', '^keceng', '^kecepek', '^kecer', '^kecewa', '^kempis',
     '^keloyang', '^kelu', '^keluai', '^keluak', '^keluan$', '^keluang$', '^keluangsa', '^keluar', '^keluarga', '^keluat',
     '^keci$', '^keciak', '^kecibak', '^kecibeling', '^kecicak', '^kecil', '^kecimpung', '^kecimus', '^kecindan', '^kecipak',
     '^kecipuk', '^keciut', '^kecoh', '^kecok', '^kecong', '^kecor', '^kecu$', '^kecuak', '^kecuali', '^kecubung',
     '^kecuh', '^keculun', '^kecundang', '^kecung', '^kecup', '^kecur', '^kecut', '^kedabu', '^kedada$', '^kedadah',
     '^kedadak', '^kedah', '^kedai', '^kedak', '^kedal$', '^kedaluwarsa', '^kedamba', '^kedampang', '^kedana', '^kedang$',
     '^kedanga$', '^kedangkang', '^kedangsa', '^kedap', '^kedarah', '^kedari', '^kedasih', '^kedau$', '^kedaung', '^kedayan',
     '^kededek', '^kedek$', '^kedekai', '^kedeking', '^kedekut', '^kedelai', '^kedemah', '^kedemat', '^kedemi', '^kedempung',
     '^kedemut', '^kedengkang', '^kedengkik$', '^kedengking', '^kedenuk', '^keder$', '^kedera', '^kederang', '^kedewas', '^kedi$',
     '^kedidi', '^kedih', '^kedik', '^kedip', '^kedok$', '^kedombak', '^kedondong', '^kedongkok', '^kedorong', '^kedu$',
     '^keduduk', '^keduk', '^kedul', '^kedunak', '^kedut$', '^keembung', '^kehek', '^kehel', '^keher', '^kei$', '^kelempai',
     '^kejai', '^kejal', '^kejam$', '^kejamas', '^kejan$', '^kejang',  '^kejap', '^kejar', '^kejat', '^kempu', '^kelengkang',
     '^kejeblos', '^kejen', '^keji$', '^kejip', '^kejora', '^kejur$', '^kejut$', '^kek$', '^kekabu', '^kekah', '^kempit',
     '^kekaki', '^kekal$', '^kekalu', '^kekam', '^kekandi', '^kekang', '^kekapal', '^kekapas', '^kekar$', '^kekara', '^kelentungi',
     '^kekaras,' '^kekaras,' '^kekas', '^kekat', '^kekau', '^kekeh', '^kekek', '^kekel', '^kekeng', '^kekepuk', '^kekwa',
     '^keker', '^keruh', '^kekgi', '^keki$', '^kekili', '^kekisi', '^kekmo', '^keknya', '^kekok', '^kekerkekong',
     '^kekot', '^kekpong', '^kekudung', '^kekuma', '^kekunci', '^kelab$', '^kelabat', '^kelabau', '^kelabu$', '^kelontang',
     '^kelabung', '^kelabut', '^keladak', '^keladan', '^keladau', '^keladi', '^kelah$', '^kelahi', '^kelai$', '^kelain',
     '^kelain', '^kelak$', '^kelakar', '^kelakeling', '^kelalang', '^kelalap', '^kelalut', '^kelam$', '^kelama', '^kelamai',
     '^kelambir', '^kelambit', '^keluang', '^kelambu', '^kelambur', '^kelamin', '^kalamkari', '^kelampung', '^kelamun',
     '^kelang$', '^kelanggar', '^kelangkang', '^kelanit', '^kelanjar', '^kelantan$', '^kelantang', '^kelap$', '^kelapa', '^kelapung',
     '^kelap$', '^kelapa$', '^kelapung', '^kelar$', '^kelarah', '^kelarai', '^kelari$', '^kelaring', '^kelas$', '^kelasa$',
     '^kelasak', '^kelasi', '^kelat$', '^kelatu', '^kelawai', '^kelawar', '^kelawat', '^kelayang', '^kelayar', '^kelayau',
     '^kelayu', '^keldai', '^kelebak', '^kelebang', '^kelebat', '^kelebek', '^kelebet', '^kelebi', '^kelebok', '^kelebu', '^kelana',
     '^kelebu$', '^kelebuk', '^kelebut', '^kelecat', '^keleceh', '^kelecek', '^kelecus', '^keledang', '^keledar', '^keledek',
     '^keledi', '^kelek$', '^kelekati', '^kelekatu', '^kelekatu', '^kelekik', '^kelelot', '^kelem$', '^kelemata', '^kelemata',
     '^kelemata', '^kelemayar', '^kelemayuh', '^kelembahang', '^kelembai', '^kelembak', '^kelemban', '^kelemek', '^kelemoyang',
     '^kelemping', '^kelemuak', '^kelemumur', '^kelemut', '^kelencong', '^kelendara', '^keleneng', '^kelengar$', '^kelenggara',
     '^kelengkiak', '^kelengkuk', '^kelening', '^kelenjar', '^kelentang', '^kelenteng', '^kelentit', '^kelentom', '^kelentong',
     '^kelentung', '^kelenung', '^kelenut', '^kelenyuk', '^kelepai', '^kelepak', '^kelepal', '^kelepek', '^kemesak',
     '^kelepet', '^kelepik', '^kelepir', '^kelepit', '^kelepot', '^kelepuk', '^kelepung', '^kelepur', '^keler$', '^kelereh',
     '^kelerek', '^kelereng', '^kelesa$', '^kelesah', '^keleseh', '^kelesek', '^keletah', '^keletak', '^keletang', '^keletap',
     '^keletar', '^keletik', '^keleting', '^keletuk', '^keletung', '^kelewak', '^kelewang', '^kelewar', '^kelewat', '^keleweh',
     '^kelewer', '^keli$', '^kelian', '^keliar', '^kelibang', '^kelibat', '^kelicap', '^kelici', '^keliding', '^kelido',
     '^kelih', '^kelik$', '^kelikah', '^kelikih', '^keliki$', '^kelikir', '^keliling', '^kelilip', '^kelim$', '^kelima',
     '^kelimun', '^kelimut', '^kelinang', '^kelinci', '^kelindan', '^keling$', '^kelingsir', '^kelinjat', '^kelintar', '^kelinting',
     '^kelip$', '^kerlip', '^kelipar', '^kelipat', '^kelimun', '^kelimun', '^kelimut', '^kelinang', '^kelimun', '^kelinci',
     '^kelindan', '^keling$', '^kelingsir', '^kelinjat', '^kelintar', '^kelinting', '^kelip', '^kerlip', '^kelindan', '^kelipar',
     '^kelipar', '^kelipat', '^kelipuk', '^kelir$', '^keliru', '^kelis$', '^kelisa', '^kelit$', '^keliti$', '^kelitik',
     '^kelkah', '^kelmarin', '^kelobak', '^kelobot', '^kelocak', '^kocak', '^kelodak', '^kelodan', '^keloi', '^kempang',
     '^kelok$', '^kelokok', '^kelola', '^keloloh', '^kelok$', '^kelolong', '^kelom$', '^kelombeng', '^kelompang', '^kelompok',
     '^kelompong', '^kelon$', '^kelona', '^keloneng', '^kelonet', '^kelong$', '^kelongkang', '^kelongkong', '^kelongsong',
     '^kelontong', '^kelonyor', '^kelop$', '^kelopak', '^kelorah', '^kelorak', '^kelos', '^kelotak', '^keloyak', '^kemis',
     '^kerosot', '^kerotok', '^kerotot', '^keroyok', '^kerpai', '^kerpak', '^kerpas', '^kerpik', '^kerpis', '^kerpuk',
     '^kerpus', '^kersai', '^kersak', '^kersang', '^kersani', '^kersau', '^kersik', '^kersing', '^kersip', '^kersuk',
     '^kersul', '^kertah', '^kertak', '^kertang', '^kertap', '^kertas', '^kertatuk', '^kertau', '^kertik', '^kerting',
     '^kertip', '^kertuk', '^kertung', '^kertup', '^kertus', '^keruan', '^kerubian', '^kerubung', '^kerubut', '^kerucut',
     '^kerudung', '^kerudut', '^keruh$', '^keruing', '^keruit', '^keruk', '^kerukup', '^kerukut', '^kerul', '^keruma',
     '^kerumit', '^kerumuk', '^kerumun', '^kerumus', '^kerun$', '^kerunas', '^kerung', '^keruntang', '^kerunting', '^keruntul',
     '^keruntum', '^keruntung', '^kerunyut', '^kerup$', '^kerap$', '^keruping', '^kerusi', '^kerusut', '^kerut$', '^kerutak',
     '^kerutis', '^kerutu$', '^kerutuk', '^kerutung', '^kerutup', '^kerutus', '^kerotot', '^kerutut', '^keruyuk', '^keruyup',
     '^kesa$', '^kesah', '^keluh', '^kesak', '^kesal', '^kesam$', '^kesambi', '^kesami', '^kesan$', '^kesandung', '^kes$',
     '^kesang$', '^kesangka', '^kesangsang', '^kesap', '^kesasar', '^kesat', '^keluh$', '^keman$', '^kemas$', '^kemi$',
     '^kelubi', '^kelubu$', '^kelubung', '^keluburan', '^keloi', '^keluih', '^keluik', '^keluk$', '^kelukup', '^kelukur',
     '^keluli', '^kelulu$', '^kelulut', '^kelum$', '^kelumbai', '^kelumit', '^kelumpang', '^kelumun', '^kelun$', '^keluna',
     '^kelung', '^kelupas', '^kelur$', '^keluron', '^keluruk', '^kelurut', '^kelus$', '^kelusuh', '^kelusuk', '^kelut$',
     '^kelutum', '^keluyu$', '^keluyuk', '^keluyur', '^kelvin', '^kem$', '^kema$', '^kemab', '^kemaca', '^kemak', '^kempa$',
     '^kemal$', '^kemala$', '^kemalau', '^kemam$', '^kemamam$', '^kemamang', '^kemamar', '^kemanakan', '^kemancar', '^kemancung',
     '^kemang$', '^kemangi', '^kemangur', '^kemani', '^kemantan', '^kemanten', '^kemantu', '^kemap', '^kemarau', '^kemaruk',
     '^kemat', '^kematu', '^kemawan', '^kemayuh', '^kembah', '^kembal$', '^kembali', '^kemban$', '^kembang', '^kembar$',
     '^kembara', '^kembayat', '^kembera', '^kembiang', '^kembili,' '^kembiri', '^kemboja', '^kembol$', '^kembola', '^kembu$',
     '^kembuk', '^kembung', '^kembur', '^kembut', '^kemdian', '^kemeh', '^kemeja$', '^kemejan', '^kemeli$', '^kemeling',
     '^kemelut', '^kememeh', '^kemendang', '^kemendelam', '^kemendur', '^kemengu', '^kementam', '^kemenyan', '^kemera',
     '^kemesit', '^kemetot', '^kemih', '^kemik', '^kemili', '^kemin', '^keminting', '^kemirau', '^kemiri', '^kemit',
     '^kemofisiologi', '^kemosintesis', '^kemotaksis', '^kemoterapi', '^kemotropisme', '^kerepas',]

v = ['^berat', '^beban$', '^bebar', '^bebas', '^bebel', '^berapa$', '^beras$', '^besi', '^bersih', '^belalang', '^beca',
     '^becah', '^becak', '^belut', '^bedah', '^bedak', '^bedal', '^beg', '^begawan', '^begini', '^begitu', '^bekas',
     '^bela$', '^belacan', '^belacak', '^belah', '^belakang', '^belalai', '^belang', '^belangkas', '^belas$', '^belasah',
     '^belek', '^belerang', '^beli', '^belia', '^belian', '^belit', '^belok', '^belum', '^belot', '^benam', '^benar',
     '^benda', '^bendahara', '^bendahari', '^bendera', '^bengkak', '^bengkel', '^bengkok', '^benih$', '^benjol', '^belajar$'
     '^benteng', '^bentuk', '^benua', '^berani', '^bernas', '^beri', '^berita', '^berkat', '^bersih', '^bersin',
     '^berudu', '^beruk', '^berus$', '^besar$', '^beta$', '^betapa', '^bentang', '^betik', '^betina', '^bentuk', '^betul$',
     '^beku$', '^betung', '^beliau', '^benci', '^bentang', '^beruang', '^bentung', '^belajaran$']

w = ['^men$', '^merah$', '^merak', '^merapu', '^medak', '^medal', '^medan', '^media', '^mendung', '^median', '^merdu$',
     '^meleset', '^memang', '^menang$', '^menara$', '^menantu$', '^mentah', '^mentega', '^mentang', '^menteri',
     '^mentol', '^megah$', '^menu$', '^mentua', '^merana$', '^memerang', '^merdeka', '^mereka', '^meriam' '^mesej',
     '^mesyuarat', '^mentah', '^meter', '^mewah$', '^meja$', '^mesra$', '^mesti$', '^mentor', '^Melayu', '^mena$',
     '^meskin', '^mesin', '^meschooling$', '^megang$', '^medium$']

x = ['^pecah', '^pecat', '^pecut', '^pedang', '^pedas', '^pedih', '^peduli', '^pegang', '^pegawai', '^peguam', '^pegun',
     '^pejam', '^pek$', '^peka', '^pekak', '^pekan', '^pekasam', '^pekat', '^pekerti', '^peket', '^pekin', '^pelan', '^pelantar',
     '^pelihara', '^pelik', '^pelita', '^peluang', '^peluh', '^peluk', '^peluru', '^pen$', '^pernah', '^penalti',
     '^penawar', '^pencen', '^penyek', '^pencil', '^pendam', '^pendap$', '^pendek$', '^pengantin', '^pengaruh', '^pening',
     '^penjara', '^pensil', '^pentas', '^penting', '^penuh$', '^penyu', '^penyapu', '^pepatah', '^perabot', '^perahu',
     '^peram', '^perang', '^perangai', '^peranti', '^perasan', '^percaya', '^percit', '^percuma', '^perdana',
     '^perencah', '^pergi', '^peribadi', '^peribumi', '^perigi', '^perihal', '^periksa', '^perinci', '^perintah',
     '^perisai', '^perit', '^periuk', '^perkakas', '^perkara', '^perkasa', '^perlahan', '^perli$', '^perlu$', '^permai$',
     '^permata', '^permit', '^pernah', '^pertama', '^perut', '^pesan', '^pesat', '^pesawat', '^pesong', '^pesta',
     '^petak', '^petaka', '^petang', '^peti', '^petik', '^petir', '^pejabat', '^pelepah', '^penat', '^peti', '^perang',
     '^perak$', '^perempuan', '^perisa', '^permatang', '^peta$', '^petai', '^perkara', '^peranan', '^perti$', '^perluan$']

y = ['^perse$', '^se$', '^ses$', '^sesnya$' '^sebab$', '^sebar', '^sebat', '^seberang', '^sebut', '^sedang', '^sedap',
     '^sedut', '^segak', '^segala', '^segan', '^segar', '^segera', '^segi', '^segitu', '^segmen', '^sejadah', '^sejak',
     '^sejahtera', '^sejat', '^sejuk', '^sekat', '^sekolah$', '^seks', '^seksa', '^seksi', '^seksual', '^sektor',
     '^sekular', '^sekutu', '^selalu', '^selam', '^selamat', '^selamba', '^selang', '^selat', '^selempang', '^selekoh',
     '^selendang', '^selera', '^selerak', '^selesa', '^selesema', '^selidik', '^selimut', '^selipar', '^selisih',
     '^seliuh', '^seloka', '^seluar', '^seludup', '^selut', '^semai', '^semak$', '^semakin', '^semangat', '^semarak',
     '^sembahyang', '^sembang', '^sembelit', '^sembuh', '^sembunyi', '^semenjak', '^sementara', '^semester', '^seminar',
     '^sempadan', '^sempat', '^sempena', '^sempit', '^semua', '^semut', '^sen$', '^senam', '^senang', '^senarai',
     '^sendi$', '^sendu', '^senduk', '^sengaja', '^sengat', '^sengau', '^seni', '^senior', '^senja', '^senjata',
     '^sensitif', '^sensor', '^sentak', '^sentap', '^sentiasa', '^senyap', '^senyum', '^sepah', '^sepak', '^sepana',
     '^sepi', '^serah', '^serai', '^seram', '^serang', '^serap', '^serat', '^serba', '^serbu', '^serbuk', '^seriau',
     '^sering', '^serius', '^serong', '^serta', '^seru', '^servis', '^server', '^sesak', '^sesat', '^sesi', '^set$',
     '^setia$', '^setuju', '^sewa', '^sedih', '^sedu', '^sejarah', '^selesai', '^selit', '^sembah', '^senat', '^sewa$',
     '^senonoh', '^seperti', '^serik', '^setem', '^senaria', '^seperti', '^seronok$', '^sekarang', '^sem$', '^in$',
     '^sedar', '^sederhana', '^sedia$', '^sekitaran$', '^seri$', '^ktu$']

z = ['^teater', '^tebal', '^tebang', '^tebas', '^tebing', '^tebu', '^tebuan', '^tebuk', '^tebus', '^teduh', '^tedung',
     '^tegang', '^tegap', '^tegar', '^tegas', '^teguh', '^tegun', '^tegur', '^teh', '^teka', '^tekad', '^tekak',
     '^tekap', '^teki', '^teknologi', '^teks$', '^teksi', '^tekstil', '^tekstur', '^tekun', '^teladan', '^telaga',
     '^telan', '^telanjang', '^telefon', '^telekung', '^televisyen', '^telinga', '^teliti', '^telor', '^teluk',
     '^telus', '^tema', '^teman', '^tembaga', '^tembak', '^tembakau', '^tembikai', '^tembikar', '^tembok', '^tepas',
     '^tempah', '^tempang', '^tempat', '^tempo', '^tempoh', '^tempuh', '^tempurung', '^temu', '^tenaga', '^tenang',
     '^tendas', '^tendensi', '^tengah', '^tenggiling', '^tengik', '^tengku', '^tengkuk', '^tengku', '^tenis', '^tetap',
     '^tentang', '^tentatif', '^tentera', '^tenteram', '^tentu$', '^tenun$', '^tenung', '^tenusu', '^teori', '^tepak',
     '^tepat', '^tepi', '^tepu$', '^tepuk', '^tepung', '^tepus$', '^terai', '^terajang', '^teraju', '^terang', '^tem$',
     '^teras', '^teratai', '^terbang', '^terbit', '^terima', '^terjun', '^terma$', '^termal', '^terminal', '^terap$',
     '^termometer', '^tetikus', '^tewas', '^tengkorak', '^tegak', '^tekan', '^telah', '^telunjuk', '^tendang', '^terus',
     '^teroka', '^teropong', '^terowong', '^tertib', '^teruk', '^terumbu', '^terung$', '^terup', '^tetamu',
     '^temenggung', '^tenggelam', '^terapi', '^tension', '^tepuk$', '^termos',]

a = t + u + v + w + x + y + z

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)


@app.route('/landing')
def index():
    return render_template("index.html")


@app.route('/')
def landing():
    return render_template("about.html")


@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':
        choice = request.form['taskoption']
        if choice == 'all':
            rawtext = request.form['rawtext']
            result = prefix1_regex.findall(rawtext)
            remove = str.maketrans('', '', '.,;:?!$^&*()_=+/<>[]{}@#%')
            result1 = [s.translate(remove) for s in result]
            print(result1)
            comp = re.compile('|'.join(a))
            results = [re.sub(comp, '', i).strip() for i in result1]
            print(results)
            info = "ALL: " \
                   "This option will display all of the complex words regardless of the types."

        elif choice == 'noun':
            rawtext = request.form['rawtext']
            result = prefix2_regex.findall(rawtext)
            remove = str.maketrans('', '', '.,;:?!$^&*()_=+/<>[]{}@#%')
            result1 = [s.translate(remove) for s in result]
            print(result1)
            comp = re.compile('|'.join(a))
            results = [re.sub(comp, '', i).strip() for i in result1]
            print(results)
            info = "NOUN: " \
                   "This option will display all complex words associated with noun. " \
                   "Complex words will be consider as noun if it starts with peN-, pe-, peR-, ke-, juru-"

        elif choice == 'verb':
            rawtext = request.form['rawtext']
            result = prefix3_regex.findall(rawtext)
            remove = str.maketrans('', '', '.,;:?!$^&*()_=+/<>[]{}@#%')
            result1 = [s.translate(remove) for s in result]
            print(result1)
            comp = re.compile('|'.join(a))
            results = [re.sub(comp, '', i).strip() for i in result1]
            print(results)
            info = "VERB: " \
                   "This option will display all complex words associated with verb. " \
                   "Complex words will be consider as verb if it starts with meN-, di-, beR-, ter-, mempeR-, dipeR-"

        elif choice == 'adjective':
            rawtext = request.form['rawtext']
            print(rawtext)
            result = prefix4_regex.findall(rawtext)
            print(result)
            remove = str.maketrans('', '', '.,;:?!$^&*()_=+/<>[]{}@#%')
            result1 = [s.translate(remove) for s in result]
            print(result1)
            comp = re.compile('|'.join(a))
            results = [re.sub(comp, '', i).strip() for i in result1]
            print(results)
            info = "ADJECTIVE: " \
                   "This option will display all complex words associated with adjective. " \
                   "Complex words will be consider as adjective if it starts with ter- & se-"

        elif choice == 'compound':
            rawtext = request.form['rawtext']
            result = comp_regex.findall(rawtext)
            remove = str.maketrans('', '', '.,;:?!$^&*()_=+/<>[]{}@#%')
            result1 = [s.translate(remove) for s in result]
            print(result1)
            comp1 = re.compile('|'.join(a))
            results = [re.sub(comp1, '', i).strip() for i in result1]
            print(results)
            info = "COMPOUND WORDS: " \
                   "This option will display all complex words associated with compound words. " \
                   "Complex words will be consider as compound words if it contains hyphen (-) between two words. " \
                   "In certain cases, two words might merged together without any hyphen (example: kerjasama which is a " \
                   "combination between two words kerja + sama)."

    return render_template("index.html", rawtext=rawtext, info=info, results=results)


if __name__ == '__main__':
    app.run(debug=True)
