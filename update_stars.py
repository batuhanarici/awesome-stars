import os, json, datetime, time
from urllib.request import urlopen, Request
from urllib.error import HTTPError

TOKEN    = os.environ["GH_TOKEN"]
USER     = os.environ["GH_USER"]
CLAUDE   = os.environ.get("ANTHROPIC_API_KEY", "")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "awesome-stars-bot"
}

def gh(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req) as r:
        return json.loads(r.read())

# ── Tüm yıldızları çek ──────────────────────────────────────────────
repos, page = [], 1
while True:
    data = gh(f"https://api.github.com/users/{USER}/starred?per_page=100&page={page}")
    if not data:
        break
    repos.extend(data)
    page += 1
print(f"✅ {len(repos)} repo çekildi.")

# ── Önbellek yükle ──────────────────────────────────────────────────
CACHE_FILE = "meta_cache.json"
try:
    with open(CACHE_FILE, encoding="utf-8") as f:
        cache = json.load(f)
except:
    cache = {}

# ── Claude API ile meta üret ─────────────────────────────────────────
def claude_meta(repo):
    if not CLAUDE:
        return None
    name  = repo["full_name"]
    desc  = repo.get("description") or ""
    lang  = repo.get("language") or ""
    topics = ", ".join(repo.get("topics") or [])
    prompt = f"""GitHub reposu hakkında bilgi:
- Repo: {name}
- Açıklama (EN): {desc}
- Dil: {lang}
- Konular: {topics}

Lütfen YALNIZCA şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "tr": "<Bu reponun ne işe yaradığını 1-2 cümleyle Türkçe açıkla>",
  "tools": ["<bu repoyla birlikte kullanılabilecek geliştirici araçları>"]
}}

tools için sadece şu listeden seç (uygun olanları): Claude Code, Cursor, Windsurf, VS Code, Gemini CLI, Codex, Terminal, Google Colab, Copilot, MCP, Tauri, Electron, Flutter, Docker, Ollama, LM Studio, API, macOS, Windows, Xcode, Standalone, Genel Referans"""

    body = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": CLAUDE,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    try:
        with urlopen(req, timeout=20) as r:
            resp = json.loads(r.read())
        text = resp["content"][0]["text"].strip()
        # JSON'u parse et
        start = text.find("{")
        end   = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        print(f"  ⚠️  Claude API hatası ({repo['full_name']}): {e}")
        return None

# ── Her repo için meta al (önbellek öncelikli) ───────────────────────
for r in repos:
    key = r["full_name"]
    if key not in cache:
        print(f"  🤖 Meta üretiliyor: {key}")
        meta = claude_meta(r)
        if meta:
            cache[key] = meta
            time.sleep(0.3)   # rate limit
        else:
            # Claude yoksa veya hata varsa İngilizce açıklamayı koy
            cache[key] = {
                "tr": (r.get("description") or "—"),
                "tools": []
            }

# Önbelleği kaydet
with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
print(f"✅ Önbellek güncellendi ({len(cache)} repo).")

# ── Kategori eşleştirme ──────────────────────────────────────────────
CATEGORIES = [
    ("🤖 AI & Agents", [
        "goose","ownpilot","wrongstack","openjarvis","vibevoice","viбevoice",
        "agent-reach","career-ops","agency-agents","ai-agent-team","bmad",
        "ai-website-cloner","vibe-kanban","gpt-oss","baguette","project-bootstrap",
        "open-jarvis","google/skills","microsoft/vibevoice"
    ]),
    ("🎯 Skills & Prompts", [
        "agents.md","karpathy-skills","frontend-design-toolkit",
        "callstackincubator/agent-skills","lenny-skills","gemini-skills",
        "ui-ux-pro-max","gsap-skills","design.md","marketingskills"
    ]),
    ("🔧 Dev Tools & CLI", [
        "claudecodeui","warpdotdev","open-design","opentokenusage",
        "openusage","fluidflow","witr","syncthing","ublock",
        "free-for-dev","microsoft/coreutils"
    ]),
    ("📱 Mobile & Cross-Platform", [
        "localsend","telegram-drive","dev-manager-desktop","opennow",
        "openwa","pear-desktop"
    ]),
    ("🎵 Medya, Ses & Video", [
        "voxcpm","voicebox","voice-pro","gpt-sovits","vidbee",
        "ytdownloader","free-tv","iptv-org"
    ]),
    ("📋 Prodüktivite & Self-Hosted", [
        "lifeforge","paperless-ngx","taxhacker","twitter-archive",
        "x-bookmark","marktext","recordly","openscreen","opendataloader-pdf"
    ]),
    ("🖥️ macOS & Desktop Apps", [
        "tw93/mole","blankie","dodopulse","awesome-native-macosx",
        "clicklight","microsoft-ui-reactor"
    ]),
    ("⚙️ Yazılım Geliştirme & Güvenlik", [
        "sherlock","vscode-dark-islands","dfmc","open-pdf-studio","claw-code"
    ]),
    ("🇹🇷 Türkçe Projeler", [
        "bakiyedefter","kurtarma-plani","yargi-mcp","turkish-apis",
        "zikiro","ai-arastirma","geo-seo-claude","metroflow"
    ]),
]

