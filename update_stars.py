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

# Tüm yıldızları çek
repos, page = [], 1
while True:
    data = gh(f"https://api.github.com/users/{USER}/starred?per_page=100&page={page}")
    if not data:
        break
    repos.extend(data)
    page += 1

print(f"Toplam {len(repos)} repo çekildi.")

# ─────────────────────────────────────────────
# Türkçe açıklamalar + uyumlu araçlar
# ─────────────────────────────────────────────
REPO_META = {
    # AI & Agents
    "aaif-goose/goose": {
        "tr": "Kod önerilerinin ötesine geçen, açık kaynaklı ve genişletilebilir bir AI ajan platformu.",
        "tools": ["Claude Code", "Cursor", "VS Code", "Windsurf"]
    },
    "ownpilot/OwnPilot": {
        "tr": "Gizlilik odaklı, otonom ajanlı ve iş akışı destekli kişisel AI asistan platformu.",
        "tools": ["Claude Code", "Gemini CLI"]
    },
    "WrongStack/WrongStack": {
        "tr": "Terminalde çalışan CLI tabanlı AI kodlama ajanı.",
        "tools": ["Terminal", "VS Code", "Claude Code"]
    },
    "open-jarvis/OpenJarvis": {
        "tr": "Kişisel cihazlarda çalışan, kişisel AI asistan sistemi.",
        "tools": ["Claude Code", "Cursor"]
    },
    "google/skills": {
        "tr": "Google ürünleri ve teknolojileri için hazırlanmış AI ajan skill'leri.",
        "tools": ["Gemini CLI", "Claude Code", "Cursor"]
    },
    "microsoft/VibeVoice": {
        "tr": "Microsoft'un açık kaynaklı, sınır sesli AI platformu.",
        "tools": ["VS Code", "Cursor", "Claude Code"]
    },
    "Panniantong/Agent-Reach": {
        "tr": "AI ajanına internet erişimi kazandır; Twitter, Reddit, YouTube ve daha fazlasını tara.",
        "tools": ["Claude Code", "Cursor", "MCP"]
    },
    "santifer/career-ops": {
        "tr": "Claude Code üzerine kurulu, 14 skill moduyla AI destekli iş arama sistemi.",
        "tools": ["Claude Code"]
    },
    "msitarzewski/agency-agents": {
        "tr": "Frontend uzmanından red team'e kadar tam bir AI ajans kadrosu.",
        "tools": ["Claude Code", "Cursor", "Windsurf"]
    },
    "oguzhaanferli/ai-agent-team-mobile-app": {
        "tr": "AI ajan takımı için mobil uygulama arayüzü.",
        "tools": ["Claude Code", "Cursor"]
    },
    "bmad-code-org/BMAD-METHOD": {
        "tr": "Çevik, AI güdümlü yazılım geliştirme için öncü metodoloji (BMAD Metodu).",
        "tools": ["Claude Code", "Cursor", "Windsurf", "Gemini CLI"]
    },
    "JCodesMore/ai-website-cloner-template": {
        "tr": "Tek komutla AI kodlama ajanlarını kullanarak herhangi bir web sitesini klonla.",
        "tools": ["Claude Code", "Cursor", "Codex"]
    },
    "BloopAI/vibe-kanban": {
        "tr": "Claude Code, Codex veya herhangi bir kodlama ajanından 10 kat daha fazla verim al.",
        "tools": ["Claude Code", "Codex", "Cursor"]
    },
    "openai/gpt-oss": {
        "tr": "OpenAI tarafından yayınlanan gpt-oss-120b ve gpt-oss-20b açık ağırlıklı dil modelleri.",
        "tools": ["API", "Ollama", "LM Studio"]
    },
    "tddworks/baguette": {
        "tr": "iOS ajan altyapısı için başsız iOS Simülatör yöneticisi ve host tarafı giriş enjeksiyonu.",
        "tools": ["Xcode", "Claude Code"]
    },
    "ersinkoc/project-bootstrap": {
        "tr": "Proje başlangıç süreçlerini otomatikleştiren bootstrap aracı.",
        "tools": ["Claude Code", "Cursor", "Terminal"]
    },
    # Skills & Prompts
    "agentsmd/agents.md": {
        "tr": "Kodlama ajanlarını yönlendirmek için basit ve açık bir format standardı (AGENTS.md).",
        "tools": ["Claude Code", "Cursor", "Codex", "Windsurf", "Gemini CLI"]
    },
    "multica-ai/andrej-karpathy-skills": {
        "tr": "Karpathy'nin prensiplerinden türetilmiş, Claude Code davranışını iyileştiren tek CLAUDE.md dosyası.",
        "tools": ["Claude Code"]
    },
    "wilwaldon/Claude-Code-Frontend-Design-Toolkit": {
        "tr": "Claude Code çıktılarını daha iyi görünen frontend'e dönüştüren her şey.",
        "tools": ["Claude Code"]
    },
    "callstackincubator/agent-skills": {
        "tr": "AI kodlama asistanları için ajan optimize edilmiş React Native skill koleksiyonu.",
        "tools": ["Claude Code", "Cursor", "Codex"]
    },
    "RefoundAI/lenny-skills": {
        "tr": "Lenny's Podcast'ten Claude Code için 86 ürün yönetimi skill'i.",
        "tools": ["Claude Code", "Cursor"]
    },
    "google-gemini/gemini-skills": {
        "tr": "Gemini API, SDK ve model/ajan etkileşimleri için hazır skill'ler.",
        "tools": ["Gemini CLI", "Claude Code", "Cursor"]
    },
    "nextlevelbuilder/ui-ux-pro-max-skill": {
        "tr": "Profesyonel UI/UX geliştirme için tasarım zekası sağlayan AI skill'i.",
        "tools": ["Claude Code", "Cursor", "Windsurf", "Codex"]
    },
    "greensock/gsap-skills": {
        "tr": "GSAP animasyonlarını öğreten, AI kodlama ajanları için resmi GSAP skill'leri.",
        "tools": ["Claude Code", "Cursor", "Codex"]
    },
    "google-labs-code/design.md": {
        "tr": "Kodlama ajanlarına görsel kimlik tanımlamak için format spesifikasyonu.",
        "tools": ["Claude Code", "Cursor", "Gemini CLI"]
    },
    "coreyhaines31/marketingskills": {
        "tr": "Claude Code ve AI ajanları için pazarlama skill'leri: CRO, metin yazarlığı, SEO.",
        "tools": ["Claude Code", "Cursor", "Codex"]
    },
    # Dev Tools
    "siteboon/claudecodeui": {
        "tr": "Claude Code'u mobil ve web üzerinden güzel bir arayüzle kullan.",
        "tools": ["Claude Code"]
    },
    "warpdotdev/warp": {
        "tr": "Terminalden doğan ajansal geliştirme ortamı.",
        "tools": ["Claude Code", "Gemini CLI", "Cursor"]
    },
    "nexu-io/open-design": {
        "tr": "Yerel çalışan, açık kaynaklı Claude Design alternatifi; yerel masaüstü uygulaması.",
        "tools": ["Claude Code", "Cursor"]
    },
    "PowerUserZ/OpenTokenUsage": {
        "tr": "AI kodlama aboneliklerini (Claude, Gemini, Codex) Windows sistem tepsisinden takip et.",
        "tools": ["Claude Code", "Codex", "Gemini CLI", "Cursor"]
    },
    "robinebers/openusage": {
        "tr": "Claude, Codex, Copilot, Cursor abonelik kullanımını izle.",
        "tools": ["Claude Code", "Codex", "Cursor", "Copilot"]
    },
    "ersinkoc/FluidFlow": {
        "tr": "Eskizleri çalışan uygulamalara dönüştür.",
        "tools": ["Claude Code", "Cursor"]
    },
    "pranshuparmar/witr": {
        "tr": "Neden çalışıyor? — süreç inceleme ve analiz aracı.",
        "tools": ["Terminal", "VS Code"]
    },
    "syncthing/syncthing": {
        "tr": "Açık kaynaklı, sürekli dosya senkronizasyon sistemi.",
        "tools": ["Terminal", "VS Code"]
    },
    "gorhill/uBlock": {
        "tr": "Chromium ve Firefox için verimli, hızlı ve hafif reklam engelleyici.",
        "tools": ["Chrome", "Firefox"]
    },
    "ripienaar/free-for-dev": {
        "tr": "Geliştiriciler için ücretsiz katmanlı SaaS, PaaS ve IaaS teklifleri listesi.",
        "tools": ["Genel Referans"]
    },
    "microsoft/coreutils": {
        "tr": "Windows için Coreutils: Yükleyici ve paketleme araçları.",
        "tools": ["Terminal", "VS Code", "Windows"]
    },
    # Mobile & Cross-Platform
    "localsend/localsend": {
        "tr": "AirDrop'a açık kaynaklı, platformlar arası alternatif.",
        "tools": ["Flutter", "VS Code", "Claude Code"]
    },
    "caamer20/Telegram-Drive": {
        "tr": "Telegram hesabını sınırsız, güvenli bulut depolama alanına dönüştür.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "webosbrew/dev-manager-desktop": {
        "tr": "webOS TV için Cihaz/DevMode Yöneticisi.",
        "tools": ["VS Code", "Cursor"]
    },
    "OpenCloudGaming/OpenNOW": {
        "tr": "Özel GeForce Now istemcisi — platformlar arası bulut oyun.",
        "tools": ["VS Code", "Cursor"]
    },
    "rmyndharis/OpenWA": {
        "tr": "Ücretsiz, açık kaynaklı, kendi sunucunda çalışan WhatsApp API ağ geçidi.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "pear-devs/pear-desktop": {
        "tr": "Pear — platformlar arası masaüstü müzik çalar eklentisi.",
        "tools": ["VS Code", "Cursor", "Claude Code"]
    },
    # Medya & Ses
    "OpenBMB/VoxCPM": {
        "tr": "Çok dilli konuşma üretimi ve ses klonlama için Tokenizer-Free TTS modeli (VoxCPM2).",
        "tools": ["Google Colab", "VS Code", "Claude Code"]
    },
    "jamiepine/voicebox": {
        "tr": "Açık kaynaklı AI ses stüdyosu. Klonla, dikte et, üret.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "abus-aikorea/voice-pro": {
        "tr": "TTS, konuşma tanıma, ses klonlama ve altyazı için Gradio WebUI.",
        "tools": ["Google Colab", "VS Code"]
    },
    "tyc0on/GPT-SoVITS-colab": {
        "tr": "GPT-SoVITS ses klonlama için hazır Colab not defteri.",
        "tools": ["Google Colab"]
    },
    "nexmoe/VidBee": {
        "tr": "Dünyanın her yerindeki web sitelerinden video indir.",
        "tools": ["VS Code", "Claude Code"]
    },
    "aandrew-me/ytDownloader": {
        "tr": "Yüzlerce siteden video ve ses indirmek için masaüstü uygulaması.",
        "tools": ["VS Code", "Electron"]
    },
    "Free-TV/IPTV": {
        "tr": "Ücretsiz TV kanalları için M3U oynatma listesi.",
        "tools": ["VLC", "Kodi", "IPTV Player"]
    },
    "iptv-org/iptv": {
        "tr": "Dünya genelinden herkese açık IPTV kanalları koleksiyonu.",
        "tools": ["VLC", "Kodi", "IPTV Player"]
    },
    # Prodüktivite
    "LifeForge-app/lifeforge": {
        "tr": "Takvim, notlar, finans ve proje yönetimini tek çatı altında toplayan kendi kendine barındırılan çözüm.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "paperless-ngx/paperless-ngx": {
        "tr": "Belgeleri tara, indeksle ve arşivle; güçlendirilmiş belge yönetim sistemi.",
        "tools": ["VS Code", "Docker"]
    },
    "vas3k/TaxHacker": {
        "tr": "Fiş, fatura ve işlemler için LLM analizörü; kendi kendine barındırılan AI muhasebe uygulaması.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "umitaltinozzz/twitter-archive": {
        "tr": "Tam metin arama destekli, kendi kendine barındırılan Twitter yer imleri ve beğeniler arşivi.",
        "tools": ["VS Code", "Claude Code"]
    },
    "sarisen/x-bookmark-manager": {
        "tr": "X (Twitter) yer imi yöneticisi.",
        "tools": ["VS Code", "Claude Code"]
    },
    "marktext/marktext": {
        "tr": "Linux, macOS ve Windows için sade ve zarif Markdown editörü.",
        "tools": ["Standalone"]
    },
    "webadderallorg/Recordly": {
        "tr": "Düzenleme becerisi gerekmeden Mac/Windows/Linux'ta parlak demo videoları oluştur.",
        "tools": ["Standalone"]
    },
    "siddharthvaddem/openscreen": {
        "tr": "Ücretsiz, açık kaynaklı, abonelik ve filigran olmadan etkileyici demolar oluştur.",
        "tools": ["Standalone", "Electron"]
    },
    "opendataloader-project/opendataloader-pdf": {
        "tr": "AI'a hazır veri için PDF ayrıştırıcı. PDF erişilebilirliğini otomatikleştir.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    # macOS
    "tw93/Mole": {
        "tr": "Mac'ini terminalden temizle, kaldır, analiz et, optimize et ve izle.",
        "tools": ["Terminal", "macOS"]
    },
    "codybrom/Blankie": {
        "tr": "Mac App Store'da bulunan macOS için ortam sesi mikseri.",
        "tools": ["macOS"]
    },
    "DodoApps/dodopulse": {
        "tr": "Gerçek zamanlı sistem izleme için hafif, yerel macOS menü çubuğu uygulaması.",
        "tools": ["macOS"]
    },
    "open-saas-directory/awesome-native-macosx-apps": {
        "tr": "En iyi Mac uygulamaları — hızlı, hafif, şişirilmemiş. Electron yok.",
        "tools": ["macOS", "Genel Referans"]
    },
    "shiiraz/clicklight-windows": {
        "tr": "Demo ve kayıt için tıklamalarını canlı olarak vurgulayan Windows tepsi uygulaması.",
        "tools": ["Windows"]
    },
    "microsoft/microsoft-ui-reactor": {
        "tr": "WinUI için deneysel uzantı seti (Reactor).",
        "tools": ["VS Code", "Visual Studio", "Windows"]
    },
    # Geliştirme & Güvenlik
    "sherlock-project/sherlock": {
        "tr": "Sosyal medya hesaplarını kullanıcı adıyla birden fazla ağda bul.",
        "tools": ["Terminal", "VS Code", "Claude Code"]
    },
    "bwya77/vscode-dark-islands": {
        "tr": "Easemate IDE ve JetBrains Islands temasından ilham alan VS Code karanlık teması.",
        "tools": ["VS Code"]
    },
    "DontFuckMyCode/dfmc": {
        "tr": "Kod koruma ve gizleme aracı.",
        "tools": ["Terminal", "VS Code"]
    },
    "OpenAEC-Foundation/open-pdf-studio": {
        "tr": "Belge düzenleme ve işleme için açık PDF stüdyosu.",
        "tools": ["Standalone", "VS Code"]
    },
    "ultraworkers/claw-code": {
        "tr": "Rust ile inşa edilmiş, ajan tarafından yönetilen müze sergisi (Gajae-Code / LazyCoder).",
        "tools": ["Claude Code", "Cursor"]
    },
    # Türkçe
    "CodeByPinar/bakiyedefter-pos": {
        "tr": "Küçük işletmeler için modern, çevrimdışı-öncelikli finansal operasyon ve POS sistemi.",
        "tools": ["VS Code", "Claude Code", "Cursor"]
    },
    "kemalersin/kurtarma-plani": {
        "tr": "Borçları kayıt altına alan, gelir-gider dengesini izleyen ve analiz eden uygulama.",
        "tools": ["VS Code", "Claude Code"]
    },
    "saidsurucu/yargi-mcp": {
        "tr": "Türk hukuk veritabanları için MCP sunucusu.",
        "tools": ["Claude Code", "Cursor", "MCP"]
    },
    "3rt4nm4n/turkish-apis": {
        "tr": "Türk API'leri listesi: BTC Türk, İşbank, Trendyol ve daha fazlası.",
        "tools": ["Genel Referans", "VS Code"]
    },
    "Garletz/zikiro-FYR": {
        "tr": "Açık kaynaklı restoran POS sistemi (FYR = For Your Restaurant).",
        "tools": ["VS Code", "Claude Code", "Tauri"]
    },
    "alicankiraz1/Ai-Arastirma-Okumalarim-TR": {
        "tr": "AI alanında yayınlanan makale ve araştırmaların Türkçe detaylı açıklamaları.",
        "tools": ["Genel Referans"]
    },
    "zubair-trabzada/geo-seo-claude": {
        "tr": "Claude Code için GEO öncelikli SEO skill'i; kapsamlı AI arama optimizasyonu.",
        "tools": ["Claude Code"]
    },
    "YusufDinanet/MetroFlow": {
        "tr": "Metro akış yönetimi uygulaması.",
        "tools": ["VS Code", "Claude Code"]
    },
}

# Kategori eşleştirme
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
    full = repo["full_name"].lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in full for kw in keywords):
            return cat_name
    topics = " ".join(repo.get("topics") or []).lower()
    if any(k in topics for k in ["agent","llm","ai","gpt","claude","gemini"]):
        return "🤖 AI & Agents"
    if any(k in topics for k in ["macos","swiftui","mac-app"]):
        return "🖥️ macOS & Desktop Apps"
    if any(k in topics for k in ["flutter","react-native","mobile"]):
        return "📱 Mobile & Cross-Platform"
    if any(k in topics for k in ["tts","voice","speech","audio"]):
        return "🎵 Medya, Ses & Video"
    return "🗂️ Diğer"

