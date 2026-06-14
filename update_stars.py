import os, json, datetime
from urllib.request import urlopen, Request

TOKEN = os.environ["GH_TOKEN"]
USER  = os.environ["GH_USER"]

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

# ── Türkçe açıklamalar & araçlar (sabit sözlük) ─────────────────────
TR_META = {
    "aaif-goose/goose": ("Kod önerilerinin ötesine geçen, açık kaynaklı ve genişletilebilir AI ajan platformu.", ["Claude Code","Cursor","VS Code","Windsurf"]),
    "ownpilot/OwnPilot": ("Gizlilik odaklı, otonom ajanlı kişisel AI asistan platformu.", ["Claude Code","Gemini CLI"]),
    "WrongStack/WrongStack": ("Terminalde çalışan CLI tabanlı AI kodlama ajanı.", ["Terminal","VS Code","Claude Code"]),
    "open-jarvis/OpenJarvis": ("Kişisel cihazlarda çalışan açık kaynaklı AI asistan.", ["Claude Code","Cursor"]),
    "google/skills": ("Google ürünleri için hazırlanmış AI ajan skill koleksiyonu.", ["Gemini CLI","Claude Code","Cursor"]),
    "microsoft/VibeVoice": ("Microsoft'un açık kaynaklı sesli AI platformu.", ["VS Code","Cursor"]),
    "Panniantong/Agent-Reach": ("AI ajanına internet erişimi kazandır; Twitter, Reddit, YouTube'u tara.", ["Claude Code","Cursor","MCP"]),
    "santifer/career-ops": ("Claude Code üzerine kurulu 14 skill moduyla AI destekli iş arama sistemi.", ["Claude Code"]),
    "msitarzewski/agency-agents": ("Frontend uzmanından red team'e kadar tam bir AI ajans kadrosu.", ["Claude Code","Cursor","Windsurf"]),
    "oguzhaanferli/ai-agent-team-mobile-app": ("AI ajan takımı için mobil uygulama arayüzü.", ["Claude Code","Cursor"]),
    "bmad-code-org/BMAD-METHOD": ("Çevik, AI güdümlü yazılım geliştirme için BMAD metodolojisi.", ["Claude Code","Cursor","Windsurf","Gemini CLI"]),
    "JCodesMore/ai-website-cloner-template": ("Tek komutla AI ajanlarını kullanarak web sitesi klonlama şablonu.", ["Claude Code","Cursor","Codex"]),
    "BloopAI/vibe-kanban": ("Claude Code, Codex veya herhangi bir kodlama ajanından daha fazla verim al.", ["Claude Code","Codex","Cursor"]),
    "openai/gpt-oss": ("OpenAI tarafından yayınlanan açık ağırlıklı dil modelleri (120b ve 20b).", ["API","Ollama","LM Studio"]),
    "tddworks/baguette": ("iOS ajan altyapısı için başsız iOS Simülatör yöneticisi.", ["Xcode","Claude Code"]),
    "ersinkoc/project-bootstrap": ("Proje başlangıç süreçlerini otomatikleştiren araç.", ["Claude Code","Cursor","Terminal"]),
    "agentsmd/agents.md": ("Kodlama ajanlarını yönlendirmek için açık format standardı (AGENTS.md).", ["Claude Code","Cursor","Codex","Windsurf","Gemini CLI"]),
    "multica-ai/andrej-karpathy-skills": ("Karpathy prensiplerinden türetilmiş Claude Code davranış iyileştirme dosyası.", ["Claude Code"]),
    "wilwaldon/Claude-Code-Frontend-Design-Toolkit": ("Claude Code çıktılarını daha iyi frontend'e dönüştüren araç seti.", ["Claude Code"]),
    "callstackincubator/agent-skills": ("AI asistanlar için optimize edilmiş React Native skill koleksiyonu.", ["Claude Code","Cursor","Codex"]),
    "RefoundAI/lenny-skills": ("Lenny's Podcast'ten Claude Code için 86 ürün yönetimi skill'i.", ["Claude Code","Cursor"]),
    "google-gemini/gemini-skills": ("Gemini API ve SDK etkileşimleri için hazır skill'ler.", ["Gemini CLI","Claude Code","Cursor"]),
    "nextlevelbuilder/ui-ux-pro-max-skill": ("Profesyonel UI/UX geliştirme için tasarım zekası sağlayan AI skill.", ["Claude Code","Cursor","Windsurf","Codex"]),
    "greensock/gsap-skills": ("GSAP animasyonlarını öğreten resmi AI ajan skill'leri.", ["Claude Code","Cursor","Codex"]),
    "google-labs-code/design.md": ("Kodlama ajanlarına görsel kimlik tanımlamak için format spesifikasyonu.", ["Claude Code","Cursor","Gemini CLI"]),
    "coreyhaines31/marketingskills": ("Claude Code için pazarlama skill'leri: CRO, metin yazarlığı, SEO.", ["Claude Code","Cursor","Codex"]),
    "siteboon/claudecodeui": ("Claude Code'u mobil ve web üzerinden güzel bir arayüzle kullan.", ["Claude Code"]),
    "warpdotdev/warp": ("Terminalden doğan ajansal geliştirme ortamı.", ["Claude Code","Gemini CLI","Cursor"]),
    "nexu-io/open-design": ("Yerel çalışan açık kaynaklı Claude Design alternatifi.", ["Claude Code","Cursor"]),
    "PowerUserZ/OpenTokenUsage": ("AI kodlama aboneliklerini Windows sistem tepsisinden takip et.", ["Claude Code","Codex","Gemini CLI","Cursor"]),
    "robinebers/openusage": ("Claude, Codex, Copilot, Cursor abonelik kullanımını izle.", ["Claude Code","Codex","Cursor","Copilot"]),
    "ersinkoc/FluidFlow": ("Eskizleri çalışan uygulamalara dönüştür.", ["Claude Code","Cursor"]),
    "pranshuparmar/witr": ("Neden çalışıyor? — süreç inceleme ve analiz aracı.", ["Terminal","VS Code"]),
    "syncthing/syncthing": ("Açık kaynaklı sürekli dosya senkronizasyon sistemi.", ["Terminal","VS Code"]),
    "gorhill/uBlock": ("Chromium ve Firefox için verimli reklam engelleyici.", ["Chrome","Firefox"]),
    "ripienaar/free-for-dev": ("Geliştiriciler için ücretsiz katmanlı SaaS, PaaS ve IaaS listesi.", ["Genel Referans"]),
    "microsoft/coreutils": ("Windows için Coreutils yükleyici ve paketleme araçları.", ["Terminal","VS Code","Windows"]),
    "localsend/localsend": ("AirDrop'a açık kaynaklı platformlar arası alternatif.", ["Flutter","VS Code","Claude Code"]),
    "caamer20/Telegram-Drive": ("Telegram hesabını sınırsız güvenli bulut depolamaya dönüştür.", ["VS Code","Claude Code","Cursor"]),
    "webosbrew/dev-manager-desktop": ("webOS TV için cihaz ve DevMode yöneticisi.", ["VS Code","Cursor"]),
    "OpenCloudGaming/OpenNOW": ("Özel GeForce Now istemcisi — platformlar arası bulut oyun.", ["VS Code","Cursor"]),
    "rmyndharis/OpenWA": ("Ücretsiz, açık kaynaklı, kendi sunucunda WhatsApp API ağ geçidi.", ["VS Code","Claude Code","Cursor"]),
    "pear-devs/pear-desktop": ("Platformlar arası masaüstü müzik çalar eklentisi.", ["VS Code","Cursor","Claude Code"]),
    "OpenBMB/VoxCPM": ("Çok dilli konuşma üretimi ve ses klonlama için TTS modeli (VoxCPM2).", ["Google Colab","VS Code","Claude Code"]),
    "jamiepine/voicebox": ("Açık kaynaklı AI ses stüdyosu — klonla, dikte et, üret.", ["VS Code","Claude Code","Cursor"]),
    "abus-aikorea/voice-pro": ("TTS, konuşma tanıma, ses klonlama için Gradio WebUI.", ["Google Colab","VS Code"]),
    "tyc0on/GPT-SoVITS-colab": ("GPT-SoVITS ses klonlama için hazır Colab not defteri.", ["Google Colab"]),
    "nexmoe/VidBee": ("Dünyanın her yerindeki web sitelerinden video indir.", ["VS Code","Claude Code"]),
    "aandrew-me/ytDownloader": ("Yüzlerce siteden video ve ses indirmek için masaüstü uygulaması.", ["VS Code","Electron"]),
    "Free-TV/IPTV": ("Ücretsiz TV kanalları için M3U oynatma listesi.", ["VLC","Kodi"]),
    "iptv-org/iptv": ("Dünya genelinden herkese açık IPTV kanalları koleksiyonu.", ["VLC","Kodi"]),
    "LifeForge-app/lifeforge": ("Takvim, notlar, finans ve proje yönetimini tek çatıda toplayan self-hosted çözüm.", ["VS Code","Claude Code","Cursor"]),
    "paperless-ngx/paperless-ngx": ("Belgeleri tara, indeksle ve arşivle — güçlü belge yönetim sistemi.", ["VS Code","Docker"]),
    "vas3k/TaxHacker": ("Fiş ve faturalar için LLM analizörü; self-hosted AI muhasebe uygulaması.", ["VS Code","Claude Code","Cursor"]),
    "umitaltinozzz/twitter-archive": ("Tam metin arama destekli self-hosted Twitter yer imleri arşivi.", ["VS Code","Claude Code"]),
    "sarisen/x-bookmark-manager": ("X (Twitter) yer imi yöneticisi.", ["VS Code","Claude Code"]),
    "marktext/marktext": ("Linux, macOS ve Windows için sade ve zarif Markdown editörü.", ["Standalone"]),
    "webadderallorg/Recordly": ("Düzenleme becerisi gerekmeden parlak demo videoları oluştur.", ["Standalone"]),
    "siddharthvaddem/openscreen": ("Ücretsiz, açık kaynaklı, abonelik ve filigran olmadan etkileyici demolar.", ["Standalone","Electron"]),
    "opendataloader-project/opendataloader-pdf": ("AI'a hazır veri için PDF ayrıştırıcı; PDF erişilebilirliğini otomatikleştir.", ["VS Code","Claude Code","Cursor"]),
    "tw93/Mole": ("Mac'ini terminalden temizle, analiz et, optimize et ve izle.", ["Terminal","macOS"]),
    "codybrom/Blankie": ("Mac App Store'da bulunan macOS için ortam sesi mikseri.", ["macOS"]),
    "DodoApps/dodopulse": ("Gerçek zamanlı sistem izleme için hafif macOS menü çubuğu uygulaması.", ["macOS"]),
    "open-saas-directory/awesome-native-macosx-apps": ("En iyi Mac uygulamaları — hızlı, hafif, Electron olmadan.", ["macOS","Genel Referans"]),
    "shiiraz/clicklight-windows": ("Demo ve kayıt için tıklamaları canlı vurgulayan Windows tepsi uygulaması.", ["Windows"]),
    "microsoft/microsoft-ui-reactor": ("WinUI için deneysel uzantı seti (Reactor).", ["VS Code","Visual Studio","Windows"]),
    "sherlock-project/sherlock": ("Sosyal medya hesaplarını kullanıcı adıyla birden fazla ağda bul.", ["Terminal","VS Code","Claude Code"]),
    "bwya77/vscode-dark-islands": ("JetBrains Islands temasından ilham alan VS Code karanlık teması.", ["VS Code"]),
    "DontFuckMyCode/dfmc": ("Kod koruma ve gizleme aracı.", ["Terminal","VS Code"]),
    "OpenAEC-Foundation/open-pdf-studio": ("Belge düzenleme ve işleme için açık PDF stüdyosu.", ["Standalone","VS Code"]),
    "ultraworkers/claw-code": ("Rust ile inşa edilmiş, ajan tarafından yönetilen müze sergisi.", ["Claude Code","Cursor"]),
    "CodeByPinar/bakiyedefter-pos": ("Küçük işletmeler için modern, çevrimdışı öncelikli finansal operasyon ve POS sistemi.", ["VS Code","Claude Code","Cursor"]),
    "kemalersin/kurtarma-plani": ("Borçları kayıt altına alan, gelir-gider dengesini izleyen uygulama.", ["VS Code","Claude Code"]),
    "saidsurucu/yargi-mcp": ("Türk hukuk veritabanları için MCP sunucusu.", ["Claude Code","Cursor","MCP"]),
    "3rt4nm4n/turkish-apis": ("Türk API'leri listesi: BTC Türk, İşbank, Trendyol ve daha fazlası.", ["Genel Referans","VS Code"]),
    "Garletz/zikiro-FYR": ("Açık kaynaklı restoran POS sistemi (For Your Restaurant).", ["VS Code","Claude Code","Tauri"]),
    "alicankiraz1/Ai-Arastirma-Okumalarim-TR": ("AI makalelerinin Türkçe detaylı açıklamaları.", ["Genel Referans"]),
    "zubair-trabzada/geo-seo-claude": ("Claude Code için GEO öncelikli SEO skill'i.", ["Claude Code"]),
    "YusufDinanet/MetroFlow": ("Metro akış yönetimi uygulaması.", ["VS Code","Claude Code"]),
    "harry0703/MoneyPrinterTurbo": ("AI ile tek tıkla yüksek kaliteli kısa video üretim platformu.", ["Google Colab","VS Code","Claude Code"]),
}

