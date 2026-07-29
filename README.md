**Language:** English
> [!WARNING]
> This Repository is not longer maintained. [New Repository](https://github.com/devankSinghChaudhary/VPipeline)

--- 
# Video Generating Pipeline

AI-powered documentary and educational video generation pipeline built with LangGraph and NVIDIA NIM.

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.otg)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue?logo=langgraph&logoColor=skyblue)](https://langchain.com/langgraph)
[![NVIDIA NIM](https://img.shields.io/badge/Built%20with-NVIDIA%20NIM-76B900?logo=nvidia&logoColor=green)](https://build.nvidia.com)
[![Mistral AI](https://img.shields.io/badge/Built%20with-Mistral%20AI-9B59B6?logo=mistralai&logoColor=orange)](https://mistral.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png&logoColor=white)]()

[![Instagram](https://img.shields.io/badge/Creator-Follow-E4405F?logo=instagram\&logoColor=white)](https://instagram.com/devanksinghchaudhary)

---

## Overview

Video Generating Pipeline is an AI driven system that transforms a single topic into structured research, documentary scripts, and eventually production-ready video assets.

Instead of relying on a single prompt, the pipeline uses multiple specialized AI agents that work together to:

* Perform research
* Extract and organize knowledge
* Information retrieval
* Generate short form documentary scripts
* Convert into TTS Friendly script
* Whisper used for getting that word spoken accuracy
* Remotion then take over for rendering

---

## Architecture
> Rough Architecture

<img src="./gitassets/rough-structure.png" alt="Rough Structure" style="border-radius: 10px;">

---

## Features

* Multi-Agent Research System
* Parallel AI Researchers
* LangGraph Orchestration
* Structured Research Outputs
* Vector Database Integration
* Long-Form Documentary Generation
* NVIDIA NIM Support
* Local & Cloud Model Compatibility

---

## Example

**Input**

```text
India reaches 3rd stage fast breeder reactor
```

**Pipeline**

```text
Topic Analysis
    ↓
Research Planning
    ↓
Parallel Domain Research
    ↓
Knowledge Storage
    ↓
Global Scene Writing
    ↓
Smaller Scenes Writing
    ↓
Script Writing
    ↓    
Video Generation
```

---

## Tech Stack

* Python
* LangGraph
* LangChain
* Pydantic
* NVIDIA NIM
* Vector Database
* Local LLM Support

---

## Roadmap

### Research Layer

* [x] Perspective Generation
* [x] Parallel Research Agents
* [ ] Fact Verification
* [ ] Citation Tracking
* [ ] Timeline Extraction

### Knowledge Layer

* [ ] Vector Database Integration
* [ ] Knowledge Graph
* [ ] Long-Term Memory

### Script Layer

* [ ] Documentary Outline Generation
* [ ] Multi-Pass Script Writing
* [ ] Narrative Optimization

---

## Running

```bash
git clone https://github.com/DevankSinghChaudhary/video-creation-pipeline
cd video-creation-pipeline
uv run main.py
```


---

## Author: 
**Devank Singh Chaudhary** \
[Instagram](https://instagram.com/devanksinghchaudhary) \
[X/Twitter](https://x.com/@devank0) \
[Email Me](mailto:devanksinghchaudhary@gmail.com)

