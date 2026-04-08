#!/usr/bin/env python3

import argparse
import json
import sys

import requests

BASE_URL = "http://localhost:18060"
TIMEOUT = 60


def get(path):
    return requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)


def post(path, payload):
    return requests.post(f"{BASE_URL}{path}", json=payload, timeout=TIMEOUT)


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def status():
    data = get("/api/v1/login/status").json()
    print_json(data)


def search(args):
    data = post("/api/v1/feeds/search", {
        "keyword": args.keyword,
        "filters": {
            "sort_by": args.sort,
            "note_type": args.type,
            "publish_time": args.time,
        }
    }).json()
    print_json(data if args.json else data.get("data", {}).get("feeds", []))


def detail(args):
    data = post("/api/v1/feeds/detail", {
        "feed_id": args.feed_id,
        "xsec_token": args.xsec_token,
        "load_all_comments": args.comments,
    }).json()
    print_json(data if args.json else data.get("data", {}))


def feeds(args):
    data = get("/api/v1/feeds/list").json()
    print_json(data if args.json else data.get("data", {}).get("feeds", []))


def publish(args):
    payload = {
        "title": args.title,
        "content": args.content,
        "images": args.images.split(","),
    }
    if args.tags:
        payload["tags"] = args.tags.split(",")
    data = post("/api/v1/publish", payload).json()
    print_json(data)


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu MCP client")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("keyword")
    search_parser.add_argument("--sort", default="综合")
    search_parser.add_argument("--type", default="不限")
    search_parser.add_argument("--time", default="不限")
    search_parser.add_argument("--json", action="store_true")

    detail_parser = subparsers.add_parser("detail")
    detail_parser.add_argument("feed_id")
    detail_parser.add_argument("xsec_token")
    detail_parser.add_argument("--comments", action="store_true")
    detail_parser.add_argument("--json", action="store_true")

    feeds_parser = subparsers.add_parser("feeds")
    feeds_parser.add_argument("--json", action="store_true")

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("title")
    publish_parser.add_argument("content")
    publish_parser.add_argument("images")
    publish_parser.add_argument("--tags")

    args = parser.parse_args()

    try:
        if args.command == "status":
            status()
        elif args.command == "search":
            search(args)
        elif args.command == "detail":
            detail(args)
        elif args.command == "feeds":
            feeds(args)
        elif args.command == "publish":
            publish(args)
        else:
            parser.print_help()
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Cannot connect to xiaohongshu-mcp on localhost:18060", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
