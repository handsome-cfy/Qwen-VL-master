#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COCO-human → Qwen-VL 格式转换
支持输出两种合法格式：
  A. jsonl  （默认，一行一个对象，官方推荐）
  B. json   （标准 JSON 数组，最外层 []）
用法：
  python convert2qwen.py -i raw.json -o qwenvl.json --img-dir ./images --json
"""
import argparse, json, os, tqdm

MAPPING = {"human": "user", "gpt": "assistant"}


def convert_one_sample(item: dict, img_dir: str) -> dict:
    new_conv = []
    for turn in item["conversations"]:
        role = MAPPING.get(turn["from"], turn["from"])
        text = turn["value"]
        if "<image>" in text:
            img_fn = item.get("image", "")
            if not img_fn:
                raise ValueError(f"对话含 <image> 但样本无 image 字段: {item}")
            text = text.replace("<image>", f"<img>{os.path.join(img_dir, img_fn)}</img>")
        new_conv.append({"from": role, "value": text})
    return {"id": item["id"], "conversations": new_conv}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--img-dir", default="./playground/data/coco/train2017")
    parser.add_argument("--json", action="store_true", help="输出标准 JSON 数组，否则为 jsonl")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    if isinstance(raw_data, dict) and "data" in raw_data:
        raw_data = raw_data["data"]

    all_data = [convert_one_sample(item, args.img_dir) for item in tqdm.tqdm(raw_data)]

    # ===== 二选一 =====
    if args.json:  # 合法 JSON 数组
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
    else:  # 合法 JSON Lines
        with open(args.output, "w", encoding="utf-8") as f:
            for sample in all_data:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    print(f"Done! 共 {len(all_data)} 条 -> {args.output}")


if __name__ == "__main__":
    main()