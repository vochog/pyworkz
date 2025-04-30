from TikTokApi import TikTokApi
import asyncio

async def get_trending():
    async with TikTokApi() as api:
        trending = await api.trending(count=10)

        for i, video in enumerate(trending):
            print(f"\n[{i + 1}] @{video.author.username}")
            print(f"Description: {video.description}")
            print(f"Likes: {video.stats.digg_count}") 
            print(f"Shares: {video.stats.share_count}")
            print(f"Comments: {video.stats.comment_count}")
            print(f"Video URL: https://www.tiktok.com/@{video.author.username}/video/{video.id}")

asyncio.run(get_trending())
