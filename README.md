
# Youcli

Youcli 是一个跨平台的 AI 终端命令补全工具，支持 **Bash、Zsh 和 PowerShell**。它只把补全结果写回当前命令行，**不会自动执行任何模型返回的命令**。

Youcli 使用 OpenAI-compatible `POST /chat/completions` 接口，因此可以使用 OpenAI、DeepSeek、通义千问兼容接口以及其他兼容服务。

## 1. 环境要求

- Python 3.8 或更高版本
- 一个 OpenAI-compatible API Key
- Bash/Zsh：Linux、macOS 或 WSL
- PowerShell：Windows PowerShell 5.1+ 或 PowerShell 7，并安装 PSReadLine

## 2. 安装

在项目目录执行：

```bash
python -m venv .venv
# Linux/macOS/WSL
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install .
```

开发或修改源码时使用可编辑安装：

```bash
python -m pip install -e .
```

安装成功后，所有用户都通过同一个 `ai-complete` 命令使用，不需要修改源码中的路径。若系统找不到命令，请使用当前虚拟环境，或把 Python 的 Scripts/bin 目录加入 PATH。

## 3. 配置 API

### 临时配置：环境变量

Linux/macOS/WSL：

```bash
export AI_COMPLETE_API_KEY="your-api-key"
export AI_COMPLETE_BASE_URL="https://api.deepseek.com/v1"
export AI_COMPLETE_MODEL="deepseek-chat"
```

PowerShell：

```powershell
$env:AI_COMPLETE_API_KEY = "your-api-key"
$env:AI_COMPLETE_BASE_URL = "https://api.deepseek.com/v1"
$env:AI_COMPLETE_MODEL = "deepseek-chat"
```

### 持久配置：配置文件

默认位置为 Linux/macOS/WSL 的 `~/.config/ai-complete/config.toml`，Windows 的 `%USERPROFILE%\.config\ai-complete\config.toml`：

```toml
base_url = "https://api.deepseek.com/v1"
model = "deepseek-chat"
api_key = "your-api-key"
timeout = 15
```

也可以通过 `AI_COMPLETE_CONFIG` 指定其他路径。Linux/macOS/WSL 上配置文件包含密钥时执行：

```bash
chmod 600 ~/.config/ai-complete/config.toml
```

环境变量优先级高于配置文件，适合多人共用项目但每个人使用自己的 Key。

## 4. 配置终端快捷键

### Bash

将下面一行加入 `~/.bashrc`，把路径替换为项目绝对路径：

```bash
source /absolute/path/to/Youcli/integrations/bash.sh
```

执行 `source ~/.bashrc` 重新加载。默认快捷键是 `Ctrl+G`，也保留 `Ctrl+X` 后按 `Ctrl+A`。

### Zsh

将下面一行加入 `~/.zshrc`，然后执行 `source ~/.zshrc`：

```bash
source /absolute/path/to/Youcli/integrations/zsh.zsh
```

快捷键是 `Ctrl+X` 后按 `Ctrl+A`。

### PowerShell

执行 `notepad $PROFILE`，加入下面一行（替换为实际路径）：

```powershell
. C:\absolute\path\to\Youcli\integrations\powershell.ps1
```

重启 PowerShell 后按 `Ctrl+G`。如果脚本策略阻止加载，可仅对当前用户放行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 5. 手动测试

```bash
ai-complete --shell bash --line "git che" --cursor 7
```

PowerShell 中：

```powershell
ai-complete --shell powershell --line "git che" --cursor 7
```

排查请求时可启用调试输出（不会打印 API Key）：

```bash
AI_COMPLETE_DEBUG=1 ai-complete --shell bash --line "git che" --cursor 7
```

## 6. 安全边界

- 模型只接收当前输入、光标位置、工作目录和 Git 分支。
- 模型必须返回单行 JSON 命令。
- 本地会拒绝明显危险命令、换行和与用户已有输入无关的替换。
- 工具不会执行模型返回的命令，用户必须自行按 Enter。
- 不要把 API Key 提交到 Git 或分享给其他人。

## 7. 常见问题

**提示“未配置 API Key”**：检查环境变量是否在当前终端生效，或确认配置文件路径和 TOML 格式正确。

**提示“模型请求失败”**：确认 `base_url` 通常需要包含 `/v1`，模型名称与服务商控制台一致，并检查网络和账户余额。

**快捷键没有反应**：确认已重新加载对应 Shell 配置，且 `ai-complete --line "echo" --cursor 4` 能在同一终端直接运行。
