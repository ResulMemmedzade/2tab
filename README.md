2Tab — İkinci Əl Kitab Marketplace

2Tab, istifadəçilərin ikinci əl kitabları alıb-sata bildiyi müasir marketplace platformasıdır. Layihənin əsas məqsədi istifadəçilərə artıq istifadə etmədikləri kitabları asanlıqla satışa çıxarmaq və münasib qiymətə ikinci əl kitablar tapmaq imkanı yaratmaqdır.

Platforma Django üzərində hazırlanıb və real marketplace tətbiqinin əsas komponentlərini özündə birləşdirir: istifadəçi autentifikasiyası, kitab elanları, axtarış və filtrasiya, mesajlaşma, favoritlər, istifadəçi dashboard-u və admin paneli.

Layihənin məqsədi

Kitab almaq istəyən istifadəçilər üçün yeni kitablarla yanaşı daha münasib qiymətə ikinci əl kitabları tapmaq imkanı yaratmaq.

2Tab vasitəsilə istifadəçi:

Kitablarını satışa çıxara bilər
Digər istifadəçilərin elanlarına baxa bilər
Kitabları axtara və filtr edə bilər
Elan sahibinə mesaj göndərə bilər
Maraqlı kitabları favoritlərə əlavə edə bilər
Öz elanlarını və hesabını idarə edə bilər
Əsas funksiyalar
İstifadəçi sistemi
İstifadəçi qeydiyyatı
Login / Logout
Şifrə dəyişdirmə
İstifadəçi profili
Profil şəkli
İstifadəçi dashboard-u
İstifadəçinin öz elanlarını idarə etməsi
Kitab elanları

İstifadəçilər yeni kitab elanı yarada bilirlər.

Elanlarda əsas məlumatlar:

Kitab adı
Müəllif
Qiymət
Kitabın vəziyyəti
Kateqoriya
Açıqlama
Şəkil
Satıcının məlumatları

İstifadəçilər öz elanlarını daha sonra dəyişdirə və silə bilirlər.

Axtarış və filtrasiya

Kitabların daha rahat tapılması üçün:

Kitab adına görə axtarış
Kateqoriyaya görə filtr
Qiymət aralığı
Digər uyğun filterlər

istifadə edilə bilər.

Favoritlər

İstifadəçilər bəyəndikləri kitabları favoritlərə əlavə edə bilirlər.

Bu kitablar daha sonra istifadəçinin dashboard-u üzərindən rahat şəkildə tapıla bilər.

Mesajlaşma sistemi

İstifadəçilər kitab elanı ilə maraqlandıqda satıcı ilə birbaşa əlaqə saxlaya bilirlər.

Mesajlaşma sistemi:

Inbox
Mesaj göndərmə
Mesaj qəbul etmə
Oxunmamış mesaj sayı
Mesajların oxunmuş kimi işarələnməsi

kimi funksiyaları dəstəkləyir.

Admin panel

Platformanın idarə olunması üçün Django Admin istifadə olunur.

Admin vasitəsilə:

İstifadəçiləri idarə etmək
Kitab elanlarını idarə etmək
Kateqoriyaları idarə etmək
İstifadəçi məlumatlarını yoxlamaq
Platformadakı digər məlumatları idarə etmək

mümkündür.

Texnologiyalar

Layihənin backend hissəsində əsasən Python və Django istifadə olunub.

Backend
Python
Django
Django ORM
Django Authentication
Django Templates
ASGI
Daphne
Database

Layihənin development mərhələsində:

SQLite

istifadə olunur.

Production mühitində isə daha böyük layihələr üçün PostgreSQL kimi relational database istifadə edilə bilər.

Frontend
HTML5
CSS3
JavaScript
Django Template Language
Responsive Design
Digər texnologiyalar
Redis / cache
WhiteNoise
Git
GitHub
Nginx
SSL/TLS
Daphne
Layihə strukturu

Layihə Django-nun modular strukturundan istifadə edir.


