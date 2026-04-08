#!/usr/bin/env python3

import argparse
import json

import requests

BASE_URL = "https://api.tikhub.io/api/v1"


class XiaohongshuAPI:
    def __init__(self, api_key=""):
        self.api_key = api_key

    def _headers(self):
        return {"X-TikHub-Api-Key": self.api_key} if self.api_key else {}

    def get_post(self, post_id):
        return requests.get(
            f"{BASE_URL}/xiaohongshu/web/post/detail",
            params={"post_id": post_id},
            headers=self._headers(),
            timeout=15,
        ).json()

    def search(self, keyword, page=1):
        return requests.get(
            f"{BASE_URL}/xiaohongshu/web/post/search",
            params={"keyword": keyword, "page": page},
            headers=self._headers(),
            timeout=15,
        ).json()

    def get_trending(self):
        return requests.get(
            f"{BASE_URL}/xiaohongshu/web/post/hot",
            headers=self._headers(),
            timeout=15,
        ).json()


def main():
    parser = argparse.ArgumentParser(description="Xiaohongshu API via TikHub")
    parser.add_argument("--post", dest="post_id")
    parser.add_argument("--post-id", dest="post_id")
    parser.add_argument("--search")
    parser.add_argument("--trending", action="store_true")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    api = XiaohongshuAPI(args.api_key)

    if args.post_id:
        result = api.get_post(args.post_id)
    elif args.search:
        result = api.search(args.search, page=args.page)
    elif args.trending:
        result = api.get_trending()
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