def categorize(repo):
    full   = repo["full_name"].lower()
    topics = " ".join(repo.get("topics") or []).lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in full for kw in keywords):
            return cat_name
    # topics ile fallback
    if any(k in topics for k in ["agent","llm","ai","gpt","claude","gemini","copilot"]):
        return "🤖 AI & Agents"
    if any(k in topics for k in ["macos","swiftui","mac-app"]):
        return "🖥️ macOS & Desktop Apps"
    if any(k in topics for k in ["flutter","react-native","mobile","ios","android"]):
        return "📱 Mobile & Cross-Platform"
    if any(k in topics for k in ["tts","voice","speech","audio","music"]):
        return "🎵 Medya, Ses & Video"
    if any(k in topics for k in ["self-hosted","homelab","docker","selfhosted"]):
        return "📋 Prodüktivite & Self-Hosted"
    if any(k in topics for k in ["security","osint","pentest","ctf"]):
        return "⚙️ Yazılım Geliştirme & Güvenlik"
    # Dil + owner dilinden Türkçe tespiti (basit)
    desc = (repo.get("description") or "").lower()
    if any(k in desc for k in ["türk","turkish","türkçe","istanbul","ankara"]):
        return "🇹🇷 Türkçe Projeler"
    return "🗂️ Diğer"

# Kategorilere ayır
order = [c[0] for c in CATEGORIES] + ["🗂️ Diğer"]
buckets = {c: [] for c in order}
for r in repos:
    buckets[categorize(r)].append(r)

# ── Badge üretici ────────────────────────────────────────────────────
COLORS = {
    "Claude Code":"5C4EFF","Cursor":"000000","Windsurf":"0099FF",
    "VS Code":"007ACC","Gemini CLI":"4285F4","Codex":"412991",
    "Terminal":"4EAA25","Google Colab":"F9AB00","Copilot":"000000",
    "MCP":"7C3AED","Tauri":"FFC131","Electron":"47848F",
    "Flutter":"02569B","Docker":"2496ED","Ollama":"000000",
    "LM Studio":"8B5CF6","API":"6C757D","macOS":"000000",
    "Windows":"0078D4","Xcode":"147EFB","Standalone":"6B7280",
    "Genel Referans":"6B7280",
}

def badges(tools):
    out = []
    for t in tools:
        c = COLORS.get(t, "6B7280")
        l = t.replace(" ", "%20").replace("-","--")
        out.append(f"![{t}](https://img.shields.io/badge/{l}-{c}?style=flat-square&logoColor=white)")
    return " ".join(out) if out else "—"

# ── README oluştur ───────────────────────────────────────────────────
today     = datetime.date.today().strftime("%d %B %Y")
total     = len(repos)
cat_count = len([b for b in buckets.values() if b])

lines = [
    "# ⭐ awesome-stars",
    "",
    "> **batuhanarici** tarafından yıldızlanan GitHub repoları — kategorilere göre otomatik düzenlenmiş",
    f"> 🕐 Son güncelleme: **{today}** &nbsp;|&nbsp; 📦 Toplam: **{total} repo** &nbsp;|&nbsp; 🗂️ Kategori: **{cat_count}**",
    "",
    "## İçindekiler", "",
]

for cat in order:
    if buckets[cat]:
        lines.append(f"- [{cat}](#) — {len(buckets[cat])} repo")

lines += ["", "---", ""]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    lines += [
        f"## {cat}", "",
        "| Repo | Açıklama | Dil | Araçlar |",
        "|------|----------|-----|---------|",
    ]
    for r in sorted(rlist, key=lambda x: x["full_name"].lower()):
        meta  = cache.get(r["full_name"], {})
        desc  = meta.get("tr") or (r.get("description") or "—")
        desc  = desc.replace("|","\\|")
        lang  = r.get("language") or "N/A"
        tools = meta.get("tools", [])
        lines.append(f"| [{r['full_name']}]({r['html_url']}) | {desc} | `{lang}` | {badges(tools)} |")
    lines += ["", "---", ""]

lines.append("*🤖 Bu dosya [GitHub Actions](.github/workflows/update.yml) tarafından her gece otomatik güncellenmektedir.*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ README güncellendi: {total} repo, {cat_count} kategori")