def get_tools_badges(tools):
    COLORS = {
        "Claude Code": "5C4EFF",
        "Cursor":       "000000",
        "Windsurf":     "0099FF",
        "VS Code":      "007ACC",
        "Gemini CLI":   "4285F4",
        "Codex":        "412991",
        "Terminal":     "4EAA25",
        "Google Colab": "F9AB00",
        "Copilot":      "000000",
        "MCP":          "7C3AED",
        "Tauri":        "FFC131",
        "Electron":     "47848F",
        "Flutter":      "02569B",
        "Ollama":       "000000",
        "Docker":       "2496ED",
        "API":          "6C757D",
        "macOS":        "000000",
        "Windows":      "0078D4",
        "Chrome":       "4285F4",
        "Firefox":      "FF7139",
        "LM Studio":    "8B5CF6",
        "Standalone":   "6B7280",
        "Genel Referans":"6B7280",
        "Xcode":        "147EFB",
        "Visual Studio":"5C2D91",
        "VLC":          "FF8800",
        "Kodi":         "17B2E7",
        "IPTV Player":  "6B7280",
        "Gradle":       "02303A",
    }
    badges = []
    for t in tools:
        color = COLORS.get(t, "6B7280")
        label = t.replace(" ", "%20").replace("-", "--")
        badges.append(f"![{t}](https://img.shields.io/badge/{label}-{color}?style=flat-square&logoColor=white)")
    return " ".join(badges)

