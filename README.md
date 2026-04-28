# NIMStats — Real-Time NVIDIA NIM Benchmark Dashboard

[![GitHub Actions](https://github.com/MauroDruwel/NIMStats/workflows/Benchmark%20NVIDIA%20NIM%20Models/badge.svg)](https://github.com/MauroDruwel/NIMStats/actions)
[![Live Dashboard](https://img.shields.io/badge/view-live%20dashboard-brightgreen)](https://nimstats.maurodruwel.be/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Automated hourly benchmarking of 20+ NVIDIA NIM models with beautiful analytics dashboard. Fully open-source, zero infrastructure costs.**

🔗 **Live Dashboard**: [nimstats.maurodruwel.be](https://nimstats.maurodruwel.be/)

---

## ⚡ Quick Start

### 1. Get Your API Key
Visit [build.nvidia.com](https://build.nvidia.com) → Create account (free) → Copy API key

### 2. Add to GitHub Secrets
**Settings** → **Secrets and variables** → **Actions** → New repository secret
- Name: `NIM_API_KEY`
- Value: Your API key

### 3. Deploy
Choose your platform:
- **Cloudflare Pages**: Push repo + connect in [Cloudflare Pages](https://pages.cloudflare.com/)
- **GitHub Pages**: Go to Settings → Pages → Deploy from main branch
- **Netlify/Vercel**: Connect repo for auto-deploy

### 4. Trigger First Run
Go to **Actions** → **Benchmark NVIDIA NIM Models** → **Run workflow**

Done! Dashboard updates every hour automatically. ✨

---

## 📊 Dashboard Features

- **KPI Cards**: Total runs, success rate, fastest response, best throughput
- **Advanced Analytics**: Consistency scores, median times, model performance stats
- **Multiple Charts**: Response times, throughput distribution, success trends, scatter plots
- **Results Table**: Sort by speed, throughput, or name + click to view full responses
- **History Tracking**: Complete audit trail of all benchmarks with trends
- **Live Status**: Real-time online/offline indicator with auto-refresh

---

## 🤖 Benchmark Models (20 Total)

| Model | Description |
|-------|----------|
| `deepseek-ai/deepseek-v4-flash` | Fast MoE model optimized for speed |
| `deepseek-ai/deepseek-v4-pro` | Professional-grade DeepSeek |
| `deepseek-ai/deepseek-v3.2` | Latest with improved reasoning |
| `z-ai/glm-5.1` | Superior code understanding |
| `z-ai/glm-4.7` | Strong mathematical capabilities |
| `minimax/minimax-m2.7` | Efficient inference model |
| `minimax/minimax-m2.5` | Previous generation MiniMax |
| `nvidia/nemotron-3-super-120b-a12b` | NVIDIA's 120B flagship |
| `nvidia/nemotron-4-340b-instruct` | Latest 340B instruction-tuned |
| `nvidia/llama-3.1-nemotron-ultra-253b-v1` | Ultra-large 253B model |
| `moonshotai/kimi-k2.5` | Context-optimized model |
| `moonshotai/kimi-k2-instruct` | Instruction-tuned Kimi |
| `gpt-oss/gpt-oss-120b` | Open-source 120B |
| `google/gemma-4-31b-it` | Lightweight edge inference |
| `qwen/qwen3-coder-480b-a35b-instruct` | Specialized coding (480B) |
| `qwen/qwen2.5-coder-32b-instruct` | Lightweight Qwen coder |
| `qwen/qwen3.5-397b-a17b` | Flagship Qwen (397B) |
| `mistralai/devstral-2-123b-instruct-2512` | Developer-focused (123B) |
| `mistralai/mistral-large-3-675b-instruct-2512` | Largest Mistral (675B) |
| `meta/llama-3.1-405b-instruct` | Meta's largest Llama (405B) |

---

## 🏗️ Architecture

```
GitHub Actions (Hourly)
├─ Group 1: Test 10 models
├─ Group 2: Test 10 models (parallel)
└─ Merge: Combine results + update history

↓ Results pushed to repo

Cloudflare Pages / GitHub Pages / Netlify
└─ Static dashboard (auto-refresh every 30s)
```

**Parallel benchmarking = ~50% faster tests** ⚡

---

## 📝 Customization

### Change Benchmark Prompt
Edit `PROMPT` in `scripts/test_models.py`:
```python
PROMPT="Your custom prompt here"
```

### Add/Remove Models
Edit model arrays in `scripts/test_models.py`:
```python
GROUP1_MODELS = [
    "your/custom-model",
    # ...
]
```

### Change Schedule
Edit `.github/workflows/benchmark.yml` line 5:
```yaml
- cron: '0 */6 * * *'  # Every 6 hours instead of hourly
```

---

## 📊 Data Format

`history.json` is the single persisted source of truth for the dashboard and history.
`scripts/results.json` is only a temporary per-job artifact during workflow execution.

```json
{
  "runs": [
    {
      "timestamp": "2026-04-28T06:49:00Z",
      "prompt": "...",
      "models": [
        {
          "model": "deepseek-ai/deepseek-v4-flash",
          "success": true,
          "responseTime": 2500,
          "tokensGenerated": 150,
          "totalTokens": 170,
          "response": "..."
        }
      ],
      "summary": {
        "successCount": 20,
        "totalModels": 20,
        "fastestModel": "...",
        "fastestTime": 2500
      }
    }
  ]
}
```

---

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/MauroDruwel/NIMStats.git
cd NIMStats

# Test locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

---

## 📈 Performance Benchmarking

- **Response Times**: Measured from API request to response (includes network)
- **Tokens Generated**: Output tokens from the model
- **Throughput**: Tokens per second (generation speed)
- **Success Rate**: % of models returning valid responses

**Test Parameters:**
- Temperature: 0.7
- Top-p: 0.9
- Max tokens: 500
- Format: OpenAI chat completions compatible

---

## 🔗 Resources

- [NVIDIA NIM API Docs](https://docs.api.nvidia.com/nim/)
- [Model Catalog](https://build.nvidia.com/models)
- [GitHub Repo](https://github.com/MauroDruwel/NIMStats)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

**Tracking model performance for the ML community. Built with ❤️**
