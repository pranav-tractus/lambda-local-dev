#!/usr/bin/env python3
"""Regenerate Procfile and Makefile from services.json."""
import json
from pathlib import Path

HERE = Path(__file__).parent
services = json.loads((HERE / "services.json").read_text())["services"]

# --- Procfile ---
lines = []
for svc in services:
    name = svc["name"]
    sam_port = svc["sam_port"]
    proxy_port = svc["proxy_port"]
    function_name = svc["function_name"]
    extra = f" {svc['sam_extra_args']}" if svc.get("sam_extra_args") else ""
    fn_override = f"FUNCTION_NAME={function_name} " if function_name != "FunctionImp" else ""

    lines.append(f"{name}-sam:    cd $BACKEND_PATH/functions/{name} && sam local start-lambda --env-vars env.json{extra} --port {sam_port}")
    lines.append(f"{name}-proxy:  {fn_override}LAMBDA_PORT={sam_port} PROXY_PORT={proxy_port} python3 $DEV_PATH/proxy.py")
    lines.append(f"{name}-tunnel: cloudflared tunnel --url http://localhost:{proxy_port}")
    lines.append("")

(HERE / "Procfile").write_text("\n".join(lines).rstrip() + "\n")
print("Wrote Procfile")

# --- Makefile ---
names = [svc["name"] for svc in services]
build_phony = " ".join(f"build-{n}" for n in names) + " build-all"
clean_phony = " ".join(f"clean-{n}" for n in names) + " clean-all"

mk_lines = [
    "BACKEND_PATH ?= $(shell grep ^BACKEND_PATH .overmind.env | cut -d= -f2)",
    "",
    f".PHONY: {build_phony} \\",
    f"        {clean_phony}",
    "",
]
for name in names:
    mk_lines.append(f"build-{name}:")
    mk_lines.append(f"\tcd $(BACKEND_PATH)/functions/{name} && sam build --use-container")
    mk_lines.append("")

all_build_targets = " ".join(f"build-{n}" for n in names)
mk_lines.append("build-all:")
mk_lines.append(f"\t$(MAKE) {all_build_targets}")
mk_lines.append("")

for name in names:
    mk_lines.append(f"clean-{name}:")
    mk_lines.append(f"\trm -rf $(BACKEND_PATH)/functions/{name}/.aws-sam")
    mk_lines.append("")

all_clean_targets = " ".join(f"clean-{n}" for n in names)
mk_lines.append("clean-all:")
mk_lines.append(f"\t$(MAKE) {all_clean_targets}")
mk_lines.append("")

(HERE / "Makefile").write_text("\n".join(mk_lines))
print("Wrote Makefile")

print(f"Done. {len(services)} services: {', '.join(names)}")