# Kategorilere ayır
order = [c[0] for c in CATEGORIES] + ["🗂️ Diğer"]
buckets = {c: [] for c in order}
for r in repos:
    buckets[categorize(r)].append(r)

# README oluştur
today = datetime.date.today().strftime("%d %B %Y")
total = len(repos)
cat_count = len([b for b in buckets.values() if b])

lines = [
    "# ⭐ awesome-stars",
    "",
    "> **batuhanarici** tarafından yıldızlanan GitHub repoları — kategorilere göre otomatik düzenlenmiş",
    f"> 🕐 Son güncelleme: **{today}** &nbsp;|&nbsp; 📦 Toplam: **{total} repo** &nbsp;|&nbsp; 🗂️ Kategori: **{cat_count}**",
    "",
    "## İçindekiler",
    "",
]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    lines.append(f"- [{cat}](#) — {len(rlist)} repo")

lines += ["", "---", ""]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    lines += [
        f"## {cat}",
        "",
        "| Repo | Açıklama | Dil | Araçlar |",
        "|------|----------|-----|---------|",
    ]
    for r in sorted(rlist, key=lambda x: x["full_name"].lower()):
        meta = REPO_META.get(r["full_name"], {})
        desc = meta.get("tr") or (r.get("description") or "—").replace("|","\\|")[:90]
        lang = r.get("language") or "N/A"
        tools = meta.get("tools", [])
        badges = get_tools_badges(tools) if tools else "—"
        lines.append(f"| [{r['full_name']}]({r['html_url']}) | {desc} | `{lang}` | {badges} |")
    lines += ["", "---", ""]

lines.append("*🤖 Bu dosya [GitHub Actions](.github/workflows/update.yml) tarafından her gece otomatik güncellenmektedir.*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ README güncellendi: {total} repo, {cat_count} kategori")
