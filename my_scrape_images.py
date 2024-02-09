import hashlib, io, requests, pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image


URLS = [
  "https://mexicoplates.moini.net/index.html",
  "https://mexicoplates.moini.net/ags.html",
  "https://mexicoplates.moini.net/bc.html",
  "https://mexicoplates.moini.net/bcs.html",
  "https://mexicoplates.moini.net/camp.html",
  "https://mexicoplates.moini.net/chis.html",
  "https://mexicoplates.moini.net/chih.html",
  "https://mexicoplates.moini.net/coah.html",
  "https://mexicoplates.moini.net/col.html",
  "https://mexicoplates.moini.net/df.html",
  "https://mexicoplates.moini.net/cdmx.html",
  "https://mexicoplates.moini.net/dgo.html",
  "https://mexicoplates.moini.net/gto.html",
  "https://mexicoplates.moini.net/gro.html",
  "https://mexicoplates.moini.net/hgo.html",
  "https://mexicoplates.moini.net/jal.html",
  "https://mexicoplates.moini.net/mex.html",
  "https://mexicoplates.moini.net/mich.html",
  "https://mexicoplates.moini.net/mor.html",
  "https://mexicoplates.moini.net/nay.html",
  "https://mexicoplates.moini.net/nl.html",
  "https://mexicoplates.moini.net/oax.html",
  "https://mexicoplates.moini.net/pue.html",
  "https://mexicoplates.moini.net/qro.html",
  "https://mexicoplates.moini.net/qr.html",
  "https://mexicoplates.moini.net/slp.html",
  "https://mexicoplates.moini.net/sin.html",
  "https://mexicoplates.moini.net/son.html",
  "https://mexicoplates.moini.net/tab.html",
  "https://mexicoplates.moini.net/tamps.html",
  "https://mexicoplates.moini.net/tlax.html",
  "https://mexicoplates.moini.net/ver.html",
  "https://mexicoplates.moini.net/yuc.html",
  "https://mexicoplates.moini.net/zac.html",
  "https://mexicoplates.moini.net/oldmex.html",
  "https://mexicoplates.moini.net/frontbc.html",
  "https://mexicoplates.moini.net/frontbcs.html",
  "https://mexicoplates.moini.net/frontchis.html",
  "https://mexicoplates.moini.net/frontchih.html",
  "https://mexicoplates.moini.net/frontcoah.html",
  "https://mexicoplates.moini.net/frontson.html",
  "https://mexicoplates.moini.net/f-tamps.html",
  "https://mexicoplates.moini.net/spf.html",
  "https://mexicoplates.moini.net/spf1.html",
  "https://mexicoplates.moini.net/fed.html",
  "https://mexicoplates.moini.net/diplo.html",
  "https://mexicoplates.moini.net/tmetro.html",
  "https://mexicoplates.moini.net/juarez.html",
  "https://mexicoplates.moini.net/sonariz.html",
  "https://mexicoplates.moini.net/euro.html",
  "https://mexicoplates.moini.net/lownum.html",
  "https://mexicoplates.moini.net/temp.html",
  "https://mexicoplates.moini.net/org.html",
  "https://mexicoplates.moini.net/movie.html",
  "https://mexicoplates.moini.net/numberblocks.html"
]

def get_content_from_url(url):
  options = ChromeOptions()
  options.add_argument("--headless=new")
  driver = webdriver.Chrome(options=options)

  driver.get(url)
  page_content = driver.page_source
  driver.quit()
  return page_content

def parse_image_urls(content, classes, location, source):
  soup = BeautifulSoup(content, "html.parser")
  results = []
  for a in soup.findAll(attrs={"class": classes}):
    name = a.find(location)
    if name not in results:
      results.append(name.get(source))
  return results

def save_urls_to_csv(image_urls):
  df = pd.DataFrame({"links": image_urls})
  df.to_csv("links.csv", index=False, encoding="utf-8")

def get_and_save_image_to_file(image_url, output_dir):
  image_content = requests.get(image_url).content
  image_file = io.BytesIO(image_content)
  image = Image.open(image_file).convert("RGB")
  filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
  file_path = output_dir / filename
  image.save(file_path, "PNG", quality=80)

def main(url):
  content = get_content_from_url(url)
  image_urls = parse_image_urls(
    content=content, classes="pic", location="img", source="src"
  )
  save_urls_to_csv(image_urls)
  for image_url in image_urls:
    new_image_url = 'https://mexicoplates.moini.net/' + image_url
    get_and_save_image_to_file(
      new_image_url, output_dir=Path("path/to/test")
    )

if __name__ == "__main__":
  for one_url in URLS:
    main(one_url)
  print("Done!")