# ── Kategori eşleştirme ──────────────────────────────────────────────
CATEGORIES = [
    ("🤖 AI & Agents", [
        "goose","ownpilot","wrongstack","openjarvis","vibevoice","agent-reach",
        "career-ops","agency-agents","ai-agent-team","bmad","ai-website-cloner",
        "vibe-kanban","gpt-oss","baguette","project-bootstrap","open-jarvis",
        "google/skills","microsoft/vibevoice","moneyprinterturbo",
    ]),
    ("🎯 Skills & Prompts", [
        "agents.md","karpathy-skills","frontend-design-toolkit",
        "callstackincubator/agent-skills","lenny-skills","gemini-skills",
        "ui-ux-pro-max","gsap-skills","design.md","marketingskills",
    ]),
    ("🔧 Dev Tools & CLI", [
        "claudecodeui","warpdotdev","open-design","opentokenusage","openusage",
        "fluidflow","witr","syncthing","ublock","free-for-dev","microsoft/coreutils",
    ]),
    ("📱 Mobile & Cross-Platform", [
        "localsend","telegram-drive","dev-manager-desktop","opennow","openwa","pear-desktop",
    ]),
    ("🎵 Medya, Ses & Video", [
        "voxcpm","voicebox","voice-pro","gpt-sovits","vidbee",
        "ytdownloader","free-tv","iptv-org",
    ]),
    ("📋 Prodüktivite & Self-Hosted", [
        "lifeforge","paperless-ngx","taxhacker","twitter-archive",
        "x-bookmark","marktext","recordly","openscreen","opendataloader-pdf",
    ]),
    ("🖥️ macOS & Desktop Apps", [
        "tw93/mole","blankie","dodopulse","awesome-native-macosx",
        "clicklight","microsoft-ui-reactor",
    ]),
    ("⚙️ Yazılım Geliştirme & Güvenlik", [
        "sherlock","vscode-dark-islands","dfmc","open-pdf-studio","claw-code",
    ]),
    ("🇹🇷 Türkçe Projeler", [
        "bakiyedefter","kurtarma-plani","yargi-mcp","turkish-apis",
        "zikiro","ai-arastirma","geo-seo-claude","metroflow",
    ]),
]

