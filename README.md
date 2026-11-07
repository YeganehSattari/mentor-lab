# mentor-lab

زمین بازی آماده برای «تسک‌های حرفه‌ای» جزوه‌ی **Mentor SHOCK 101** (DiapaZon · INTERN.EXE · پژواک هوشمند).

## چرا این ریپو؟
تسک‌های جزوه به «repo ِ TA بات RL خودتان» اشاره می‌کنند. لازم نیست به کد Cadence دست بزنید و لازم نیست کد بخش‌های قبل را تغییر بدهید. **همه‌ی تسک‌ها را می‌توانید روی همین یک ریپو انجام دهید.** هر بخش چیزی به آن اضافه می‌کند و در پایان، همین ریپو پایه‌ی پروژه‌ی پایانی Echo-Mentor می‌شود.

## داخلش چه هست؟
- `src/mentor_lab/env.py`: شبیه‌ساز یک cohort با ۱۲ کارآموز ساختگی (H-01 تا H-12). هر روز باید به **۳ نفر** بازخورد بدهید. Reward یعنی تعداد کارآموزهایی که فردا فعال‌اند. Cost یعنی تعداد کسانی که بیش از ۴ روز بی‌بازخورد مانده‌اند (قید عدالت، مثل CMDP).
- `src/mentor_lab/policies.py`: سه Policy پایه، یعنی Random، RoundRobin (چرخش دستی منتور) و LinUCB، به‌علاوه‌ی `softmax_topk` که احتمال انتخاب (propensity) را هم برای OPE برمی‌گرداند.
- `src/mentor_lab/llm.py`: یک LLM ساختگی و قطعی که پیش‌نویس بازخورد را به‌صورت JSON می‌سازد و حدود ۱۰٪ مواقع قالب را خراب می‌کند، درست مثل یک مدل واقعی.
- `src/mentor_lab/evaluate.py`: اجرای چند seed، IQM و بازه‌ی bootstrap.
- `src/mentor_lab/seeds.py`: `derive_seed` برای RNGهای مستقل و تکرارپذیر.
- `tests/` و `.github/workflows/ci.yml`.

## اجرا
```bash
uv sync
uv run pytest -q
uv run python scripts/run_baselines.py
```
(بدون uv هم کار می‌کند: `python3 -m pytest -q` و `python3 scripts/run_baselines.py`؛ فقط stdlib است.)

## اولین معمای جالب
خروجی فعلی `run_baselines.py`:
```
random       IQM≈250   fairness-cost/ep≈76
round-robin  IQM≈321   fairness-cost/ep≈0
linucb       IQM≈174   fairness-cost/ep≈172
```
LinUCB ِ ساده از چرخش دستی هم بدتر است، چون چند کارآموز را مدام انتخاب می‌کند و بقیه را از یاد می‌برد. یعنی Reward ِ هر نفر را بهینه می‌کند، نه Reward ِ کل cohort را. **هدف بزرگ این هفته:** یک Policy بسازید که هم از round-robin بیشتر Reward بگیرد و هم قید ۴ روز را نقض نکند. بخش‌های ۴ تا ۷ ابزار این کار را می‌دهند و پروژه‌ی پایانی آن را به n8n و Telegram وصل می‌کند.

## قانون تسک‌ها
از بندهای هر «🧪 تسک حرفه‌ای»، **دست‌کم ۳ بند اجباری است** و بقیه امتیاز اضافه دارند. در «📝 گزارش بخش» بنویسید کدام بندها را انجام دادید. نقشه‌ی بند به بند در `TASKS.md` است.
