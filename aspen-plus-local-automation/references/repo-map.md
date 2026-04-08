# Local Repo Map

Use this reference only when you need exact local files or paths.

## Primary Workspace

- Repo root:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main`

## Existing Aspen Wrapper

- Core wrapper:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\示例脚本\CodeLibrary.py`
- Main entry class:
  `Simulation`
- Known COM entry:
  `win32.gencache.EnsureDispatch("Apwn.Document")`

## Starter Project

- Starter root:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project`
- Config:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\project_config.json`
- Session wrapper:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\app\aspen_runner.py`
- Postprocess helpers:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\app\postprocess.py`
- Smoke test:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\scripts\env_check.py`
- Single run:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\scripts\single_run.py`
- Sensitivity template:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\scripts\sensitivity_radfrac.py`
- Structured outputs:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project\outputs`

## Aspen Model Folder

- Model folder:
  `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\Aspen模型`

Expect Aspen-generated `.rep`, `.sum`, and `.cpm` files to appear here.

## Known Stable Example Cases

- Minimal closed-loop example model:
  `01_入门教程配套模型.bkp`
- Stable RADFRAC sensitivity example model:
  `03_优化案例配套模型1.bkp`

## Practical Search Hints

- Search existing wrapper functions:
  `rg -n "def BLK_|def STRM_" "D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\示例脚本\CodeLibrary.py"`
- Open starter configuration first when remapping a model.
- Prefer extending the starter project over editing the original tutorial scripts.