def categorize(repo):
    full   = repo["full_name"].lower()
    topics = " ".join(repo.get("topics") or []).lower()
    desc   = (repo.get("description") or "").lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in full for kw in keywords):
            return cat_name
    # topics tabanlı fallback
    if any(k in topics for k in ["agent","llm","ai","gpt","claude","gemini","copilot","mcp"]):
        return "🤖 AI & Agents"
    if any(k in topics for k in ["prompt","skill","template"]):
        return "🎯 Skills & Prompts"
    if any(k in topics for k in ["cli","terminal","devtool","developer-tool"]):
        return "🔧 Dev Tools & CLI"
    if any(k in topics for k in ["macos","swiftui","mac-app","menubar"]):
        return "🖥️ macOS & Desktop Apps"
    if any(k in topics for k in ["flutter","react-native","mobile","ios","android"]):
        return "📱 Mobile & Cross-Platform"
    if any(k in topics for k in ["tts","voice","speech","audio","music","video","iptv"]):
        return "🎵 Medya, Ses & Video"
    if any(k in topics for k in ["self-hosted","homelab","docker","productivity","note"]):
        return "📋 Prodüktivite & Self-Hosted"
    if any(k in topics for k in ["security","osint","pentest","ctf","privacy"]):
        return "⚙️ Yazılım Geliştirme & Güvenlik"
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
    "Terminal":"4EAA25","Google Colab":"F9AB00","Copilot":"555555",
    "MCP":"7C3AED","Tauri":"FFC131","Electron":"47848F",
    "Flutter":"02569B","Docker":"2496ED","Ollama":"222222",
    "LM Studio":"8B5CF6","API":"6C757D","macOS":"222222",
    "Windows":"0078D4","Xcode":"147EFB","Standalone":"6B7280",
    "Genel Referans":"6B7280","Chrome":"4285F4","Firefox":"FF7139",
    "VLC":"FF8800","Kodi":"17B2E7","Visual Studio":"5C2D91",
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
        key   = r["full_name"]
        meta  = TR_META.get(key)
        if meta:
            desc, tools = meta
        else:
            # Yeni repo — İngilizce açıklama, topics'ten araç tahmini
            desc  = (r.get("description") or "—")
            topics = " ".join(r.get("topics") or []).lower()
            tools = []
            if any(k in topics for k in ["claude","mcp"]): tools.append("Claude Code")
            if "cursor" in topics: tools.append("Cursor")
            if any(k in topics for k in ["flutter","dart"]): tools.append("Flutter")
            if any(k in topics for k in ["docker","container"]): tools.append("Docker")
            if any(k in topics for k in ["vscode","vs-code"]): tools.append("VS Code")
        desc = desc.replace("|","\\|")
        lang  = r.get("language") or "N/A"
        lines.append(f"| [{key}]({r['html_url']}) | {desc} | `{lang}` | {badges(tools)} |")
    lines += ["", "---", ""]

lines.append("*🤖 Bu dosya [GitHub Actions](.github/workflows/update.yml) tarafından her gece otomatik güncellenmektedir.*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ README güncellendi: {total} repo, {cat_count} kategori")
