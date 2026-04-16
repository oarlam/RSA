ІНСТРУКЦІЯ ДО ЗАПУСКУ

1. перейти у відповідну папку і запустити файл server.py
<img width="899" height="48" alt="image" src="https://github.com/user-attachments/assets/3495d845-2ad4-42ab-bfab-b798a9344e5d" />

2. запустити файл client.py
<img width="827" height="24" alt="image" src="https://github.com/user-attachments/assets/94bec7ae-ee0c-473f-85a2-4be58242a044" />

3. тепер можна писати повідомлення
<img width="875" height="121" alt="image" src="https://github.com/user-attachments/assets/527cd34d-4fa6-4a06-b2f4-fde3d68bd8b2" />

PS: якщо було виявлно помилку під час розшифрування повідомлення, на екран виведеться текст:\n
'[ERROR] The recieved message had an error'



ПОЯСНЕННЯ ІМПЛЕМЕНТАЦІЇ

У файлі encription.py реалізовано два класи:
1. RSA
    число е стале (65537);
    вибираються два простих числа p і q за допомогою теста Міллера-Рабіна;
    n = pq;
    обчислюють секретний ключ d , який є цілим числом, оберненим до e за
модулем ( p −1)(q −1):
    d = e**–1 mod((p–1)(q–1))

   реалізовано функцію encrypt та decrypt:
   повідомлення перетвоють в байти потім в int і підносять до степеня e за модулем n
   для розшифрування підносять до степеня d за модулем n і перетворюють в байти

2. XOR
   encrypt(msg, secret_key):
   перетворює повідомлення в байти
   робить побайтовий XOR із байтами ключа
   повертає результат як Hex-рядок.

   decrypt(msg, secret_key):
   Hex-рядок перетворює в байти
   робить побайтовий XOR із байтами ключа
   декодує відновлені байти назад у звичайний текст.


При створені сервера та кліжнта генеруються усі необхідні ключі для RSA та вони обмінюються ними. Далі secretkey для XOR надсилає сервер клієнту попередньо закодувавши його використовуючи public key клієнта, клієнт розшифровує його за доп private key. 

Тепер повідомлення написання клієнтом будуть шифруватися XOR з цим secretkey. 
Окрім повідомлення надсилається hash (реалізовано за допомогою бібліотеки hashlib методу sha3_512). Клієнт розшифровує повідомлення і наново рахує hash, якщо він збігається відображається повідомлення, в іншому - error message.




<img width="1071" height="168" alt="image" src="https://github.com/user-attachments/assets/c4d436b8-2652-4f5e-9332-721ea19bd078" />
<img width="934" height="192" alt="image" src="https://github.com/user-attachments/assets/b42df830-67e5-4d9b-a8c7-caf59324a551" />
<img width="1049" height="171" alt="image" src="https://github.com/user-attachments/assets/6e0d8f8e-24d5-4f5e-a9ba-2b7ea1fda290" />

