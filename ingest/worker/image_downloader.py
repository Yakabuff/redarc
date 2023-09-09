import os
from gallery_dl import config, job

def download_image(url, subreddit):
   if not os.path.exists('gallery-dl'):
      os.makedirs('gallery-dl')
   config.load()  # load default config files
   config.set(("extractor",), "base-directory", "gallery-dl")
   config.set(("extractor",), "directory", [subreddit])

   return job.DownloadJob(url).run()

