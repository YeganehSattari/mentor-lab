# نقشه‌ی تسک‌ها روی mentor-lab
هر بخش: **دست‌کم ۳ بند**. پیشنهاد ما برای ۳ بندِ اول هر بخش با ⭐ مشخص شده است. هر بخش را در یک یا چند commit با پیشوند `mN:` ثبت کنید.

## m1 · Python در سطح پژوهش
- ⭐ (۱) `protocols.py` را Generic کنید (`Env[S, A]`, `Policy[S, A]`) و `uv run mypy --strict src` را پاس کنید.
- ⭐ (۲) خروجی `llm.feedback_draft` را با یک pydantic model (`strict=True`, `extra="forbid"`) validate و نرخ شکست قالب را روی ۱۰۰۰ فراخوانی log کنید (باید حدود ۱۰٪ باشد).
- ⭐ (۴) با `derive_seed` نشان دهید دو اجرا با `PYTHONHASHSEED` متفاوت عدد یکسان می‌دهند (تست آماده در `tests/test_sim.py` را گسترش دهید).
- (۳) یک `evaluate_async` با `TaskGroup`، `Semaphore`، timeout و retry ِ full-jitter؛ (۵) cProfile روی `run_baselines.py` و بهینه‌سازی `LinUCB.scores`؛ (۶) `uv.lock` و `uv sync --locked` در CI.

## m2 · Git در مقیاس
- ⭐ (۲) `.pre-commit-config.yaml` با ruff، ruff-format و detect-secrets.
- ⭐ (۳) در CI یک job ِ gate که اگر IQM ِ round-robin بیش از ۳٪ افت کرد fail شود.
- ⭐ (۴) دو آزمایش `alpha` ِ LinUCB (مثلاً 0.3 و 1.5) در دو `git worktree` و tag ِ annotated برای برنده.
- (۱) یک regression عمدی در `env.py` بکارید و با `git bisect run` و یک `scripts/bisect_eval.py` پیدایش کنید؛ (۵) review ِ یک PR ِ کارآموز با Conventional Comments.

## m3 · مبانی Agentic AI
- ⭐ یک Agent loop ِ کوچک که با `llm.feedback_draft` کار می‌کند و validator ِ JSON دارد؛ ⭐ loop guard و budget؛ ⭐ ۵ گزارش مسموم (prompt injection) و نرخ موفقیت حمله قبل و بعد از guardrail.

## m4 · RL I
- ⭐ یک Q-learning ِ جدولی یا خطی روی `InternSim` (state را از context بسازید)؛ ⭐ نسخه‌ی Double Q؛ ⭐ مقایسه‌ی overestimation روی ۲۰ seed با نمودار.

## m5 · RL II
- ⭐ Policy ِ softmax روی همان انتخاب روزانه با REINFORCE + baseline؛ ⭐ actor-critic با GAE؛ ⭐ PPO-clip و نمودار clip_fraction و approx_kl. (سناریوی یانیس: lr بزرگ و ۱۰ epoch.)

## m6 · RL III (مهم‌ترین بخش برای هدف بزرگ)
- ⭐ LinUCB را به شکل top-K با قید عدالت درآورید: Lagrangian (λ per-step) یا shield ِ «هر کس gap ≥ ۴ دارد اول انتخاب شود».
- ⭐ با `softmax_topk` لاگ با propensity بسازید و ارزش Policy را با IPS، SNIPS و DR تخمین بزنید.
- ⭐ هدف: IQM بالاتر از round-robin با fairness-cost = 0؛ عدد و CI را گزارش کنید.

## m7 · RL برای LLMها
- ⭐ ۲۰۰ جفت ترجیح بین پیش‌نویس‌های `llm.feedback_draft` (یا پیش‌نویس‌های واقعی خودتان) بسازید؛ ⭐ Bradley–Terry ِ خطی؛ ⭐ حمله‌ی «بلند و پرتمجید» و تحلیل reward hacking.

## m8 · RAG
- ⭐ ۴۰ سؤال از متن جزوه‌ها با چانک‌های مرتبط؛ ⭐ BM25 در برابر hybrid با RRF؛ ⭐ recall@5 و MRR.

## m9 · MCP
- ⭐ یک FastMCP Server به اسم `intern-dossiers` که از `InternSim` داده می‌خواند؛ ⭐ اعتبارسنجی کدنام؛ ⭐ transcript ِ tools/list و tools/call.

## m10 · n8n I
- ⭐ n8n با Docker؛ ⭐ workflow ِ digest ِ روزانه (داده‌ی ساختگی هم قبول است)؛ ⭐ Error Workflow و export ِ JSON در `n8n/`.

## m11 · n8n II
- ⭐ AI Agent node با یک Tool که MCP Server ِ m9 را صدا می‌زند؛ ⭐ Structured Output Parser؛ ⭐ تأیید شما در Telegram قبل از ارسال.

## m12 · مرزهای تازه
- ⭐ golden set ِ ۲۰ نمونه؛ ⭐ grader ِ code-based؛ ⭐ اجرای خودکار در GitHub Actions.

## پروژه‌ی پایانی Echo-Mentor
همین ریپو + Policy ِ m6 + MCP ِ m9 + workflow ِ m11 + eval ِ m12. یعنی اگر بخش‌ها را روی mentor-lab جلو ببرید، پروژه‌ی پایانی تقریباً خودش سر هم می‌شود.
