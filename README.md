# بوت تيليجرام بالذكاء الاصطناعي 🤖

بوت تيليجرام يستخدم نموذج ذكاء اصطناعي **مجاني ومفتوح المصدر** (عبر Groq، يشغّل نماذج مثل Llama) للرد على الرسائل. مبني بـ Python وFastAPI، وجاهز للنشر على Vercel مجانًا.

## المتطلبات

- حساب [Telegram](https://telegram.org)
- حساب [GitHub](https://github.com) مجاني
- حساب [Vercel](https://vercel.com) مجاني
- حساب [Groq](https://console.groq.com) مجاني (بدون بطاقة ائتمان)
- Python 3.12+ (للتجربة المحلية فقط — اختياري)

---

## 1) أنشئ بوت تيليجرام

1. افتح تيليجرام وابحث عن [@BotFather](https://t.me/BotFather)
2. أرسل له `/newbot` واتبع التعليمات (اسم للبوت، ثم username ينتهي بـ `bot`)
3. احفظ الـ **token** اللي بيعطيك ياه (شكله شبيه: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyz`)

## 2) احصل على مفتاح Groq المجاني

1. روح إلى [console.groq.com](https://console.groq.com) وسجّل حساب مجاني
2. من قسم **API Keys** أنشئ مفتاح جديد واحفظه

## 3) جرّب المشروع محليًا (اختياري)

```bash
python -m venv venv
source venv/bin/activate      # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# افتح .env وعبّي TELEGRAM_BOT_TOKEN و GROQ_API_KEY
uvicorn app:app --reload
```

افتح `http://localhost:8000` بالمتصفح، إذا شفت `{"status":"ok"}` فكل شي تمام.

## 4) ارفع المشروع على GitHub

داخل مجلد المشروع:

```bash
git init
git add .
git commit -m "Initial commit: Telegram AI bot"
```

بعدين أنشئ مستودع (repository) جديد وفاضي من [github.com/new](https://github.com/new)، وارجع للطرفية (terminal):

```bash
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## 5) انشر على Vercel

1. روح إلى [vercel.com/new](https://vercel.com/new) وسجّل دخول بحساب GitHub
2. اختر المستودع اللي رفعته
3. **قبل** ما تضغط Deploy، افتح قسم **Environment Variables** وأضف:
   - `TELEGRAM_BOT_TOKEN`
   - `GROQ_API_KEY`
   - `WEBHOOK_SECRET` (اختياري — أي نص عشوائي، لحماية إضافية)
4. اضغط **Deploy** وانتظر لين يخلص البناء
5. انسخ رابط المشروع بعد ما ينشر (مثال: `https://your-project.vercel.app`)

## 6) اربط البوت برابط النشر (Webhook)

افتح هذا الرابط بالمتصفح بعد ما تعوّض TOKEN ورابط مشروعك:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-project.vercel.app/api/webhook
```

إذا رجعلك `"ok":true` صار الربط تمام ✅.
إذا فعّلت `WEBHOOK_SECRET`، ضيف بنهاية الرابط: `&secret_token=القيمة_اللي_حطيتها`

## 7) جرّب البوت

روح لمحادثة بوتك بتيليجرام وأرسل `/start` أو أي سؤال.

---

## أفكار لتطوير المشروع لاحقًا

- **تذكّر المحادثة**: حاليًا كل رسالة تُعامَل لحالها؛ لإضافة ذاكرة محادثة تحتاج تخزين خارجي (مثل Vercel KV أو Postgres)
- **"جاري الكتابة..."**: إضافة مؤشر انتظار أثناء تجهيز الرد
- **تخصيص شخصية البوت**: عدّل متغيّر `SYSTEM_PROMPT` داخل `app.py`
- **تبديل الموديل**: غيّر `GROQ_MODEL` في متغيرات البيئة (مثلاً `llama-3.1-8b-instant` للسرعة الأعلى)

## ملاحظة

Groq يشغّل نماذج مفتوحة المصدر (مثل Llama) على معالجات سريعة جدًا، وخطته المجانية لا تحتاج بطاقة ائتمان وتكفي للاستخدام الشخصي والمشاريع الصغيرة.
